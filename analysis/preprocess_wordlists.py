import csv
import json
import codecs
import nltk
from HanTa import HanoverTagger as ht
from itertools import zip_longest
import preprocessor as pre
import re

# Preprocessing wordlist: Stemming, Lemmatization

RESULTS_FILE = 'preprocessed_wordlist.csv'
WORDLIST_STEM = 'wordlist_stem.json'
WORDLIST_LEM = 'wordlist_lem.json'
WORDLIST_FUZ = 'wordlist_fuz.json'
WORDLIST_NEW = 'wordlist_new.json'
WORDLIST = '../assets/wordlist.json'

wordlist = json.load(codecs.open(WORDLIST, 'r', 'utf-8-sig'))
pre.set_options(pre.OPT.NUMBER)


# Lemmatization (HanoverTagger)
def preprocess_wordlist_lemma(wordlist):
    tagger = ht.HanoverTagger('morphmodel_ger.pgz')
    wordlist_lemma = []
    for word in wordlist:
        # Cleaning (Numbers)
        word = pre.clean(word)
        # Remove Punctuations
        word = re.sub(r'[^\w\s]', '', word)
        # Lemmatization
        word = tagger.analyze(word, taglevel=1)
        wordlist_lemma.append(word[0].lower())
    # Remove duplicates
    wordlist_lemma = set(wordlist_lemma)
    return list(wordlist_lemma)


# Stemming
def preprocess_wordlist_stem(wordlist):
    ps = nltk.PorterStemmer()
    wordlist_stem = []
    for word in wordlist:
        lower_word = word.lower()
        # Cleaning (Numbers)
        word = pre.clean(lower_word)
        # Remove Punctuations
        word = re.sub(r'[^\w\s]', '', word)
        # Stemming
        word = ps.stem(word)
        wordlist_stem.append(word)
    # Remove duplicates
    wordlist_stem = set(wordlist_stem)
    return list(wordlist_stem)


# Fuzzy
def preprocess_wordlist_fuzzy(wordlist):
    wordlist_fuz = []
    for word in wordlist:
        lower_word = word.lower()
        # Cleaning (Numbers)
        word = pre.clean(lower_word)
        # Removal of digits
        word = re.sub('\d+', '', word)
        # Remove Punctuations
        word = re.sub(r'[^\w\s]', '', word)
        wordlist_fuz.append(word)
    # Remove duplicates
    wordlist_fuz = set(wordlist_fuz)
    return list(wordlist_fuz)


# wordlist_lemma = preprocess_wordlist_lemma(wordlist)
wordlist_lemma = []
# wordlist_stemming = preprocess_wordlist_stem(wordlist)
wordlist_stemming = []

remove_words1 = ["R0", "#n95"]
update_wordlist = [word for word in wordlist if word not in remove_words1]

new_wordlist = preprocess_wordlist_fuzzy(update_wordlist)
remove_words2 = ["pcr", "rzahl", "rwert", "rwerte"]
wordlist_fuzzy = [word for word in new_wordlist if word not in remove_words1]

d = [wordlist, wordlist_stemming, wordlist_lemma, wordlist_fuzzy]
data = zip_longest(*d, fillvalue='')
with open(RESULTS_FILE, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(('wordlist', 'wordlist (Stemming)', 'wordlist (Lemmatization)', 'wordlist (Fuzzy)'))
    writer.writerows(data)

with open(WORDLIST_STEM, 'w', encoding='utf-8') as f:
    json.dump(wordlist_stemming, f, ensure_ascii=False)

with open(WORDLIST_LEM, 'w', encoding='utf-8') as f:
    json.dump(wordlist_lemma, f, ensure_ascii=False)

with open(WORDLIST_NEW, 'w', encoding='utf-8') as f:
    json.dump(new_wordlist, f, ensure_ascii=False)

with open(WORDLIST_FUZ, 'w', encoding='utf-8') as f:
    json.dump(wordlist_fuzzy, f, ensure_ascii=False)
