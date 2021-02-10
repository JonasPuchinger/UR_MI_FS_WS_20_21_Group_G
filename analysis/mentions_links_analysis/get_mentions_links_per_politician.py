import json
import os
from operator import itemgetter
import regex
import requests

TWEETS_SOURCE_FOLDER = '../formated_data/tweet/'
POLITICIANS_LIST = '../../assets/all_politicians.json'

def get_politicians_list():
    new = []
    with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
        for p in json.load(infile):
            new.append(p)
    return new

politicians_list = get_politicians_list()

def get_politician_info(name):
    info = dict.fromkeys(['name', 'screen_name','id', 'party'])
    for p in politicians_list:
        if p['screen_name'] == name:
            info['name'] = p['Name']
            info['screen_name'] = name
            info['id'] = p['id']
            info['party'] = p['Partei']
    return info

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

def get_detailed_info(all_tweets):
    info = get_politician_info(filename[:-5])
    return {
        "name": info['name'],
        "screen_name": info['screen_name'],
        "id": info['id'],
        "party": info['party'],
        "mentions": get_mentions(all_tweets),
        "urls": get_links(all_tweets)
    }

def sort_list(list_of_dicts):
    return sorted(list_of_dicts, key=itemgetter('count'), reverse=True)  

def get_mentions(all_tweets):
    mentions_list_of_dicts = []
    for tweet in all_tweets:
        mentions_of_tweet = tweet.get('raw_data').get('entities').get('user_mentions')
        if len(mentions_of_tweet) > 0:
            for mention in mentions_of_tweet:
                screen_name = mention.get('screen_name')
                found_entry = next((item for item in mentions_list_of_dicts if item['screen_name'] == screen_name), None)
                if found_entry != None:
                    found_entry['count'] = found_entry['count'] + 1
                else:
                    mention_dict = dict.fromkeys(['screen_name','count'])
                    mention_dict['screen_name'] = screen_name
                    mention_dict['count'] = 1
                    mentions_list_of_dicts.append(mention_dict)
    sorted_list = sort_list(mentions_list_of_dicts)
    return sorted_list

def get_links(all_tweets):
    links_list_of_dicts = []
    for tweet in all_tweets:
        links_of_tweet = tweet.get('raw_data').get('entities').get('urls')
        if len(links_of_tweet) > 0:
            for link in links_of_tweet:
                url = link.get('expanded_url')
                if "bit.ly" in url or "tinyurl.com" in url:
                    url = expand_url(url)   
                domain = get_domain(url)
                found_entry = next((item for item in links_list_of_dicts if item['domain'] == domain), None)
                if found_entry != None:
                    found_entry['count'] = found_entry['count'] + 1
                else:
                   link_dict = dict.fromkeys(['domain','count'])
                   link_dict['domain'] = domain
                   link_dict['count'] = 1
                   links_list_of_dicts.append(link_dict)
    sorted_list = sort_list(links_list_of_dicts)
    return sorted_list                       

full_list = []

for filename in os.listdir(TWEETS_SOURCE_FOLDER):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, filename)
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            all_tweets = [t for t in json.load(infile)]
            full_list.append(get_detailed_info(all_tweets))

def create_file():
    with open('mentions_links_per_politician.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(full_list), outfile, ensure_ascii=False)

create_file()
