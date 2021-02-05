import os
import json
from TwitterFollowChecker import TwitterFollowChecker
import configparser

# Constants
RESULTS_FOLDER_POLITICIANS = '../analysis/formated_data/relationship_politicians/'
RESULTS_FOLDER_ADDITIONAL_ACCOUNTS = '../analysis/formated_data/relationship_additional_accounts/'
ALL_POLITICIANS_FILE = '../assets/all_politicians.json'
MDBS_FILE = '../assets/mdbs_data.json'
ADDITIONAL_POLITICIANS_FILE = '../assets/additional_politicians.json'
NEWS_PORTALS_FILE = '../assets/news_portals.json'
VIROLOGISTS_FILE = '../assets/virologists.json'
MDB_RELATIONSHIPS_FILE = '../assets/mdbs_relations.json'

# Create folder if it does not already exist
if not os.path.exists(RESULTS_FOLDER_POLITICIANS):
    os.makedirs(RESULTS_FOLDER_POLITICIANS)

# Open files
with open(ALL_POLITICIANS_FILE, 'r', encoding='utf-8') as infile_all_politicians:
    all_politicians = json.load(infile_all_politicians)
with open(MDBS_FILE, 'r', encoding='utf-8') as infile_mdbs:
    mdbs = json.load(infile_mdbs)
with open(ADDITIONAL_POLITICIANS_FILE, 'r', encoding='utf-8') as infile_additional_politicians:
    additional_politicians = json.load(infile_additional_politicians)
with open(NEWS_PORTALS_FILE, 'r', encoding='utf-8') as infile_news_portals:
    news_portals = json.load(infile_news_portals)
with open(VIROLOGISTS_FILE, 'r', encoding='utf-8') as infile_virologists:
    virologists = json.load(infile_virologists)
additional_accounts = news_portals + virologists
with open(MDB_RELATIONSHIPS_FILE, 'r', encoding='utf-8') as infile_mdb_relations:
    mdb_rels = json.load(infile_mdb_relations)

# Load config for TwitterFollowChecker
config = configparser.ConfigParser()
config.read('twitter_account_credentials.cfg')
twitter_username = config['twitter_account_credentials']['twitter_username']
twitter_handle = config['twitter_account_credentials']['twitter_handle']
twitter_pw = config['twitter_account_credentials']['twitter_pw']

