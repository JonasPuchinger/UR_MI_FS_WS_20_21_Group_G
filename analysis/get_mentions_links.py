import json
import os
import collections
import regex
import urlexpander

TWEETS_SOURCE_FOLDER = './formated_data/tweet/'
POLITICIANS_LIST = '../assets/all_politicians.json'

mentions_list = []
mentions_dict = {}
domains_list = []
domains_dict = {}
link_list = []

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
    try: 
        return urlexpander.expand(url)
    except:
        return url

def get_all_mentions(all_tweets):
     for tweet in all_tweets:
        mentions_of_tweet = tweet.get('raw_data').get('entities').get('user_mentions')
        if len(mentions_of_tweet) > 0:
            party = get_party_of_politician(filename[:-5])
            for mention in mentions_of_tweet:
                mentions_list.append(mention.get('screen_name'))
                if party in mentions_dict:
                    mentions_dict[party].append(mention.get('screen_name'))
                else:
                    mentions_dict[party] = [mention.get('screen_name')] 

def get_all_links(all_tweets):
    for tweet in all_tweets:
        links_of_tweet = tweet.get('raw_data').get('entities').get('urls')
        if len(links_of_tweet) > 0:
            party = get_party_of_politician(filename[:-5])
            for link in links_of_tweet:
                url = link.get('expanded_url')
                if "bit.ly" in url or "tinyurl.com" in url:
                     url = expand_url(url)
                # If the bit.ly or tinyurl link doesn't work anymore
                if not "_ERROR_" in url:
                    link_list.append(url)
                domain = get_domain(url)
                domains_list.append(domain)
                if party in domains_dict:
                    domains_dict[party].append(domain)
                else:
                    domains_dict[party] = [domain]

for filename in os.listdir(TWEETS_SOURCE_FOLDER):
    f_path = os.path.join(TWEETS_SOURCE_FOLDER, filename)
    if os.path.isfile(f_path):
        with open(f_path, 'r', encoding='utf-8') as infile:
            all_tweets = [t for t in json.load(infile)]
            get_all_mentions(all_tweets)
            get_all_links(all_tweets)

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
    count_list = collections.Counter(mentions_list).most_common()
    with open('mentions_count.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(count_list), outfile, ensure_ascii=False)

def create_mentions_party_file():
    mentions_dict_opt = combine_afd(mentions_dict)

    for key, value in mentions_dict_opt.items():
        count_list = collections.Counter(value).most_common()
        mentions_dict_opt[key] = count_list

    with open('mentions_party.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(mentions_dict_opt), outfile, ensure_ascii=False)

create_mentions_count_file()
create_mentions_party_file()

def create_domains_count_file():
    count_list = collections.Counter(domains_list).most_common()
    with open('domains_count.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(count_list), outfile, ensure_ascii=False)

def create_domains_party_file():
    links_dict_opt = combine_afd(domains_dict)
    for key, value in links_dict_opt.items():
        count_list = collections.Counter(value).most_common()
        links_dict_opt[key] = count_list
    with open('domains_party.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(links_dict_opt), outfile, ensure_ascii=False)

def create_links_count_file():
    count_list = collections.Counter(link_list).most_common()
    with open('links_count.json', 'w', encoding='utf-8') as outfile:
        json.dump(str(count_list), outfile, ensure_ascii=False)

create_domains_count_file()
create_domains_party_file()
create_links_count_file()
