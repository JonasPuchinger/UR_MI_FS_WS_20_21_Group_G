import networkx as nx
from infomap import Infomap

# Read in graph object from .gexf file
# Change filename to whatever graph is needed

G = nx.read_gexf('./multi_graph_non_covid.gexf')

# Infomap cannot deal with lenghty ids, therefore the nodes are renamed to their index

nodes_rename = {n: i for i, n in enumerate(G.nodes)}
G = nx.relabel_nodes(G, nodes_rename)

# Initialize Infomap; the '--directed' flag is important because we are dealing with directed network graphs

im = Infomap('--two-level --directed')

# For each edge in the graph create a link for Infomap

for e in G.edges:
    im.add_link(int(e[0]), int(e[1]))

# Run the Infomap algorithm on the modified graph object 

im.run()

# Set the community attribute for each node

communities = im.get_modules()
nx.set_node_attributes(G, communities, 'community')

# Save graph object to .gexf file (can be imported in Gephi)
# Change filename to whatever graph is imported at the start of the file

# nx.write_gexf(G, 'communities_multigraph_non_covid_directed.gexf')