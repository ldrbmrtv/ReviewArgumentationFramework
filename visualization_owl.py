import os
from owlready2 import *
import networkx as nx
import textwrap
from plotly.express.colors import sample_colorscale
import plotly.graph_objects as go

#Data
path = os.path.join('JLC_reviews', 'JLC_reviews_inferred.owl')
onto = get_ontology(path).load()

nodes = []
edges = []
texts = []
sides = []
rounds = []
numbers = []
acceptables = []

with onto:
    for inst in onto.individuals():
        label = inst.label[0]
        nodes.append(label)
        texts.append(inst.text[0])
        sides.append(label.split('.')[0])
        rounds.append(inst.round[0])
        numbers.append(inst.number[0])
        acceptable = False
        for cl in inst.is_a:
            if str(cl).endswith('Admissible'):
                acceptable = True
                break
        acceptables.append(acceptable)

    for rel in onto.attacks.get_relations():
        rel = [x.label[0] for x in rel]
        edges.append(rel)

color_scale = 'Viridis'
sides_set = set(sides)
colors_set = sample_colorscale(color_scale, len(sides_set))
color_map = {}
for side, color in zip(sides_set, colors_set):
    color_map[side] = color

borders = []
for accept in acceptables:
    if accept:
        borders.append('Green')
    else:
        borders.append('Red')

#Creating graph
G = nx.Graph()

for node in nodes:
    G.add_node(node)

for edge in edges:
    G.add_edge(edge[0], edge[1])

texts = [textwrap.fill(x, 100) for x in texts]
texts = [x.replace('\n', '<br>') for x in texts]

templates = []
for side, round, number, text in zip(sides, rounds, numbers, texts):
    templates.append(f'<b>Side</b>: {side}<br><b>Round</b>: {round}<br><b>Number</b>: {number}<br><b>Text</b>: {text}')


#Layouting graph
pos = nx.fruchterman_reingold_layout(G)
Xv = [pos[k][0] for k in G.nodes()]
Yv = [pos[k][1] for k in G.nodes()]
Xed = []
Yed = []
for edge in G.edges():
    Xed += [pos[edge[0]][0], pos[edge[1]][0], None]
    Yed += [pos[edge[0]][1], pos[edge[1]][1], None]

edge_trace = go.Scatter(
    x = Xed, y = Yed,
    line = dict(width = 0.5, color = '#888'),
    hoverinfo = 'none',
    mode = 'lines',
    showlegend = False)

node_trace = go.Scatter(
    x = Xv, y = Yv,
    mode = 'markers+text',
    textposition = 'top center',
    customdata = templates,
    hovertemplate = '%{customdata}<extra></extra>',
    marker = dict(size = 12,
                  line_width = 2,
                  line_color = borders),
    showlegend = False)

node_trace.text = nodes
node_trace.marker.color = [color_map[x] for x in sides]

fig = go.Figure(data = [edge_trace, node_trace],
    layout = go.Layout(
        title = 'Peer review argumentation framework',
        hovermode = 'closest',
        margin = dict(b = 20, l = 5, r = 5, t = 60),
        xaxis = dict(showgrid = False, zeroline = False, showticklabels = False),
        yaxis = dict(showgrid = False, zeroline = False, showticklabels = False)))

for side in sides_set:
    fig.add_trace(
        go.Scatter(
            x=[None], 
            y=[None],
            name=side,
            mode='markers',
            marker=dict(color=color_map[side]),
            showlegend=True
        )
    )

fig.write_html(f'{path.split(".")[0]}.html')
