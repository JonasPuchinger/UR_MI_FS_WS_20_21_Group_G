#LOAD LDA FROM CORPUS

from gensim import corpora
import pickle
import gensim
import warnings
import pyLDAvis.gensim
import os
warnings.filterwarnings("ignore", category=DeprecationWarning)
dates = ['Quarter_4'] # Top 5

for date in dates:  
    path = os.getcwd() + '\\' + date + '\\' 
    id2word = gensim.corpora.Dictionary.load(path + 'dictionary.gensim')
    corpus = pickle.load(open(path + 'corpus.pkl', 'rb'))

    # get LDA model and the topics
    if __name__ == '__main__':
        num_topics = 5
        lda_model = gensim.models.LdaMulticore(corpus=corpus, num_topics = num_topics, id2word=id2word, passes=10)
        lda_model.save(path + 'model5.gensim')
        topics = lda_model.print_topics(num_words=6)
        with open(path + "Topics.txt", "w") as text_file:
            text_file.write(str(topics))
