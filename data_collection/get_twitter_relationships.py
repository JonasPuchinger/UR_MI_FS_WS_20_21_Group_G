import os
import json
from TwitterFollowChecker import TwitterFollowChecker
import configparser

# Constants
RESULTS_FOLDER = '../analysis/formated_data/relationship/'
ALL_POLITICIANS_FILE = '../assets/all_politicians.json'
MDBS_FILE = '../assets/mdbs_data.json'
ADDITIONAL_POLITICIANS_FILE = '../assets/additional_politicians.json'
ADDITIONAL_ACCOUNTS_FILE = ''
MDB_RELATIONSHIPS_FILE = 'mdbs_relations.json'

# Create folder if it does not already exist
if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

# Open files
with open(ALL_POLITICIANS_FILE, 'r', encoding='utf-8') as infile_all_politicians:
    all_politicians = json.load(infile_all_politicians)
with open(MDBS_FILE, 'r', encoding='utf-8') as infile_mdbs:
    mdbs = json.load(infile_mdbs)
with open(ADDITIONAL_POLITICIANS_FILE, 'r', encoding='utf-8') as infile_additional_politicians:
    additional_politicians = json.load(infile_additional_politicians)
with open(ADDITIONAL_ACCOUNTS_FILE, 'r', encoding='utf-8') as infile_additional_accounts:
    additional_accounts = json.load(infile_additional_accounts)
with open(MDB_RELATIONSHIPS_FILE, 'r', encoding='utf-8') as infile_mdb_relations:
    mdb_rels = json.load(infile_mdb_relations)

# Load config for TwitterFollowChecker
config = configparser.ConfigParser()
config.read('twitter_account_credentials.cfg')
twitter_username = config['twitter_account_credentials']['twitter_username']
twitter_handle = config['twitter_account_credentials']['twitter_handle']
twitter_pw = config['twitter_account_credentials']['twitter_pw']

# Create TwitterFollowChecker
follow_checker = TwitterFollowChecker(twitter_username=twitter_username, twitter_handle=twitter_handle, twitter_pw=twitter_pw)

# Get and save relations for all politicians
for p in all_politicians:
    p_screen_name = p['screen_name']
    p_relationships = []
    # Save mdb relations
    for mdb in [m for m in mdbs if m['screen_name'] != p_screen_name]:
        # filter for relationship with current mdb
        curr_mdb_rel = next([m for m in mdb_rels[p_screen_name] if m['source'] == mdb['id'] or m['target'] == mdb['id']], None)
        # mdb and p have some form of relation
        if curr_mdb_rel:
            if curr_mdb_rel['value'] == 1:
                # mdb follows p
                if mdb['id'] == curr_mdb_rel['source']:
                    p_relationships.append({})
                # p follows mdb
                elif mdb['id'] == curr_mdb_rel['target']:
                    p_relationships.append({})
            # mdb and p follow each other
            elif curr_mdb_rel['value'] == 2:
                p_relationships.append({})
        # mdb and p have no relation
        else:
            p_relationships.append({})

    # Get and save relations with additional politicians through TwitterFollowChecker
    for ap in additional_politicians:
        rel_ap = follow_checker.get_follow(p, ap)
        p_relationships.append({})
    
    # Get and save relations with additional accounts through TwitterFollowChecker
    for aa in additional_accounts:
        rel_aa = follow_checker.get_follow(p, aa)
        p_relationships.append({})

    with open(os.path.join(RESULTS_FOLDER, f'{p_screen_name}.json'), 'w+', encoding='utf-8') as outfile:
        json.dump(p_relationships, outfile, ensure_ascii=False)
