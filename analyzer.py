import os
from owlready2 import *
import pandas as pd


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
    for annotation in os.listdir(os.path.join(path, review)):
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
            
            reviews.append({
                'Review': review,
                'Annotator': annotator,
                'Number of argument sets': n_classes,
                'Number of author\'s arguments': n_arg_author,
                'Numbers of reviewers\' argumnets': n_arg_revs,
                'Lengths of argument chains': lengths,
                'Maximal length of argument chains': max(lengths),
                'Number of author\'s admissible arguments': adm_author,
                'Numbers of reviewers\' admissible arguments': adm_revs,
                'Is author\'s extension preferable': author_pref})
            
            onto.destroy()

    #if i == 10:
    #    break
        
reviews = pd.DataFrame.from_dict(reviews)
reviews.to_csv('stats.csv')
