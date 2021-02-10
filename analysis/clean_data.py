import spacy
from spacy.lang.de import German
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import wordnet as wn
import re
from textblob_de import TextBlobDE as TextBlob


#nltk.download('wordnet')
#nltk.download('stopwords')
de_stop = set(nltk.corpus.stopwords.words('german'))
nlp = spacy.load("de_core_news_md")

parser = German()

def clean_for_lda(text):
    tokens = nlp(text)
    #tokens = parser(text)
    tokens = [token for token in tokens if remove_whitespaces(token)]
    tokens = [get_lemma(token) for token in tokens]
    tokens = [to_lower(token) for token in tokens]
    tokens = [token for token in tokens if remove_stopwords(token)]
    tokens = [token for token in tokens if remove_url(token)]
    tokens = [token for token in tokens if remove_hashtags(token)]
    tokens = [token for token in tokens if remove_mention(token)]
    tokens = [token for token in tokens if remove_punctuation_and_smileys(token)]
    tokens = [token for token in tokens if get_nouns_blob(token)]
    return [str(token) for token in tokens]


def clean_for_filtering(text):
    tokens = nlp(text)
    tokens = [token for token in tokens if remove_whitespaces(token)]
    tokens = [token for token in tokens if remove_stopwords(token)]
    tokens = [token for token in tokens if remove_url(token)]
    tokens = [token for token in tokens if remove_mention(token)]
    tokens = [token for token in tokens if remove_punctuation_and_smileys(token)]
    tokens = [to_lower(token) for token in tokens]
    return tokens



# Has to be called before tokenization because # gets seperated otherwise
def remove_hashtags(token):
    # TODO use regex and change order in function
    return False if token.orth_.startswith('#') else True  


def remove_stopwords(token):
    return True if str(token) not in de_stop else False

def remove_url(token):
    return False if token.like_url else True

def remove_mention(token):
    return False if token.orth_.startswith('@') else True

def remove_whitespaces(token):
    return True if not token.orth_.isspace() else False

def get_nouns(token):
    if token.pos_ == 'NOUN':
        return True
    return False

def get_nouns_blob(token):
    blob = TextBlob(str(token))
    if blob.tags[0][1] == 'NN':
        return True
    return False

def to_lower(token):
    return nlp(token.lower_)[0]

def remove_punctuation_and_smileys(token):
    if re.sub(r'[^\w\s]','', str(token)) == '': 
        return False
    return True

# Reduce word to lemma to get the root
def get_lemma(token):
    return nlp(token.lemma_)[0]
    
    
testdata = "@petergruenn https://t.co/jLq2Vy1HLh Wie oft noch? Vorschläge FFP-2 des Bundes für eine stärkere 🦉 Koordination in Krisen werden in ruhigen Zeiten regelmäßig als Angriff auf die Verfassung und das Föderalismusprinzip brüsk genau von denen zurückgewiesen, die dann in der Not mangelnde Führung des Bundes beklagen! #corona"


#print(clean_for_lda(testdata))

