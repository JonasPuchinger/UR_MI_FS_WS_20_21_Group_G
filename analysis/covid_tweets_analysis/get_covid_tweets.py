import os
import numpy as np
import csv
import json
import re
import codecs
from fuzzywuzzy import fuzz
from analysis.clean_data import clean_for_filtering

POLITICIANS_LIST = '../../assets/all_politicians.json'
TWEETS_SOURCE_FOLDER = '../formated_data/tweet/'
COVID_TWEETS_BY_POL_FOLDER = '../filtered_data/covid_tweets_by_politician/'
NON_COVID_TWEETS_BY_POL_FOLDER = '../filtered_data/non_covid_tweets_by_politician/'
QUOTE_COVID_TWEETS_FOLDER = '../filtered_data/quote_covid_tweets/'
QUOTE_NON_COVID_TWEETS_FOLDER = '../filtered_data/quote_non_covid_tweets/'
RESULTS_FILE_OVERVIEW = 'covid_tweets_overview.csv'
RESULTS_FILE_COVID_TWEETS_BY_P = 'covid_tweets_by_politician.csv'
RESULTS_FILE_NON_COVID_TWEETS_BY_P = 'non_covid_tweets_by_politician.csv'
RESULTS_FILE_QUOTE_COVID_TWEETS = 'quote_covid_tweets.csv'
RESULTS_FILE_QUOTE_NON_COVID_TWEETS = 'quote_non_covid_tweets.csv'
PREPROCESSED_WORDLIST = '../preprocessing_wordlist/preprocessed_wordlist.json'
UNCERTAIN_WORDS = '../preprocessing_wordlist/uncertain_words.json'

dict_results_overview = []
dict_results_detail = []
dict_non_covid_tweets = []
covid_tweet_by_politician_id = []
non_covid_tweet_by_politician_id = []
quote_covid_tweet_id = []
quote_non_covid_tweet_id = []

wordlist = json.load(codecs.open(PREPROCESSED_WORDLIST, 'r', 'utf-8-sig'))
uncertain_words = json.load(codecs.open(UNCERTAIN_WORDS, 'r', 'utf-8-sig'))


# Attaching hashtags, card title, card description to tweet
def add_info(tweet):
    info = ""
    if tweet['raw_data']['entities']['hashtags']:
        for tag in tweet['raw_data']['entities']['hashtags']:
            info += " " + tag['text']
    if tweet['raw_data'].get('card') is not None:
        if tweet['raw_data']['card']['binding_values'].get('title') is not None:
            info += " " + tweet['raw_data']['card']['binding_values']['title']['string_value']
        if tweet['raw_data']['card']['binding_values'].get('description') is not None:
            info += " " + tweet['raw_data']['card']['binding_values']['description']['string_value']
    return info


def get_all_tweets(screen_name):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')

    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            all_tweets = [t for t in json.load(infile)]
            result = []
            for t in all_tweets:
                tweet_info = t['raw_data']['full_text'] + add_info(t)
                result.append([t, clean_for_filtering(tweet_info)])
            return result
    return ""


# Check if there is a clear match (word from tweet/ word from wordlist)
def check_match(tweets):
    remaining_tweets = []
    matched_tweets = []

    def match_wordlist_and_tweet(tweet):
        list_uncertain_words = []

        for word in wordlist:
            if word in tweet[1]:
                if word in uncertain_words and len(np.unique(list_uncertain_words)) < 2:
                    list_uncertain_words.append(word)
                else:
                    return [word, 'match', tweet[0], tweet[1]]

    for t in tweets:
        result = match_wordlist_and_tweet(t)
        if result is not None:
            matched_tweets.append(result)
        else:
            remaining_tweets.append(t)

    return matched_tweets, remaining_tweets


