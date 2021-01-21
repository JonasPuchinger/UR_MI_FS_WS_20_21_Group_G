
import json
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import pickle
import scipy
import spacy
spacy.load('de_core_news_sm')
from spacy.lang.de import German
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
import operator
from gensim import corpora

TWEETS_SOURCE_FOLDER = './formated_data/tweet/_MartinNeumann.json'


def getAllTweets():
    all_tweets = []
    with open(TWEETS_SOURCE_FOLDER, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for tweet in data:
            text = tweet.get("raw_data").get("full_text")
            all_tweets.append(text)
    return all_tweets


def matrix():
    tweets = getAllTweets()
    df = pd.DataFrame({'text': tweets})
    cv = CountVectorizer()
    data_cv = cv.fit_transform(df['text'])
    pickle.dump(cv, open("cv_stop.pkl", "wb"))
    data_cv.to_pickle("dtm_stop.pkl")
    #data_stop.to_pickle("dtm_stop.pkl") #saving the pickled data
    data = pd.read_pickle('dtm_stop.pkl')
    #data
    tdm = data.transpose()
    tdm.head()

    sparse_counts = scipy.sparse.csr_matrix(data_cv)
    corpus = matutils.Sparse2Corpus(sparse_counts)
    cv = pickle.load(open("cv_stop.pkl", "rb"))
    id2word = dict((v, k) for k, v in cv.vocabulary_.items())


