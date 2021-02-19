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
PATH = os.getcwd() + "\\" + 'CDU'

print(datetime.now())

def get_politicians_list():
    with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
      return [p for p in json.load(infile)]

politicians_list = get_politicians_list()

Path(PATH).mkdir(parents=True, exist_ok=True)

CDU_List = [str(politician['id']) for politician in politicians_list if politician['Partei'] == 'CDU']

for politician in politicians_list:
    # get text of tweets
    text_data = []
    with open(TWEETS_SOURCE_FOLDER + politician['screen_name'] + '.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        if data != []:
            for tweet in data:
                if(str(tweet.get('raw_data').get('user_id_str')) in CDU_List):
                    text = tweet.get("raw_data").get("full_text")
                    cleaned_data = cd(text)
                    text_data.append(cleaned_data)

if text_data != []:
    id2word = corpora.Dictionary(text_data)
    corpus = [id2word.doc2bow(text) for text in text_data]
    new_path = PATH + "\\"
    Path(new_path).mkdir(parents=True, exist_ok=True)
    new_path = new_path + "\\"
    pickle.dump(corpus, open(new_path + 'corpus.pkl', 'wb'))
    id2word.save(new_path + 'dictionary.gensim')

    # get coherence value for different amounts of topics and create line charts for the two value types
    if __name__ == '__main__':
        start=3
        limit=6 # not included
        step=1

        def compute_coherence_values():
            coherence_values_c_v = []
            coherence_values_u_mass = []
            model_list = []
            for num_topics in range(start, limit, step):
                lda_model = gensim.models.LdaMulticore(corpus=corpus, num_topics = num_topics, id2word=id2word, passes=10)
                model_list.append(lda_model)
                lda_model.save(new_path + 'topics_' + num_topics + '_model5.gensim')
                coherence_model_c_v = CoherenceModel(model=lda_model, texts=text_data, dictionary=id2word, coherence='c_v')
                coherence_values_c_v.append(coherence_model_c_v.get_coherence())
                coherence_model_u_mass = CoherenceModel(model=lda_model, corpus=corpus, coherence='u_mass')
                coherence_values_u_mass.append(coherence_model_u_mass.get_coherence())
            return model_list, coherence_values_c_v, coherence_values_u_mass

        model_list, coherence_values_c_v, coherence_values_u_mass = compute_coherence_values()
        
        topic_list = []
        for model in model_list:
            topics = model.print_topics(num_words=6)
            topic_list.append(topics)
            
        with open(new_path + "Topics.txt", "w") as text_file:
            text_file.write(str(topic_list))

        x = range(start, limit, step)
        plt.plot(x, coherence_values_c_v)
        plt.xlabel("Num Topics")
        plt.ylabel("Coherence score c_v")
        plt.legend(("coherence_values"), loc='best')
        plt.savefig(new_path + "c_v_CDU" + ".png")
        plt.close()
        
        plt.plot(x, coherence_values_u_mass)
        plt.xlabel("Num Topics")
        plt.ylabel("Coherence score_u_mass")
        plt.legend(("coherence_values"), loc='best')
        plt.savefig(new_path + "u_mass_CDU" + ".png")
        plt.close()

        with open(new_path + "c_v_coherence_CDU.txt", "w") as text_file:
            for m, cv in zip(x, coherence_values_c_v): 
                text_file.write("Num Topics =", m, " has Coherence Value (c_v) of", round(cv, 4))
        
        with open(new_path + "u_mass_coherence_CDU.txt", "w") as text_file:
            for m, cv in zip(x, coherence_values_u_mass):
                text_file.write("Num Topics =", m, " has Coherence Value (u_mass) of", round(cv, 4))
        
        print(datetime.now())
