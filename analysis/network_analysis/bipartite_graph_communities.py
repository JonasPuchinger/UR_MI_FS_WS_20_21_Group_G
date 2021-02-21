import networkx as nx
from infomap import Infomap

G = nx.read_gexf('./bipartite_graph_domains.gexf')

nodes_rename = {n: i for i, n in enumerate(G.nodes)}

G = nx.relabel_nodes(G, nodes_rename)

im = Infomap('--two-level')

for e in G.edges:
    im.add_link(int(e[0]), int(e[1]))

im.run()

print(f'Found {im.num_top_modules} modules with codelength: {im.codelength}')

communities = im.get_modules()
nx.set_node_attributes(G, communities, 'community')
# nx.write_gexf(G, 'communities_bipartite_graph_hashtags.gexf')