import os
from owlready2 import *
import pandas as pd
import json


def get_paths(current_arg, visited):
    visited.append(current_arg)
    for arg in current_arg.isAttackedBy:
        if arg not in visited:
            get_paths(arg, visited.copy())
    if not current_arg.isAttackedBy:
        chains.append(visited)


path = 'mdpi_annotated'
reviews = []
for i, review in enumerate(os.listdir(path)):
    n_annotations = 0
    annotations = {'Review': review}
    for j, annotation in enumerate(os.listdir(os.path.join(path, review))):
        annotator = annotation.split('_')[1]
        onto = os.path.join(path, review, annotation, f'{annotation}_inferred.owl')
        if os.path.exists(onto):
            onto = get_ontology(onto).load()

            n_classes = len(list(Thing.subclasses()))
            
            n_arg_revs = []
            for cl in Thing.subclasses():
                n_args = len(list(cl.instances()))
                if cl.iri.endswith('Author'):
                    n_arg_author = n_args
                else:
                    n_arg_revs.append(n_args)
            
            paper = onto.search_one(is_a = onto['Author'],
                                    round = '0',
                                    number = '0')
            chains = []
            get_paths(paper, [])
            lengths = [len(x) for x in chains]

            adm_revs = []
            for cl in onto.classes():
                n_args = len(list(cl.instances()))
                if cl.iri.endswith('AuthorAdmissible'):
                    adm_author = n_args
                elif cl.iri.endswith('Admissible'):
                    adm_revs.append(n_args)

            author_pref = adm_author > sum(adm_revs)

            annotations[f'Annotator{j}: Number of argument sets'] = n_classes
            annotations[f'Annotator{j}: Number of author\'s arguments'] = n_arg_author
            annotations[f'Annotator{j}: Average number of reviewers\' arguments'] = sum(n_arg_revs)/len(n_arg_revs)
            annotations[f'Annotator{j}: Average length of argument chains'] = sum(lengths)/len(lengths)
            annotations[f'Annotator{j}: Number of author\'s admissible arguments'] = adm_author
            annotations[f'Annotator{j}: Average number of reviewers\' admissible arguments'] = sum(adm_revs)/len(adm_revs)
            annotations[f'Annotator{j}: Is author\'s extension preferable'] = author_pref
            n_annotations += 1

            onto.destroy()
            
            if n_annotations == 2:
                reviews.append(annotations)
                break

    #if i == 10:
    #    break
        
reviews = pd.DataFrame.from_dict(reviews)
reviews.to_csv('stats.csv')

total = {
    'Annotator0: average number of argument sets': round(reviews['Annotator0: Number of argument sets'].mean(), 2),
    'Annotator0: average number of author\'s arguments': round(reviews['Annotator0: Number of author\'s arguments'].mean(), 2),
    'Annotator0: average number of reviewers\' arguments': round(reviews['Annotator0: Average number of reviewers\' arguments'].mean(), 2),
    'Annotator0: average length of argument chains': round(reviews['Annotator0: Average length of argument chains'].mean(), 2),
    'Annotator0: average number of author\'s admissible arguments': round(reviews['Annotator0: Number of author\'s admissible arguments'].mean(), 2),
    'Annotator0: average number of reviewers\' admissible arguments': round(reviews['Annotator0: Average number of reviewers\' admissible arguments'].mean(), 2),
    'Annotator0: average if author\'s extension preferable': round(reviews['Annotator0: Is author\'s extension preferable'].mean(), 2),
    'Annotator1: average number of argument sets': round(reviews['Annotator1: Number of argument sets'].mean(), 2),
    'Annotator1: average number of author\'s arguments': round(reviews['Annotator1: Number of author\'s arguments'].mean(), 2),
    'Annotator1: average number of reviewers\' arguments': round(reviews['Annotator1: Average number of reviewers\' arguments'].mean(), 2),
    'Annotator1: average length of argument chains': round(reviews['Annotator1: Average length of argument chains'].mean(), 2),
    'Annotator1: average number of author\'s admissible arguments': round(reviews['Annotator1: Number of author\'s admissible arguments'].mean(), 2),
    'Annotator1: average number of reviewers\' admissible arguments': round(reviews['Annotator1: Average number of reviewers\' admissible arguments'].mean(), 2),
    'Annotator1: average if author\'s extension preferable': round(reviews['Annotator1: Is author\'s extension preferable'].mean(), 2),
    'Correlation in number of argument sets': round(reviews['Annotator0: Number of argument sets'].corr(reviews['Annotator1: Number of argument sets']), 2),
    'Correlation in number of author\'s arguments': round(reviews['Annotator0: Number of author\'s arguments'].corr(reviews['Annotator1: Number of author\'s arguments']), 2),
    'Correlation in average number of reviewers\' arguments': round(reviews['Annotator0: Average number of reviewers\' arguments'].corr(reviews['Annotator1: Average number of reviewers\' arguments']), 2),
    'Correlation in average length of argument chains': round(reviews['Annotator0: Average length of argument chains'].corr(reviews['Annotator1: Average length of argument chains']), 2),
    'Correlation in number of author\'s admissible arguments': round(reviews['Annotator0: Number of author\'s admissible arguments'].corr(reviews['Annotator1: Number of author\'s admissible arguments']), 2),
    'Correlation in average number of reviewers\' admissible arguments': round(reviews['Annotator0: Average number of reviewers\' admissible arguments'].corr(reviews['Annotator1: Average number of reviewers\' admissible arguments']), 2),
    'Correlation in if author\'s extension preferable': round(reviews['Annotator0: Is author\'s extension preferable'].corr(reviews['Annotator1: Is author\'s extension preferable']), 2),
}
with open('total.json', 'w') as f:
    json.dump(total, f, indent = 2)
