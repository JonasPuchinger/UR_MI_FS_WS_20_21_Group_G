import csv
from analysis.clean_data import clean_for_n_gram_analysis

# Paths for data directories and files
RESULTS_FILE = 'clean_tweets_n-gram.csv'
dict_covid_tweets = []

# Clean all COVID-tweets for n-gram analysis
# Loop over COVID-tweets by politicians
# For every tweet, a object with the following values is generated:
# party: Political party the politician belongs to
# original tweet: Unique COVID-tweet of the politician
# tweet: cleaned tweet for n-gram analysis
with open('../covid_tweets_analysis/covid_tweets_by_politician.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        p_cleaned_covid_tweets = {
            'party': row[1],
            'original tweet': row[6],
            'tweet': clean_for_n_gram_analysis(row[6]),
        }
        dict_covid_tweets.append(p_cleaned_covid_tweets)

    # Saving the collected data in a .csv file
    keys_results = dict_covid_tweets[0].keys()
    with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as outfile:
        dict_writer = csv.DictWriter(outfile, keys_results)
        dict_writer.writeheader()
        dict_writer.writerows(dict_covid_tweets)
