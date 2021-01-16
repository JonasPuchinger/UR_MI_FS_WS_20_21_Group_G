import statistics
import pandas as pd


def getAllCounts():
    rawData = pd.read_csv(r"number_of_tweets.csv")
    all = rawData.covid_tweets.tolist()
    newData = rawData[rawData.covid_tweets != 0]
    withoutZero = newData.covid_tweets.tolist()
    print("{}{}".format("All: ", len(all)))
    print("{}{}".format("Politicians left after deleting zero-covid-tweets: ", len(withoutZero)))
    print("{}{}".format("Amount Zero Tweets: ", len(all) - len(withoutZero)))
    print("{}{}".format("Percentage Zero Tweets: ", len(all)/len(withoutZero)))
    return withoutZero

all_counts = getAllCounts()

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



getMean()
getMedian()
getMin()
getMax()
getAmountFor357()