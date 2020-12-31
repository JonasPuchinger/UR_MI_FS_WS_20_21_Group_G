import os
import json
import csv

POLITICIANS_LIST = '../assets/all_politicians.json'
TWEETS_SOURCE_FOLDER = './formated_data/tweet/'
RESULTS_FILE = 'politicians_tweets_stats.csv'

results = []

def count_tweets_for_user(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            all_tweets = [t for t in json.load(infile)]
            tweets_by_user = [t for t in all_tweets if t['raw_data']['user_id_str'] == str(user_id)]
        return len(all_tweets), len(tweets_by_user)
    return 0, 0

with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
    for p in json.load(infile):
        p_name = p['Name']
        p_screen_name = p['screen_name']
        p_user_id = p['id']
        p_party = p['Partei']
        p_total_tweets_found, p_tweets_by_politician = count_tweets_for_user(screen_name=p_screen_name, user_id=p_user_id)
        p_ratio = round((float(p_tweets_by_politician) / float(p_total_tweets_found)) * 100, 2) if p_total_tweets_found != 0 else 0
        p_tweets_stats = {
            'name': p_name,
            'screen_name': p_screen_name,
            'party': p_party,
            'total_tweets_found': p_total_tweets_found,
            'tweets_by_politician': p_tweets_by_politician,
            'ratio': p_ratio
        }
        results.append(p_tweets_stats)

keys = results[0].keys()

with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as outfile:
    dict_writer = csv.DictWriter(outfile, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
