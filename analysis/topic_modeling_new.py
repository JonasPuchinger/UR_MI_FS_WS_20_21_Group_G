import json
import spacy
from spacy.lang.de import German
parser = German()
nlp = spacy.load("de_core_news_md")

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
            lda_tokens.append(token.lower_)
    return lda_tokens


import nltk
nltk.download('wordnet')


from nltk.corpus import wordnet as wn
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('german'))

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens


TWEETS_SOURCE_FOLDER = './formated_data/tweet/_MartinNeumann.json'


import random
text_data = []
with open(TWEETS_SOURCE_FOLDER, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for tweet in data:
        text = tweet.get("raw_data").get("full_text")
        tokens = prepare_text_for_lda(text)
        text_data.append(tokens)




from gensim import corpora
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]
import pickle
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')


import gensim
NUM_TOPICS = 5
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')
topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)