# -*- coding: utf-8 -*-

import opener

from pymongo import MongoClient
import init_tags


class SilverEye:

    def __init__(self, server_ip, server_port):
        self.ciudadanos = []
        self.democracia_llibertat = []
        self.ehbildu = []
        self.erc = []
        self.podemos = []
        self.pp = []
        self.psoe = []
        self.unio = []
        self.upyd = []
        self.client = MongoClient(server_ip, server_port)

    def load_objective_tags(self):

        db = self.client.SilverEye.SelectedTags

        self.ciudadanos = db.find_one( { "_id": "ciudadanos" } )['tags']
        self.democracia_llibertat = db.find_one( { "_id": "democracia_llibertat" } )['tags']
        self.ehbildu = db.find_one( { "_id": "ehbildu" } )['tags']
        self.erc = db.find_one( { "_id": "erc" } )['tags']
        self.podemos = db.find_one( { "_id": "podemos" } )['tags']
        self.pp = db.find_one( { "_id": "pp" } )['tags']
        self.psoe = db.find_one( { "_id": "psoe" } )['tags']
        self.unio = db.find_one( { "_id": "unio" } )['tags']
        self.upyd = db.find_one( { "_id": "upyd" } )['tags']

    def load_in_db_the_init_tags_for_capture(self):

        db = self.client.SilverEye.SelectedTags

        db.update({"_id":"ciudadanos"}, {'tags': init_tags.ciudadanos}, upsert=True)
        db.update({"_id":"democracia_llibertat"}, {'tags': init_tags.democracia_llibertat}, upsert=True)
        db.update({"_id":"ehbildu"}, {'tags': init_tags.ehbildu}, upsert=True)
        db.update({"_id":"erc"}, {'tags': init_tags.erc}, upsert=True)
        db.update({"_id":"podemos"}, {'tags': init_tags.podemos}, upsert=True)
        db.update({"_id":"pp"}, {'tags': init_tags.pp}, upsert=True)
        db.update({"_id":"psoe"}, {'tags': init_tags.psoe}, upsert=True)
        db.update({"_id":"unio"}, {'tags': init_tags.unio}, upsert=True)
        db.update({"_id":"upyd"}, {'tags': init_tags.upyd}, upsert=True)

    def add_tag_to_objective_set(self, objective_set, tag):

        db = self.client.SilverEye.SelectedTags

        db.update({"_id":objective_set}, {"$addToSet": {"tags": tag}}, upsert=True)

    def delete_tag_to_objective_set(self, objective_set, tag):

        db = self.client.SilverEye.SelectedTags

        db.update({"_id":objective_set}, {"$pull": {"tags": tag}}, upsert=True)

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

    def analyze_set_of_tweets(self, data_set, destiny_data, destiny_user):
        for data in data_set:
            self.analyze_and_save_user_tweet(data, destiny_data,destiny_user)

    def analyze_and_save_user_tweet(self, tweet, destiny_data_db, destiny_user_db):



        text = tweet['text'].encode('utf8')
        user = tweet['user']['id']
        coordinates = tweet['coordinates']

        entities = self.get_entities_by_tweet(text)
        political = self.get_politic_party_by_entities(entities)
        polarity = opener.analyze_text(text)
        polarity = self.get_aprox_polarity(polarity)


        destiny_data_db.update({'user': user, 'text': text}, {'user': user, "text": text, "coordinates": coordinates,\
                                                               'entities': entities, 'polarity': polarity,\
                                                           'political': political}, upsert=True)
        destiny_user_db.update({'user': user}, {'user': user}, upsert=True)

    def get_politic_party_by_entities(self, entities):

        political = {}

        no_reconized_entities = []

        for entity in entities:

            classified_entity = False

            if entity in self.ciudadanos:
                if political.has_key('ciudadanos'):
                    political['ciudadanos'] += political['ciudadanos']
                else:
                    political['ciudadanos'] = 1
                classified_entity = True

            if entity in self.democracia_llibertat:
                if political.has_key('democracia_llibertat'):
                    political['democracia_llibertat'] += political['democracia_llibertat']
                else:
                    political['democracia_llibertat'] = 1
                classified_entity = True

            if entity in self.ehbildu:
                if political.has_key('ehbildu'):
                    political['ehbildu'] += political['ehbildu']
                else:
                    political['ehbildu'] = 1
                classified_entity = True

            if entity in self.erc:
                if political.has_key('erc'):
                    political['erc'] += political['erc']
                else:
                    political['erc'] = 1
                classified_entity = True

            if entity in self.podemos:
                if political.has_key('podemos'):
                    political['podemos'] += political['podemos']
                else:
                    political['podemos'] = 1
                classified_entity = True

            if entity in self.pp:
                if political.has_key('pp'):
                    political['pp'] += political['pp']
                else:
                    political['pp'] = 1
                classified_entity = True

            if entity in self.psoe:
                if political.has_key('psoe'):
                    political['psoe'] += political['psoe']
                else:
                    political['psoe'] = 1
                classified_entity = True

            if entity in self.unio:
                if political.has_key('unio'):
                    political['unio'] += political['unio']
                else:
                    political['unio'] = 1
                classified_entity = True

            if entity in self.upyd:
                if political.has_key('upyd'):
                    political['upyd'] += political['upyd']
                else:
                    political['upyd'] = 1
                classified_entity = True

            if not classified_entity:

                no_reconized_entities.append(entity)

                print "HOLA"

        db_data = self.client.SilverEye.UnclassifiedEntities
        #Save no recognized entities
        for no_rec_ent in no_reconized_entities:
            print "Adeu:"+ no_rec_ent
            db_data.update({'entity': str(no_rec_ent)}, {'$inc': {'repeat': 1}},upsert=True)
            for entity in entities:
                db_data.update({'entity': str(no_rec_ent)}, {"$addToSet": {"entities": entity}}, upsert=True)

        return political

    def get_entities_by_tweet(self, text):
        text = text.replace(".", " ")
        text = text.replace(":", " ")
        text = text.replace(",", " ")

        entities = []

        for entity in self.ciudadanos:
            if entity in text:
                entities.append(entity)

        for entity in self.democracia_llibertat:
            if entity in text:
                entities.append(entity)

        for entity in self.ehbildu:
            if entity in text:
                entities.append(entity)

        for entity in self.erc:
            if entity in text:
                entities.append(entity)

        for entity in self.podemos:
            if entity in text:
                entities.append(entity)

        for entity in self.pp:
            if entity in text:
                entities.append(entity)

        for entity in self.psoe:
            if entity in text:
                entities.append(entity)

        for entity in self.unio:
            if entity in text:
                entities.append(entity)

        for entity in self.unio:
            if entity in text:
                entities.append(entity)


        split_text = text.split(' ')

        if split_text[0] == "RT":
            del split_text[0]
            del split_text[1]

        for word in split_text:
            if len(word) > 0 and word[0] == "@":
                if word not in entities:
                    entities.append(word)
            if len(word) > 0 and word[0] == "#":
                if word not in entities:
                    entities.append(word)

        return entities

    def get_aprox_polarity(self, sentiment):
        negative = int(sentiment['opinion']['negative'])
        negative = negative + int(sentiment['polarity']['negative'])

        positive = int(sentiment['opinion']['positive'])
        positive = positive + int(sentiment['polarity']['positive'])

        if negative == positive:
            return 0
        elif negative > positive:
            return -1
        elif negative < positive:
            return 1

    def get_result_of_a_data_set_by_entities(self, data_set):
        entities_collection = []
        user_entities = []
        result_entities = {}

        # Optimize
        for data in data_set:
            data_entities = data['entities']
            entities = {}
            for entity in set(data_entities):
                entities[entity] = int(data["polarity"])
                if entity not in user_entities:
                    user_entities.append(entity)

            entities_collection.append(entities)

        #print entities_collection

        for entity in user_entities:
            result_entities[entity] = 0

        for tweet_entity in entities_collection:
            for user in user_entities:
                for key in tweet_entity.keys():
                    if user == key:
                        result_entities[user] += tweet_entity[user]

        return result_entities


    def analyze_and_save_result_of_user(self, user_id):

        db_data = self.client.SilverEye['TestSentiment']
        db_user = self.client.SilverEye['TestSentimentUser']

        data = db_data.find({"user": user_id})

        #By entities
        result = self.get_result_of_a_data_set_by_entities(data)

        db_user.update({"user": user_id}, {"$set": {"result": result}}, upsert=True)


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

        print data
        print data['result']


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
            ciudadanos_total = value +ciudadanos_total

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

        result = {"ciudadanos":ciudadanos_total,"democracia_llibertat":democracia_llibertat_total, "ehbildu":ehbildu_total, \
                  "erc":erc_total, "podemos":podemos_total, "pp":pp_total, "psoe":psoe_total, "unio":unio_total, "upyd":upyd_total }

        db_user.update({"user": user_id}, {"$set": {"result_political": result}}, upsert=True)


    def analyze_all_users(self):
        db_user = self.client.SilverEye['TestSentimentUser']

        for user in db_user.find():
            #print user
            if "result" not in user.keys():
                self.analyze_and_save_result_of_user(user['user'])
                #analyze_political_sentiment_by_entities_for_one_user(user['user'])





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




