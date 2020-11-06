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
nx.draw(G, pos, with_labels = True)
plt.savefig('womenClubNet')
plt.show()

# degree distribution
totalDegree = 2*E
degrees = [G.degree(n) for n in G.nodes()]

binwidth = 1
binsList = np.arange(min(degrees)-binwidth, max(degrees) + binwidth, binwidth)
plt.hist(degrees, bins=binsList, weights=np.zeros_like(degrees) + 1. / len(degrees))
plt.xticks(range(max(degrees)+1))
plt.xlabel('Degree')
plt.ylabel('Probability')
plt.savefig('womenClubNetDegDist')
plt.show()


f = open("fifa2015.csv")
ncols = len(f.readline().split(','))
df = pd.read_csv("fifa2015.csv", skiprows = 1, usecols = range(1, ncols), header = None)
col_names = {i : i-1 for i in range(1, ncols)}
df = df.rename(columns = col_names)
G = nx.from_pandas_adjacency(df)

plt.figure(figsize = (10, 10))
nx.draw(G, node_size = 5)
plt.savefig('fifa2015')
plt.show()

# degree distribution
degrees = [G.degree(n) for n in G.nodes()]

binwidth = 1
binsList = np.arange(min(degrees)-binwidth, max(degrees) + binwidth, binwidth)
plt.hist(degrees, bins=binsList, weights=np.zeros_like(degrees) + 1. / len(degrees))
plt.xticks(range(0, max(degrees)+1, 20))
plt.xlabel('Degree')
plt.ylabel('Probability')
plt.savefig('fifa2015DegDist')
plt.show()