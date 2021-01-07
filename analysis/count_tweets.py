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

def count_lang_tweets_for_user(screen_name, user_id, lang):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            all_tweets = [t for t in json.load(infile) if t['raw_data']['lang'] == lang]
            tweets_by_user = [t for t in all_tweets if t['raw_data']['user_id_str'] == str(user_id) and t['raw_data']['lang'] == lang]
        return len(all_tweets), len(tweets_by_user)
    return 0, 0

def count_replies_for_user(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            replies = [t for t in json.load(infile) if t['raw_data']['user_id_str'] == str(user_id) and t['raw_data']['in_reply_to_status_id'] != None]
        return len(replies)
    return 0

with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
    for p in json.load(infile):
        p_name = p['Name']
        p_screen_name = p['screen_name']
        p_user_id = p['id']
        p_party = p['Partei']
        p_total_tweets_found, p_tweets_by_politician = count_tweets_for_user(screen_name=p_screen_name, user_id=p_user_id)
        p_ratio_own_tweets = round((float(p_tweets_by_politician) / float(p_total_tweets_found)) * 100, 2) if p_total_tweets_found != 0 else 0
        p_total_german_tweets, p_german_tweets_by_polititcian = count_lang_tweets_for_user(screen_name=p_screen_name, user_id=p_user_id, lang='de')
        p_replies_by_politician = count_replies_for_user(screen_name=p_screen_name, user_id=p_user_id)
        p_tweets_stats = {
            'name': p_name,
            'screen_name': p_screen_name,
            'party': p_party,
            'total_tweets_found': p_total_tweets_found,
            'tweets_by_politician': p_tweets_by_politician,
            'ratio_own_tweets': p_ratio_own_tweets,
            'total_german_tweets': p_total_german_tweets, 
            'german_tweets_by_politician': p_german_tweets_by_polititcian,
            'replies_by_politician': p_replies_by_politician
        }
        results.append(p_tweets_stats)

keys = results[0].keys()

with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as outfile:
    dict_writer = csv.DictWriter(outfile, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
