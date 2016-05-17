# -*- coding: utf-8 -*-

import tweepy
import json
import logging
import datetime

logging.basicConfig(
    filename='political.log',
    level=logging.WARNING,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%d-%m-%y %H:%M')


class TwitterStream(tweepy.StreamListener):
    def __init__(self, api, twitter_controller):
        super(tweepy.StreamListener, self).__init__()
        self.api = api
        self.last_time = None
        self.tweets_counter = 0
        self.twitter_controller = twitter_controller

    def on_data(self, data):
        tweet = json.loads(data)

        # This code ignores limit notices
        # https://dev.twitter.com/streaming/overview/messages-types#limit_notices
        if tweet.get('limit'):
            logging.debug('Limit notice received: ' + str(tweet['limit']['track']))
            logging.debug(datetime.datetime.now())
            self.twitter_controller.on_limit_notice(tweet)
            return True

        self.tweets_counter += 1

        if self.last_time is None:
            self.last_time = datetime.datetime.now().hour

        if self.last_time != datetime.datetime.now().hour:
            self.last_time = datetime.datetime.now().hour
            logging.debug('Number Tweets: ' + str(self.tweets_counter))
            self.tweets_counter = 0

        #print tweet['text']

        try:

            self.twitter_controller.on_tweet_received(tweet)

        except Exception as exception:
            # Oh well, reconnect and keep trucking
            logging.error("On send tweet to controller")
            logging.error(datetime.datetime.now())
            logging.error(exception.__class__)
            logging.error(exception.message)
            logging.error("------------------")

            self.twitter_controller.on_error(exception.message + str(datetime.datetime.now()))
            return True

        return True



    def on_error(self, status):
        if status == 420:
            logging.error('RATE LIMITED')
            logging.error(datetime.datetime.now())
            logging.error("------------------")
            self.twitter_controller.on_error("RATE LIMITED" + str(datetime.datetime.now()))
        else:
            logging.error(status)
            logging.error(datetime.datetime.now())
            logging.error("------------------")
            self.twitter_controller.on_error("Status:"+str(status)+ str(datetime.datetime.now()))
        return True

    def on_timeout(self):
        logging.error('On TimeOut')
        logging.error(datetime.datetime.now())
        logging.error("------------------")
        self.twitter_controller.on_error("On time out:"+ str(datetime.datetime.now()))
