import os, glob
from parser import csv2json
from generate_onto import json2owl


path = 'examples'
for review in os.listdir(path):
    print(review)
    for annotation in os.listdir(os.path.join(path, review)):
        print(annotation)
        file = os.path.join(path, review, annotation, f'{annotation}.csv')
        name = file.split('.')[0]

        print('CSV -> JSON')
        try:
            csv2json(name)
        except Exception as e:
            print(e)

        print('JSON -> OWL')
        file = os.path.join(path, review, annotation, f'{annotation}.json')
        name = file.split('.')[0]
        try:
            json2owl(name)
        except Exception as e:
            print(e)
