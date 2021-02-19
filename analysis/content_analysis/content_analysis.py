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

TWEETS_SOURCE_FOLDER = '../formated_data/tweet/'
POLITICIANS_LIST = '../../assets/all_politicians.json'

#quarters = [['01/01/2020', '31/03/2020'], ['01/04/2020', '30/06/2020'], ['01/07/2020', '30/09/2020'], ['01/10/2020', '31/12/2020']]
quarters = [['01/10/2020', '31/12/2020']]

def get_politicians_list():
        with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
            return [p for p in json.load(infile)]
politicians_list = get_politicians_list()

def format_date(current_date):
    return datetime.strftime(datetime.strptime(current_date,'%a %b %d %H:%M:%S +0000 %Y'), '%d/%m/%Y') 

def check_date(current_date):
    return True if time.strptime(current_date, '%d/%m/%Y') >= time.strptime(quarter[0], '%d/%m/%Y') and time.strptime(current_date, '%d/%m/%Y') <= time.strptime(quarter[1], '%d/%m/%Y') else False

for quarter in quarters:
    quarter_value = quarters.index(quarter) + 4
    print(quarter_value)
    path = os.getcwd() + "\\" + 'Quarter_' + str(quarter_value)
    Path(path).mkdir(parents=True, exist_ok=True)
    path = path + "\\"
    text_data = []

    for politician in politicians_list:  
        with open(TWEETS_SOURCE_FOLDER +  politician['screen_name'] + '.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            if data != []:
                for tweet in data:
                    if(check_date(format_date(tweet.get('raw_data').get('created_at')))):
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
            lda_model = gensim.models.LdaMulticore(corpus=corpus, num_topics = num_topics, id2word=id2word, passes=2)
            lda_model.save(path + 'model5.gensim')
            topics = lda_model.print_topics(num_words=6)
            with open(path + "Topics.txt", "w") as text_file:
                text_file.write(str(topics))
        