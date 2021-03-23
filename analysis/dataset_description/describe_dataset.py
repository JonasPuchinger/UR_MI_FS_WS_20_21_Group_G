import os
import json
import csv
from statistics import mean, median

# Paths for data directories and files

POLITICIANS_LIST = '../../assets/all_politicians.json'
TWEETS_SOURCE_FOLDER = '../formated_data/tweet/'
USERS_SOURCE_FOLDER = '../formated_data/user/'
RESULTS_FILE = 'politicians_tweets_stats.csv'

results = []

# Functions to calculate/collect tweet statisitics for a given politician in our dataset
# For an explanation of the statistics check the list below

def count_tweets_for_user(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                all_tweets = [t for t in f_content]
                tweets_by_user = [t for t in all_tweets if t['raw_data']['user_id_str'] == str(user_id)]
                return len(all_tweets), len(tweets_by_user)
    return 0, 0

def count_lang_tweets_for_user(screen_name, user_id, lang):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                all_tweets = [t for t in f_content if t['raw_data']['lang'] == lang]
                tweets_by_user = [t for t in all_tweets if t['raw_data']['user_id_str'] == str(user_id) and t['raw_data']['lang'] == lang]
                return len(all_tweets), len(tweets_by_user)
    return 0, 0

def count_tweets_by_lang_for_user(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                tweets_by_user = [t for t in f_content if t['raw_data']['user_id_str'] == str(user_id)]
                tweets_by_lang = {}
                for t in tweets_by_user:
                    if 'lang' in t['raw_data']:
                        tweets_by_lang[t['raw_data']['lang']] = tweets_by_lang.get(t['raw_data']['lang'], 0) + 1 
                return tweets_by_lang
    return {}

def count_replies_for_user(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                replies = [t for t in f_content if t['raw_data']['user_id_str'] == str(user_id) and t['raw_data']['in_reply_to_status_id'] != None]
                return len(replies)
    return 0

def count_replies_to_self_for_user(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                replies = [t for t in f_content if t['raw_data']['user_id_str'] == str(user_id)
                                                and t['raw_data']['in_reply_to_status_id'] != None
                                                and t['raw_data']['in_reply_to_user_id_str'] == str(user_id)]
                return len(replies)
    return 0

def count_replies_to_others_for_user(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                replies = [t for t in f_content if t['raw_data']['user_id_str'] == str(user_id)
                                                and t['raw_data']['in_reply_to_status_id'] != None
                                                and t['raw_data']['in_reply_to_user_id_str'] != str(user_id)]
                return len(replies)
    return 0

def count_likes_for_user(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                likes = [t['raw_data']['favorite_count'] for t in f_content if t['raw_data']['user_id_str'] == str(user_id)]
                return sum(likes), mean(likes), median(likes)
    return 0, 0, 0

def count_retweets_for_user(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                retweets = [t['raw_data']['retweet_count'] for t in f_content if t['raw_data']['user_id_str'] == str(user_id)]
                return sum(retweets), mean(retweets), median(retweets)
    return 0, 0, 0

def count_replies_to_user(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                replies = [t['raw_data']['reply_count'] for t in f_content if t['raw_data']['user_id_str'] == str(user_id)]
                return sum(replies), mean(replies), median(replies)
    return 0, 0, 0

def get_followers(screen_name, user_id):
    f_path = os.path.join(USERS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                # followers = [u['raw_data']['followers_count'] for u in json.load(infile) if u['id_'] == str(user_id)][0]
                followers = next((u['raw_data']['followers_count'] for u in f_content if u['id_'] == str(user_id)), 0)
                return followers
    return 0

def get_verification_status(screen_name, user_id):
    f_path = os.path.join(USERS_SOURCE_FOLDER, f'{screen_name}.json')
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                verified = str(next((u['raw_data']['verified'] for u in f_content if u['id_'] == str(user_id)), 'False'))
                return verified
    return 'False'

# Loop over all politicians in our dataset
# For every politician, a object with the following statistics is generated:
# name: Name of the politician
# screen_name: Twitter handle
# followers: number of followers
# verified: If account is verified or not
# party: Politicial party the politician belongs to
# total_tweets_found: How many tweets were scraped by requests for this politician
# tweets_by_politician: How many of the scraped tweets are authored by the politician itself
# ratio_own_tweets: Ratio tweets_by_politician / total_tweets_found
# total_german_tweets: How many of all scraped tweets for a politician are annotated by Twitter as German
# german_tweets_by_politician: How many of the politicians tweets are annotated by Twitter as German
# tweets_by_annotated_language: Dictionary of how many tweets per language are in the politicians scraped tweets
# replies_by_politician: How many of the politicians tweets are replies
# replies_by_politician_to_self: How many of the politicians replies are replies to themself (part of a thread)
# replies_by_politician_to_others: How many of the politicians replies are replies to other accounts
# ratio_replies_to_own_tweets: Ratio replies_by_politician / tweets_by_politician
# total_likes: Number of total likes of all tweets by the politician in the dataset
# mean_likes: Mean number of likes over all tweets by the politician in the dataset
# median_likes: Median number of likes over all tweets by the politician in the dataset
# total_retweets: Number of total retweets of all tweets by the politician in the dataset
# mean_retweets: Mean number of retweets over all tweets by the politician in the dataset
# median_retweets: Median number of retweets over all tweets by the politician in the dataset
# total_replies_to: Number of total replies to all tweets by the politician in the dataset
# mean_replies_to: Mean number of retweets to all tweets by the politician in the dataset
# median_replies_to: Median number of retweets to all tweets by the politician in the dataset

with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
    for p in json.load(infile):
        p_name = p['Name']
        p_screen_name = p['screen_name']
        p_user_id = p['id']
        p_followers = get_followers(screen_name=p_screen_name, user_id=p_user_id)
        p_verified = get_verification_status(screen_name=p_screen_name, user_id=p_user_id)
        p_party = p['Partei']
        p_total_tweets_found, p_tweets_by_politician = count_tweets_for_user(screen_name=p_screen_name, user_id=p_user_id)
        p_ratio_own_tweets = round((float(p_tweets_by_politician) / float(p_total_tweets_found)) * 100, 2) if p_total_tweets_found != 0 else 0
        p_total_german_tweets, p_german_tweets_by_polititcian = count_lang_tweets_for_user(screen_name=p_screen_name, user_id=p_user_id, lang='de')
        p_tweets_by_annotated_language = count_tweets_by_lang_for_user(screen_name=p_screen_name, user_id=p_user_id)
        p_replies_by_politician = count_replies_for_user(screen_name=p_screen_name, user_id=p_user_id)
        p_replies_to_self = count_replies_to_self_for_user(screen_name=p_screen_name, user_id=p_user_id)
        p_replies_to_others = count_replies_to_others_for_user(screen_name=p_screen_name, user_id=p_user_id)
        p_ratio_replies = round((float(p_replies_by_politician) / float(p_tweets_by_politician)) * 100, 2) if p_tweets_by_politician != 0 else 0
        p_total_likes, p_mean_likes, p_median_likes = count_likes_for_user(screen_name=p_screen_name, user_id=p_user_id)
        p_total_retweets, p_mean_retweets, p_median_retweets = count_retweets_for_user(screen_name=p_screen_name, user_id=p_user_id)
        p_total_replies_to, p_mean_replies_to, p_median_replies_to = count_replies_to_user(screen_name=p_screen_name, user_id=p_user_id)
        p_tweets_stats = {
            'name': p_name,
            'screen_name': p_screen_name,
            'followers': p_followers,
            'verified': p_verified,
            'party': p_party,
            'total_tweets_found': p_total_tweets_found,
            'tweets_by_politician': p_tweets_by_politician,
            'ratio_own_tweets': p_ratio_own_tweets,
            'total_german_tweets': p_total_german_tweets,
            'german_tweets_by_politician': p_german_tweets_by_polititcian,
            'tweets_by_annotated_language': p_tweets_by_annotated_language,
            'replies_by_politician': p_replies_by_politician,
            'replies_by_politician_to_self': p_replies_to_self,
            'replies_by_politician_to_others': p_replies_to_others,
            'ratio_replies_to_own_tweets': p_ratio_replies,
            'total_likes': p_total_likes,
            'mean_likes': p_mean_likes,
            'median_likes': p_median_likes,
            'total_retweets': p_total_retweets,
            'mean_retweets': p_mean_retweets,
            'median_retweets': p_median_retweets,
            'total_replies_to': p_total_replies_to,
            'mean_replies_to': p_mean_replies_to,
            'median_replies_to': p_median_replies_to
        }
        results.append(p_tweets_stats)

# Saving the collected statistics in a .csv file

keys = results[0].keys()

with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as outfile:
    dict_writer = csv.DictWriter(outfile, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
