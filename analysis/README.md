# Analysis

- `/formated_data`: contains the combined and formated data from all scraping procedures.

- `/filtered_data`: contains filterd data (tweets), sorted by their relation (or lack thereof) to COVID-19.

- `/analysis_utils`: contains some helper classes and functions used in multiple analyses.

- `/dataset_description`: contains scripts and files that calculate and collect descriptive statistics on our dataset (total number of tweets, tweets by language, Twitter statistics by party, ...). Also contains the files for the qualitative annotation.

- `/preprocessing_wordlist`: contains scripts and files that deal with processing the list of keywords used to detect COVID-tweets.

- `/covid_tweets_analysis`: contains scripts and files to detect, analyse and visualize COVID-tweets.

- `/tweet_entities_analysis`: contains scripts and files that deal with filtering, analysing and visualizing tweet entities (hashtags, mentions, links and domains).

- `/network_analysis`: contains scripts and files to generate network graphs from our collected data.

- `clean_data.py`: script with helper functions to preprocess and clean textual tweet data.

- `pluralize_textblob.py`: script that uses the textblob package to pluralize German words.

- `covid_data_visualized.ipynb`: notebook that contains different visualizatins and dashboard presenting COVID_19 case numbers and various Twitter statsitics in comparison.