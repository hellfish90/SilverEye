import pymongo


class DAOTags:

    def __init__(self, mongo_client):
        self.mongo_client = mongo_client
        self.tags_db = self.mongo_client.SilverEye['Tags']
        self.collections_db = self.mongo_client.SilverEye['CollectionsSet']

    def get_all_collection_name(self):

        collection_tags = self.get_all_classified_tags()

        collections_names = []

        for collections in collection_tags:
                for collection in collections:
                    collections_names.append(collection)
        return collections_names

    def get_all_classified_tags_name(self):

        collection_tags = self.get_all_classified_tags()

        tags_name = []

        for collections in collection_tags:
                for collection in collections:
                    for tags in collections[collection]:
                        tags_name.append(tags["_id"])
        return tags_name

    def get_all_classified_tags(self):
        collections = list(self.collections_db.find())
        collection_tags = []

        for collection in collections:
            collection_tags.append({collection["_id"]: self.get_classified_tags(collection["_id"])})
        return collection_tags

    def get_classified_tags(self, collection_name):
        collection = list(self.collections_db.find({"_id": {"$eq": collection_name}}))
        tags = []
        if len(collection) > 0:
            for tag_name in collection[0]["tags"]:
                tags.append(self.tags_db.find_one({"_id": {"$eq": tag_name}}))
        return tags

    def get_unclassified_tags(self):
        return list(self.tags_db.find({"classified": {"$eq": False}},).sort("repeat",pymongo.DESCENDING))

    def get_collection_name_by_tag(self, tag_name):

        result_list = list(self.collections_db.find({"tags": {"$eq": tag_name}}))

        if len(result_list) > 0:
            return result_list[0]["_id"]
        return None

    def tag_exist(self,tag_name):
        return len(list(self.tags_db.find({"_id": {"$eq": tag_name}}))) > 0

    def add_tag(self, tag, related_tags, classified=False):
        self.tags_db.update_one({"_id": tag}, {"$set": {"repeat": 0}}, upsert=True)
        self.tags_db.update_one({"_id": tag}, {"$set": {"classified": classified}})

        for related_tag in related_tags:
            self.tags_db.update_one({"_id": tag}, {"$set": {"related."+related_tag: 0}})
        if len(related_tags) < 1:
            self.tags_db.update_one({"_id": tag}, {"$set": {"related": {}}})

    def add_collection(self, collection_name):
        self.collections_db.insert_one({"_id": collection_name,"tags": []})

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
