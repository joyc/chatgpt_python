import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

def post(tweet):
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_secret
    )
    response = client.create_tweet(
        text=tweet
    )
    print(f"https://twitter.com/user/status/{response.data['id']}")

if __name__ == "__main__":
    post("test")

