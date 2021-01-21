
from textblob_de import TextBlobDE
import json
import codecs
from textblob.inflect import singularize as _singularize, pluralize as _pluralize

WORDLIST = '../assets/wordlistWithoutHashtags.json'
# Vorher:
# Männliche & weibliche Formen eintragen
# Hashtags manuell entfernen & danach wieder hinzufügen


new_final_list = []

def get_words():
    return json.load(codecs.open(WORDLIST, 'r', 'utf-8-sig'))

def get_singular(word):  
    return word.singularize()

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

for word in get_blob_words():
    #new_final_list.append(get_singular(word))
    new_final_list.append(word)
    new_final_list.append(get_plural(word))
    new_final_list = list(dict.fromkeys(new_final_list))


with open('new_list.json', 'w') as outfile:
    json.dump(new_final_list, outfile)