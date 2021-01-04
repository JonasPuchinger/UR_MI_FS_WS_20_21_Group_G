import json
import os
import statistics


TWEETS_SOURCE_FOLDER = './formated_data/tweet/'

all_counts = []

def getAllCounts():
    for filename in os.listdir(TWEETS_SOURCE_FOLDER):
        f_path = os.path.join(TWEETS_SOURCE_FOLDER, filename)
        if os.path.isfile(f_path):
            with open(f_path, 'r', encoding='utf-8') as infile:
                all_tweets = [t for t in json.load(infile)]
                all_counts.append(len(all_tweets))
    print("{}{}".format("All: ", len(all_counts)))       


def getMedian():
    median = statistics.median(all_counts)
    print("{}{}".format("Median: ", median))
    getRemaining(median)


def getMean():
    mean = statistics.mean(all_counts)
    print("{}{}".format("Mean: ", mean))
    getRemaining(mean)


def getMin():
    minVal = min(all_counts)
    print("{}{}".format("Min: ", minVal))


def getMax():
    maxVal = max(all_counts)
    print("{}{}".format("Max: ", maxVal))


def getRemaining(value):
    remainingList = [i for i in all_counts if i >= value]
    print("{}{}".format("Remaining: ", len(remainingList)))


def getAmountFor357():
    remainingList = [i for i in all_counts if i >= 357]
    print("{}{}".format("Remaining with >= 357 tweets: ", len(remainingList)))


getAllCounts()
getMean()
getMedian()
getMin()
getMax()
getAmountFor357()