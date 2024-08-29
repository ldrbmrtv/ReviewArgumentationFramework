import os, glob
from parser import csv2json
from generate_onto import json2owl
import timeit
import statistics


times = []
path = 'mdpi_annotated'
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
        start = timeit.timeit()
        try:
            json2owl(name)
        except Exception as e:
            print(e)
        end = timeit.timeit()
        times.append(end - start)

print((round(sum(times)/len(times), 3), round(statistics.stdev(times), 3)))
