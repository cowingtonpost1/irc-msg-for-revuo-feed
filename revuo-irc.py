import feedparser
import os
import time
import json
import pickle
import tweepy
import requests

webhook_endpoint = os.environ['WMB_LIBERACHAT_URL']
webhook_password = os.environ['WMB_LIBERACHAT_PASSWORD']

rizon_webhook_endpoint = os.environ['WMB_RIZON_URL']
rizon_webhook_password = os.environ['WMB_RIZON_PASSWORD']

api_key = os.environ['API_KEY']
api_secret_key = os.environ['API_SECRET_KEY']

#loc_long = os.environ.get('LOC_LON')
#loc_lat = os.environ.get('LOC_LAT')

api_bearer = os.environ['API_BEARER']

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

reload_minutes = int(os.environ.get('RELOAD_MINUTES', 0))

url_preview = 1

def send_msg(msg,webhook_password,webhook_endpoint):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = {
        'message': msg,
        'password': webhook_password,
        'broadcast': True
    }
    r = requests.post(webhook_endpoint, data=json.dumps(data), headers=headers)

def send_tweet(tweet):
	global consumer_key, consumer_secret, access_token, access_token_secret
	#global loc_long, loc_lat

	client = tweepy.Client(consumer_key=consumer_key,
	                   consumer_secret=consumer_secret,
	                   access_token=access_token,
	                   access_token_secret=access_token_secret
	)
	response = client.create_tweet(text=tweet)
	print(response)
	'''
	global api_key, api_secret_key, access_token, access_token_secret
	global loc_lat, loc_long, url_preview
	global bearer_token
	auth = tweepy.OAuthHandler(api_key, api_secret_key)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	#return
	if url_preview == 0:
	    api.update_status(status = tweet, card_uri='tombstone://card', long=loc_long, lat=loc_lat, display_coordinates=1 )
	else:
	    api.update_status(status = tweet, lat=loc_lat, long=loc_long, display_coordinates=1 )
	'''
def main():
    global webhook_password, webhook_endpoint, rizon_webhook_endpoint, rizon_webhook_password
    if os.path.isfile("filename.pickle"):
        with open('filename.pickle', 'rb') as handle:
            unserialized_data = pickle.load(handle)
        last_msg = unserialized_data["msg"]
    else:
        last_msg = "~"
    chanlist = [b"#monero-community", b"#monero", b"#monero-markets", b"#monero-pools"]
    NewsFeed = feedparser.parse("https://revuo-xmr.com/atom.xml")
    entry = NewsFeed.entries[0]

    msg = f"Revuo Monero {entry['title']}. {entry['link']}"
    tweet = f"We're pleased to share Revuo #Monero {entry['title']} is now available! {entry['link']}"
    print(msg)
    if last_msg != msg:
        data = {"msg": msg}
        # Store data (serialize)
        with open('filename.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # Load data (deserialize)
        print("New")
        #msg = bytes(msg, 'ascii')
        #send_msg(chanlist, msg)
        send_tweet(tweet)
        send_msg(msg,webhook_password,webhook_endpoint)
        send_msg(msg,rizon_webhook_password,rizon_webhook_endpoint)

def daemonize():
    '''Makes the script run in a loop, starting every reload_minutes minutes'''
    while True:
        main()
        time.sleep(reload_minutes * 60)

if __name__ == "__main__":
    if reload_minutes > 0:
        daemonize()
    else:
        main()
