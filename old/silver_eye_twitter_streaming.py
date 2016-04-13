# !/usr/bin/python

# -*- coding: utf-8 -*-

__author__ = 'Marc Sole Farre'

"""
For do this program I use the next code of Jordi Vilaplana.
https://github.com/eMOVIX/emovix-twitter-streaming/blob/master/emovix_twitter_streaming.py

Thanks for the help.

"""

import tweepy
import pymongo
from pymongo import MongoClient
import json
import logging
import json
import logging
import datetime



client = None
db = None


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        self.db = pymongo.MongoClient().SilverEye
        self.tweets_counter = 0
        self.last_time = None

    def on_data(self, data):
        tweet = json.loads(data)

        # This code ignores limit notices
        # https://dev.twitter.com/streaming/overview/messages-types#limit_notices


        try:
            print tweet['text']

        except Exception as e:

            return True

        return True

    def on_error(self, status):

        return True

    def on_timeout(self):

        return True  # Don't kill the stream


if __name__ == '__main__':


    # Load configuration
    with open('Config.json', 'r') as f:
        config = json.load(f)
        access_token = config['access_token']
        access_token_secret = config['access_token_secret']
        consumer_key = config['consumer_key']
        consumer_secret = config['consumer_secret']
        database_name = config['database_name']



    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    while True:
        try:
            logging.debug('Connecting to Twitter stream ...')
            stream = tweepy.streaming.Stream(auth, CustomStreamListener(api))
            stream.filter(track= [u'ramon', u'Joan'])
        except Exception as e:
            # Oh well, reconnect and keep trucking
            logging.error(e.__class__)
            logging.error(e)
            logging.error("------------------")
            continue
        except KeyboardInterrupt:
            stream.disconnect()
            break
