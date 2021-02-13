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

def get_acc_association(acc):
    if acc in all_politicians:
        return acc['Partei']
    else:
        return 'Nachrichtenportal' if acc in news_portals else 'Virologe'

nodes = [(acc['id'], {
            'label': acc['Name'],
            'name': acc['Name'],
            'screen_name': acc['screen_name'],
            'association': get_acc_association(acc),
            'color': node_colors_hex[get_acc_association(acc)]
        }) for acc in all_accounts]

MENTIONS_BY_USERS_FILE = './tweets_by_user/mentions_tweets_by_user.csv'

with open(MENTIONS_BY_USERS_FILE, encoding='utf-8') as infile_mentions:
    mentions = [{k: v for k, v in row.items()} for row in csv.DictReader(infile_mentions, skipinitialspace=True)]

print(mentions)

edges_mentions = []