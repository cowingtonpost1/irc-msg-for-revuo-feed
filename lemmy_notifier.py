from notifier import Notifier
import tweepy
from pythorhead import Lemmy
import re

class LemmyNotifier(Notifier):
    
    def __init__(self, instance, username, password, communities, format):
        self.instance = instance
        self.username = username
        self.password = password
        self.communities = communities
        self.lemmy = None
        self.format = format
        self.ready = False
        
    def is_ready(self): 
        return self.ready

    def run(self):
        self.lemmy = Lemmy(self.instance, request_timeout=5)
        self.lemmy.log_in(self.username, self.password)
        self.ready = True

    def format_message(self, title, link):
        issue_num = re.match(r"Issue (\d+): .*", title).group(1)
        return {"name":f"Revuo Monero Issue {issue_num} - Weekly newsletter", "url": link, "body": link}
        

    def send_message(self, message):
        try:
            for community in self.communities:
                self.lemmy.post.create(community, **message)
        except Exception as e:
            print(f"Lemmy: error sending post: {e}")
