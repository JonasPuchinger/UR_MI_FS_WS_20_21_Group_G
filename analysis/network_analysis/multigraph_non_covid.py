import os
import json
import csv
import networkx as nx
from matplotlib import colors
from collections import Counter

# Color palette

node_colors_hex = {
    'SPD': '#D62728',
    'CDU': '#000000',
    'AfD': '#1F77B4',
    'FDP': '#FFD700',
    'Bündnis 90/Die Grünen': '#2CA02C',
    'Die Linke': '#9467BD',
    'CSU': '#17BECF',
    'Fraktionslos': '#7F7F7F',
    'Nachrichtenportal': '#FF8C00',
    'Virologe': '#800000',
}

# Paths for data directories and files

USERS_FOLDER = '../formated_data/user/'
ALL_POLITICIANS_FILE = '../../assets/all_politicians.json'
NEWS_PORTALS_FILE = '../../assets/news_portals.json'
VIROLOGISTS_FILE = '../../assets/virologists.json'
POLITICIANS_RELATIONS_FOLDER = '../formated_data/relationship_politicians'
ADDITIONAL_ACCOUNTS_RELATIONS_FOLDER = '../formated_data/relationship_additional_accounts'
MENTIONS_BY_USERS_FILE = '../tweet_entities_analysis/tweets_by_user_non_covid/mentions_tweets_by_user_non_covid.csv'
TWEETS_FOLDER = '../filtered_data/non_covid_tweets_by_politician/'
QUOTE_TWEETS_FOLDER = '../filtered_data/quote_non_covid_tweets/'

# Opening and reading data from files

with open(ALL_POLITICIANS_FILE, 'r', encoding='utf-8') as infile_all_politicians:
    all_politicians = json.load(infile_all_politicians)
with open(NEWS_PORTALS_FILE, 'r', encoding='utf-8') as infile_news_portals:
    news_portals = json.load(infile_news_portals)
with open(VIROLOGISTS_FILE, 'r', encoding='utf-8') as infile_virologists:
    virologists = json.load(infile_virologists)

# Preparing files and data

additional_accounts = news_portals + virologists
all_accounts = all_politicians + additional_accounts
all_screen_names = [a['screen_name'] for a in all_accounts]
all_acc_ids = [a['id'] for a in all_accounts]

# Helper functions

def get_user_id(screen_name):
    return next((u['id'] for u in all_accounts if u['screen_name'] == screen_name), None)

def get_acc_association(acc):
    if acc in all_politicians:
        return acc['Partei']
    else:
        return 'Nachrichtenportal' if acc in news_portals else 'Virologe'

def convert_color_to_rgba_dict(hex_color):
    rgba = colors.to_rgba(hex_color)
    return {'r': f'{int(rgba[0] * 255)}', 'g': f'{int(rgba[1] * 255)}', 'b': f'{int(rgba[2] * 255)}', 'a': f'{rgba[3]}'}

def get_tweet_from_list(tweet_id, tweet_list):
    return next((t for t in tweet_list if t['id_'] == tweet_id), None)

# Creating nodes for the network graph

nodes = [(acc['id'], {
            'label': acc['Name'],
            'name': acc['Name'],
            'screen_name': acc['screen_name'],
            'association': get_acc_association(acc),
            'color': node_colors_hex[get_acc_association(acc)]
        }) for acc in all_accounts]

node_color_map = [n[1]['color'] for n in nodes]

# Creating edges based on follower relationships

edges_followers = []

for p_rel_file in os.listdir(POLITICIANS_RELATIONS_FOLDER):
    curr_p_screen_name = os.path.splitext(p_rel_file)[0]
    curr_p_id = next((p['id'] for p in all_politicians if p['screen_name'] == curr_p_screen_name), None)
    with open(os.path.join(POLITICIANS_RELATIONS_FOLDER, p_rel_file), 'r', encoding='utf-8') as infile_curr_p_rels:
        curr_p_rels = json.load(infile_curr_p_rels)
        edges_followers += [(curr_p_id, r['target_id']) for r in curr_p_rels if  r['value'] in (1, 2)]

