#!/usr/bin/env python
import random
import json
from twython import Twython

# Credentials setup
# Loads in 'creds.json' values as a dictionary
with open('creds.json') as f:
    credentials = json.loads(f.read())

# Sets config values from the config file
CONSUMER_KEY = credentials["consumer_key"]
CONSUMER_SECRET = credentials["consumer_secret"]
ACCESS_TOKEN_KEY = credentials["access_token_key"]
ACCESS_TOKEN_SECRET = credentials["access_token_secret"]

# Create the Twython Twitter client using our credentials
twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                  ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

# Sample random tweets
potential_tweets = [
    'I\'m having a good time in COMP4968 lab 05!',
    'COMP4968 lab 05 is fun!',
    'AWS Lambda Function is awesome!'
]

def send_tweet(tweet_text):
    """Sends a tweet to Twitter"""
    twitter.update_status(status = tweet_text)

def handler(event,context):
    """Sends random tweet from list of potential tweets"""
    send_tweet(random.choice(potential_tweets))