# Check if there is a match between the regular expression and a word from the tweet
def check_match_regex(tweets):
    remaining_tweets = []
    matched_tweets = []

    def match_regex(tweet):
        list_uncertain_words = []
        for word in wordlist:
            pattern = "\\b" + word
            for token in tweet[1]:
                match = re.match(pattern, token)
                if match is not None:
                    if token in uncertain_words and len(np.unique(list_uncertain_words)) < 2:
                        list_uncertain_words.append(token)
                    else:
                        return [pattern, token, tweet[0], tweet[1]]

    for t in tweets:
        result = match_regex(t)
        if result is not None:
            matched_tweets.append(result)
        else:
            remaining_tweets.append(t)

    return matched_tweets, remaining_tweets


# Using Fuzzy Matching to check, if there is a match between tweet and wordlist
def check_match_fuzzy(tweets):
    remaining_tweets = []
    matched_tweets = []

    def match_fuzzy(tweet):
        list_uncertain_words = []
        for word in wordlist:
            for token in tweet[1]:
                if fuzz.ratio(word, token) > 90:
                    if token in uncertain_words and len(np.unique(list_uncertain_words)) < 2:
                        list_uncertain_words.append(token)
                    else:
                        return [word, token, tweet[0], tweet[1]]

    for t in tweets:
        result = match_fuzzy(t)
        if result is not None:
            matched_tweets.append(result)
        else:
            remaining_tweets.append(t)

    return matched_tweets, remaining_tweets


# Matching takes place in three steps: Clear match, Pattern Matching, Fuzzy Matching
def match_tweets(tweets_by_pol):
    matched_covid_tweets = []
    matching_part_1 = check_match(tweets_by_pol)
    matched_covid_tweets.extend(matching_part_1[0])
    matching_part_2 = check_match_regex(matching_part_1[1])
    matched_covid_tweets.extend(matching_part_2[0])
    matching_part_3 = check_match_fuzzy(matching_part_2[1])
    matched_covid_tweets.extend(matching_part_3[0])
    return matched_covid_tweets, matching_part_3[1]


def create_dict_results_overview(name, screen_name, party, results):
    p_tweets_stats = {
        'name': name,
        'screen_name': screen_name,
        'party': party,
        'covid_tweets': len(results),
    }
    dict_results_overview.append(p_tweets_stats)


def create_dict_covid_tweets_by_pol(name, party, results):
    for i in results:
        p_tweets_stats = {
            'name': name,
            'party': party,
            'created at': i[2]['raw_data']['created_at'],
            'id': i[2]['id_'],
            'word from wordlist': i[0],
            'match': i[1],
            'original tweet': i[2]['raw_data']['full_text'],
            'tweet': i[3],
        }
        dict_results_detail.append(p_tweets_stats)


def create_dict_non_covid_tweets_by_pol(name, party, results):
    for tweet in results:
        p_tweets_stats = {
            'name': name,
            'party': party,
            'created at': tweet[0]['raw_data']['created_at'],
            'tweet': tweet[0]['raw_data']['full_text'],
        }
        dict_non_covid_tweets.append(p_tweets_stats)


