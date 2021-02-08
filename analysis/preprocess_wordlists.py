import json
import codecs
import preprocessor as pre
import re

# Preprocessing wordlists

WORDLIST_FUZZY = 'wordlist_fuzzy.json'
WORDLIST_MATCHING = 'wordlist_matching.json'
WORDLIST = '../assets/wordlist.json'

wordlist = json.load(codecs.open(WORDLIST, 'r', 'utf-8-sig'))
pre.set_options(pre.OPT.NUMBER)


def preprocess_wordlist(wordlist):
    preprocessed_words = []
    for word in wordlist:
        lower_word = word.lower()
        # Cleaning (Numbers)
        word = pre.clean(lower_word)
        # Removal of digits
        word = re.sub('\d+', '', word)
        # Remove Punctuations
        word = re.sub(r'[^\w\s]', '', word)
        preprocessed_words.append(word)
    # Remove duplicates
    preprocessed_wordlist = set(preprocessed_words)
    return list(preprocessed_wordlist)


remove_words = ["R0", "#n95"]
updated_wordlist = [word for word in wordlist if word not in remove_words]

wordlist_matching = preprocess_wordlist(updated_wordlist)
remove_words_fuz = ["pcr", "rzahl", "rwert", "rwerte"]
wordlist_fuzzy = [word for word in wordlist_matching if word not in remove_words_fuz]

with open(WORDLIST_MATCHING, 'w', encoding='utf-8') as f:
    json.dump(wordlist_matching, f, ensure_ascii=False)

with open(WORDLIST_FUZZY, 'w', encoding='utf-8') as f:
    json.dump(wordlist_fuzzy, f, ensure_ascii=False)
