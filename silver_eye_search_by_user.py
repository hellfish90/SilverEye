# -*- coding: utf-8 -*-
__author__ = 'Marc'

import tweepy
import json
import logging
import datetime

logging.basicConfig(
    filename='search_by_user.log',
    level=logging.WARNING,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%d-%m-%y %H:%M')

# Configuration parameters
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""
database_name = ""

if __name__ == '__main__':
    logging.debug('silver_eye_twitter_streaming.py starting ...')
    logging.error(datetime.datetime.now())
    logging.debug("------------------")

    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
        access_token = config['access_token']
        access_token_secret = config['access_token_secret']
        consumer_key = config['consumer_key']
        consumer_secret = config['consumer_secret']
        database_name = config['database_name']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    stuff = api.user_timeline(screen_name = 'ferrangadea', count = 100, include_rts = True)

    for status in stuff:
        print status.user.screen_name, status.text

