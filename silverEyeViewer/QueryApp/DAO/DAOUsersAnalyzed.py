import pymongo


class UsersAnalyzed:

    def __init__(self, mongo_client, database):
        self.mongo_client = mongo_client
        self.users_analyzed_db = self.mongo_client[database]['UsersAnalyzed']

    def save_update_users_analyzed(self, user_id, result_collections, tweets_num, timestamp_last_update,
                                   collection_counter, tags_counter):

        self.users_analyzed_db.update({"_id": user_id}, {"$set": {"result_collections": result_collections}}, upsert=True)
        self.users_analyzed_db.update({"_id": user_id}, {"$set": {"tweets_num": tweets_num}}, upsert=True)
        self.users_analyzed_db.update({"_id": user_id}, {"$set": {"timestamp_last_update": timestamp_last_update}}, upsert=True)
        self.users_analyzed_db.update({"_id": user_id}, {"$set": {"collection_counter": collection_counter}}, upsert=True)
        self.users_analyzed_db.update({"_id": user_id}, {"$set": {"tags_counter": tags_counter}}, upsert=True)

    def user_analyzed_exist(self, user_id):
        return self.users_analyzed_db.find_one({"_id": {"$eq": user_id}})

    def get_all_users_analyzed(self):
        return self.users_analyzed_db.find()

    def get_size(self):
        return self.users_analyzed_db.count()

