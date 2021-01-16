import statistics
import pandas as pd
from array import *
import numpy


def getAllCounts():
    rawData = pd.read_csv(r"number_of_tweets.csv")
    newData = rawData[rawData.covid_tweets != 0]
    return newData.covid_tweets.tolist()

def getAllPercentages():
    rawData = pd.read_csv(r"number_of_tweets.csv")
    newData = rawData[rawData.covid_tweets != 0]
    return newData.ratio.tolist()

all_counts = getAllCounts()
all_percentages = getAllPercentages()

def getAllData():
    combined = list(zip(all_counts, all_percentages))
    return combined

all_data = getAllData()


def getMedian():
    median_counts = statistics.median(all_counts)
    median_percentages = statistics.median(all_percentages)
    print("MEDIAN: ")
    getRemaining(median_counts, median_percentages)


def getMean():
    mean_counts = statistics.mean(all_counts)
    mean_percentages = statistics.mean(all_percentages)
    print("MEAN: ")
    getRemaining(mean_counts, mean_percentages)


def getRemaining(value_counts, value_percentages):
    print(value_counts, value_percentages)
    count = 0
    for i,j in all_data: 
        if i >= value_counts:
            if j >= value_percentages:
                count = count + 1
    print("{}{}".format("Remaining: ", count))
    

    """ remainingList = [i for i in all_data[0][i] if i >= value_counts] 
    remainingList = [j for j in all_data[1][j] if j >= value_percentages]
    print("{}{}".format("Remaining: ", len(remainingList)))
 """


getMean()
getMedian()
