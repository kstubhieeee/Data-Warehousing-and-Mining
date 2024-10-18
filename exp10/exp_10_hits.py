# Importing modules
import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()  # Fixed typo from DiGarph to DiGraph

# Adding edges to the graph
G.add_edges_from([
    ('A', 'D'), 
    ('B', 'C'), 
    ('B', 'E'), 
    ('C', 'A'),
    ('D', 'C'), 
    ('E', 'D'), 
    ('E', 'B'), 
    ('E', 'F'),
    ('E', 'C'), 
    ('F', 'C'), 
    ('F', 'H'), 
    ('G', 'A'),
    ('G', 'C'), 
    ('H', 'A')
])

# Set up the plot
plt.figure(figsize=(10, 10))

# Draw the graph with labels
nx.draw_networkx(G, with_labels=True)

# Calculate HITS scores
hubs, authorities = nx.hits(G, max_iter=50, normalized=True)

# The in-built hits function returns two dictionaries keyed by nodes
# containing hub scores and authority scores respectively.
print("Hub Scores: ", hubs)
print("Authority Scores: ", authorities)
