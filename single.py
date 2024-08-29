import os
from parser import csv2json
from generate_onto import json2owl


if __name__ == '__main__':

    path = ''
    review = ''
    annotation = 'JLC_reviews'
    file = os.path.join(path, review, annotation, f'{annotation}.csv')
    name = file.split('.')[0]

    print('CSV -> JSON')
    csv2json(name)
    
    print('JSON -> OWL')
    file = os.path.join(path, review, annotation, f'{annotation}.json')
    name = file.split('.')[0]
    json2owl(name)
