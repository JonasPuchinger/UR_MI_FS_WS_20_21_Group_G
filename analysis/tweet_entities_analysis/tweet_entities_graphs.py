import os
import json
import csv
import networkx as nx
from matplotlib import colors
from collections import Counter

node_colors_hex = {
    'SPD': '#ff0000',
    'CDU': '#000000',
    'AfD': '#0000ff',
    'FDP': '#ffff00',
    'Bündnis 90/Die Grünen': '#00ff00',
    'Die Linke': '#800080',
    'CSU': '#add8e6',
    'Fraktionslos': '#777777',
    'Nachrichtenportal': '#ffa500',
    'Virologe': '#800000',
}

USERS_FOLDER = '../formated_data/user/'
ALL_POLITICIANS_FILE = '../../assets/all_politicians.json'
NEWS_PORTALS_FILE = '../../assets/news_portals.json'
VIROLOGISTS_FILE = '../../assets/virologists.json'

with open(ALL_POLITICIANS_FILE, 'r', encoding='utf-8') as infile_all_politicians:
    all_politicians = json.load(infile_all_politicians)
with open(NEWS_PORTALS_FILE, 'r', encoding='utf-8') as infile_news_portals:
    news_portals = json.load(infile_news_portals)
with open(VIROLOGISTS_FILE, 'r', encoding='utf-8') as infile_virologists:
    virologists = json.load(infile_virologists)

additional_accounts = news_portals + virologists
all_accounts = all_politicians + additional_accounts
all_screen_names = [a['screen_name'] for a in all_accounts]
all_acc_ids = [a['id'] for a in all_accounts]

def get_user_id(screen_name):
    return next((u['id'] for u in all_accounts if u['screen_name'] == screen_name), None)

def get_acc_association(acc):
    if acc in all_politicians:
        return acc['Partei']
    else:
        return 'Nachrichtenportal' if acc in news_portals else 'Virologe'

def convert_color_to_rgba_dict(hex_color):
    rgba = colors.to_rgba(hex_color)
    return {'r': f'{int(rgba[0] * 255)}','g': f'{int(rgba[1] * 255)}', 'b': f'{int(rgba[2] * 255)}', 'a': f'{rgba[3]}'}

nodes = [(acc['id'], {
            'label': acc['Name'],
            'name': acc['Name'],
            'screen_name': acc['screen_name'],
            'association': get_acc_association(acc),
            'color': node_colors_hex[get_acc_association(acc)]
        }) for acc in all_accounts]

node_color_map = [n[1]['color'] for n in nodes]

MENTIONS_BY_USERS_FILE = './tweets_by_user/mentions_tweets_by_user.csv'

with open(MENTIONS_BY_USERS_FILE, encoding='utf-8') as infile_mentions:
    mentions = [{k: v for k, v in row.items()} for row in csv.DictReader(infile_mentions, skipinitialspace=True)]

edges_mentions = [(int(m['id']), get_user_id(m['mention'])) for m in mentions if m['mention'] in all_screen_names]

edges_mentions_counter = Counter(edges_mentions)
weighted_edges_mentions = [(e[0], e[1], edges_mentions_counter[e]) for e in edges_mentions_counter]

G_mentions = nx.DiGraph()

G_mentions.add_nodes_from(nodes)
G_mentions.add_weighted_edges_from(weighted_edges_mentions)

for i, n in enumerate(G_mentions.nodes):
    G_mentions.add_node(n, viz={'color': convert_color_to_rgba_dict(node_color_map[i]), 'size': 20})

nx.write_gexf(G_mentions, 'mentions_graph.gexf')


TWEETS_FOLDER = '../formated_data/tweet/'

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

G_replies = nx.DiGraph()

G_replies.add_nodes_from(nodes)
G_replies.add_weighted_edges_from(weighted_edges_replies)

for i, n in enumerate(G_replies.nodes):
    G_replies.add_node(n, viz={'color': convert_color_to_rgba_dict(node_color_map[i]), 'size': 20})

nx.write_gexf(G_replies, 'replies_graph.gexf')


def get_tweet_from_list(tweet_id, tweet_list):
    return next((t for t in tweet_list if t['id_'] == tweet_id), None)

edges_quotes = []

for p_tweet_file in os.listdir(TWEETS_FOLDER):
    curr_p_screen_name = os.path.splitext(p_tweet_file)[0]
    curr_p_id = next((p['id'] for p in all_politicians if p['screen_name'] == curr_p_screen_name), None)
    with open(os.path.join(TWEETS_FOLDER, p_tweet_file), 'r', encoding='utf-8') as infile_curr_p_tweets:
        curr_p_tweets = json.load(infile_curr_p_tweets)
        # edges_quotes += [(curr_p_id, int(get_tweet_from_list(t['raw_data']['quoted_status_id_str'], curr_p_tweets)['raw_data']['user_id_str'])) 
        #                     for t in curr_p_tweets 
        #                     if t['raw_data']['is_quote_status'] and 'quoted_status_id_str' in t['raw_data']]
        for t in curr_p_tweets:
            if t['raw_data']['is_quote_status'] and 'quoted_status_id_str' in t['raw_data']:
                curr_quote_tweet = get_tweet_from_list(t['raw_data']['quoted_status_id_str'], curr_p_tweets)
                if curr_quote_tweet is not None:
                    edges_quotes.append((curr_p_id, int(curr_quote_tweet['raw_data']['user_id_str'])))

edges_quotes = [e for e in edges_quotes if e[0] in all_acc_ids and e[1] in all_acc_ids]
edges_quotes_counter = Counter(edges_quotes)
weighted_edges_quotes = [(e[0], e[1], edges_quotes_counter[e]) for e in edges_quotes_counter]

G_quotes = nx.DiGraph()

G_quotes.add_nodes_from(nodes)
G_quotes.add_weighted_edges_from(weighted_edges_quotes)

for i, n in enumerate(G_quotes.nodes):
    G_quotes.add_node(n, viz={'color': convert_color_to_rgba_dict(node_color_map[i]), 'size': 20})

nx.write_gexf(G_quotes, 'quotes_graph.gexf')
