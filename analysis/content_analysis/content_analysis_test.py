import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
from gensim.models import CoherenceModel
import gensim
from gensim import corpora
import pickle
from analysis.clean_data import clean_for_lda as cd
from datetime import datetime


TWEETS_SOURCE_FOLDER = '../formated_data/tweet/'
POLITICIANS_LIST = '../../assets/all_politicians.json'
DATE = '2020-02-05'
PATH = os.getcwd() + "\\" + DATE + "_test"

def get_politicians_list():
    with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
      return [p for p in json.load(infile)]

politicians_list = get_politicians_list()

Path(PATH).mkdir(parents=True, exist_ok=True)
PATH = PATH + "\\"

def format_date(date):
    return datetime.strftime(datetime.strptime(date,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d') 


for politician in politicians_list:
    # get text of tweets
    text_data = []
    politician_name = politician['screen_name']
    with open(TWEETS_SOURCE_FOLDER + politician_name + '.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        if data != []:
            for tweet in data:
                if(format_date(tweet.get('raw_data').get('created_at')) == DATE):
                    text = tweet.get("raw_data").get("full_text")
                    cleaned_data = cd(text)
                    text_data.append(cleaned_data)
if text_data != []:
    id2word = corpora.Dictionary(text_data)
    corpus = [id2word.doc2bow(text) for text in text_data]
    pickle.dump(corpus, open(PATH + 'corpus.pkl', 'wb'))
    id2word.save(PATH + 'dictionary.gensim')

    # get coherence value for different amounts of topics and create line charts for the two value types
    if __name__ == '__main__':
        num_topics = 5
        lda_model = gensim.models.LdaMulticore(corpus=corpus, num_topics = num_topics, id2word=id2word, passes=10)
        lda_model.save(PATH + 'model5.gensim')
        topics = lda_model.print_topics(num_words=6)
        with open(PATH + "Topics.txt", "w") as text_file:
            text_file.write(str(topics))
       