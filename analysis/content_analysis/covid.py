import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
from gensim.models import CoherenceModel
import gensim
from gensim import corpora
import pickle
from analysis.clean_data import clean_for_lda as cd
from datetime import datetime, date, timedelta
import time

TWEETS_SOURCE_FOLDER = '../filtered_data/covid_tweets/'
POLITICIANS_LIST = '../../assets/all_politicians.json'
DATE = '2020-11-18'
PATH = os.getcwd() + "\\" + DATE + "_covid"

def get_politicians_list():
        with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
            return [p for p in json.load(infile)]
politicians_list = get_politicians_list()

Path(PATH).mkdir(parents=True, exist_ok=True)

def format_date(current_date):
    return datetime.strftime(datetime.strptime(current_date,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d') 

path = PATH + "\\"
text_data = []

for politician in politicians_list:  
    with open(TWEETS_SOURCE_FOLDER +  politician['screen_name'] + '.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        if data != []:
            for tweet in data:
                if(format_date(tweet.get('raw_data').get('created_at'))==DATE):
                    text = tweet.get("raw_data").get("full_text")
                    cleaned_data = cd(text)
                    text_data.append(cleaned_data)
if text_data != []:
    id2word = corpora.Dictionary(text_data)
    corpus = [id2word.doc2bow(text) for text in text_data]
    pickle.dump(corpus, open(path + 'corpus.pkl', 'wb'))
    id2word.save(path + 'dictionary.gensim')

    # get LDA model and the topic
    if __name__ == '__main__':
        num_topics = 5
        lda_model = gensim.models.LdaMulticore(corpus=corpus, num_topics = num_topics, id2word=id2word, passes=10)
        lda_model.save(path + 'model5.gensim')
        topics = lda_model.print_topics(num_words=6)
        with open(path + "Topics.txt", "w") as text_file:
            text_file.write(str(topics))
    