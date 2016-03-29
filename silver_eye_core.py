# -*- coding: utf-8 -*-

import opener

from pymongo import MongoClient
from twitter_extractor import Extractor
from group_identifier import GroupClassifier


class SilverEye:

    def __init__(self, server_ip, server_port):
        self.client = MongoClient(server_ip, server_port)
        self.extractor = Extractor(self.client)
        self.group_classifier = GroupClassifier(self.extractor, self.client)

        self.extractor.load_objective_tags()

        self.origin_tweets_db = self.client.SilverEye['twitterPolitical']

    '''
    '   Analyze one tweet and save the user and the analyzed tweet
    '''

    def analyze_and_save_user_tweet(self, tweet, destiny_data_db, destiny_user_db):

        text = tweet['text'].encode('utf8')
        user = tweet['user']['id']
        coordinates = tweet['coordinates']

        entities = self.group_classifier.get_entities_by_tweet(text)
        political = self.group_classifier.get_political_party_counter_by_entities(entities)
        polarity = opener.analyze_text(text)
        polarity = opener.get_aprox_polarity(polarity)

        destiny_data_db.update({'user': user, 'text': text}, {'user': user, "text": text, "coordinates": coordinates, \
                                                              'entities': entities, 'polarity': polarity, \
                                                              'political': political}, upsert=True)
        destiny_user_db.update({'user': user}, {'user': user}, upsert=True)

    '''
    '   Analyze a set of tweets by blocks of the db_origin and save the tweet analyzed in db_destiny_data
    '   and the user in to db_destiny_user
    '''

    def analyze_set_of_tweets_by_blocks(self):
        db_origin = self.client.SilverEye['twitterPolitical']
        db_destiny_data = self.client.SilverEye.TestSentimentPolitical
        db_destiny_user = self.client.SilverEye['TestSentimentUser']

        size = int(db_origin.count())

        max_set = 5;

        data_analyzed = 0;

        while data_analyzed < size:
            init = data_analyzed + 1
            final = max_set + data_analyzed + 1

            data_set = db_origin.find()[init:final]
            for data in data_set:
                self.analyze_and_save_user_tweet(data, db_destiny_data, db_destiny_user)

            data_analyzed = final

    '''
    '   Analyze all tweets by one user by the political party of her tweets
    '''

    def political_analysis_for_one_user_by_political_party(self, user_id):

        db_user_result = self.client.SilverEye.TestSentimentUser
        db_sentiment_tweet = self.client.SilverEye.TestSentimentPolitical

        data = db_sentiment_tweet.find({"user": user_id})

        political_results = {}
        political_counter = {}

        for tweet in data:
            political_entities = tweet['political']

            for political in set(political_entities):

                if political in political_results.keys():
                    political_results[political] += int(tweet["polarity"])
                    political_counter[political] += 1
                else:
                    political_results[political] = int(tweet["polarity"])
                    political_counter[political] = 1

        db_user_result.update({"user": user_id}, {"$set": {"political_result": political_results}}, upsert=True)
        db_user_result.update({"user": user_id}, {"$set": {"political_counter": political_counter}}, upsert=True)
        return political_results

    def political_analysis_for_all_user_by_political_party(self):

        db_user_result = self.client.SilverEye.TestSentimentUser

        data = db_user_result.find()

        for user in data:
            self.political_analysis_for_one_user_by_political_party(user['user'])

    '''
    '   Global results by politican group
    '''
    def global_result_by_political_group(self):

        db_user_result = self.client.SilverEye.TestSentimentUser
        db_result = self.client.SilverEye['TestGlobalResult']

        data = db_user_result.find()

        final_political_results = {}
        final_political_counter = {}
        users = 0

        for user in data:
            users += 1
            for political in user["political_result"].keys():

                political_result = user["political_result"]

                if political in final_political_results.keys():
                    final_political_results[political] += int(political_result[political])
                    final_political_counter[political] += 1
                else:
                    final_political_results[political] = int(political_result[political])
                    final_political_counter[political] = 1

        db_result.update({"unique": "unique"}, {"$set": {"result_political": final_political_results}}, upsert=True)
        db_result.update({"unique": "unique"}, {"$set": {"political_counter" : final_political_counter}}, upsert=True)
        db_result.update({"unique": "unique"}, {"$set": {"users": users}}, upsert=True)

    '''
    '   Get all entities and assign the polarity of the tweet
    '   For each entity adds the polarity of the tweet that is found
    '''
    # Old strategy
    def get_result_of_a_data_set_by_entities(data_set):
        entities_collection = []
        no_repeat_entities = []
        result_entities = {}

        for data in data_set:
            data_entities = data['entities']
            entities = {}
            for entity in set(data_entities):
                entities[entity] = int(data["polarity"])
                # Identify not repeat entities
                if entity not in no_repeat_entities:
                    no_repeat_entities.append(entity)

            entities_collection.append(entities)

        for entity in no_repeat_entities:
            result_entities[entity] = 0

        # For each entity adds the polarity of the tweet that is found
        for entity in entities_collection:
            for unique_entity in no_repeat_entities:
                for key in entity.keys():
                    if unique_entity == key:
                        result_entities[unique_entity] += entity[unique_entity]

        return result_entities

    '''
    '   Analyze a set of tweets of one user
    '''
    # Old Strategy
    def analyze_and_save_result_of_user(self, user_id):

        db_data = self.client.SilverEye['TestSentiment']
        db_user = self.client.SilverEye['TestSentimentUser']

        data = db_data.find({"user": user_id})

        #By entities
        result = self.get_result_of_a_data_set_by_entities(data)

        db_user.update({"user": user_id}, {"$set": {"result": result}}, upsert=True)

    '''
    '   Analyze a set of tweets of one user by entities and her polarity
    '''
    # Old Strategy
    def analyze_political_sentiment_by_entities_for_one_user(self, user_id):

        db_user = self.client.SilverEye['TestSentimentUser']

        ciudadanos_tag = []
        democracia_llibertat_tag = []
        ehbildu_tag = []
        erc_tag = []
        podemos_tag = []
        pp_tag = []
        psoe_tag = []
        unio_tag = []
        upyd_tag = []

        ciudadanos_total = 0
        democracia_llibertat_total = 0
        ehbildu_total = 0
        erc_total = 0
        podemos_total = 0
        pp_total = 0
        psoe_total = 0
        unio_total = 0
        upyd_total = 0

        data = db_user.find({"user": user_id})[0]

        #print data
        #print data['result']

        for key, value in data['result'].items():
            if key in self.ciudadanos:
                ciudadanos_tag.append(value)

            if key in self.democracia_llibertat:
                democracia_llibertat_tag.append(value)

            if key in self.ehbildu:
                ehbildu_tag.append(value)

            if key in self.erc:
                erc_tag.append(value)

            if key in self.podemos:
                podemos_tag.append(value)

            if key in self.pp:
                pp_tag.append(value)

            if key in self.psoe:
                psoe_tag.append(value)

            if key in self.unio:
                unio_tag.append(value)

            if key in self.upyd:
                upyd_tag.append(value)

        for value in ciudadanos_tag:
            ciudadanos_total = value + ciudadanos_total

        for value in democracia_llibertat_tag:
            democracia_llibertat_total = value + democracia_llibertat_total

        for value in ehbildu_tag:
            ehbildu_total = value + ehbildu_total

        for value in erc_tag:
            erc_total = value + erc_total

        for value in podemos_tag:
            podemos_total = value + podemos_total

        for value in pp_tag:
            pp_total = value + pp_total

        for value in psoe_tag:
            psoe_total += value

        for value in unio_tag:
            unio_total += value

        for value in upyd_tag:
            upyd_total += value

        result = {"ciudadanos": ciudadanos_total,"democracia_llibertat": democracia_llibertat_total, \
                  "ehbildu": ehbildu_total, "erc": erc_total, "podemos": podemos_total, "pp": pp_total, \
                  "psoe": psoe_total, "unio": unio_total, "upyd": upyd_total }

        db_user.update({"user": user_id}, {"$set": {"result_political": result}}, upsert=True)

    # Old Strategy
    def analyze_all_users(self):
        db_user = self.client.SilverEye['TestSentimentUser']

        for user in db_user.find():
            if "result" not in user.keys():
                self.analyze_and_save_result_of_user(user['user'])
    '''
    '   Analyze all the users and found the global polarity by sum the results of all users
    '''
    # Old Strategy
    def global_results(self):

        db_data = self.client.SilverEye['TestSentimentUser']
        db_result = self.client.SilverEye['TestGlobalResult']

        ciudadanos_total = 0
        democracia_llibertat_total = 0
        ehbildu_total = 0
        erc_total = 0
        podemos_total = 0
        pp_total = 0
        psoe_total = 0
        unio_total = 0
        upyd_total = 0

        ciudadanos_total_counter = 0
        democracia_llibertat_total_counter = 0
        ehbildu_total_counter = 0
        erc_total_counter = 0
        podemos_total_counter = 0
        pp_total_counter = 0
        psoe_total_counter = 0
        unio_total_counter = 0
        upyd_total_counter = 0

        total_users =0

        for user in db_data.find():

            if user.get('result_political', None) is not None:

                total_users = total_users + 1

                for key, value in user['result_political'].items():

                    if key == "ciudadanos":
                        ciudadanos_total = ciudadanos_total + value
                        ciudadanos_total_counter += 1
                    if key == "democracia_llibertat":
                        democracia_llibertat_total = democracia_llibertat_total + value
                        democracia_llibertat_total_counter += 1
                    if key == "ehbildu":
                        ehbildu_total = ehbildu_total + value
                        democracia_llibertat_total_counter += 1
                    if key == "erc":
                        erc_total = erc_total + value
                        democracia_llibertat_total_counter += 1
                    if key == "podemos":
                        podemos_total = podemos_total + value
                        democracia_llibertat_total_counter += 1
                    if key == "pp":
                        pp_total = pp_total + value
                        democracia_llibertat_total_counter += 1
                    if key == "unio":
                        unio_total = unio_total + value
                        democracia_llibertat_total_counter += 1
                    if key == "upyd":
                        upyd_total = upyd_total + value
                        democracia_llibertat_total_counter += 1
                    if key == "psoe":
                        psoe_total = psoe_total + value
                        democracia_llibertat_total_counter += 1



        result = {"ciudadanos":ciudadanos_total,"democracia_llibertat":democracia_llibertat_total, "ehbildu":ehbildu_total, \
                  "erc":erc_total, "podemos":podemos_total, "pp":pp_total, "psoe":psoe_total, "unio":unio_total, "upyd":upyd_total }

        result_counter = {"ciudadanos":ciudadanos_total_counter,"democracia_llibertat":democracia_llibertat_total_counter, \
                          "ehbildu":ehbildu_total_counter,"erc":erc_total_counter, "podemos":podemos_total_counter, \
                          "pp":pp_total_counter, "psoe":psoe_total_counter, "unio":unio_total_counter, "upyd":upyd_total_counter }


        db_result.update({"unique": "unique"}, {"$set": {"result_political": result}}, upsert=True)
        db_result.update({"unique": "unique"}, {"$set": {"users" : total_users}}, upsert=True)
        db_result.update({"unique": "unique"}, {"$set": {"political_entities_counter": result_counter}}, upsert=True)



'''

    def identify_sentiment_by_text_entities_and_user(self):

        db_origin = self.client.SilverEye['twitterPolitical']
        db_destiny_data = self.client.SilverEye['TestSentiment']
        db_destiny_user = self.client.SilverEye['TestSentimentUser']

        size = int(db_origin.count())

        max_set = 5;

        data_analyzed = 0;

        while data_analyzed < size:
            init = data_analyzed + 1
            final = max_set + data_analyzed + 1

            data_set = db_origin.find()[init:final]
            self.analyze_set_of_tweets(data_set, db_destiny_data, db_destiny_user)

            data_analyzed = final

'''
