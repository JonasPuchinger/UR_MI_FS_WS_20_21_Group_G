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
COVID_TWEETS_FOLDER = '../filtered_data/covid_tweets/'
NON_COVID_TWEETS_FOLDER = '../filtered_data/non_covid_tweets/'
RESULTS_FILE_OVERVIEW = 'covid_tweets_overview.csv'
RESULTS_FILE_DETAIL = 'covid_tweets_detail.csv'
PREPROCESSED_WORDLIST = '../preprocessing_wordlist/preprocessed_wordlist.json'
UNCERTAIN_WORDS = '../preprocessing_wordlist/uncertain_words.json'
NON_COVID_TWEETS = 'non_covid_tweets.csv'

results_overview = []
results_detail = []
non_covid_tweets = []
covid_tweets_ids = []

wordlist = json.load(codecs.open(PREPROCESSED_WORDLIST, 'r', 'utf-8-sig'))
uncertain_words = json.load(codecs.open(UNCERTAIN_WORDS, 'r', 'utf-8-sig'))


def get_all_tweets_by_politician(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')

    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            all_tweets = [t for t in json.load(infile)]
            tweets_by_user = [t for t in all_tweets if t['raw_data']['user_id_str'] == str(user_id)]
            result = []
            for t in tweets_by_user:
                result.append([t, clean_for_filtering(t['raw_data']['full_text'])])
            return result
    return ""


def get_quote_tweets(screen_name, remaining_tweets):
    quote_tweets_ids = [t[0]['raw_data']['quoted_status_id_str'] for t in remaining_tweets if
                        t[0]['raw_data']['is_quote_status'] and 'quoted_status_id_str' in t[0]['raw_data']]
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')

    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            all_tweets = [t for t in json.load(infile)]

            quote_tweets = [t for t in all_tweets if t['id_'] in quote_tweets_ids]
            result = []
            for t in quote_tweets:
                result.append([t['id_'], clean_for_filtering(t['raw_data']['full_text'])])
            return result
    return ""


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
    results_overview.append(p_tweets_stats)


def create_dict_results_detail(name, party, results):
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
        covid_tweets_ids.append(i[2]['id_'])
        results_detail.append(p_tweets_stats)


def create_dict_remaining_tweets(name, party, results):
    for tweet in results:
        p_tweets_stats = {
            'name': name,
            'party': party,
            'created at': tweet[0]['raw_data']['created_at'],
            'tweet': tweet[0]['raw_data']['full_text'],
        }
        non_covid_tweets.append(p_tweets_stats)


with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
    for p in json.load(infile):
        p_name = p['Name']
        p_user_id = p['id']
        p_screen_name = p['screen_name']
        p_party = p['Partei']

        all_tweets_by_politician = get_all_tweets_by_politician(screen_name=p_screen_name, user_id=p_user_id)

        results_matching = match_tweets(all_tweets_by_politician)

        remaining_tweets = results_matching[1]
        quote_tweets_by_politician = get_quote_tweets(p_screen_name, remaining_tweets)
        results_quote_tweet_matching = match_tweets(quote_tweets_by_politician)

        all_covid_quote_tweet_ids = [i[2] for i in results_quote_tweet_matching[0]]

        covid_quote_tweets = [["", "quote", t[0], t[1]] for t in remaining_tweets if (
                t[0]['raw_data']['is_quote_status'] and 'quoted_status_id_str' in t[0]['raw_data'] and
                t[0]['raw_data']['quoted_status_id_str'] in all_covid_quote_tweet_ids)]

        results_matching[0].extend(covid_quote_tweets)

        all_remaining_tweets = []
        for t in results_matching[1]:
            if not t[0]['raw_data']['is_quote_status']:
                all_remaining_tweets.append(t)
            if t[0]['raw_data']['is_quote_status'] and 'quoted_status_id_str' not in t[0]['raw_data']:
                all_remaining_tweets.append(t)
            if 'quoted_status_id_str' in t[0]['raw_data'] and t[0]['raw_data'][
                'quoted_status_id_str'] not in all_covid_quote_tweet_ids:
                all_remaining_tweets.append(t)

        create_dict_results_overview(p_name, p_screen_name, p_party, results_matching[0])
        create_dict_results_detail(p_name, p_party, results_matching[0])
        create_dict_remaining_tweets(p_name, p_party, all_remaining_tweets)

    keys_results_overview = results_overview[0].keys()
    keys_results_detail = results_detail[0].keys()
    keys_remaining_tweets = non_covid_tweets[0].keys()

    with open(RESULTS_FILE_OVERVIEW, 'w', newline='', encoding='utf-8') as outfile:
        dict_writer = csv.DictWriter(outfile, keys_results_overview)
        dict_writer.writeheader()
        dict_writer.writerows(results_overview)

    with open(RESULTS_FILE_DETAIL, 'w', newline='', encoding='utf-8') as outfile:
        dict_writer = csv.DictWriter(outfile, keys_results_detail)
        dict_writer.writeheader()
        dict_writer.writerows(results_detail)

    with open(NON_COVID_TWEETS, 'w', newline='', encoding='utf-8') as outfile:
        dict_writer = csv.DictWriter(outfile, keys_remaining_tweets)
        dict_writer.writeheader()
        dict_writer.writerows(non_covid_tweets)


for filename in os.listdir(TWEETS_SOURCE_FOLDER):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, filename)
    f_path_covid_tweets = os.path.join(COVID_TWEETS_FOLDER, filename)
    f_path_non_covid_tweets = os.path.join(NON_COVID_TWEETS_FOLDER, filename)
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            all_tweets = [t for t in json.load(infile)]
            covid_tweets = [t for t in all_tweets if t['id_'] in covid_tweets_ids]
            non_covid_tweets = [t for t in all_tweets if t['id_'] not in covid_tweets_ids]
    with open(f_path_covid_tweets, 'w', encoding='utf-8') as outfile:
        json.dump(covid_tweets, outfile, ensure_ascii=False)

    with open(f_path_non_covid_tweets, 'w', encoding='utf-8') as outfile:
        json.dump(non_covid_tweets, outfile, ensure_ascii=False)
