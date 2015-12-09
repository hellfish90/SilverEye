# coding=utf-8
# This Python file uses the following encoding: utf-8
# !/usr/bin/python
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

ciudadanos = ["@GirautaOficial" or
            "#AlbertRivera" or
            "@Albert_Rivera" or
            "@CiudadanosCs" or
            "#RutaCiudadana" or
            "#ConIlusion" or
            "@sdelcampocs" or
            "#Ilusión" or
            "#Ciudadanos" or
            "@InesArrimadas" or
            "#AlbertPresidente"]

democracia_llibertat = ["@ConvergenciaCAT" or
            "@DemocratesCAT" or
            "@reagrupament" or
            "#possible" or
            "@20dl_cat" or
            "@joseprull" or
            "@joanbague" or
            "@peresalo68" or
            "@Ferran_Bel" or
            "@franceschoms"]

ehbildu = ["@ehbildu" or
            "#BilduErabakira" or
            "#BilduErabakira" or
            "@ehbildu_legebil"]

erc = ["ERC" or
            "#SomRepública" or
            "@Esquerra_ERC" or
            "@GabrielRufian" or
            "@Esquerra_ERC" or
            "@JoanTarda" or
            "@junqueras" or
            "@MartaRovira"]

podemos = ["#UNPAISCONTIGO" or
            "@ahorapodemos" or
            "#Un6Dcontigo" or
            "#6DHagamosHistoria" or
            "@Pablo_Iglesias_" or
            "@AdaColau" or
            "@VickyRosell" or
            "#LeyDeImpunidad"]

pp = ["partidopopular" or
            "partido popular"or
            "pp"or
            "#PP"or
            "#EspañaEnSerio"or
            "@marianorajoy"or
            "@AlfonsoAlonsoPP"or
            "@PPopular"or
            "#VotaPP"or
            "@Sorayapp"or
            "@mdcospedal"or
            "pablocasado_"or
            "#YoVotoPP"or
            "#EmpleoEnSerio"or
            "@NNGG_Es"]

psoe = ["psoe" or
            "psc" or
            "@socialistes_cat" or
            "#FemForaRajoy" or
            "#SomLaSolucio" or
            "@carmechacon" or
            "@sanchezcastejon" or
            "@PSOE" or
            "#OrgulloSocialista" or
            "#VOTAPSOE" or
            "#PedroPresidente" or
            "#UnFuturoParaLaMayoría"]

unio = ["@unio_cat" or
            "@DuranLleida" or
            "#Solucions!" or
            "@Marti_Barbera" or
            "@Ramon_Espadaler"]

upyd = ["@UPYD" or
            "#VotaUPYD" or
            "#MásEspaña" or
            "@Herzogoff" or
            "@sryuriaguilar"]

keywords = ciudadanos + democracia_llibertat + ehbildu + erc + podemos + pp + psoe + unio + upyd

client = None
db = None


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        # Dev
        client = MongoClient('192.168.101.73', 27017)
        self.db = client.SilverEye
        self.tweets_counter = 0
        self.tweets_counter_pp = 0
        self.tweets_counter_ciudadanos = 0
        self.tweets_counter_democracia_llibertat = 0
        self.tweets_counter_ehbildu = 0
        self.tweets_counter_erc = 0
        self.tweets_counter_podemos = 0
        self.tweets_counter_psoe = 0
        self.tweets_counter_unio = 0
        self.tweets_counter_upyd = 0
        self.last_time = None

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

        if self.last_time == None:
            self.last_time = datetime.datetime.now().hour

        if self.last_time != datetime.datetime.now().hour:
            self.last_time = datetime.datetime.now().hour
            logging.warning('Tweets: ' + str(self.tweets_counter))
            self.db.twitterCounter.insert({"Political": "Streaming", "datetime": datetime.datetime.now(),
                                                "num": self.tweets_counter})
            # print self.tweets_counter
            self.tweets_counter = 0

        print tweet['text']
        tag = "NONE"

        if any(word in tweet['text'] for word in pp):
            tag = "PP"
        elif any(word in tweet['text'] for word in ciudadanos):
            tag = "CIUDADANOS"
        elif any(word in tweet['text'] for word in psoe):
            tag = "PSOE"
        elif any(word in tweet['text'] for word in podemos):
            tag = "PODEMOS"
        elif any(word in tweet['text'] for word in erc):
            tag = "ERC"
        elif any(word in tweet['text'] for word in democracia_llibertat):
            tag = "DEMOCRACIA LLIBERTAT"
        elif any(word in tweet['text'] for word in upyd):
            tag = "UPYD"
        elif any(word in tweet['text'] for word in unio):
            tag = "UNIO"
        elif any(word in tweet['text'] for word in ehbildu):
            tag = "EHBILDU"

        try:
            tweet["Political"] = tag
            self.db.twitterPolitical.update(tweet, tweet, upsert=True)
            self.db.twitterUser.update({"screen_name": tweet['user']['screen_name']}, user, upsert=True)
        except Exception as e:
            # Oh well, reconnect and keep trucking
            logging.error("On save to db:")
            logging.error(datetime.datetime.now())
            logging.error(e.__class__)
            logging.error(e)
            logging.error("------------------")
            return True

        return True

    def on_error(self, status):
        if status == "402":
            logging.error('RATE LIMITED')
            logging.error(self.TAG)
            logging.error(datetime.datetime.now())
            logging.error("------------------")
        else:
            logging.error(status)
            logging.error(self.TAG)
            logging.error(datetime.datetime.now())
            logging.error("------------------")
        return True

    def on_timeout(self):
        logging.error('CustomStreamListener on_timeout')
        logging.error(datetime.datetime.now())
        logging.error("------------------")


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

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    while True:
        try:
            logging.debug('Connecting to Twitter stream ...')
            stream = tweepy.streaming.Stream(auth, CustomStreamListener(api))
            stream.filter(track=keywords)

        except Exception as e:
            # Oh well, reconnect and keep trucking
            logging.error(e.__class__)
            logging.error(e)
            logging.error("------------------")
            continue
        except KeyboardInterrupt:
            stream.disconnect()
            break

'''
    stream = tweepy.streaming.Stream(auth, CustomStreamListener(api))
    stream.filter(track=keywords, async=True)

'''