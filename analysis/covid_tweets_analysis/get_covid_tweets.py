import os
import numpy as np
import csv
import json
import re
import preprocessor as pre
from nltk.corpus import stopwords
import codecs
from fuzzywuzzy import fuzz
from nltk.tokenize import TweetTokenizer

POLITICIANS_LIST = '../../assets/test_politicians.json'
TWEETS_SOURCE_FOLDER = '../formated_data/tweet/'
COVID_TWEETS_FOLDER = '../filtered_data/covid_tweets/'
NON_COVID_TWEETS_FOLDER = '../filtered_data/non_covid_tweets/'
RESULTS_FILE_OVERVIEW = 'covid_tweets_overview.csv'
RESULTS_FILE_DETAIL = 'covid_tweets_detail.csv'
PREPROCESSED_WORDLIST_FUZ = '../preprocessing_wordlist/wordlist_fuzzy.json'
PREPROCESSED_WORDLIST = '../preprocessing_wordlist/wordlist_matching.json'
UNCERTAIN_WORDS = '../preprocessing_wordlist/uncertain_words.json'
NON_COVID_TWEETS = 'non_covid_tweets.csv'

results_overview = []
results_detail = []
non_covid_tweets = []
covid_tweets_ids = []

tweets_of_pol = []
matching_part_1 = []

wordlist_fuzzy = json.load(codecs.open(PREPROCESSED_WORDLIST_FUZ, 'r', 'utf-8-sig'))
wordlist = json.load(codecs.open(PREPROCESSED_WORDLIST, 'r', 'utf-8-sig'))
uncertain_words = json.load(codecs.open(UNCERTAIN_WORDS, 'r', 'utf-8-sig'))


# Source: https://towardsdatascience.com/basic-tweet-preprocessing-in-python-efd8360d529e
def preprocessing_tweet(original_tweet):
    tokenizer = TweetTokenizer()
    # Text-Cleaning (URLs, Mentions, Reserved words, Smileys, Numbers)
    pre.set_options(pre.OPT.URL, pre.OPT.MENTION, pre.OPT.RESERVED, pre.OPT.SMILEY, pre.OPT.NUMBER)
    preprocessed_tweet = pre.clean(original_tweet)
    # Removal of digits
    preprocessed_tweet = re.sub('\d+', '', preprocessed_tweet)
    # lowercase
    preprocessed_tweet = preprocessed_tweet.lower()

    def remove_punctuation(words):
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', (word))
            if new_word != '':
                new_words.append(new_word)
        return new_words

    # Tokenization
    preprocessed_words = tokenizer.tokenize(preprocessed_tweet)
    # Remove Punctuations
    preprocessed_words = remove_punctuation(preprocessed_words)
    # Remove stop words
    stop_words = set(stopwords.words('german'))
    preprocessed_words = [word for word in preprocessed_words if not word in stop_words]
    return preprocessed_words


def get_all_tweets_by_politician(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')

    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            all_tweets = [t for t in json.load(infile)]
            tweets_by_user = [t for t in all_tweets if t['raw_data']['user_id_str'] == str(user_id)]
            result = []
            for t in tweets_by_user:
                result.append([t['raw_data']['created_at'], preprocessing_tweet(t['raw_data']['full_text']),
                               t['raw_data']['full_text'], t['id_']])
            return result
    return ""


def check_match(tweets):
    covid_tweets = []
    remaining_tweets = []

    def match_wordlist_and_tweet(tweet):
        list_uncertain_words = []
        for word in wordlist:
            if word in tweet[1]:
                if word in uncertain_words and len(np.unique(list_uncertain_words)) < 2:
                    list_uncertain_words.append(word)
                else:
                    return [word, 'match', tweet[0], tweet[1], tweet[2], tweet[3]]

    for t in tweets:
        result = match_wordlist_and_tweet(t)
        if not result is None:
            covid_tweets.append(result)
        else:
            remaining_tweets.append(t)

    return covid_tweets, remaining_tweets


def check_match_fuzzy(tweets):
    covid_tweets = []
    remaining_tweets = []

    def match_fuzzy(tweet):
        list_uncertain_words = []
        for word in wordlist_fuzzy:
            for token in tweet[1]:
                if fuzz.ratio(word, token) > 90:
                    if token in uncertain_words and len(np.unique(list_uncertain_words)) < 2:
                        list_uncertain_words.append(token)
                    else:
                        return [word, token, tweet[0], tweet[1], tweet[2], tweet[3]]

    for t in tweets:
        result = match_fuzzy(t)
        if not result is None:
            covid_tweets.append(result)
        else:
            remaining_tweets.append(t)

    return covid_tweets, remaining_tweets


def check_match_regex(tweets):
    covid_tweets = []
    remaining_tweets = []

    def match_regex(tweet):
        list_uncertain_words = []
        for word in wordlist:
            pattern = "\\b" + word
            for token in tweet[1]:
                result = re.match(pattern, token)
                if result is not None:
                    if token in uncertain_words and len(np.unique(list_uncertain_words)) < 2:
                        list_uncertain_words.append(token)
                    else:
                        return [pattern, token, tweet[0], tweet[1], tweet[2], tweet[3]]

    for t in tweets:
        result = match_regex(t)
        if not result is None:
            covid_tweets.append(result)
        else:
            remaining_tweets.append(t)

    return covid_tweets, remaining_tweets


with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
    for p in json.load(infile):
        p_name = p['Name']
        p_user_id = p['id']
        p_screen_name = p['screen_name']
        p_party = p['Partei']
        tweets_of_pol = get_all_tweets_by_politician(screen_name=p_screen_name, user_id=p_user_id)
        print(p_name)
        matching_part_1 = check_match(tweets_of_pol)
        covid_tweets = matching_part_1[0]
        matching_part_2 = check_match_regex(matching_part_1[1])
        covid_tweets.extend(matching_part_2[0])
        matching_part_3 = check_match_fuzzy(matching_part_2[1])
        non_covid_tweets = matching_part_3[1]
        covid_tweets.extend(matching_part_3[0])

        p_tweets_stats = {
            'name': p_name,
            'screen_name': p_screen_name,
            'party': p_party,
            'covid_tweets': len(covid_tweets),
        }
        results_overview.append(p_tweets_stats)

        for i in covid_tweets:
            p_tweets_stats = {
                'name': p_name,
                'party': p_party,
                'created at': i[2],
                'id': i[5],
                'word from wordlist': i[0],
                'match': i[1],
                'original tweet': i[3],
                'tweet': i[4],
            }
            covid_tweets_ids.append(i[5])
            results_detail.append(p_tweets_stats)

        for tweet in non_covid_tweets:
            p_remaining_tweets_stats = {
                'name': p_name,
                'party': p_party,
                'created at': tweet[0],
                'tweet': tweet[2],
            }
            non_covid_tweets.append(p_remaining_tweets_stats)

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
