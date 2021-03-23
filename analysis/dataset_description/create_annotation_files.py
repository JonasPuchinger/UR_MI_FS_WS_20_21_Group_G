import json
import csv

# Paths for data directories and files
POPULAR_COVID_TWEETS_FILE = './most_popular_covid_tweets.json'
POPULAR_NON_COVID_TWEETS_FILE = './most_popular_non_covid_tweets.json'
COVID_TWEETS_ANNOTATION_FILE = 'covid_tweets_annotation.csv'
NON_COVID_TWEETS_ANNOTATION_FILE = 'non_covid_tweets_annotation.csv'

# Opening and reading data from files
with open(POPULAR_COVID_TWEETS_FILE, 'r', encoding='utf-8') as popular_covid_tweets_infile:
    popular_covid_tweets = json.load(popular_covid_tweets_infile)

with open(POPULAR_NON_COVID_TWEETS_FILE, 'r', encoding='utf-8') as popular_non_covid_tweets_infile:
    popular_non_covid_tweets = json.load(popular_non_covid_tweets_infile)


# Extracting the relevant from the viral COVID-tweets
covid_tweets_for_annotation = []

for t in popular_covid_tweets:
    curr_tweet_for_annotation = {
        'tweet_id': t['tweet']['id_'],
        'tweet_content': t['tweet']['raw_data']['full_text'].replace('\n', ' '),
        'annotation_sentiment': None,
        'annotation_qualifier': None 
    }
    covid_tweets_for_annotation.append(curr_tweet_for_annotation)

# Saving the formated COVID-tweets
annotation_covid_keys = covid_tweets_for_annotation[0].keys()

with open(COVID_TWEETS_ANNOTATION_FILE, 'w', newline='', encoding='utf-8') as annotation_covid_outfile:
    dict_writer = csv.DictWriter(annotation_covid_outfile, annotation_covid_keys)
    dict_writer.writeheader()
    dict_writer.writerows(covid_tweets_for_annotation)

# Extracting the relevant from the viral COVID-tweets
non_covid_tweets_for_annotation = []

for t in popular_non_covid_tweets:
    curr_tweet_for_annotation = {
        'tweet_id': t['tweet']['id_'],
        'tweet_content': t['tweet']['raw_data']['full_text'].replace('\n', ' '),
        'annotation_sentiment': None
    }
    non_covid_tweets_for_annotation.append(curr_tweet_for_annotation)

# Saving the formated COVID-tweets
annotation_non_covid_keys = non_covid_tweets_for_annotation[0].keys()

with open(NON_COVID_TWEETS_ANNOTATION_FILE, 'w', newline='', encoding='utf-8') as annotation_non_covid_outfile:
    dict_writer = csv.DictWriter(annotation_non_covid_outfile, annotation_non_covid_keys)
    dict_writer.writeheader()
    dict_writer.writerows(non_covid_tweets_for_annotation)
