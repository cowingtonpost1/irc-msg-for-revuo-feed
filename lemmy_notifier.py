from notifier import Notifier
import tweepy
from pythorhead import Lemmy

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
        

    def send_message(self, message):
        try:
            for community in self.communities:
                self.lemmy.post.create(community, message)
        except Exception as e:
            print(f"Lemmy: error sending post: {e}")
