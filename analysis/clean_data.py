import spacy
from spacy.lang.de import German
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import wordnet as wn
import re
from textblob_de import TextBlobDE as TextBlob

nlp = spacy.load("de_core_news_md")

try:
    de_stop = set(nltk.corpus.stopwords.words('german'))
    eng_stop = set(nltk.corpus.stopwords.words('english'))
except:
    # download wordnet and stopwords if necessary
    nltk.download('wordnet')
    nltk.download('stopwords')
    de_stop = set(nltk.corpus.stopwords.words('german'))
    eng_stop = set(nltk.corpus.stopwords.words('english'))

def clean_for_lda(text):
    tokens = nlp(text)
    tokens = [token for token in tokens if remove_whitespaces(token)]
    tokens = [token for token in tokens if remove_punctuation_and_smileys(token)]
    tokens = [token for token in tokens if remove_stopwords(token)]
    tokens = [token for token in tokens if remove_url(token)]
    tokens = [token for token in tokens if remove_mention(token)]
    tokens = [get_lemma(token) for token in tokens]
    tokens = [to_lower(token) for token in tokens]
    tokens = [token for token in tokens if remove_amp_tb(token)]
    tokens = [token for token in tokens if get_nouns(token)]
    tokens = [token for token in tokens if len(token) > 2]
    return [str(token) for token in tokens]

def clean_for_filtering(text):
    tokens = nlp(text)
    tokens = [token for token in tokens if remove_whitespaces(token)]
    tokens = [token for token in tokens if remove_stopwords(token)]
    tokens = [token for token in tokens if remove_url(token)]
    tokens = [token for token in tokens if remove_mention(token)]
    tokens = [token for token in tokens if remove_punctuation_and_smileys(token)]
    tokens = [to_lower(token) for token in tokens]
    return [str(token) for token in tokens]

def remove_stopwords(token):
    return True if str(token) not in de_stop and str(token) not in eng_stop else False

def remove_url(token):
    return False if token.like_url else True

def remove_mention(token):
    return False if token.orth_.startswith('@') else True

def remove_whitespaces(token):
    if str(token) == "" or re.sub(r'\s*', '', str(token)) == '':
        return False
    return True if not token.text.isspace() else False

# The abbreviation TB has to be removed. The ampersand (&) was transformed into '&amp;' in the scraping process. This has to be deleted as well.
def remove_amp_tb(token):
    return True if str(token) != 'amp' and str(token) != 'tb' else False

def get_nouns(token):
    blob = TextBlob(str(token))
    try:
        if blob.tags[0][1] == 'NN':
            return True
    except: 
        False
    return False

def to_lower(token):
    return nlp(token.lower_)[0]

def remove_punctuation_and_smileys(token):
    if re.sub(r'[^\w\s]', '', str(token)) == '':
        return False
    return True

# Reduce word to lemma to get the root
def get_lemma(token):
    return nlp(token.lemma_)[0]
