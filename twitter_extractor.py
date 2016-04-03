# -*- coding: utf-8 -*-

from pymongo import MongoClient
import init_tags


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

        self.tags_db = client_db.SilverEye.SelectedTags

    def load_objective_tags(self):

        self.ciudadanos = self.tags_db.find_one({"_id": "ciudadanos" })['tags']
        self.democracia_llibertat = self.tags_db.find_one({"_id": "democracia_llibertat"})['tags']
        self.ehbildu = self.tags_db.find_one({"_id": "ehbildu"})['tags']
        self.erc = self.tags_db.find_one({"_id": "erc"})['tags']
        self.podemos = self.tags_db.find_one({"_id": "podemos"})['tags']
        self.pp = self.tags_db.find_one({"_id": "pp"})['tags']
        self.psoe = self.tags_db.find_one({"_id": "psoe"})['tags']
        self.unio = self.tags_db.find_one({"_id": "unio"})['tags']
        self.upyd = self.tags_db.find_one({"_id": "upyd"})['tags']

    def load_in_db_the_init_tags_for_capture(self):

        self.tags_db.update({"_id": "ciudadanos"}, {'tags': init_tags.ciudadanos}, upsert=True)
        self.tags_db.update({"_id": "democracia_llibertat"}, {'tags': init_tags.democracia_llibertat}, upsert=True)
        self.tags_db.update({"_id": "ehbildu"}, {'tags': init_tags.ehbildu}, upsert=True)
        self.tags_db.update({"_id": "erc"}, {'tags': init_tags.erc}, upsert=True)
        self.tags_db.update({"_id": "podemos"}, {'tags': init_tags.podemos}, upsert=True)
        self.tags_db.update({"_id": "pp"}, {'tags': init_tags.pp}, upsert=True)
        self.tags_db.update({"_id": "psoe"}, {'tags': init_tags.psoe}, upsert=True)
        self.tags_db.update({"_id": "unio"}, {'tags': init_tags.unio}, upsert=True)
        self.tags_db.update({"_id": "upyd"}, {'tags': init_tags.upyd}, upsert=True)

    def add_tag_to_objective_set(self, objective_set, tag):

        self.tags_db.update({"_id": objective_set}, {"$addToSet": {"tags": tag}}, upsert=True)

    def delete_tag_to_objective_set(self, objective_set, tag):

        self.tags_db.update({"_id": objective_set}, {"$pull": {"tags": tag}}, upsert=True)

    def get_all_tags(self):
        collections = self.tags_db.find()

        tags = []

        for collection in collections:
            for tag in collection['tags']:
                tags.append(tag)

        return tags