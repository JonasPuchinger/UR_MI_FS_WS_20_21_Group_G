import json
import os
import collections
import regex
import requests

TWEETS_SOURCE_FOLDER = '../formated_data/tweet/'
POLITICIANS_LIST = '../../assets/all_politicians.json'

mentions_list = []
mentions_dict = {}
domains_list = []
domains_dict = {}
link_list = []
hashtags_list = []
hashtags_dict = {}

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

def get_all_mentions(all_tweets):
     for tweet in all_tweets:
        mentions_of_tweet = tweet.get('raw_data').get('entities').get('user_mentions')
        if len(mentions_of_tweet) > 0:
            party = get_party_of_politician(filename[:-5])
            for mention in mentions_of_tweet:
                name = mention.get('screen_name')
                mentions_list.append(name)
                if party in mentions_dict:
                    mentions_dict[party].append(name)
                else:
                    mentions_dict[party] = [name] 

def get_all_links(all_tweets):
    for tweet in all_tweets:
        links_of_tweet = tweet.get('raw_data').get('entities').get('urls')
        if len(links_of_tweet) > 0:
            party = get_party_of_politician(filename[:-5])
            for link in links_of_tweet:
                url = link.get('expanded_url')
                if "bit.ly" in url or "tinyurl.com" in url:
                     url = expand_url(url)
                link_list.append(url) 
                domain = get_domain(url)
                domains_list.append(domain)
                if party in domains_dict:
                    domains_dict[party].append(domain)
                else:
                    domains_dict[party] = [domain]

def get_all_hashtags(all_tweets):
    for tweet in all_tweets:
        hashtags_of_tweet = tweet.get('raw_data').get('entities').get('hashtags')
        if len(hashtags_of_tweet) > 0:
            party = get_party_of_politician(filename[:-5])
            for hashtag in hashtags_of_tweet:
                text = hashtag.get('text')
                hashtags_list.append(text)
                if party in hashtags_dict:
                    hashtags_dict[party].append(text)
                else:
                    hashtags_dict[party] = [text] 

for entry in politicians_list:
    filename = entry['screen_name'] + '.json'
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, filename)
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            #all_tweets = [t for t in json.load(infile)]
            all_tweets = [t for t in json.load(infile) if t['raw_data']['user_id_str'] == str(entry['id'])] #just tweets by user
            get_all_mentions(all_tweets)
            get_all_links(all_tweets)
            get_all_hashtags(all_tweets)

def create_mentions_count_file():
    count_list = collections.Counter(mentions_list).most_common()
    with open('tweets_by_user/mentions_count_all_tweets.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(count_list), outfile, ensure_ascii=False)

def create_mentions_party_file():
    for key, value in mentions_dict.items():
        count_list = collections.Counter(value).most_common()
        mentions_dict[key] = count_list

    with open('tweets_by_user/mentions_party_all_tweets.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(mentions_dict), outfile, ensure_ascii=False)

create_mentions_count_file()
create_mentions_party_file()

def create_domains_count_file():
    count_list = collections.Counter(domains_list).most_common()
    with open('tweets_by_user/domains_count_all_tweets.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(count_list), outfile, ensure_ascii=False)

def create_domains_party_file():
    for key, value in domains_dict.items():
        count_list = collections.Counter(value).most_common()
        domains_dict[key] = count_list
    with open('tweets_by_user/domains_party_all_tweets.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(domains_dict), outfile, ensure_ascii=False)

def create_links_count_file():
    count_list = collections.Counter(link_list).most_common()
    with open('tweets_by_user/links_count_all_tweets.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(count_list), outfile, ensure_ascii=False)

create_domains_count_file()
create_domains_party_file()
create_links_count_file()

def create_hashtags_count_file():
    count_list = collections.Counter(hashtags_list).most_common()
    with open('tweets_by_user/hashtags_count_all_tweets.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(count_list), outfile, ensure_ascii=False)

def create_hashtags_party_file():
    for key, value in hashtags_dict.items():
        count_list = collections.Counter(value).most_common()
        hashtags_dict[key] = count_list
    with open('tweets_by_user/hashtags_party_all_tweets.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(hashtags_dict), outfile, ensure_ascii=False)


create_hashtags_count_file()
create_hashtags_party_file()