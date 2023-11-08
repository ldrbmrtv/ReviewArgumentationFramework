import os
import networkx as nx
import json
import pandas as pd


path = 'mdpi_annotated'
reviews = []
for i, review in enumerate(os.listdir(path)):
    print(review)
    graphs = []
    nn_args = []
    for annotation in os.listdir(os.path.join(path, review)):
        G = nx.Graph()
        n_args = 0
        with open(os.path.join(path, review, annotation, f'{annotation}.json')) as f:
            data = json.load(f)
            argument_sets = data['argument_sets']
            for argument_set, arguments in argument_sets.items():
                for argument in arguments.keys():
                    G.add_node(argument)
                n_args += len(arguments)
            attack_pairs = data['attack_pairs']
            for pair in attack_pairs:
                argument1 = pair[0]
                argument2 = pair[1]
                G.add_edge(argument1, argument2)
        graphs.append(G)
        nn_args.append(n_args)

    if len(graphs) == 2:
        for i, dist in enumerate(nx.optimize_graph_edit_distance(graphs[0], graphs[1])):
            dist = int(dist)
            print(dist)
            if i == 0:
                break
        mean_n_args = sum(nn_args)/2
        print(mean_n_args)
        reviews.append({'review': review,
                        'dist': dist,
                        'mean_n_args': mean_n_args,
                        'dist_per_mean_n_args': dist/mean_n_args})
               
reviews = pd.DataFrame.from_dict(reviews)
reviews.to_csv('dists.csv', sep = ';')

total = {
    'dist': reviews['dist'].mean(),
    'mean_n_args': reviews['mean_n_args'].mean(),
    'dist_per_mean_n_args': reviews['dist_per_mean_n_args'].mean()
}
with open('dist.json', 'w') as f:
    json.dump(total, f, indent = 2)
