# -*- coding: utf-8 -*-

import tweepy
from pymongo import MongoClient
import json
import logging
import datetime

__author__ = 'Marc Sole Farre'

"""
For do this program I use the next code of Jordi Vilaplana.
https://github.com/eMOVIX/emovix-twitter-streaming/blob/master/emovix_twitter_streaming.py

Thanks for the help.

"""
'''
logging.basicConfig(
    filename='political.log',
    level=logging.WARNING,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%d-%m-%y %H:%M')
'''


class ExtractorTwitterListener(tweepy.StreamListener):
    def __init__(self, api, mongoClient, silvereye_core):
        super(tweepy.StreamListener, self).__init__()
        self.api = api
        self.db = mongoClient.SilverEye
        self.last_time = None
        self.silverEye = silvereye_core
        self.tweets_counter = 0

    def on_data(self, data):
        tweet = json.loads(data)

        # This code ignores limit notices
        # https://dev.twitter.com/streaming/overview/messages-types#limit_notices
        if tweet.get('limit'):
            logging.debug('Limit notice received: ' + str(tweet['limit']['track']))
            logging.debug(datetime.datetime.now())
            self.db.twitterLimitNotice.insert(tweet)
            return True

        user = tweet['user']

        self.tweets_counter += 1

        if self.last_time is None:
            self.last_time = datetime.datetime.now().hour

        if self.last_time != datetime.datetime.now().hour:
            self.last_time = datetime.datetime.now().hour
            logging.debug('Number Tweets: ' + str(self.tweets_counter))
            self.db.twitterCounter.insert({"Extractor": "Streaming",
                                           "datetime": datetime.datetime.now(),
                                           "num": self.tweets_counter})
            self.tweets_counter = 0

        print tweet['text']

        try:
            self.db.twitterPolitical.update(tweet, tweet, upsert=True)
            self.db.twitterUser.update({"screen_name": tweet['user']['screen_name']}, user, upsert=True)
            self.silverEye.analyze_and_save_user_tweet(tweet, self.db.twitterPoliticalAnalyzed, self.db.twitterUser)

        except Exception as exception:
            # Oh well, reconnect and keep trucking
            logging.error("On save to db:")
            logging.error(datetime.datetime.now())
            logging.error(exception.__class__)
            logging.error(exception.message)
            logging.error("------------------")
            return True

        return True

    def on_error(self, status):
        if status == 420:
            logging.error('RATE LIMITED')
            logging.error(datetime.datetime.now())
            logging.error("------------------")
        else:
            logging.error(status)
            logging.error(datetime.datetime.now())
            logging.error("------------------")
        return True

    def on_timeout(self):
        logging.error('On TimeOut')
        logging.error(datetime.datetime.now())
        logging.error("------------------")

'''

if __name__ == '__main__':
    logging.debug('silver_eye_twitter_streaming.py starting ...')
    logging.debug("------------------")

    # Load configuration
    with open('Config.json', 'r') as f:
        Config = json.load(f)
        access_token = Config['access_token']
        access_token_secret = Config['access_token_secret']
        consumer_key = Config['consumer_key']
        consumer_secret = Config['consumer_secret']
        database_name = Config['database_name']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    mongoClient = MongoClient('0.0.0.0', 27017)

    while True:
        try:
            logging.debug('Connecting to Twitter stream ...')
            stream = tweepy.streaming.Stream(auth, ExtractorTwitterListener(api, mongoClient))
            stream.filter(track=keywords)

        except Exception as e:
            logging.error(e.__class__)
            logging.error(e)
            logging.error("------------------")
            continue

        except KeyboardInterrupt:
            stream.disconnect()
            mongoClient.close()
            break
'''

'''
    stream = tweepy.streaming.Stream(auth, CustomStreamListener(api))
    stream.filter(track=keywords, async=True)

'''
