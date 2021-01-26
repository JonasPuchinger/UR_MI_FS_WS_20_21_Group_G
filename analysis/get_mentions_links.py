import json
import os
from collections import Counter
import collections
import regex
from re import finditer

TWEETS_SOURCE_FOLDER = './formated_data/tweet/'
POLITICIANS_LIST = '../assets/all_politicians.json'


mentions_dict = {}
links_list = []
links_dict = {}

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


def get_start_url(url):
    try:
        return url[:regex.search(r'(?<!http:|https:|\/)\/', url).span()[0]]
    except:
        return url
    #return url[:regex.search(r'(?<!http:|https:|\/)\/', url).span()[0]]


def get_mentions_and_links():
    mentions = []
    for filename in os.listdir(TWEETS_SOURCE_FOLDER):
        f_path = os.path.join(TWEETS_SOURCE_FOLDER, filename)
        if os.path.isfile(f_path):
            with open(f_path, 'r', encoding='utf-8') as infile:
                all_tweets = [t for t in json.load(infile)]
                for tweet in all_tweets:
                    #get mentions
                    mentions_list = tweet.get('raw_data').get('entities').get('user_mentions')
                    if len(mentions_list) > 0:
                        party = get_party_of_politician(filename[:-5])
                        for mention in mentions_list:
                            mentions.append(mention.get('screen_name'))
                            if party in mentions_dict:
                                mentions_dict[party].append(mention.get('screen_name'))
                            else:
                                mentions_dict[party] = [mention.get('screen_name')] 
                    #get links
                    link_list = tweet.get('raw_data').get('entities').get('urls')
                    if len(link_list) > 0:
                        party = get_party_of_politician(filename[:-5])
                        for link in link_list:
                            url = get_start_url(link.get('expanded_url'))
                            links_list.append(url)
                            if party in links_dict:
                                links_dict[party].append(url)
                            else:
                                links_dict[party] = [url]

    return mentions


all_mentions = get_mentions_and_links()


def combine_afd(dict):
    for key, value in dict.items():
        if key == "AFD":
            dict["AfD"].extend(value)
    try:
        del dict["AFD"]
    except:
        pass
    return dict


def create_mentions_count_file():
    count_list = collections.Counter(all_mentions).most_common()
    with open('mentions_count.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(count_list), outfile, ensure_ascii=False)


def create_mentions_party_file():
    mentions_dict_opt = combine_afd(mentions_dict)

    for key, value in mentions_dict_opt.items():
        count_list = collections.Counter(value).most_common()
        mentions_dict_opt[key] = count_list

    with open('mentions_party.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(mentions_dict_opt), outfile, ensure_ascii=False)

#create_mentions_count_file()
#create_mentions_party_file()

def create_links_count_file():
    count_list = collections.Counter(links_list).most_common()
    with open('links_count.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(count_list), outfile, ensure_ascii=False)


def create_links_party_file():
    links_dict_opt = combine_afd(links_dict)

    for key, value in links_dict_opt.items():
        count_list = collections.Counter(value).most_common()
        links_dict_opt[key] = count_list

    with open('links_party.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(links_dict_opt), outfile, ensure_ascii=False)


create_links_count_file()
create_links_party_file()