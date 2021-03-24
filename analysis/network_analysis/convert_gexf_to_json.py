import json
import networkx as nx

G = nx.read_gexf('./communities_multigraph_directed.gexf')

json.dump(nx.node_link_data(G), open('communities_multigraph.json', 'w', encoding='utf-8'), indent=2)