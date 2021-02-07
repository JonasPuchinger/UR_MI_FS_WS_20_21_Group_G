import json
import spacy
from spacy.lang.de import German
import matplotlib.pyplot as plt
from gensim.models import CoherenceModel
import nltk
from nltk.corpus import wordnet as wn
from gensim import corpora
import pickle
import gensim

nltk.download('wordnet')
nltk.download('stopwords')
de_stop = set(nltk.corpus.stopwords.words('german'))
parser = German()
nlp = spacy.load("de_core_news_md")
TWEETS_SOURCE_FOLDER = '../formated_data/tweet/marcobuelow.json'

# tokenization for getting nouns and removing hashtags and mentions
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            continue
        elif token.orth_.startswith('@'):
            continue
        elif token.orth_.startswith('#'):
            continue
        else:
            nlp_token = nlp(str(token))
            for token in nlp_token:
                if token.pos_ == 'NOUN':
                    lda_tokens.append(token.lower_)
    return lda_tokens

# Reduce word to lemma to get the root
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

# Remove stopwords 
def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 3]
    tokens = [token for token in tokens if token not in de_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

# get text of tweets
text_data = []
with open(TWEETS_SOURCE_FOLDER, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for tweet in data:
        text = tweet.get("raw_data").get("full_text")
        tokens = prepare_text_for_lda(text)
        text_data.append(tokens)

id2word = corpora.Dictionary(text_data)
corpus = [id2word.doc2bow(text) for text in text_data]
pickle.dump(corpus, open('corpus.pkl', 'wb'))
id2word.save('dictionary.gensim')

# get coherence value for different amounts of topics and create a line chart
if __name__ == '__main__':
    limit=10
    start=1
    step=1

    def compute_coherence_values():
        coherence_values_c_v = []
        coherence_values_u_mass = []
        model_list = []
        for num_topics in range(start, limit, step):
            lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics = num_topics, id2word=id2word, passes=10)
            model_list.append(lda_model)
            lda_model.save('model5.gensim')
            coherence_model_c_v = CoherenceModel(model=lda_model, texts=text_data, dictionary=id2word, coherence='c_v')
            coherence_values_c_v.append(coherence_model_c_v.get_coherence())
            coherence_model_u_mass = CoherenceModel(model=lda_model, corpus=corpus, coherence='u_mass')
            coherence_values_u_mass.append(coherence_model_u_mass.get_coherence())
        return model_list, coherence_values_c_v, coherence_values_u_mass

    model_list, coherence_values_c_v, coherence_values_u_mass = compute_coherence_values()
    
    for model in model_list:
        topics = model.print_topics(num_words=4)
        for topic in topics:
            print(topic) 

    x = range(start, limit, step)
    plt.plot(x, coherence_values_c_v)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score c_v")
    plt.legend(("coherence_values"), loc='best')
    plt.savefig("c_v.png")
    plt.show()

    plt.plot(x, coherence_values_u_mass)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score_u_mass")
    plt.legend(("coherence_values"), loc='best')
    plt.show()

    for m, cv in zip(x, coherence_values_c_v):
        print("Num Topics =", m, " has Coherence Value (c_v) of", round(cv, 4))

    for m, cv in zip(x, coherence_values_u_mass):
        print("Num Topics =", m, " has Coherence Value (u_mass) of", round(cv, 4))
