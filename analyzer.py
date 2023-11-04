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
        onto = os.path.join(path, review, annotation, f'{annotation}.owl')
        if os.path.exists(onto):
            onto = get_ontology(onto).load()
            n_classes = len(list(Thing.subclasses()))
            
            rev_arg_dist = []
            for cl in Thing.subclasses():
                n_arguments = len(list(cl.instances()))
                if cl.iri.endswith('Author'):
                    n_arg_author = n_arguments
                else:
                    rev_arg_dist.append(len(list(cl.instances())))
            
            paper = onto.search_one(is_a = onto['Author'],
                                    round = '0',
                                    number = '0')
            chains = []
            get_paths(paper, [])
            lengths = [len(x) for x in chains]
            
            reviews.append({
                'review': review,
                'annotator': annotator,
                'n_arg_sets': n_classes,
                'n_arg_author': n_arg_author,
                'arg_revs': rev_arg_dist,
                'arg_chain_lens': lengths,
                'arg_chain_len_max': max(lengths)})
            
            onto.destroy()

    #if i == 10:
    #    break
        
reviews = pd.DataFrame.from_dict(reviews)
reviews.to_csv('stats.csv')