# Get and save relations for all politicians
for p in [pol for pol in all_politicians if f'{pol["screen_name"]}.json' not in os.listdir(RESULTS_FOLDER_POLITICIANS) and pol["screen_name"] not in ['Wellenreuther', 'ChristophFDP']]:
    p_screen_name = p['screen_name']
    p_relationships = []
    # Save mdb relations
    for mdb in [m for m in mdbs if m['screen_name'] != p_screen_name]:
        # filter for relationship with current mdb
        curr_mdb_rel = next((m for m in mdb_rels[p_screen_name] if m['source'] == mdb['id'] or m['target'] == mdb['id']), None)
        # mdb and p have some form of relation
        if curr_mdb_rel:
            if curr_mdb_rel['value'] == 1:
                # mdb follows p
                if mdb['id'] == curr_mdb_rel['source']:
                    p_relationships.append({
                        'target_screen_name': mdb['screen_name'],
                        'target_id': mdb['id'],
                        'value': 0
                    })
                # p follows mdb
                elif mdb['id'] == curr_mdb_rel['target']:
                    p_relationships.append({
                        'target_screen_name': mdb['screen_name'],
                        'target_id': mdb['id'],
                        'value': 1
                    })
            # mdb and p follow each other
            elif curr_mdb_rel['value'] == 2:
                p_relationships.append({
                    'target_screen_name': mdb['screen_name'],
                    'target_id': mdb['id'],
                    'value': 2
                })
        # mdb and p have no relation
        else:
            p_relationships.append({
                'target_screen_name': mdb['screen_name'],
                'target_id': mdb['id'],
                'value': 0
            })

    # Get and save relations with additional politicians through TwitterFollowChecker
    # Create TwitterFollowChecker
    follow_checker = TwitterFollowChecker(twitter_username=twitter_username, twitter_handle=twitter_handle, twitter_pw=twitter_pw)
    for ap in [a_pol for a_pol in additional_politicians if a_pol['screen_name'] != p_screen_name]:
        print(p_screen_name, ap['screen_name'])
        rel_ap = follow_checker.get_follow(p_screen_name, ap['screen_name'])
        if rel_ap[0] == True:
            if rel_ap[0] == True:
                p_relationships.append({
                    'target_screen_name': ap['screen_name'],
                    'target_id': ap['id'],
                    'value': 2
                })
            elif rel_ap[0] == False:
                p_relationships.append({
                    'target_screen_name': ap['screen_name'],
                    'target_id': ap['id'],
                    'value': 1
                })
        elif rel_ap[0] == False:
            p_relationships.append({
                    'target_screen_name': ap['screen_name'],
                    'target_id': ap['id'],
                    'value': 0
                })
    
    # Get and save relations with additional accounts through TwitterFollowChecker
    # Create TwitterFollowChecker
    follow_checker = TwitterFollowChecker(twitter_username=twitter_username, twitter_handle=twitter_handle, twitter_pw=twitter_pw)
    for aa in additional_accounts:
        print(p_screen_name, aa['screen_name'])
        rel_aa = follow_checker.get_follow(p_screen_name, aa['screen_name'])
        if rel_aa[0] == True:
            if rel_aa[0] == True:
                p_relationships.append({
                    'target_screen_name': aa['screen_name'],
                    'target_id': aa['id'],
                    'value': 2
                })
            elif rel_aa[0] == False:
                p_relationships.append({
                    'target_screen_name': aa['screen_name'],
                    'target_id': aa['id'],
                    'value': 1
                })
        elif rel_aa[0] == False:
            p_relationships.append({
                    'target_screen_name': aa['screen_name'],
                    'target_id': aa['id'],
                    'value': 0
                })

    with open(os.path.join(RESULTS_FOLDER_POLITICIANS, f'{p_screen_name}.json'), 'w+', encoding='utf-8') as outfile:
        json.dump(p_relationships, outfile, ensure_ascii=False)


# Create folder if it does not already exist
if not os.path.exists(RESULTS_FOLDER_ADDITIONAL_ACCOUNTS):
    os.makedirs(RESULTS_FOLDER_ADDITIONAL_ACCOUNTS)

# Get and save relations for all additional accounts
for add_acc in [acc for acc in additional_accounts if f'{acc["screen_name"]}.json' not in os.listdir(RESULTS_FOLDER_ADDITIONAL_ACCOUNTS)]:
    aa_screen_name = add_acc['screen_name']
    aa_relationships = []
    # Create TwitterFollowChecker
    follow_checker = TwitterFollowChecker(twitter_username=twitter_username, twitter_handle=twitter_handle, twitter_pw=twitter_pw)
    for pol in all_politicians:
        print(aa_screen_name, pol['screen_name'])
        cur_rel = follow_checker.get_follow(aa_screen_name, pol['screen_name'])
        if cur_rel[0] == True:
            if cur_rel[0] == True:
                aa_relationships.append({
                    'target_screen_name': pol['screen_name'],
                    'target_id': pol['id'],
                    'value': 2
                })
            elif cur_rel[0] == False:
                aa_relationships.append({
                    'target_screen_name': pol['screen_name'],
                    'target_id': pol['id'],
                    'value': 1
                })
        elif cur_rel[0] == False:
            aa_relationships.append({
                    'target_screen_name': pol['screen_name'],
                    'target_id': pol['id'],
                    'value': 0
                })

    with open(os.path.join(RESULTS_FOLDER_ADDITIONAL_ACCOUNTS, f'{aa_screen_name}.json'), 'w+', encoding='utf-8') as outfile:
        json.dump(aa_relationships, outfile, ensure_ascii=False)
