import os
import json

TWEETS_SOURCE_FOLDER = './formated_data/tweet/'
USERS_SOURCE_FOLDER = './formated_data/user/'

total_tweets, total_users = 0, 0

for tweet_file in os.listdir(TWEETS_SOURCE_FOLDER):
    total_tweets += len(json.load(open(TWEETS_SOURCE_FOLDER + tweet_file, 'r', encoding='utf-8')))

for user_file in os.listdir(USERS_SOURCE_FOLDER):
    total_users += len(json.load(open(USERS_SOURCE_FOLDER + user_file, 'r', encoding='utf-8')))

print(f'Total Tweets: {total_tweets}')
print(f'Total Users: {total_users}')