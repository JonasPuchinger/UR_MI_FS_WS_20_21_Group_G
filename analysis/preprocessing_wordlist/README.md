# Preprocessing wordlist

- `preprocessing_wordlist.py`: Script that deals with processing the list of keywords used to detect COVID tweets.
  
    Output file: `preprocessed_wordlist.json`

- `uncertain_words.json`: A .json file containing the words that are not clearly covid-related. At least two different words from this list must appear in a tweet for it to be considered a COVID-tweet.
