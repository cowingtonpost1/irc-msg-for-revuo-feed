from notifier import Notifier
import tweepy
import praw
import re

class RedditNotifier(Notifier):
    
    def __init__(self, client_id, client_secret, user_agent, subreddits, username, password, format):
        self.client_id=client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.subreddits = subreddits
        self.username = username
        self.password = password
        self.format = format
        self.ready = False
        
    def is_ready(self): 
        return self.ready

    def run(self):
        self.ready = True


    def format_message(self, title, link):
        issue_num = re.match(r"Issue (\d+): .*", title).group(1)
        return {"title":f"Revuo Monero Issue {issue_num} - Weekly newsletter", "url": link}
        

    def send_message(self, message):
        try:
            reddit = praw.Reddit(client_id=self.client_id,
                     client_secret=self.client_secret,
                     username=self.username,
                     password=self.password,
                     user_agent=self.user_agent)

            for r in self.subreddits:

                subreddit = reddit.subreddit(r)

                submission = subreddit.submit(**message)
        except Exception as e:
            print(f"Reddit: error sending post: {e}")
