#!/usr/bin/env python
import boto3
import base64
import random
import json
import requests
from twython import Twython
from urllib2 import urlopen
from bs4 import BeautifulSoup

# Credentials setup
# Loads in 'creds.json' values as a dictionary
with open('creds.json') as f:
    credentials = json.loads(f.read())

def decrypt(ciphertext):
    """Decrypt ciphertext with KMS""" 
    kms = boto3.client('kms')
    print 'Decrypting ciphertext with KMS'
    plaintext = kms.decrypt(CiphertextBlob = base64.b64decode(ciphertext))['Plaintext']
    return plaintext

# Decrypts API keys and sets config values from the config file
# Make sure this is loading KMS encrypted values in creds.json 
# or else you may see a TypeError: Incorrect padding error
CONSUMER_KEY = decrypt(credentials["consumer_key"])
CONSUMER_SECRET = decrypt(credentials["consumer_secret"])
ACCESS_TOKEN_KEY = decrypt(credentials["access_token_key"])
ACCESS_TOKEN_SECRET = decrypt(credentials["access_token_secret"])

# Create the Twython Twitter client using our credentials
twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                  ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

# Sample random tweets
potential_tweets = [
    'I\'m having a good time in COMP4968 lab 05!',
    'COMP4968 lab 05 is fun!',
    'AWS Lambda Function is awesome!'
]

def grab_quote():
    url = 'https://www.brainyquote.com/quotes_of_the_day.html'
    headers = {'User-Agent':'Mozilla/5.0'}
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    for element in soup.find_all("div", {"class": "mbl_qtbox qotd-qbox boxy bqQt"}):
        quote_node = element.find("a", {"class": "b-qt"})
        quote_text = quote_node.text
        quote_link = quote_node.href
        author_node = element.find("a", {"class": "bq-aut"})
        quote_author = author_node.text
        send_tweet('"'+quote_text+'" - '+quote_author+' \n source: brainyquote')
        break


def send_tweet(tweet_text):
    """Sends a tweet to Twitter"""
    twitter.update_status(status = tweet_text)

# entry point
def handler(event,context):
    """Sends random tweet from list of potential tweets"""
    """send_tweet(random.choice(potential_tweets))"""
    grab_quote()

