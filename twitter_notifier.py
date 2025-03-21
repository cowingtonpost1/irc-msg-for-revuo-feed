from notifier import Notifier
import tweepy

class TwitterNotifier(Notifier):
    
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, format):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.format = format
        
    def is_ready(self): 
        return True

    def send_message(self, message):
        """Posts a tweet."""
        try:
            client = tweepy.Client(consumer_key=self.consumer_key,
                               consumer_secret=self.consumer_secret,
                               access_token=self.access_token,
                               access_token_secret=self.access_token_secret
            )
            response = client.create_tweet(text=message)
            print("Twitter: " + str(response))
        except Exception as e:
            print(f"Twitter: error sending tweet: {e}")
