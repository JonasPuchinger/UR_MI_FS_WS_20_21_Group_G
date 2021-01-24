import os
import csv
import json
import re
import preprocessor as pre
from nltk.corpus import stopwords
import codecs
from fuzzywuzzy import fuzz
from nltk.tokenize import RegexpTokenizer

# Preprocessing tweets: Text-Cleaning (tweet-preprocessor), Tokenization, Stop words and Punctuations

POLITICIANS_LIST = '../assets/test_politicians.json'
# POLITICIANS_LIST = '../assets/all_politicians.json'
TWEETS_SOURCE_FOLDER = './formated_data/tweet/'
RESULTS_FILE_RATIO = 'combine_methods_ratio.csv'
RESULTS_FILE_DETAIL = 'combine_methods_detail.csv'
WORDLIST_FUZ = 'wordlist_fuz.json'

results_ratio = []
results_detail = []

tweets_of_pol = []
tweets = []
matched_tweets = []

wordlist = json.load(codecs.open(WORDLIST_FUZ, 'r', 'utf-8-sig'))


# Source: https://towardsdatascience.com/basic-tweet-preprocessing-in-python-efd8360d529e
def preprocessing_tweet(original_tweet):
    tokenizer = RegexpTokenizer("\s+", gaps=True)
    # Text-Cleaning (URLs, Mentions, Reserved words, Smileys, Numbers)
    pre.set_options(pre.OPT.URL, pre.OPT.MENTION, pre.OPT.RESERVED, pre.OPT.SMILEY, pre.OPT.NUMBER)
    original_tweet = pre.clean(original_tweet)
    # lowercase
    lower_text = original_tweet.lower()

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
                result.append(preprocessing_tweet(t['raw_data']['full_text']))
            return result

    return ""


def check_match(tweets):
    covid_tweets = []
    new_tweet_list = []

    def match_wordlist_and_tweet(tweet):
        for word in wordlist:
            if word in tweet:
                return [word, 'match', tweet]

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
            for token in tweet:
                if fuzz.ratio(word, token) > 87:
                    return [word, token, tweet]

    for t in tweets:
        result = match_fuzzy(t)
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
        result = []
        matched_tweets = check_match(tweets_of_pol)
        print(p_name)
        result = check_match_fuzzy(matched_tweets[1])
        list = matched_tweets[0]
        list.extend(result[0])

        p_tweets_stats = {
            'name': p_name,
            'screen_name': p_screen_name,
            'party': p_party,
            'total_tweets': len(tweets_of_pol),
            'covid_tweets': len(list),
        }
        results_ratio.append(p_tweets_stats)

        for i in list:
            p_tweets_stats = {
                'name': p_name,
                'word from wordlist': i[0],
                'original tweet': i[1],
                'tweet': i[2],
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
