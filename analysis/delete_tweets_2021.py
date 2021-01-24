import json
import os
import statistics
import numpy as np


TWEETS_SOURCE_FOLDER = './formated_data/tweet/'

def getAllTweets():
    
    for filename in os.listdir(TWEETS_SOURCE_FOLDER):
        f_path = os.path.join(TWEETS_SOURCE_FOLDER, filename)
        if os.path.isfile(f_path):
            all_needed_tweets = []
            with open(f_path, 'r', encoding='utf-8') as infile:
                all_tweets = [t for t in json.load(infile)]
                if len(all_tweets) > 0:
                    all_needed_tweets = [tweet for tweet in all_tweets if not tweet['raw_data']['created_at'].endswith('2021')]
            infile.close
            if len(all_needed_tweets) > 0:
                with open(f_path, 'w', encoding='utf-8') as outfile:
                    json.dump(all_needed_tweets, outfile, ensure_ascii=False)
          
getAllTweets()