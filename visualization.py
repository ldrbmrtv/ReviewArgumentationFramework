import os
import json
import networkx as nx
import textwrap
import plotly.graph_objects as go

#Data
path = os.path.join('JLC_reviews', 'JLC_reviews.json')
with open(path) as f:
    data = json.load(f)

nodes = data['argument_sets']
edges = data['attack_pairs']
label = []
color = []
text = []

#Creating graph
G = nx.Graph()

for i, (argument_set, arguments) in enumerate(nodes.items()):
    for argument_id, argument_text in arguments.items():
        G.add_node(argument_id)
        label.append(argument_id)
        color.append(i)
        text.append(argument_text)

for edge in edges:
    G.add_edge(edge[0], edge[1])

text = [textwrap.fill(x, 100) for x in text]
text = [x.replace('\n', '<br>') for x in text]

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
    customdata = text,
    hovertemplate = '%{customdata}<extra></extra>',
    marker = dict(size = 10),
    showlegend = False)

node_trace.marker.color = color
node_trace.text = label

fig = go.Figure(data = [edge_trace, node_trace],
    layout = go.Layout(
        title = 'Peer review argumentation framework',
        hovermode = 'closest',
        showlegend = False,
        margin = dict(b = 20, l = 5, r = 5, t = 60),
        xaxis = dict(showgrid = False, zeroline = False, showticklabels = False),
        yaxis = dict(showgrid = False, zeroline = False, showticklabels = False)))

#for i, side in enumerate(nodes.keys()):
#    fig.add_trace(
#        go.Scatter(
#            x=[None], 
#            y=[None],
#            name=side,
#            mode='markers',
#            marker=dict(color=i),
#            showlegend=True
#        )
#    )

fig.write_html(f'{path.split(".")[0]}.html')
