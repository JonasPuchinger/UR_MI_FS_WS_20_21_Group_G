import os
import csv
import json

# get all tweets of politician

POLITICIANS_LIST = '../assets/test_politicians.json'
# POLITICIANS_LIST = '../assets/all_politicians.json'
TWEETS_SOURCE_FOLDER = './formated_data/tweet/'
RESULTS_FILE = 'all_tweets_politician.csv'

results = []


def get_all_tweets(screen_name, user_id):
    result = []
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')

    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            all_tweets = [t for t in json.load(infile)]
            tweets_by_user = [t for t in all_tweets if t['raw_data']['user_id_str'] == str(user_id)]
            for t in tweets_by_user:
                result.append([t['raw_data']['full_text']])
            return result
    return ""


with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
    for p in json.load(infile):
        p_name = p['Name']
        p_screen_name = p['screen_name']
        p_user_id = p['id']
        tweets = get_all_tweets(screen_name=p_screen_name, user_id=p_user_id)

        for i in tweets:
            p_tweets_stats = {
                'name': p_name,
                'tweet': i,
            }
            results.append(p_tweets_stats)

keys = results[0].keys()

with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as outfile:
    dict_writer = csv.DictWriter(outfile, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
