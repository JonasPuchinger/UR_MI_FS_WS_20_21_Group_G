import sys
sys.path.append('../TweetScraper')
sys.path.append('../analysis')
import os
import json
from TwitterUserScraper_API import start_twitter_user_scraper
from combine_files import combine_files

# Paths to directories and files
POLITICIANS_LIST = '../assets/all_politicians.json'
USERS_SOURCE_FOLDER = '../analysis/formated_data/user/'

with open(POLITICIANS_LIST, 'r', encoding='utf-8') as infile:
    f_content = json.load(infile)
    politicians_screen_names = [p['screen_name'] for p in f_content]

missing_politcicans = []

# Loop over all politicians to get the ones without user account information
for p in politicians_screen_names:
    f_content = json.load(open(USERS_SOURCE_FOLDER + p + '.json', 'r', encoding='utf-8'))
    if f_content == []:
        missing_politcicans.append(p)

# Fetch the user account information for the missing politicians
start_twitter_user_scraper(requests=missing_politcicans)

RAW_DATA_USERS = '../Data/user/'
USER_SAVE_DIR = '../analysis/formated_data/user/'

# Combine and save the new data
combine_files(source_folder=RAW_DATA_USERS, results_folder=USER_SAVE_DIR)
