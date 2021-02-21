import os
import json
import csv
from textblob_de import TextBlobDE as TextBlob

POLITICIANS_LIST = '../../assets/all_politicians.json'
COVID_TWEETS_FOLDER = '../filtered_data/covid_tweets_by_politician/'
NON_COVID_TWEETS_FOLDER = '../filtered_data/non_covid_tweets_by_politician/'
RESULTS_FILE_COVID = 'covid_tweets_sentiment.csv'
RESULTS_FILE_NON_COVID = 'non_covid_tweets_sentiment.csv'

covid_tweet_sentiment = []
non_covid_tweet_sentiment = []


def get_sentiment(screen_name, type):
    if type == "covid":
        folder = COVID_TWEETS_FOLDER
    else:
        folder = NON_COVID_TWEETS_FOLDER

    f_path = os.path.join(folder, f'{screen_name}.json')

    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            covid_tweets = [t for t in json.load(infile)]
            result = []
            for t in covid_tweets:
                result.append([t, TextBlob(t['raw_data']['full_text']).polarity])
            return result
    return ""


with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
    for p in json.load(infile):
        p_name = p['Name']
        p_user_id = p['id']
        p_screen_name = p['screen_name']
        p_party = p['Partei']
        print(p_name)
        covid_tweets_sent = get_sentiment(p_screen_name, "covid")
        non_covid_tweets_sent = get_sentiment(p_screen_name, "non-covid")

        for tweet in covid_tweets_sent:
            covid_tweet_sentiment_stats = {
                'name': p_name,
                'party': p_party,
                'created at': tweet[0]['raw_data']['created_at'],
                'tweet': tweet[0]['raw_data']['full_text'],
                'polarity': tweet[1],
            }
            covid_tweet_sentiment.append(covid_tweet_sentiment_stats)

        for tweet in non_covid_tweets_sent:
            non_covid_tweet_sentiment_stats = {
                'name': p_name,
                'party': p_party,
                'created at': tweet[0]['raw_data']['created_at'],
                'tweet': tweet[0]['raw_data']['full_text'],
                'polarity': tweet[1],
            }
            non_covid_tweet_sentiment.append(non_covid_tweet_sentiment_stats)

    keys_covid_tweet = covid_tweet_sentiment[0].keys()
    keys_non_covid_tweet = non_covid_tweet_sentiment[0].keys()

    with open(RESULTS_FILE_COVID, 'w', newline='', encoding='utf-8') as outfile:
        dict_writer = csv.DictWriter(outfile, keys_covid_tweet)
        dict_writer.writeheader()
        dict_writer.writerows(covid_tweet_sentiment)

    with open(RESULTS_FILE_NON_COVID, 'w', newline='', encoding='utf-8') as outfile:
        dict_writer = csv.DictWriter(outfile, keys_non_covid_tweet)
        dict_writer.writeheader()
        dict_writer.writerows(non_covid_tweet_sentiment)
