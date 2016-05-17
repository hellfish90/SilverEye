# -*- coding: utf-8 -*-
import os
import sys

sys.path.append( os.path.dirname(os.path.dirname(__file__)) )
from pymongo import MongoClient
from AnalysisController import AnalysisController
from TwitterController import TwitterController
from silverEyeViewer.QueryApp.DAO.DAOCollectionTags import DAOTags


class SilverEye:

    def __init__(self, server_ip, server_port, database):
        self.client = MongoClient(server_ip, server_port, connect=True)
        self.database = database

        self.twitter_controller = TwitterController(self)
        self.analysis_controller = AnalysisController(self.client, database)

        self.dao_collection_tags = DAOTags(self.client, self.database)

    def start(self):
        keywords = self.dao_collection_tags.get_array_of_the_name_of_classified_tags()
        self.twitter_controller.start(keywords)

    def stop(self):
        self.twitter_controller.stop()

    def analyze_tweet(self, tweet):
        self.analysis_controller.analyze_tweet(tweet)

    def analyse_temporal_time(self, init_time=0):
        self.analysis_controller.analyse_temporal_lines(init_time)

if __name__ == "__main__":
    silver_eye = SilverEye("127.0.0.1", 27017, "Test")

    my_input = raw_input("Please press enter to start")
    silver_eye.start()

    my_input = raw_input("Please press enter to stop")
    silver_eye.stop()

    #TODO bucle que llegeixi un fitxer, si es 0 no paris, sino para, etc...