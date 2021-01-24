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
    return wordlist_lemma


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
    return wordlist_stem


# Fuzzy
def preprocess_wordlist_fuzzy(wordlist):
    wordlist_stem = []
    for word in wordlist:
        lower_word = word.lower()
        # Cleaning (Numbers)
        word = pre.clean(lower_word)
        # Remove Punctuations
        word = re.sub(r'[^\w\s]', '', (word))
        wordlist_stem.append(word)
    return wordlist_stem


wordlist_lemma = preprocess_wordlist_lemma(wordlist)
wordlist_stemming = preprocess_wordlist_stem(wordlist)
wordlist_fuzzy = preprocess_wordlist_fuzzy(wordlist)

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

with open(WORDLIST_FUZ, 'w', encoding='utf-8') as f:
    json.dump(wordlist_fuzzy, f, ensure_ascii=False)
