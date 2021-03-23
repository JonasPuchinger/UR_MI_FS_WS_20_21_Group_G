from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class TwitterFollowChecker:

    def __init__(self, twitter_username, twitter_handle, twitter_pw):
        '''
        Initialize the class with the passed credentials and start a headless browser.
        Note: geckodriver.exe needs to be on the PATH or in this directory for this script to work.
        '''
        self.start_url = 'https://www.unfollowspy.com/'
        self.twitter_username = twitter_username
        self.twitter_handle = twitter_handle
        self.twitter_pw = twitter_pw
        options = FirefoxOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)
        self.login()


    def login(self):
        '''
        Logs into the webapp with the provided credentials.
        If Twitter intercepts the login, authenticates itself to the Twitter API.
        '''
        self.driver.get(self.start_url)
        login_btn = self.driver.find_element_by_class_name('twitbutton')
        login_btn.click()

        wait = WebDriverWait(self.driver, 20)
        wait.until(lambda driver: driver.current_url != self.start_url)

        redirect_url = self.driver.current_url
        username_input = self.driver.find_element_by_id('username_or_email')
        pw_input = self.driver.find_element_by_id('password')
        username_input.send_keys(self.twitter_username)
        pw_input.send_keys(self.twitter_pw)
        submit_btn = self.driver.find_element_by_id('allow')
        submit_btn.click()

        wait.until(lambda driver: driver.current_url != redirect_url)
        if self.driver.current_url.startswith('https://twitter.com'):
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR , 'input[name="session[username_or_email]"]'))) 
            security_username_input = self.driver.find_element_by_css_selector('input[name="session[username_or_email]"]')
            security_username_input.send_keys(self.twitter_handle)
            security_pw_input = self.driver.find_element_by_css_selector('input[name="session[password]"]')
            security_pw_input.send_keys(self.twitter_pw)
            security_submit_btn = self.driver.find_element_by_css_selector('div[data-testid="LoginForm_Login_Button"]')
            security_submit_btn.click()
        
        wait.until(lambda driver: driver.current_url.startswith(self.start_url))
        self.driver.get('https://www.unfollowspy.com/isfriends.php')


    def get_follow(self, user1, user2):
        '''
        Uses the webapp to request the follower relationship between two accounts and returns them.
        '''
        user1_input = self.driver.find_element_by_id('userone')
        user2_input = self.driver.find_element_by_id('usertwo')
        user1_input.send_keys(Keys.CONTROL + 'a')
        user1_input.send_keys(f'@{user1}')
        user2_input.send_keys(Keys.CONTROL + 'a')
        user2_input.send_keys(f'@{user2}')
        check_btn = self.driver.find_element_by_id('submit')
        check_btn.click()

        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR , '#Result fieldset:nth-of-type(1) .part'), f'Part 1: Does @{user2} follow @{user1} ?'))

        user1_follows_user2 = False
        user2_follows_user1 = False

        try:
            self.driver.find_element_by_css_selector('#Result fieldset:nth-of-type(1) .doesfollow')
            user1_follows_user2 = True
        except NoSuchElementException:
            self.driver.find_element_by_css_selector('#Result fieldset:nth-of-type(1) .doesntfollow')
            user1_follows_user2 = False
        try:
            self.driver.find_element_by_css_selector('#Result fieldset:nth-of-type(2) .doesfollow')
            user2_follows_user1 = True
        except NoSuchElementException:
            self.driver.find_element_by_css_selector('#Result fieldset:nth-of-type(2) .doesntfollow')
            user2_follows_user1 = False

        return user1_follows_user2, user2_follows_user1
