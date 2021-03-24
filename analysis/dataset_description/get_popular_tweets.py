import os
import json

# Paths for data directories and files

ALL_POLITICIANS_FILE = '../../assets/all_politicians.json'
COVID_TWEETS_FOLDER = '../filtered_data/covid_tweets_by_politician'
NON_COVID_TWEETS_FOLDER = '../filtered_data/non_covid_tweets_by_politician'

# How many tweets are collected

NUMBER_OF_TOP_TWEETS = 15

all_covid_tweets = []
all_non_covid_tweets = []

with open(ALL_POLITICIANS_FILE, 'r', encoding='utf-8') as all_politicians_infile:
    all_politicians = json.load(all_politicians_infile)

# All unique political parties in our dataset

parties = list(set([p['Partei'] for p in all_politicians]))

# Reading in all COVID- and non-COVID-tweets from all politicians

for p in all_politicians:
    p_screen_name = p['screen_name']

    p_covid_tweets_path = os.path.join(COVID_TWEETS_FOLDER, f'{p_screen_name}.json')
    if os.path.isfile(p_covid_tweets_path):
        with open(p_covid_tweets_path, 'r', encoding='utf-8') as p_covid_tweets_infile:
            p_covid_tweets = json.load(p_covid_tweets_infile)
            for covid_tweet in p_covid_tweets:
                p_covid_tweet = {
                    'name': p['Name'],
                    'screen_name': p_screen_name,
                    'p_user_id': p['id'],
                    'party': p['Partei'],
                    'tweet': covid_tweet
                }
                all_covid_tweets.append(p_covid_tweet)

    p_non_covid_tweets_path = os.path.join(NON_COVID_TWEETS_FOLDER, f'{p_screen_name}.json')
    if os.path.isfile(p_non_covid_tweets_path):
        with open(p_non_covid_tweets_path, 'r', encoding='utf-8') as p_non_covid_tweets_infile:
            p_non_covid_tweets = json.load(p_non_covid_tweets_infile)
            for non_covid_tweet in p_non_covid_tweets:
                p_non_covid_tweet = {
                    'name': p['Name'],
                    'screen_name': p_screen_name,
                    'p_user_id': p['id'],
                    'party': p['Partei'],
                    'tweet': non_covid_tweet
                }
                all_non_covid_tweets.append(p_non_covid_tweet)


most_popular_covid_tweets = []
most_popular_non_covid_tweets = []

for party in parties:
    # Collecting the number of the most viral (likes + retweets) COVID-tweets per party 
    all_covid_tweets_per_party = [t for t in all_covid_tweets if t['party'] == party]
    most_popular_covid_tweets_per_party = sorted(all_covid_tweets_per_party,
                                                 key=lambda t: (t['tweet']['raw_data']['favorite_count'] + t['tweet']['raw_data']['retweet_count']),
                                                 reverse=True)[:NUMBER_OF_TOP_TWEETS]
    most_popular_covid_tweets += most_popular_covid_tweets_per_party

    # Collecting the number of the most viral (likes + retweets) non-COVID-tweets per party
    all_non_covid_tweets_per_party = [t for t in all_non_covid_tweets if t['party'] == party]
    most_popular_non_covid_tweets_per_party = sorted(all_non_covid_tweets_per_party,
                                                     key=lambda t: (t['tweet']['raw_data']['favorite_count'] + t['tweet']['raw_data']['retweet_count']),
                                                     reverse=True)[:NUMBER_OF_TOP_TWEETS]
    most_popular_non_covid_tweets += most_popular_non_covid_tweets_per_party

# Writing the collected popular tweets to .json files to process them further for anntotation

with open('most_popular_covid_tweets.json', 'w', encoding='utf-8') as most_popular_covid_tweets_outfile:
    json.dump(most_popular_covid_tweets, most_popular_covid_tweets_outfile, ensure_ascii=False)

with open('most_popular_non_covid_tweets.json', 'w', encoding='utf-8') as most_popular_non_covid_tweets_outfile:
    json.dump(most_popular_non_covid_tweets, most_popular_non_covid_tweets_outfile, ensure_ascii=False)