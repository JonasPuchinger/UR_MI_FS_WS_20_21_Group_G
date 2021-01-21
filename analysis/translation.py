import googletrans
from googletrans import Translator
import os
import json
import preprocessor as pre
from google_trans_new import google_translator  
from deep_translator import MyMemoryTranslator
from textblob import TextBlob
import time

TWEETS_SOURCE_FOLDER = './formated_data/tweet/'


def translate():
    tweets = getAllTweets()
    result = []
    for i in tweets:
        #translated = MyMemoryTranslator(source='en', target='de').translate(i)
        lang = TextBlob(i).detect_language()
        try:
            translated = TextBlob(i).translate(from_lang= 'en', to = 'de')
        except:
            continue
        result.append(str(translated))
        time.sleep(1)
        print('check')
    with open('translated_tweets.json', 'w') as outfile:
        json.dump(str(result), outfile)


def preprocessing_tweet(original_tweet):
    pre.set_options(pre.OPT.URL, pre.OPT.MENTION, pre.OPT.RESERVED, pre.OPT.SMILEY, pre.OPT.NUMBER)
    tweet = pre.clean(original_tweet)
    return tweet

def getAllTweets():
    all_tweets = []
    for filename in os.listdir(TWEETS_SOURCE_FOLDER):
        f_path = os.path.join(TWEETS_SOURCE_FOLDER, filename)
        if os.path.isfile(f_path):
            with open(f_path, 'r', encoding='utf-8') as infile:
                tweets = [t for t in json.load(infile) if t['raw_data']['lang'] == 'en']
                for i in tweets:
                    text = i.get("raw_data").get("full_text")
                    if(len(text) > 25):
                        opt = preprocessing_tweet(text)
                        all_tweets.append(opt)
    #strList = '; '.join(all_tweets)
    #n = 4990
    #new = [strList[i:i+n] for i in range(0, len(strList), n)]# len(new) = 255
    return all_tweets     


translate()