import pymongo

import time


class DAOTags:

    def __init__(self, mongo_client, database):
        self.mongo_client = mongo_client
        self.tags_db = self.mongo_client[database]['Tags']
        self.collections_db = self.mongo_client[database]['CollectionsSet']

    def get_tag_by_id(self, tag_id):
        return self.tags_db.find_one({"_id": {"$eq": tag_id}})

    def get_all_collection(self):

        collections = self.collections_db.find()
        complete_collections = []

        for collection in collections:
            tags = []
            for tag in collection["tags"]:
                cmpl_tag = self.get_tag_by_id(tag)
                tags.append(cmpl_tag)
            collection["tags"] = tags
            complete_collections.append(collection)

        return complete_collections

    def get_all_tags(self):
        return self.tags_db.find()

    def get_array_of_the_name_of_classified_tags(self):

        tags = []

        for tag in self.get_list_of_all_classified_tags():
            tags.append(tag["_id"])

        return map(unicode, tags)

    def get_list_of_all_classified_tags(self):
        return list(self.tags_db.find({"classified": {"$eq": True}},).sort("repeat", pymongo.DESCENDING))

    def get_unclassified_tags(self):
        return list(self.tags_db.find({"classified": {"$eq": False}},).sort("repeat", pymongo.DESCENDING))

    def get_tags_by_collection(self, collection_name):
        collection = list(self.collections_db.find({"_id": {"$eq": collection_name}}))
        tags = []
        if len(collection) > 0:
            for tag_name in collection[0]["tags"]:
                tags.append(self.tags_db.find_one({"_id": {"$eq": tag_name}}))
        return tags

    def get_the_collection_name_of_tag(self, tag_name):

        result_list = self.collections_db.find({"tags": {"$eq": tag_name}})

        for result in result_list:
            return result
        return None

    def tag_exist(self, tag_name):
        return len(list(self.tags_db.find({"_id": {"$eq": tag_name}}))) > 0

    def add_tag(self, tag, related_tags, classified=False):

        self.tags_db.update_one({"_id": tag}, {"$set": {"repeat": 0}}, upsert=True)
        self.tags_db.update_one({"_id": tag}, {"$set": {"classified": classified}})
        self.tags_db.update_one({"_id": tag}, {"$set": {"suggested_collection": {}}})
        self.tags_db.update_one({"_id": tag}, {"$set": {"timestamp_last_update": int(time.time())}})

        for related_tag in related_tags:
            self.tags_db.update_one({"_id": tag}, {"$set": {"related."+related_tag: 0}})
        if len(related_tags) < 1:
            self.tags_db.update_one({"_id": tag}, {"$set": {"related": {}}})

    def add_suggested_collection_to_tag(self, tag, suggested_collection):
        self.tags_db.update_one({"_id": tag}, {"$set": {"suggested_collection": suggested_collection}})

    def add_collection(self, collection_name):
        self.collections_db.insert_one({"_id": collection_name, "tags": []})

    def remove_collection(self, collection_name):
        self.collections_db.delete_many({"_id": collection_name})

    def add_tag_to_collection(self, collection_name, tag_name):
        self.collections_db.update_one({"_id": collection_name}, {"$addToSet": {"tags": tag_name}}, upsert=True)
        self.add_tag(tag_name, [], True)

    def remove_tag_of_collection(self, collection_name, tag_name):
        self.collections_db.update_one({"_id": collection_name}, {"$pull": {"tags": tag_name}}, upsert=True)
        self.tags_db.update_one({"_id": tag_name}, {"$set": {"classified": False}})

    def update_related_tags_and_plus_repeat(self, tag_name, related_tags):
        for r_tags in related_tags:
            self.tags_db.update_one({'_id': tag_name}, {'$inc': {'related.'+r_tags: 1}})
        self.tags_db.update_one({'_id': tag_name}, {'$inc': {'repeat': 1}})
        self.tags_db.update_one({"_id": tag_name}, {"$set": {"timestamp_last_update": int(time.time())}})

    def get_size_collections(self):
        return self.collections_db.count()

    def get_size_tags(self):
        return self.tags_db.count()
