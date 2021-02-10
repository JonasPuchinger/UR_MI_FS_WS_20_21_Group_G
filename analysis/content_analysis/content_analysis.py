import json
import matplotlib.pyplot as plt
from gensim.models import CoherenceModel
import gensim
from gensim import corpora
import pickle
#from ..clean_data import clean_for_lda

import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, '..')))
from clean_data import clean_for_lda

TWEETS_SOURCE_FOLDER = '../formated_data/tweet/'
POLITICIAN = 'Hansjoerg_Durz'

# get text of tweets
text_data = []
with open(TWEETS_SOURCE_FOLDER + POLITICIAN + '.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for tweet in data:
        text = tweet.get("raw_data").get("full_text")
        cleaned_data = clean_for_lda(text)
        text_data.append(cleaned_data)
id2word = corpora.Dictionary(text_data)
corpus = [id2word.doc2bow(text) for text in text_data]
pickle.dump(corpus, open('corpus.pkl', 'wb'))
id2word.save('dictionary.gensim')

# get coherence value for different amounts of topics and create line charts for the two value types
if __name__ == '__main__':
    limit=15 # not included
    start=1
    step=1

    def compute_coherence_values():
        coherence_values_c_v = []
        coherence_values_u_mass = []
        model_list = []
        for num_topics in range(start, limit, step):
            lda_model = gensim.models.LdaMulticore(corpus=corpus, num_topics = num_topics, id2word=id2word, passes=10)
            model_list.append(lda_model)
            lda_model.save('model5.gensim')
            coherence_model_c_v = CoherenceModel(model=lda_model, texts=text_data, dictionary=id2word, coherence='c_v')
            coherence_values_c_v.append(coherence_model_c_v.get_coherence())
            coherence_model_u_mass = CoherenceModel(model=lda_model, corpus=corpus, coherence='u_mass')
            coherence_values_u_mass.append(coherence_model_u_mass.get_coherence())
            print(num_topics)
        return model_list, coherence_values_c_v, coherence_values_u_mass

    model_list, coherence_values_c_v, coherence_values_u_mass = compute_coherence_values()
    
    for model in model_list:
        topics = model.print_topics(num_words=6)
        for topic in topics:
            print(topic) 

    x = range(start, limit, step)
    plt.plot(x, coherence_values_c_v)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score c_v")
    plt.legend(("coherence_values"), loc='best')
    plt.savefig("c_v_" + POLITICIAN + ".png")
    plt.close()
    
    plt.plot(x, coherence_values_u_mass)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score_u_mass")
    plt.legend(("coherence_values"), loc='best')
    plt.savefig("u_mass_" + POLITICIAN + ".png")

    for m, cv in zip(x, coherence_values_c_v):
        print("Num Topics =", m, " has Coherence Value (c_v) of", round(cv, 4))

    for m, cv in zip(x, coherence_values_u_mass):
        print("Num Topics =", m, " has Coherence Value (u_mass) of", round(cv, 4))
