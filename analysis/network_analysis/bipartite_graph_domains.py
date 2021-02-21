import json
import networkx as nx
import pandas as pd
from matplotlib import colors

DOMAINS_FILE = '../tweet_entities_analysis/tweets_by_user/domains_tweets_by_user.csv'
ALL_POLITICIANS_FILE = '../../assets/all_politicians.json'

node_colors_hex = {
    'SPD': '#D62728',
    'CDU': '#000000',
    'AfD': '#1F77B4',
    'FDP': '#FFD700',
    'Bündnis 90/Die Grünen': '#2CA02C',
    'Die Linke': '#9467BD',
    'CSU': '#17BECF',
    'Fraktionslos': '#7F7F7F'
}

df_domains = pd.read_csv(DOMAINS_FILE)

top_domains = df_domains['domain'].value_counts(sort=True, ascending=False).head(5)
top_domains = list(top_domains.reset_index()['index'])

with open(ALL_POLITICIANS_FILE, 'r', encoding='utf-8') as infile_all_politicians:
    all_politicians = json.load(infile_all_politicians)

domains_per_p = {}

for p in all_politicians:
    curr_p_id = p['id']
    domains_per_p[curr_p_id] = []
    for d in top_domains:
        curr_p_h_uses = len(df_domains.loc[df_domains['id'] == curr_p_id].loc[df_domains['domain'] == d].index)
        if curr_p_h_uses > 0:
            domains_per_p[curr_p_id].append((d, curr_p_h_uses))

G = nx.Graph()

for user in domains_per_p:
    for domain in domains_per_p[user]:
        G.add_edge(user, domain[0], weight=domain[1])

actual_users_with_hashtags = [x for x in domains_per_p.keys() if x in G.nodes()]

G = nx.bipartite.weighted_projected_graph(G, nodes=actual_users_with_hashtags)

# G.add_nodes_from([x for x in domains_per_p.keys() if x not in G.nodes()])

def get_acc_association(id):
    return next((a['Partei'] for a in all_politicians if a['id'] == id), None)

def convert_color_to_rgba_dict(hex_color):
    rgba = colors.to_rgba(hex_color)
    return {'r': f'{int(rgba[0] * 255)}','g': f'{int(rgba[1] * 255)}', 'b': f'{int(rgba[2] * 255)}', 'a': f'{rgba[3]}'}

for i, n in enumerate(G.nodes):
    G.add_node(n, viz={'color': convert_color_to_rgba_dict(node_colors_hex[get_acc_association(n)]), 'size': 20})

# nx.write_gexf(G, 'bipartite_graph_domains_2.gexf')