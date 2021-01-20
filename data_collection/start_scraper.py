import sys
sys.path.append('../TweetScraper')
sys.path.append('../analysis')
import configparser
import datetime
import json
from timeit import default_timer as timer
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor
from generate_requests import twitter_requests
from TweetScraper_API import start_tweet_scraper
from combine_files import combine_files

# Read in config file
config = configparser.ConfigParser()
config.read('config.cfg')

# Set up script according to config
START_DATE = datetime.datetime.strptime(config['scraping_settings']['start_date'], '%Y-%m-%d').date()
END_DATE = datetime.datetime.strptime(config['scraping_settings']['end_date'], '%Y-%m-%d').date()
DAYS_STEP = int(config['scraping_settings']['days_step'])

with open(config['scraping_settings']['politicians_list'], 'r') as politicians_file:
    politcians_list = json.loads(politicians_file.read())

POLITICIANS_SCREEN_NAMES = [p['screen_name'] for p in politcians_list]

# Generate requests to the Twitter Advanced Search
politicians_requests = twitter_requests(screen_names=POLITICIANS_SCREEN_NAMES, start=START_DATE, end=END_DATE, step=DAYS_STEP)

start_tweet_scraper(requests=politicians_requests)

# Combine tweets
combine_files(source_folder='../Data/tweet/', results_folder='../analysis/formated_data_2/tweet/')

# Combine users
combine_files(source_folder='../Data/user/', results_folder='../analysis/formated_data_2/user/')
