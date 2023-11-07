import os
from owlready2 import *
import pandas as pd


path = 'mdpi_annotated'
reviews = []
for i, review in enumerate(os.listdir(path)):
    n_adm = {}
    for j, annotation in enumerate(os.listdir(os.path.join(path, review))):
        onto = os.path.join(path, review, annotation, f'{annotation}_inferred.owl')
        if os.path.exists(onto):
            onto = get_ontology(onto).load()
            adm_revs = []
            for cl in onto.classes():
                n_args = len(list(cl.instances()))
                if cl.iri.endswith('AuthorAdmissible'):
                    n_adm[f'Annotator{j}_aut'] = n_args
                elif cl.iri.endswith('Admissible'):
                    adm_revs.append(n_args)
            n_adm[f'Annotator{j}_rev'] = sum(adm_revs)
            onto.destroy()

    if len(n_adm) == 4:
        n_adm['Review'] = review
        reviews.append(n_adm)
            
    #if i == 10:
    #    break
        
reviews = pd.DataFrame.from_dict(reviews)
reviews.to_csv('correlation.csv')
print(reviews['Annotator0_aut'].corr(reviews['Annotator1_aut']))
print(reviews['Annotator0_rev'].corr(reviews['Annotator1_rev']))
