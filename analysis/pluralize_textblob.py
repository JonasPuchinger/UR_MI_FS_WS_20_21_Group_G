from textblob_de import TextBlobDE
import json
import codecs
from textblob.inflect import singularize as _singularize, pluralize as _pluralize

WORDLIST_SOURCE = '../assets/wordlist_old.json'
WORDLIST_NEW_SOURCE = '../assets/wordlist.json'


new_final_list = []
hashtags = []

def get_words():
    words = json.load(codecs.open(WORDLIST_SOURCE, 'r', 'utf-8-sig'))
    list_without_hashtags = []
    for word in words:
        if word.startswith('#'):
            hashtags.append(word)
        else:
            list_without_hashtags.append(word)
    return list_without_hashtags

def get_plural(word):
    return word.pluralize()

def get_nouns(blob):
    new_list=[]
    tags = blob.tags
    for tag in tags:
        if tag[1] == 'NN':
            new_list.append(tag[0])
        else:
            new_final_list.append(tag[0])
    return new_list

def get_blob_words():
    strList = '; '.join(get_words())
    blob = TextBlobDE(strList)
    just_nouns = get_nouns(blob)
    return just_nouns

def remove_duplicates(list):
    elements = set()
    for elem in list:
        if not elem in elements:
            elements.add(elem)         
    return elements

for word in get_blob_words():
    new_final_list.append(word)
    new_final_list.append(get_plural(word))
    new_final_list = list(dict.fromkeys(new_final_list))

list_without_duplicates = list(remove_duplicates(new_final_list))

sorted_hashtags = sorted(hashtags, key=str.lower)
sorted_list = sorted(list_without_duplicates, key=str.lower)

for hashtag in sorted_hashtags:
    sorted_list.append(hashtag)

with open(WORDLIST_NEW_SOURCE, 'w', encoding='utf-8') as outfile:
    json.dump(sorted_list, outfile, ensure_ascii=False)
