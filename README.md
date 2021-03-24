# UR_MI_FS_WS_20_21_Group_G

## Get started

To install the required packages and initialize the project, run

`pip install . && pip install -r requirements.txt`

## Structure

Nearly all folder and subfolders contain their own README, which explains the contents of the respective folders.

- `/data_collection`: contains all scripts and files that deal with fetching the data we need for this project.

- `/TweetScraper`: submodule that contains Scrapy CrawlerSpiders to retrieve Twitter data without the need to access the highly rate-limited Twitter API. Used by `/data_collection`.

- `/assets`: contains list and files, which contain data we do not need to scrape from Twitter, but nonetheless need for our project.

- `/analysis`: contains all scripts and files that deal with processing, analysing and visualizing our collected data.