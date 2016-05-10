#!/usr/local/bin/python
import time


from pymongo import MongoClient

import SentimentAnalysisController
from CollectionClassifierController import CollectionClassifierController
from silverEyeViewer.QueryApp.DAO.DAOAnalyzedTweets import AnalyzedTweets
from silverEyeViewer.QueryApp.DAO.DAOGlobalResults import GlobalResults
from silverEyeViewer.QueryApp.DAO.DAOLastTweet import LastTweet
from silverEyeViewer.QueryApp.DAO.DAOTweets import Tweets
from silverEyeViewer.QueryApp.DAO.DAOTwitterUsers import TwitterUsers
from silverEyeViewer.QueryApp.DAO.DAOUsersAnalyzed import UsersAnalyzed


class AnalysisController:

    def __init__(self, db_client, database):
        self.collection_classifier_controller = CollectionClassifierController(db_client, database)

        self.tweets_dao = Tweets(db_client, database)
        self.users_dao = TwitterUsers(db_client, database)
        self.analyzed_tweets_dao = AnalyzedTweets(db_client, database)
        self.analyzed_twitter_users_dao = UsersAnalyzed(db_client, database)
        self.global_results_dao = GlobalResults(db_client, database)
        self.last_tweet_dao = LastTweet(db_client, database)

    def analyze_tweet(self, tweet):

        try:
            user = tweet["user"]
            user_id = user["id"]
            tweet_id = tweet["id"]

            self.tweets_dao.save_new_tweet(tweet_id, tweet)
            self.users_dao.save_new_user(user_id, user)

            coordinates = tweet["coordinates"]
            place = tweet["place"]
            timestamp = tweet["timestamp_ms"]
            text = tweet["text"]

            tags = self.collection_classifier_controller.get_tags_of_tweet(text)

            collections = self.collection_classifier_controller.get_collection_by_tags(tags)

            polarity = SentimentAnalysisController.analyze_text_and_get_polarity(text)

            self.analyzed_tweets_dao.save_new_analyzed_tweet(user_id, tweet_id, collections, tags, coordinates,
                                                             timestamp, place, polarity, text)
            self.analyze_user(user_id, polarity, collections, tags, timestamp)

        except Exception as exception:
            # Oh well, reconnect and keep trucking
            raise Exception("AnalysisController->" + exception.message + str(exception.__class__))

    def analyze_user(self, user_id, polarity, new_collection_counter, new_tags, timestamp):

        collection_result = {}
        tags_counter = {}

        user_analyzed = self.analyzed_twitter_users_dao.user_analyzed_exist(user_id)

        if user_analyzed is None:
            for key in new_collection_counter.keys():
                collection_result[key] = polarity

            for key in new_tags:
                tags_counter[key] = 1

            self.analyzed_twitter_users_dao.save_update_users_analyzed(user_id, collection_result, 1,
                                                                       timestamp, new_collection_counter, tags_counter)
        else:
            now_tags = user_analyzed["tags_counter"]
            now_collections_results = user_analyzed["result_collections"]
            now_collections_counter = user_analyzed["collection_counter"]
            now_tweets_num = user_analyzed["tweets_num"]

            now_tweets_num += 1

            new_collections_keys = list(new_collection_counter.keys())

            # Plus the new polarity about the collections founded in the tweet
            for key in now_collections_results.keys():
                if key in new_collections_keys:
                    now_collections_results[key] += polarity

            # Add the new collections with the actual polarity
            for key in new_collections_keys:
                if key not in now_collections_results.keys():
                    now_collections_results[key] = polarity

            # Plus the repeat collection
            for key in new_collections_keys:
                if key in now_collections_counter.keys():
                    now_collections_counter[key] += new_collection_counter[key]
                else:
                    now_collections_counter[key] = 1

            # Update the repeat tags by user
            for tag in new_tags:
                if tag in now_tags.keys():
                    now_tags[tag] += 1
                else:
                    now_tags[tag] = 1
            self.analyzed_twitter_users_dao.save_update_users_analyzed(user_id, now_collections_results, now_tweets_num,
                                                                       timestamp, now_collections_counter, now_tags)

    def overall_analysis(self):

        collections_global_users_results = {}
        collections_global_counter_results = {}
        collection_global_positive_results = {}
        collection_global_negative_results = {}
        collection_global_neutral_results = {}

        num_tweets = self.analyzed_tweets_dao.get_size()
        users_num = 0

        for analyzed_user in self.analyzed_twitter_users_dao.get_all_users_analyzed():
            users_num += 1
            for collection in analyzed_user["result_collections"].keys():
                if collection in collections_global_users_results.keys():
                    polarity = analyzed_user["result_collections"][collection]
                    collections_global_users_results[collection] += polarity
                    collections_global_counter_results[collection] += 1

                    if polarity > 0:
                        collection_global_positive_results[collection] += 1
                    elif polarity < 0:
                        collection_global_negative_results[collection] += 1
                    else:
                        collection_global_neutral_results[collection] += 1
                else:
                    polarity = analyzed_user["result_collections"][collection]
                    collections_global_users_results[collection] = polarity
                    collections_global_counter_results[collection] = 1

                    collection_global_positive_results[collection] = 0
                    collection_global_negative_results[collection] = 0
                    collection_global_neutral_results[collection] = 0

                    if polarity > 0:
                        collection_global_positive_results[collection] = 1
                    elif polarity < 0:
                        collection_global_negative_results[collection] = 1
                    else:
                        collection_global_neutral_results[collection] = 1

        self.global_results_dao.update_global_results(collections_global_users_results, num_tweets, users_num,
                                                      time.time(), collections_global_counter_results,
                                                      collection_global_positive_results,
                                                      collection_global_neutral_results,
                                                      collection_global_negative_results)

    def analyze_tags_without_collections(self):
        pass

if __name__ == '__main__':

    client = MongoClient("127.0.0.1", 27017, connect=True)
    database_name = "Test"

    analysis_controller = AnalysisController(client, database_name)
    analysis_controller.overall_analysis()