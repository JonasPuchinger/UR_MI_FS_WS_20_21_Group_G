import json
import csv
import requests
import regex
import os
from datetime import datetime

TWEETS_SOURCE_FOLDER = '../formated_data/tweet/'
POLITICIANS_LIST = '../../assets/all_politicians.json'

def get_politicians_list():
    politicians = []
    with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
        for p in json.load(infile):
            politicians.append(p)
    return politicians

politicians_list = get_politicians_list()

def get_domain(url):
    try:
        return url[:regex.search(r'(?<!http:|https:|\/)\/|\\', url).span()[0]]
    except:
        return url

# Expands shortened URLs to get the actual link
def expand_url(url):
    session = requests.Session()
    try: 
        resp = session.head(url, allow_redirects=True)
        return resp.url
    # If the bit.ly or tinyurl link doesn't exist anymore
    except: 
        return url

def get_detail_info(tweet):
    info = dict.fromkeys(['name', 'screen_name','id', 'party'])
    for p in politicians_list:
        if p['screen_name'] == filename[:-5]:
            info['name'] = p['Name']
            info['screen_name'] = p['screen_name']
            info['id'] = p['id']
            info['party'] = p['Partei']
    return info

def format_date(date):
    return datetime.strftime(datetime.strptime(date,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d') 

def get_hashtags(all_tweets, info_dict):
    hashtags_list_of_dicts = []
    for tweet in all_tweets:
        hashtags_of_tweet = tweet.get('raw_data').get('entities').get('hashtags')
        if len(hashtags_of_tweet) > 0:
            date = format_date(tweet.get('raw_data').get('created_at'))
            tweet_id = tweet.get('raw_data').get('id')
            for hashtag in hashtags_of_tweet:
                hashtag_dict = dict.fromkeys(['hashtag', 'date', 'tweet_id'])
                hashtag_dict['hashtag'] = hashtag.get('text')
                hashtag_dict['date'] = date
                hashtag_dict['tweet_id'] = tweet_id
                hashtags_list_of_dicts.append(hashtag_dict)
    info_dict['hashtags'] = hashtags_list_of_dicts
    return info_dict

def get_mentions(all_tweets, info_dict):
    mentions_list_of_dicts = []
    for tweet in all_tweets:
        mentions_of_tweet = tweet.get('raw_data').get('entities').get('user_mentions')
        if len(mentions_of_tweet) > 0:
            date = format_date(tweet.get('raw_data').get('created_at'))
            tweet_id = tweet.get('raw_data').get('id')
            for mention in mentions_of_tweet:
                mention_dict = dict.fromkeys(['mention', 'date', 'tweet_id'])
                mention_dict['mention'] = mention.get('screen_name')
                mention_dict['date'] = date
                mention_dict['tweet_id'] = tweet_id
                mentions_list_of_dicts.append(mention_dict)
    info_dict['mentions'] = mentions_list_of_dicts
    return info_dict

def get_links(all_tweets, info_dict):
    links_list_of_dicts = []
    domains_list_of_dicts = []
    for tweet in all_tweets:
        links_of_tweet = tweet.get('raw_data').get('entities').get('urls')
        if len(links_of_tweet) > 0:
            date = format_date(tweet.get('raw_data').get('created_at'))
            tweet_id = tweet.get('raw_data').get('id')
            for link in links_of_tweet:
                url = link.get('expanded_url')
                if "bit.ly" in url or "tinyurl.com" in url:
                    url = expand_url(url)   
                link_dict = dict.fromkeys(['link', 'date', 'tweet_id'])
                link_dict['link'] = url
                link_dict['date'] = date
                link_dict['tweet_id'] = tweet_id
                links_list_of_dicts.append(link_dict)   
                domain = get_domain(url)
                domain_dict = dict.fromkeys(['domain', 'date', 'tweet_id'])
                domain_dict['domain'] = domain
                domain_dict['date'] = date
                domain_dict['tweet_id'] = tweet_id
                domains_list_of_dicts.append(domain_dict)  
    all_links_dict = info_dict.copy()
    all_links_dict['links'] = links_list_of_dicts
    all_domains_dict = info_dict.copy()
    all_domains_dict['domains'] = domains_list_of_dicts   
    return all_links_dict, all_domains_dict                   

hashtags_tweets_by_user = []
hashtags_all_tweets = []
mentions_tweets_by_user = []
mentions_all_tweets = []
links_tweets_by_user = []
links_all_tweets = []
domains_tweet_by_user = []
domains_all_tweets = []

for entry in politicians_list:
    filename = entry['screen_name'] + '.json'
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, filename)
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            f_content = json.load(infile)
            if f_content != []:
                all_tweets = [t for t in f_content]
                detail_info = get_detail_info(all_tweets[0])
                hashtags_all_tweets.append(get_hashtags(all_tweets, detail_info.copy()))
                mentions_all_tweets.append(get_mentions(all_tweets, detail_info.copy()))
                links, domains = get_links(all_tweets, detail_info.copy())
                links_all_tweets.append(links)
                domains_all_tweets.append(domains)
                
                #just tweets by user himself
                all_tweets = [t for t in all_tweets if t['raw_data']['user_id_str'] == str(entry['id'])] 
                hashtags_tweets_by_user.append(get_hashtags(all_tweets, detail_info.copy()))
                mentions_tweets_by_user.append(get_mentions(all_tweets, detail_info.copy()))
                links, domains = get_links(all_tweets, detail_info.copy())
                links_tweets_by_user.append(links)
                domains_tweet_by_user.append(domains)

def create_file(data, file):
    keys = data[0].keys()
    with open(file, 'w', newline='', encoding='utf-8') as outfile:
        dict_writer = csv.DictWriter(outfile, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def create_files():
    create_file(hashtags_tweets_by_user, 'tweets_by_user/hashtags_tweets_by_user.csv')
    create_file(mentions_tweets_by_user, 'tweets_by_user/mentions_tweets_by_user.csv')
    create_file(links_tweets_by_user, 'tweets_by_user/links_tweets_by_user.csv')
    create_file(domains_tweet_by_user, 'tweets_by_user/domains_tweets_by_user.csv')
    create_file(hashtags_all_tweets, 'all_tweets/hashtags_all_tweets.csv')
    create_file(mentions_all_tweets, 'all_tweets/mentions_all_tweets.csv')
    create_file(links_all_tweets, 'all_tweets/links_all_tweets.csv')
    create_file(domains_all_tweets, 'all_tweets/domains_all_tweets.csv')

create_files()
