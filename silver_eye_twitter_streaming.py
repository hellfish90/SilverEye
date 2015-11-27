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
import datetime

logging.basicConfig(
    filename='silver_eye_twitter_streaming.log',
    level=logging.WARNING,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%d-%m-%y %H:%M')

# Configuration parameters
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""
database_name = ""

ignored_languages = ["ja", "in", "tr", "tl", "ar", "ru", "th"]

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
        if tweet.get('limit'):
            logging.debug('Limit notice received: ' + str(tweet['limit']['track']))
            self.db.twitterLimitNotice.insert(tweet)
            return True

        if tweet.get('lang') in ignored_languages:
            return True

        user = tweet['user']

        self.tweets_counter += 1

        if self.last_time == None:
            self.last_time = datetime.datetime.now().hour

        if self.last_time != datetime.datetime.now().hour:
            self.last_time = datetime.datetime.now().hour
            logging.warning('Tweets: ' + str(self.tweets_counter))
            #print self.tweets_counter
            self.tweets_counter = 0

        try:
            self.db.twitterStatus.update(tweet, tweet, upsert=True)
            self.db.twitterUser.update({"screen_name": tweet['user']['screen_name']}, user, upsert=True)
        except Exception as e:
            # Oh well, reconnect and keep trucking
            logging.error("On save to db:")
            logging.error(e.__class__)
            logging.error(e)
            logging.error("------------------")
            return True

        return True

    def on_error(self, status):
        logging.error('CustomStreamListener on_error')
        logging.error(status)
        logging.error("------------------")
        return True

    def on_timeout(self):
        logging.error('CustomStreamListener on_timeout')
        logging.error("------------------")
        return True  # Don't kill the stream


if __name__ == '__main__':
    logging.debug('silver_eye_twitter_streaming.py starting ...')
    logging.debug("------------------")

    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
        access_token = config['access_token']
        access_token_secret = config['access_token_secret']
        consumer_key = config['consumer_key']
        consumer_secret = config['consumer_secret']
        database_name = config['database_name']

    client = MongoClient('mongodb://localhost:27017/')
    db = client[database_name]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    while True:
        try:
            logging.debug('Connecting to Twitter stream ...')
            stream = tweepy.streaming.Stream(auth, CustomStreamListener(api))
            stream.filter(locations = [-12.885216, 34.998484, 3.766846, 43.564009],languages=["es"])
        except Exception as e:
            # Oh well, reconnect and keep trucking
            logging.error(e.__class__)
            logging.error(e)
            logging.error("------------------")
            continue
        except KeyboardInterrupt:
            stream.disconnect()
            break
