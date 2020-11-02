# -*- coding: utf-8 -*-
"""
Math 168 Networkx Demo
Fall 2020
Week 4
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd # won't need right away

'''
Intro: Manually making a network 
'''

#G = nx.Graph() # Makes an empty (undirected) network
G = nx.DiGraph()    # Makes an empty directed network
G.add_node(0)
G.add_node(1)

# Let's make a star network
for i in range(1, 10):
    G.add_edge(0, i)    # Adds an edge between 0 and node i. Automatically creates node i if it doesn't already exist
nx.draw(G, with_labels = True)
plt.show()

''' 
Basic functions for analyzing your network
'''

N = len(G)  # returns number of nodes in G
G.has_edge(0,1) # Returns true
G.has_edge(1, 0) # returns false because G is directed and only has 0-->1, not 1-->0
nx.has_path(G, 0, 1) # returns true because there's a path from 0 to 1
nx.shortest_path(G, 0,1) # returns list of nodes in the shortest path from 0 to 1
G.degree() # returns dictionary where keys are the nodes and values are the degrees
G.degree()[0]   # Degree of node 0

'''
Reading in network data from an edge list
Example: Russian trade network.
'''

file = open("russiantrade_edges.txt", "r")  # saves the file
lines = file.read().splitlines()    # Reads in the file line by line, saves each line as an element in a list

# L.split('\t') splits line L every time it sees \t and stores each piece in a list. 
# It returns a list with two elements, the source node and target node.
sources = [int(L.split('\t')[0]) for L in lines]
targets = [int(L.split('\t')[1]) for L in lines]

# Make the network
G = nx.Graph()
E = len(sources)    # Number of edges
for i in range(E):
    G.add_edge(sources[i], targets[i])

# Draw the network.
nx.draw(G, with_labels = True)
plt.show()

# Better visualization. (Can make a bigger difference with larger networks.)
pos = nx.spring_layout(G)   # Uses Fruchterman-Reingold algorithm to find "optimal" node positions
nx.draw(G, pos, with_labels = True)
plt.show()

'''
Reading in network data from an adjacency matrix stored as csv file
Example: Paul Revere network. Nodes are individuals associated with P. Revere's ride.
Edges are number of organizations that both nodes are affiliated with. 
(Projection from a bipartite network.)
'''

f = open("PREVERE1MODE.csv")
ncols = len(f.readline().split(','))
df = pd.read_csv("PREVERE1MODE.csv", skiprows = 1, usecols = range(1, ncols), header = None)    # skips the top row in the file and only uses columns 1 though ncols (using 0-indicing). Tells pandas not to expect a header
print(df) # notice the column names are 1, ...., ncols-1
col_names = {i : i-1 for i in range(1, ncols)}  # Column names must match column indices (It's what networkx wants, I don't know why.)
df = df.rename(columns = col_names) # Renaming columns so that column names match column indices.
G = nx.from_pandas_adjacency(df)    # Makes a network from the pandas adjacency matrix

# Visualize the network
pos = nx.spring_layout(G)
plt.figure(figsize = (50, 50))  # Make figure bigger so we can actually see all the edges! (See what happens otherwise by calling nx.draw(G) before this line.)
nx.draw(G, pos, node_size = 25)
plt.show()

# How should we visualize the edge weights?
# Access edge data and assign colors according to edge weight. (This is just one option for visualizing edge weights.)
color = ['k', 'y', 'r'] # k means black, y means yellow, r means red.
for u, v in G.edges():  # Iterate through all edges (u, v).
    G[u][v]['weight']   # weight of edge (u,v). This edge attribute is already stored in G, because it was in the df adjacency matrix that we created the network from.
    G[u][v]['color'] = color[min(G[u][v]['weight']-1, 2)] # Assign new edge attribute 'color'.
my_edge_colors = [G[u][v]['color'] for u, v in G.edges()]
nx.draw(G, pos, node_size = 25, edge_color = my_edge_colors)

# View just the high-weight edges (excluding self-edges) plus the nodes incident to those edges
high_wgt_edges = [(u, v) for u, v in G.edges() if G[u][v]['weight'] > 1 and not u == v]
high_wgt_colors = [G[u][v]['color'] for u, v in high_wgt_edges]
H = G.edge_subgraph(high_wgt_edges) # Network that contains the edges of G w/ weight > 1 (excluding self-edges), plus all nodes incident to those edges.
plt.figure(figsize = (50, 50)) 
pos = nx.spring_layout(H)
nx.draw(H, pos, with_labels = True, node_size = 20, edge_color = high_wgt_colors)
plt.show()

'''
Reading in network data from gexf file
Example: Primary school contact network. Nodes are students in a primary school
plus teachers. There are edges between nodes that have contact with each other.
(Weighted by amount of contact, but we're ignoring the weights for this visualization.)
'''

G = nx.read_gexf("sp_data_school_day_1_g.gexf")
plt.figure(figsize = (50, 50))
nx.draw(G)
plt.show()

print(G.nodes(data = True)) # This network comes with extra data in addition to the adjacency information. These are the node attributes.
labels = set([G.nodes[u]['classname'] for u in G])   # A list of all the classroom names.

# Assign colors to nodes based on grade level.
class_colors = {'1A' : 'm', '1B': 'm', '2A': 'b', '2B': 'b', '3A' : 'g', '3B': 'g', '4A': 'r', '4B': 'r', '5A': 'y', '5B': 'y', 'Teachers': 'r'}
for u in G:
    # One of the node attributes is 'viz', a dictionary that contains parameters for visualizing. One of the keys in viz is 'position', which gives you node positions.
    G.nodes[u]['pos'] = (G.nodes[u]['viz']['position']['x'], G.nodes[u]['viz']['position']['y'])    # set new node attribute 'pos'
    G.nodes[u]['color'] = class_colors[G.nodes[u]['classname']] # set new node attribute 'color'

pos = nx.get_node_attributes(G, 'pos') # Assign node positions using the given node positions that came in the gexf file
color = [G.nodes[u]['color'] for u in G]
plt.figure(figsize = (50, 50))
nx.draw(G, pos, node_color = color, node_size = 700)
plt.show()

# Visualize just one classroom, say '1A'
my_class = [u for u in G if G.nodes[u]['classname'] == '1A']
H = G.subgraph(my_class)    # Network with the nodes in class '1A' plus edges whose endpoints are both in class 1A.
my_class_pos = nx.get_node_attributes(H, 'pos')
nx.draw(H, my_class_pos, with_labels = True)