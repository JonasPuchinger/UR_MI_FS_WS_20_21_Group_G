import os
import json
import csv
import networkx as nx
from matplotlib import colors

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

def get_user_id(screen_name):
    f_path = os.path.join(USERS_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                return next((u['id_'] for u in f_content if u['raw_data']['screen_name'] == screen_name), None)
    return None

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

edges_mentions = [(m['id'], get_user_id(m['mention'])) for m in mentions if m['mention'] in all_screen_names]

G_mentions = nx.DiGraph()

G_mentions.add_nodes_from(nodes)
G_mentions.add_weighted_edges_from(edges_mentions)
