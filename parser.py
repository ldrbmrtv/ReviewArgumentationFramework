import pandas as pd
import json
import os
from generate_onto import json2owl


def format_id(side, round, number):
    id = (side, round, number)
    return '.'.join(id)


def csv2json(name):

    # Reading CSV
    df = pd.read_csv(f'{name}.csv', sep = ';')
    #print(df.info())
    df['Side'] = df['Side'].apply(lambda x: str(x).strip())
    df['Side'] = df['Side'].apply(lambda x: str(x).replace(' ', '_'))
    df['Opponent'] = df['Opponent'].apply(lambda x: str(x).strip())
    df['Opponent'] = df['Opponent'].apply(lambda x: str(x).replace(' ', '_'))
    df['Round'] = df['Round'].apply(lambda x: str(int(x)))
    df['Number'] = df['Number'].apply(lambda x: str(int(x)))
    df['Attacks'] = df['Attacks'].apply(lambda x: str(x).replace(' ', ''))
    df['Attacks'] = df['Attacks'].apply(lambda x: str(x).split(','))
    df = df.explode('Attacks', ignore_index = True)
    df['Attacks'] = df['Attacks'].apply(lambda x: str(int(x)))
    #df.to_csv(f'{name}_test.csv', sep = ';')
    #print(df.info())

    round_old = '1'
    for index, row in df.iterrows():
        if row['Side'] == 'Author':
            if row['Round'] != round_old:
                round_old = row['Round']
                number = 1
            else:                
                number += 1
            df.at[index, 'Number'] = str(number)
        else:
            if row['Attacks'] != '0':
                if int(row['Round']) > 1:
                    print(name)
                rev_i = int(row['Side'].split('_')[1])
                n_args_before = 0
                for i in range(1, rev_i):
                    rev_i_args = df[(df['Side'] == 'Author') & (df['Opponent'] == f'Reviewer_{i}') & (df['Round'] == (str(int(row['Round']) - 1)))]
                    n_args_before += len(rev_i_args.index)
                df.at[index, 'Attacks'] = str(int(row['Attacks']) + n_args_before)
    df.to_csv(f'{name}_fixed.csv', sep = ';', index = False)

    # Collecting argument sets
    argument_sets = {}
    sides = df['Side']
    for side in sides.unique():
        side_df = df[df['Side'] == side]
        args = {}
        for index, row in side_df.iterrows():
            id = format_id(row['Side'],
                           row['Round'],
                           row['Number'])
            args[id] = row['Text']
        argument_sets[side] = args
    argument_sets['Author']['Author.0.0'] = 'Paper'

    # Collecting attack pairs
    attack_pairs = []
    for index, row in df.iterrows():
        attacks = format_id(row['Side'],
                            row['Round'],
                            row['Number'])
        if row['Attacks'] == '0':
            round = '0'
        else:
            round = str(int(row['Round']) - 1)
        attacked = format_id(row['Opponent'],
                             round,
                             row['Attacks'])
        attack_pairs.append([attacks, attacked])

    # Preparing result 
    result = {
        'argument_sets': argument_sets,
        'attack_pairs': attack_pairs
    }

    # Wrighting JSON 
    with open(f'{name}.json', 'w') as file:
        json.dump(result, file, indent = 2)
