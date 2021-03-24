# Formated Data

- `/tweet`: directory that contains all scraped tweets. For each politician in our dataset, a file with all the tweets scraped for the respective politician is present in this directory.

- `/user`: directory that contains all scraped account data. For each politician in our dataset, a file with all the accounts found in the scraped tweets for the respective politician is present in this directory.

- `/relationship_politicians`: directory that contains all follower relationships of all politicians in our dataset to all other accounts in our dataset. For each politician in our dataset, a file with the follower relationships to every other account in our dataset is present in this directory.

- `/relationship_politicians`: directory that contains all follower relationships of all additional accounts (news portals + virologists) in our dataset to all other accounts in our dataset. For each additional account in our dataset, a file with the follower relationships to every other account in our dataset is present in this directory. 

    Follower relationships in these files are formated as follows: 

    `{"target_screen_name": <Twitter Handle>, "target_id": <Twitter ID>, "value": <either 1 or 2 or 0>}`

    - `"value": 0`: The source account does not follow the target account
    - `"value": 1`: The source account follows the target account
    - `"value": 2`: The source account and the target account both follow each other