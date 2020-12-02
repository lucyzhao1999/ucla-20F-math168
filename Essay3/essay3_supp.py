import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file = open("womenClub.txt", "r")  # saves the file
lines = file.read().splitlines()

sources = [int(L.split(' ')[0]) for L in lines]
targets = [int(L.split(' ')[1]) for L in lines]

G = nx.Graph()
E = len(sources)
for i in range(E):
    G.add_edge(sources[i], targets[i])

# visualize
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels = True, node_shape='d')
plt.savefig('womenClubNet_nodesShape')
plt.show()


# visualize
colorList = []
degrees = [G.degree(n) for n in G.nodes()]

for i in range(len(degrees)):
    color = 'y' if degrees[i] == max(degrees) else'b'
    colorList.append(color)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels = True, node_color = colorList)
plt.savefig('womenClubNet_nodesColor')
plt.show()


f = open("fifa2015.csv")
ncols = len(f.readline().split(','))
df = pd.read_csv("fifa2015.csv", skiprows = 1, usecols = range(1, ncols), header = None)
col_names = {i : i-1 for i in range(1, ncols)}
df = df.rename(columns = col_names)
G = nx.from_pandas_adjacency(df)

plt.figure(figsize = (5, 5))
nx.draw(G, node_size = 5)
plt.savefig('fifa2015')
plt.show()


# visualize
colorList = []
degrees = [G.degree(n) for n in G.nodes()]

for i in range(len(degrees)):
    color = 'y' if degrees[i] == max(degrees) else'b'
    colorList.append(color)

# pos = nx.spring_layout(G)
pos = nx.spring_layout(G,k=0.15,iterations=20)
plt.figure(figsize = (20, 20))
nx.draw(G, pos, node_size = 5)
plt.savefig('fifa_nodesColor')
plt.show()