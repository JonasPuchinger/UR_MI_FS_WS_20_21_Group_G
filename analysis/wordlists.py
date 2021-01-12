import csv
import json
import codecs
import nltk
import spacy
from HanTa import HanoverTagger as ht
from itertools import zip_longest

# Wordlist: Stemming, Lemmatization

RESULTS_FILE = 'result_wordlists.csv'
WORDLIST_STEM = 'wordlist_stem.json'
WORDLIST_LEM = 'wordlist_lem.json'
WORDLIST = '../assets/wordlist.json'

wordlist = json.load(codecs.open(WORDLIST, 'r', 'utf-8-sig'))


# Lemmatization (spacy)
def clean_wordlist_lemma1(list):
    nlp = spacy.load('de_core_news_sm')
    wordlist_lemma = []
    for word in list:
        word = word.lower()
        for x in nlp(word):
            wordlist_lemma.append(x.lemma_)
    return wordlist_lemma


# Lemmatization (HanoverTagger)
def clean_wordlist_lemma2(list):
    tagger = ht.HanoverTagger('morphmodel_ger.pgz')
    wordlist_lemma = []
    for word in list:
        word = tagger.analyze(word, taglevel=1)
        wordlist_lemma.append(word[0].lower())
    return wordlist_lemma


def clean_wordlist_stem(list):
    ps = nltk.PorterStemmer()
    wordlist_stem = []
    for word in list:
        lower_word = word.lower()
        word = ps.stem(lower_word)
        wordlist_stem.append(word)
    return wordlist_stem


wordlist_lemma1 = clean_wordlist_lemma1(wordlist)
wordlist_lemma2 = clean_wordlist_lemma2(wordlist)
wordlist_stemming = clean_wordlist_stem(wordlist)

d = [wordlist, wordlist_stemming,  wordlist_lemma1, wordlist_lemma2]
data = zip_longest(*d, fillvalue='')
with open(RESULTS_FILE, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(('wordlist', 'wordlist (stemming)', 'wordlist (spacy)', 'wordlist (HanoverTagger)'))
    writer.writerows(data)

with open(WORDLIST_STEM, 'w', encoding='utf-8') as f:
    json.dump(wordlist_stemming, f, ensure_ascii=False)

with open(WORDLIST_LEM, 'w', encoding='utf-8') as f:
    json.dump(wordlist_lemma2, f, ensure_ascii=False)
