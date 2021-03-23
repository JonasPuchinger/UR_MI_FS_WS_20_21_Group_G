# Dataset Description

- `describe_dataset.py`: script to collect tweet- and account-level Twitter statistics for all politicians in our dataset. A explained list of all collected statisitcs can be found in the file.

    Output file: `politicians_tweets_stats.csv`

- `tweets_stats_visualized.ipynb`: notebook that visualizes the statistics collected in `politicians_tweets_stats.csv` on a party-level.

- `tweet_counts.ipynb`: notebook that calculates some descriptive quantitaive statistics of the dataset (number of total tweets, number of unique tweets, number of tweets per party, ...). Different visualizations of the number of politicians per party by number of tweets are also plotted here. These statistics are mainly for section 3.1 (Dataset Description) of our paper.

- `get_popular_tweets`: script that collects the most viral (likes + retweets) COVID- and non-COVID-tweets per party. These tweets are the used for qualitative content and sentiment annotation.

    Output files:

    - `most_popular_covid_tweets.json`
    - `most_popular_non_covid_tweets.json`

- `create_annotation_files.py`: script that formats the collected viral COVID- and non-COVID-tweets and outputs them for the actual annotation.

    Output files:
    
    - `covid_tweets_annotation.csv`
    - `non_covid_tweets_annotation.csv`