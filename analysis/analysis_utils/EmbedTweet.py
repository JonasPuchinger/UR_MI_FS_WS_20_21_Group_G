import requests
from IPython.core.display import HTML, display

class EmbedTweet(object):
    
    def __init__(self, s, embed_str=False):
        if not embed_str:
            # Use Twitter's oEmbed API
            # https://dev.twitter.com/web/embedded-tweets
            api = f'https://publish.twitter.com/oembed?url={s}'
            response = requests.get(api)
            self.text = response.json()['html']
        else:
            self.text = s

    def _repr_html_(self):
        return self.text

    def display_tweet(self):
        display(HTML(self.text))