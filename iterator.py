import os, glob
from parser import csv2json
from generate_onto import json2owl


path = 'Размеченные рецензии/'
print('CSV -> JSON')
for name in glob.glob(os.path.join(path, '*.csv')):
    name = name.split('.')[0]
    print(name)
    try:
        csv2json(name)
    except Exception as e:
        print(e)
        

print('JSON -> OWL')
for name in glob.glob(os.path.join(path, '*.json')):
    name = name.split('.')[0]
    print(name)
    try:
        json2owl(name)
    except Exception as e:
        print(e)
