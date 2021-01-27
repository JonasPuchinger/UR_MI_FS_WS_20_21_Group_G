import os
import csv
import json
import re
import preprocessor as pre
from nltk.corpus import stopwords
import codecs
from fuzzywuzzy import fuzz
from nltk.tokenize import TweetTokenizer

# Preprocessing tweets: Text-Cleaning (tweet-preprocessor), Tokenization (TweetTokenizer), Removal of digits, Stop words and Punctuations

POLITICIANS_LIST = '../assets/test_politicians.json'
# POLITICIANS_LIST = '../assets/all_politicians.json'
TWEETS_SOURCE_FOLDER = './formated_data/tweet/'
RESULTS_FILE_RATIO = 'combine_methods_ratio_test_27_1_all.csv'
RESULTS_FILE_DETAIL = 'combine_methods_detail_test_27_1_all.csv'
WORDLIST_FUZ = 'wordlist_fuz.json'

results_ratio = []
results_detail = []

tweets_of_pol = []
matching_part_1 = []

wordlist = json.load(codecs.open(WORDLIST_FUZ, 'r', 'utf-8-sig'))


# Source: https://towardsdatascience.com/basic-tweet-preprocessing-in-python-efd8360d529e
def preprocessing_tweet(original_tweet):
    tokenizer = TweetTokenizer()
    # Text-Cleaning (URLs, Mentions, Reserved words, Smileys, Numbers)
    pre.set_options(pre.OPT.URL, pre.OPT.MENTION, pre.OPT.RESERVED, pre.OPT.SMILEY, pre.OPT.NUMBER)
    original_tweet = pre.clean(original_tweet)
    # Removal of digits
    tweet = re.sub('\d+', '', original_tweet)
    # lowercase
    lower_text = tweet.lower()

    def remove_punctuation(words):
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', (word))
            if new_word != '':
                new_words.append(new_word)
        return new_words

    # Tokenization
    words = tokenizer.tokenize(lower_text)
    # Remove Punctuations
    words = remove_punctuation(words)
    # Remove stop words
    stop_words = set(stopwords.words('german'))
    words = [word for word in words if not word in stop_words]
    return words


def get_all_tweets_by_politician(screen_name, user_id):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, f'{screen_name}.json')

    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            all_tweets = [t for t in json.load(infile)]
            tweets_by_user = [t for t in all_tweets if t['raw_data']['user_id_str'] == str(user_id)]
            result = []
            for t in tweets_by_user:
                result.append([t['raw_data']['created_at'], preprocessing_tweet(t['raw_data']['full_text']),
                               t['raw_data']['full_text']])
            return result

    return ""


def check_match(tweets):
    covid_tweets = []
    new_tweet_list = []

    def match_wordlist_and_tweet(tweet):
        for word in wordlist:
            word = re.sub('\d+', '', word)
            if word in tweet[1]:
                return [word, 'match', tweet[0], tweet[1], tweet[2]]

    for t in tweets:
        result = match_wordlist_and_tweet(t)
        if not result is None:
            covid_tweets.append(result)
        else:
            new_tweet_list.append(t)

    return covid_tweets, new_tweet_list


def check_match_fuzzy(tweets):
    covid_tweets = []
    new_tweet_list = []

    def match_fuzzy(tweet):
        for word in wordlist:
            word = re.sub('\d+', '', word)
            for token in tweet[1]:
                if fuzz.ratio(word, token) > 87:
                    return [word, token, tweet[0], tweet[1], tweet[2]]

    for t in tweets:
        result = match_fuzzy(t)
        if not result is None:
            covid_tweets.append(result)
        else:
            new_tweet_list.append(t)

    return covid_tweets, new_tweet_list


def check_match_regex(tweets):
    covid_tweets = []
    new_tweet_list = []
    print(tweets)

    def match_regex(tweet):
        for word in wordlist:
            word = re.sub('\d+', '', word)
            pattern = "\\b" + word
            for token in tweet[1]:
                result = re.match(pattern, token)
                if result is not None:
                    return [pattern, token, tweet[0], tweet[1], tweet[2]]

    for t in tweets:
        result = match_regex(t)
        if not result is None:
            covid_tweets.append(result)
        else:
            new_tweet_list.append(t)

    return covid_tweets, new_tweet_list


with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
    for p in json.load(infile):
        p_name = p['Name']
        p_user_id = p['id']
        p_screen_name = p['screen_name']
        p_party = p['Partei']
        tweets_of_pol = get_all_tweets_by_politician(screen_name=p_screen_name, user_id=p_user_id)
        matching_part_1 = check_match(tweets_of_pol)
        covid_tweets = matching_part_1[0]
        matching_part_2 = check_match_regex(matching_part_1[1])
        covid_tweets.extend(matching_part_2[0])
        matching_part_3 = check_match_fuzzy(matching_part_2[1])
        covid_tweets.extend(matching_part_3[0])

        p_tweets_stats = {
            'name': p_name,
            'screen_name': p_screen_name,
            'party': p_party,
            'total_tweets': len(tweets_of_pol),
            'covid_tweets': len(covid_tweets),
        }
        results_ratio.append(p_tweets_stats)

        for i in covid_tweets:
            p_tweets_stats = {
                'name': p_name,
                'party': p_party,
                'created at': i[2],
                'word from wordlist': i[0],
                'match': i[1],
                'original tweet': i[3],
                'tweet': i[4],
            }
            results_detail.append(p_tweets_stats)

    keys_results_ratio = results_ratio[0].keys()
    keys_results_detail = results_detail[0].keys()

    with open(RESULTS_FILE_RATIO, 'w', newline='', encoding='utf-8') as outfile:
        dict_writer = csv.DictWriter(outfile, keys_results_ratio)
        dict_writer.writeheader()
        dict_writer.writerows(results_ratio)

    with open(RESULTS_FILE_DETAIL, 'w', newline='', encoding='utf-8') as outfile:
        dict_writer = csv.DictWriter(outfile, keys_results_detail)
        dict_writer.writeheader()
        dict_writer.writerows(results_detail)
