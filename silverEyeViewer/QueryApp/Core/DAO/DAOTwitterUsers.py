import pymongo


class TwitterUsers:

    def __init__(self, mongo_client, database):
        self.mongo_client = mongo_client
        self.twitter_users_collection = self.mongo_client[database]['TwitterUsers']

    def save_new_user(self, id, user):
        self.twitter_users_collection.update({"_id": id}, {"user": user}, upsert=True)

    def get_user_by_id(self, id):
        return self.twitter_users_collection.find_one({"_id": {"$eq": id}})

    def get_size(self):
        return self.twitter_users_collection.count()

    def get_all_users(self):
        return self.twitter_users_collection.find()
