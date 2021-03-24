import json
import codecs
from analysis.clean_data import clean_for_filtering

# Preprocessing wordlist

# Paths for data directories and files
PREPROCESSED_WORDLIST = 'preprocessed_wordlist.json'
WORDLIST = '../../assets/wordlist.json'

wordlist = json.load(codecs.open(WORDLIST, 'r', 'utf-8-sig'))

# Clean wordlist for filtering
preprocessed_wordlist = [clean_for_filtering(word)[0] for word in wordlist]

# Writing the preprocessed wordlist to .json file
with open(PREPROCESSED_WORDLIST, 'w', encoding='utf-8') as f:
    json.dump(preprocessed_wordlist, f, ensure_ascii=False)

