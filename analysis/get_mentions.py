import json
import os
from collections import Counter
import collections

TWEETS_SOURCE_FOLDER = './formated_data/tweet/'
POLITICIANS_LIST = '../assets/all_politicians.json'


mentions_dict = {}

def get_politicians_list():
    new = []
    with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
        for p in json.load(infile):
            new.append(p)
    return new

politicians_list = get_politicians_list()

def get_party_of_politician(name):
    for p in politicians_list:
        if p['screen_name'] == name:
            return p['Partei']


def get_all_mentions():
    mentions = []
    for filename in os.listdir(TWEETS_SOURCE_FOLDER):
        f_path = os.path.join(TWEETS_SOURCE_FOLDER, filename)
        if os.path.isfile(f_path):
            with open(f_path, 'r', encoding='utf-8') as infile:
                all_tweets = [t for t in json.load(infile)]
                for tweet in all_tweets:
                    mentions_list = tweet.get('raw_data').get('entities').get('user_mentions')
                    if len(mentions_list) > 0:
                        party = get_party_of_politician(filename[:-5])
                        for mention in mentions_list:
                            mentions.append(mention.get('screen_name'))
                            if party in mentions_dict:
                                mentions_dict[party].append(mention.get('screen_name'))
                            else:
                                mentions_dict[party] = [mention.get('screen_name')]    
    return mentions


all_mentions = get_all_mentions()


def create_count_list():
    count_list = collections.Counter(all_mentions).most_common()
    with open('mentions_count.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(count_list), outfile, ensure_ascii=False)


def create_party_list():
    for key, value in mentions_dict.items():
        if key == "AFD":
            mentions_dict["AfD"].extend(value)
    del mentions_dict["AFD"]

    for key, value in mentions_dict.items():
        count_list = collections.Counter(value).most_common()
        mentions_dict[key] = count_list

    with open('mentions_party.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(mentions_dict), outfile, ensure_ascii=False)

create_count_list()
create_party_list()