with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
    for p in json.load(infile):

        covid_tweet_by_politician = []
        non_covid_tweet_by_politician = []
        quote_covid_tweet = []
        quote_non_covid_tweet = []

        p_name = p['Name']
        p_user_id = p['id']
        p_screen_name = p['screen_name']
        p_party = p['Partei']

        all_tweets = get_all_tweets(screen_name=p_screen_name)
        results_matching = match_tweets(all_tweets)

        all_covid_tweets = results_matching[0]
        all_non_covid_tweets = results_matching[1]

        for t in all_covid_tweets:
            tweet = t[2]
            if tweet['raw_data']['user_id_str'] == str(p_user_id):
                covid_tweet_by_politician.append(t)
                covid_tweet_by_politician_id.append(tweet['id_'])
            elif tweet['raw_data']['user_id_str'] != str(p_user_id):
                quote_covid_tweet.append(t)
                quote_covid_tweet_id.append(tweet['id_'])

        # A quoted tweet is also considered a COVID-tweet if the original tweet is viewed as such
        for t in all_non_covid_tweets:
            tweet = t[0]
            if tweet['raw_data']['user_id_str'] == str(p_user_id):
                if tweet['raw_data']['is_quote_status'] and 'quoted_status_id_str' in tweet['raw_data']:
                    if tweet['raw_data']['quoted_status_id_str'] in quote_covid_tweet_id:
                        covid_tweet_by_politician.append(["quote", "quote", t[0], t[1]])
                        covid_tweet_by_politician_id.append(tweet['id_'])
                    else:
                        non_covid_tweet_by_politician.append(t)
                        non_covid_tweet_by_politician_id.append(tweet['id_'])
                else:
                    non_covid_tweet_by_politician.append(t)
                    non_covid_tweet_by_politician_id.append(tweet['id_'])

            elif tweet['raw_data']['user_id_str'] != str(p_user_id):
                quote_non_covid_tweet.append(t)
                quote_non_covid_tweet_id.append(tweet['id_'])

        create_dict_results_overview(p_name, p_screen_name, p_party, covid_tweet_by_politician)
        create_dict_covid_tweets_by_pol(p_name, p_party, covid_tweet_by_politician)
        create_dict_non_covid_tweets_by_pol(p_name, p_party, non_covid_tweet_by_politician)

    keys_results_overview = dict_results_overview[0].keys()
    keys_results_detail = dict_results_detail[0].keys()
    keys_remaining_tweets = dict_non_covid_tweets[0].keys()

    with open(RESULTS_FILE_OVERVIEW, 'w', newline='', encoding='utf-8') as outfile:
        dict_writer = csv.DictWriter(outfile, keys_results_overview)
        dict_writer.writeheader()
        dict_writer.writerows(dict_results_overview)

    with open(RESULTS_FILE_COVID_TWEETS_BY_P, 'w', newline='', encoding='utf-8') as outfile:
        dict_writer = csv.DictWriter(outfile, keys_results_detail)
        dict_writer.writeheader()
        dict_writer.writerows(dict_results_detail)

    with open(RESULTS_FILE_NON_COVID_TWEETS_BY_P, 'w', newline='', encoding='utf-8') as outfile:
        dict_writer = csv.DictWriter(outfile, keys_remaining_tweets)
        dict_writer.writeheader()
        dict_writer.writerows(dict_non_covid_tweets)

for filename in os.listdir(TWEETS_SOURCE_FOLDER):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, filename)
    f_path_covid_tweets_by_pol = os.path.join(COVID_TWEETS_BY_POL_FOLDER, filename)
    f_path_non_covid_tweets_by_pol = os.path.join(NON_COVID_TWEETS_BY_POL_FOLDER, filename)
    f_path_quote_covid_tweets = os.path.join(QUOTE_COVID_TWEETS_FOLDER, filename)
    f_path_quote_non_covid_tweets = os.path.join(QUOTE_NON_COVID_TWEETS_FOLDER, filename)
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            all_tweets = [t for t in json.load(infile)]
            covid_tweets_by_pol = [t for t in all_tweets if t['id_'] in covid_tweet_by_politician_id]
            non_covid_tweets_by_pol = [t for t in all_tweets if t['id_'] in non_covid_tweet_by_politician_id]
            quote_covid_tweets = [t for t in all_tweets if t['id_'] in quote_covid_tweet_id]
            quote_non_covid_tweets = [t for t in all_tweets if t['id_'] in quote_non_covid_tweet_id]

    with open(f_path_covid_tweets_by_pol, 'w', encoding='utf-8') as outfile:
        json.dump(list({v['id_']: v for v in covid_tweets_by_pol}.values()), outfile, ensure_ascii=False)
    with open(f_path_non_covid_tweets_by_pol, 'w', encoding='utf-8') as outfile:
        json.dump(list({v['id_']: v for v in non_covid_tweets_by_pol}.values()), outfile, ensure_ascii=False)
    with open(f_path_quote_covid_tweets, 'w', encoding='utf-8') as outfile:
        json.dump(list({v['id_']: v for v in quote_covid_tweets}.values()), outfile, ensure_ascii=False)
    with open(f_path_quote_non_covid_tweets, 'w', encoding='utf-8') as outfile:
        json.dump(list({v['id_']: v for v in quote_non_covid_tweets}.values()), outfile, ensure_ascii=False)
