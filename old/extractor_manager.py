# -*- coding: utf-8 -*-

import json
import logging
import threading

import tweepy
# Max 400 keywords

# https://dev.twitter.com/streaming/overview/request-parameters

from old.extractor_twitter import ExtractorTwitterListener
import silverEyeViewer.QueryApp.Core.load_dummy_tags

logging.basicConfig(
    filename='QueryApp/Log/extractor.log',
    level=logging.WARNING,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%d-%m-%y %H:%M')


class Extractor:
    def __init__(self, client_db):

        self.ciudadanos = []
        self.democracia_llibertat = []
        self.ehbildu = []
        self.erc = []
        self.podemos = []
        self.pp = []
        self.psoe = []
        self.unio = []
        self.upyd = []

        self.db = client_db

        self.twitter_extractor = None

        self.tags_db = self.db.SilverEye.SelectedTags
        self.unclassified_tags_db = self.db.SilverEye.UnclassifiedEntities

    def load_objective_tags(self):

        self.ciudadanos = self.tags_db.find_one({"_id": "ciudadanos"})['tags']
        self.democracia_llibertat = self.tags_db.find_one({"_id": "democracia_llibertat"})['tags']
        self.ehbildu = self.tags_db.find_one({"_id": "ehbildu"})['tags']
        self.erc = self.tags_db.find_one({"_id": "erc"})['tags']
        self.podemos = self.tags_db.find_one({"_id": "podemos"})['tags']
        self.pp = self.tags_db.find_one({"_id": "pp"})['tags']
        self.psoe = self.tags_db.find_one({"_id": "psoe"})['tags']
        self.unio = self.tags_db.find_one({"_id": "unio"})['tags']
        self.upyd = self.tags_db.find_one({"_id": "upyd"})['tags']

    def load_in_db_the_init_tags_for_capture(self):

        self.tags_db.update({"_id": "ciudadanos"}, {'tags': silverEyeViewer.QueryApp.Core.load_dummy_tags.ciudadanos}, upsert=True)
        self.tags_db.update({"_id": "democracia_llibertat"}, {'tags': silverEyeViewer.QueryApp.Core.load_dummy_tags.democracia_llibertat}, upsert=True)
        self.tags_db.update({"_id": "ehbildu"}, {'tags': silverEyeViewer.QueryApp.Core.load_dummy_tags.ehbildu}, upsert=True)
        self.tags_db.update({"_id": "erc"}, {'tags': silverEyeViewer.QueryApp.Core.load_dummy_tags.erc}, upsert=True)
        self.tags_db.update({"_id": "podemos"}, {'tags': silverEyeViewer.QueryApp.Core.load_dummy_tags.podemos}, upsert=True)
        self.tags_db.update({"_id": "pp"}, {'tags': silverEyeViewer.QueryApp.Core.load_dummy_tags.pp}, upsert=True)
        self.tags_db.update({"_id": "psoe"}, {'tags': silverEyeViewer.QueryApp.Core.load_dummy_tags.psoe}, upsert=True)
        self.tags_db.update({"_id": "unio"}, {'tags': silverEyeViewer.QueryApp.Core.load_dummy_tags.unio}, upsert=True)
        self.tags_db.update({"_id": "upyd"}, {'tags': silverEyeViewer.QueryApp.Core.load_dummy_tags.upyd}, upsert=True)

    def init_twitter_extractor(self, silver_eye_core):
        self.twitter_extractor = self.TwitterExtractorThread(silver_eye_core, self.db)
        self.twitter_extractor.start()

    def restart_twitter_extractor(self, silver_eye_core):
        if self.twitter_extractor is not None:
            self.twitter_extractor.stop()
        self.init_twitter_extractor(silver_eye_core)

    def stop_twitter_extractor(self):
        if self.twitter_extractor is not None:
            self.twitter_extractor.stop()
        print "Stopped"

    class TwitterExtractorThread (threading.Thread):

        def __init__(self, silvereye_core, db):
            threading.Thread.__init__(self)
            self.silvereye_core = silvereye_core
            self.stream = None
            self.db = db
            self.search = True

        def run(self):
            self.init_twitter_extractor()

        def init_twitter_extractor(self):
            keywords = self.silvereye_core.get_all_classified_tags_name()
            logging.debug('extractor starting ...')
            logging.debug("------------------")

            with open('QueryApp/Config/config.json', 'r') as f:
                config = json.load(f)
                access_token = config['access_token']
                access_token_secret = config['access_token_secret']
                consumer_key = config['consumer_key']
                consumer_secret = config['consumer_secret']
                database_name = config['database_name']

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)

            print keywords

            while self.search:
                try:
                    logging.debug('Connecting to Twitter stream ...')
                    self.stream = tweepy.streaming.Stream(auth, ExtractorTwitterListener(api, self.db, self.silvereye_core))
                    self.stream.filter(track=keywords)

                except Exception as e:
                    logging.error(e.__class__)
                    logging.error(e.__class__)
                    logging.error(e)
                    logging.error("------------------")
                    continue

                except KeyboardInterrupt:
                    self.stream.disconnect()
                    self.db.close()
                    break

        def stop(self):
            self.search = False
            self.stream.disconnect()