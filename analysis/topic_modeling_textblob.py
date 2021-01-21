
from textblob_de import TextBlobDE
from textblob.np_extractors import ConllExtractor
import pandas as pandas
import json
import operator
import nltk
import preprocessor as pre

TWEETS_SOURCE_FOLDER = './formated_data/tweet/_MartinNeumann.json'

#TODO: Vorher Daten cleanen (Hashtags raus usw.-> Code von Theresa, wenn fertig)


def getAllTweets():
    all_tweets = []
    with open(TWEETS_SOURCE_FOLDER, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for tweet in data:
            text = tweet.get("raw_data").get("full_text")
            text = preprocessing_tweet(text)
            all_tweets.append(text)
    strList = '; '.join(all_tweets)
    blob = TextBlobDE(strList)
    #print(blob.tags)
    
    nouns = blob.noun_phrases
    dict1 = dict((x,nouns.count(x)) for x in set(nouns))
    # for sentence in blob.sentences:
        #print(sentence.sentiment.polarity)

    sorted_dict = dict( sorted(dict1.items(), key=operator.itemgetter(1),reverse=True))

    print(list(sorted_dict.items())[0])
    print(list(sorted_dict.items())[1])
    print(list(sorted_dict.items())[2])


def preprocessing_tweet(original_tweet):
    pre.set_options(pre.OPT.URL, pre.OPT.MENTION, pre.OPT.RESERVED, pre.OPT.SMILEY, pre.OPT.NUMBER)
    tweet = pre.clean(original_tweet)
    return tweet


    
getAllTweets()
