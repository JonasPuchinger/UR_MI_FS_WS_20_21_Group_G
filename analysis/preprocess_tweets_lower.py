import os
import csv
import json
import re
import preprocessor as pre
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import codecs

# Preprocessing tweets: Text-Cleaning (tweet-preprocessor), Tokenization, Removal of Digits, Stop words and Punctuations

POLITICIANS_LIST = '../assets/test_politicians.json'
#POLITICIANS_LIST = '../assets/all_politicians.json'
TWEETS_SOURCE_FOLDER = './formated_data/tweet/'
RESULTS_FILE_RATIO = 'preprocess_tweets_lower_ratio.csv'
RESULTS_FILE_DETAIL = 'preprocess_tweets_lower_detail.csv'
WORDLIST = '../assets/wordlist.json'

results_ratio = []
results_detail = []


# Source: https://towardsdatascience.com/basic-tweet-preprocessing-in-python-efd8360d529e
def preprocessing_tweet(original_tweet):
    # Text-Cleaning (URLs, Mentions, Reserved words, Smileys, Numbers)
    pre.set_options(pre.OPT.URL, pre.OPT.MENTION, pre.OPT.RESERVED, pre.OPT.SMILEY, pre.OPT.NUMBER)
    original_tweet = pre.clean(original_tweet)
    # Remove Digits and lowercase
    tweet = re.sub('\d+', '', original_tweet)
    lower_text = tweet.lower()
    w_tokenizer = TweetTokenizer()

    # Tokenization
    def token_text(text):
        token = []
        for word in w_tokenizer.tokenize(text):
            token.append(word)
        return token

    def remove_punctuation(words):
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', (word))
            if new_word != '':
                new_words.append(new_word)
        return new_words

    words = token_text(lower_text)
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
                result.append([t['raw_data']['full_text'], preprocessing_tweet(t['raw_data']['full_text']),
                               t['raw_data']['created_at']])
            return result

    return ""


def check_match(tweets_list):
    result_tweets = []
    wordlist = json.load(codecs.open(WORDLIST, 'r', 'utf-8-sig'))

    def match_wordlist_and_tweet(tweet):
        for word in wordlist:
            # Remove Digits, lowercase, Text-Cleaning
            word = word.lower()
            word = re.sub('\d+', '', word)
            pre.set_options(pre.OPT.HASHTAG, pre.OPT.NUMBER)
            word = pre.clean(word)
            if word in tweet[1]:
                return [word, tweet[0], tweet[1], tweet[2]]

    for t in tweets_list:
        result = match_wordlist_and_tweet(t)
        if not result is None:
            result_tweets.append(result)

    return result_tweets


with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
    for p in json.load(infile):
        p_name = p['Name']
        p_user_id = p['id']
        p_screen_name = p['screen_name']
        p_party = p['Partei']
        tweets = get_all_tweets_by_politician(screen_name=p_screen_name, user_id=p_user_id)
        matched_tweets = check_match(tweets)
        p_ratio = round((float(len(matched_tweets)) / float(len(tweets))) * 100,
                        2) if len(matched_tweets) != 0 else 0

        p_tweets_stats = {
            'name': p_name,
            'screen_name': p_screen_name,
            'party': p_party,
            'total_tweets': len(tweets),
            'covid_tweets': len(matched_tweets),
            'ratio': p_ratio
        }
        results_ratio.append(p_tweets_stats)

        for i in matched_tweets:
            p_tweets_stats = {
                'name': p_name,
                'created_at': i[3],
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