for a_rel_file in os.listdir(ADDITIONAL_ACCOUNTS_RELATIONS_FOLDER):
    curr_a_screen_name = os.path.splitext(a_rel_file)[0]
    curr_a_id = next((a['id'] for a in additional_accounts if a['screen_name'] == curr_a_screen_name), None)
    with open(os.path.join(ADDITIONAL_ACCOUNTS_RELATIONS_FOLDER, a_rel_file), 'r', encoding='utf-8') as infile_curr_a_rels:
        curr_a_rels = json.load(infile_curr_a_rels)
        edges_followers += [(curr_a_id, r['target_id']) for r in curr_a_rels if  r['value'] in (1, 2)]

# Creating edges based on mentions

with open(MENTIONS_BY_USERS_FILE, encoding='utf-8') as infile_mentions:
    mentions = [{k: v for k, v in row.items()} for row in csv.DictReader(infile_mentions, skipinitialspace=True)]

edges_mentions = [(int(m['id']), get_user_id(m['mention'])) for m in mentions if m['mention'] in all_screen_names]

edges_mentions_counter = Counter(edges_mentions)
weighted_edges_mentions = [(e[0], e[1], edges_mentions_counter[e]) for e in edges_mentions_counter]

# Creating edges based on replies 

edges_replies = []

for p_tweet_file in os.listdir(TWEETS_FOLDER):
    curr_p_screen_name = os.path.splitext(p_tweet_file)[0]
    curr_p_id = next((p['id'] for p in all_politicians if p['screen_name'] == curr_p_screen_name), None)
    with open(os.path.join(TWEETS_FOLDER, p_tweet_file), 'r', encoding='utf-8') as infile_curr_p_tweets:
        curr_p_tweets = json.load(infile_curr_p_tweets)
        edges_replies += [(curr_p_id, int(t['raw_data']['in_reply_to_user_id_str'])) for t in curr_p_tweets if t['raw_data']['in_reply_to_screen_name'] in all_screen_names]

edges_replies = [e for e in edges_replies if e[0] in all_acc_ids and e[1] in all_acc_ids]
edges_replies_counter = Counter(edges_replies)
weighted_edges_replies = [(e[0], e[1], edges_replies_counter[e]) for e in edges_replies_counter]

# Creating edges based on quote tweets

edges_quotes = []

for p_tweet_file in os.listdir(TWEETS_FOLDER):
    curr_p_screen_name = os.path.splitext(p_tweet_file)[0]
    curr_p_id = next((p['id'] for p in all_politicians if p['screen_name'] == curr_p_screen_name), None)
    with open(os.path.join(TWEETS_FOLDER, p_tweet_file), 'r', encoding='utf-8') as infile_curr_p_tweets:
        curr_p_tweets = json.load(infile_curr_p_tweets)
        curr_p_quote_tweets_file = os.path.join(QUOTE_TWEETS_FOLDER, f'{curr_p_screen_name}.json')
        curr_p_quote_tweets = json.load(open(curr_p_quote_tweets_file, 'r', encoding='utf-8'))
        for t in curr_p_tweets:
            if t['raw_data']['is_quote_status'] and 'quoted_status_id_str' in t['raw_data']:
                curr_quote_tweet = get_tweet_from_list(t['raw_data']['quoted_status_id_str'], curr_p_quote_tweets)
                if curr_quote_tweet is not None:
                    edges_quotes.append((curr_p_id, int(curr_quote_tweet['raw_data']['user_id_str'])))

edges_quotes = [e for e in edges_quotes if e[0] in all_acc_ids and e[1] in all_acc_ids]
edges_quotes_counter = Counter(edges_quotes)
weighted_edges_quotes = [(e[0], e[1], edges_quotes_counter[e]) for e in edges_quotes_counter]

# Initializing the network graph

G = nx.MultiDiGraph()

# Adding all nodes and edges to the graph

G.add_nodes_from(nodes)
G.add_edges_from(edges_followers)
G.add_weighted_edges_from(weighted_edges_mentions)
G.add_weighted_edges_from(weighted_edges_replies)
G.add_weighted_edges_from(weighted_edges_quotes)

# Associating color information with the nodes (needs to be done like this for Gephi to correctly read it)

for i, n in enumerate(G.nodes):
    G.add_node(n, viz={'color': convert_color_to_rgba_dict(node_color_map[i]), 'size': 20})

# Save graph object to .gexf file (can be imported in Gephi)

# nx.write_gexf(G, 'multi_graph_non_covid.gexf')