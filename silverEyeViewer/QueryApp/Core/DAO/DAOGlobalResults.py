import pymongo


class GlobalResults:
    def __init__(self, mongo_client, database):
        self.mongo_client = mongo_client
        self.global_results_db = self.mongo_client[database]['GlobalResults']

    def get_global_results(self):
        return self.global_results_db.find_one({'_id': "unique"})

    def update_global_results(self, result_collections, num_tweets, users_num, timestamp_last_update,
                              collection_counter, collection_global_positive_results,
                              collection_global_neutral_results, collection_global_negative_results):

        self.global_results_db.update_one({"_id": "unique"},
                                          {"$set": {"result_collections": result_collections}}, upsert=True)
        self.global_results_db.update_one({"_id": "unique"},
                                          {"$set": {"num_tweets": num_tweets}}, upsert=True)
        self.global_results_db.update_one({"_id": "unique"},
                                          {"$set": {"users_num": users_num}}, upsert=True)
        self.global_results_db.update_one({"_id": "unique"},
                                          {"$set": {"timestamp_last_update": timestamp_last_update}}, upsert=True)
        self.global_results_db.update_one({"_id": "unique"},
                                          {"$set": {"collection_counter": collection_counter}}, upsert=True)
        self.global_results_db.update_one({"_id": "unique"},
                                          {"$set": {"collection_global_positive_results":
                                                    collection_global_positive_results}}, upsert=True)
        self.global_results_db.update_one({"_id": "unique"},
                                          {"$set": {"collection_global_neutral_results":
                                                    collection_global_neutral_results}}, upsert=True)
        self.global_results_db.update_one({"_id": "unique"},
                                          {"$set": {"collection_global_negative_results":
                                                    collection_global_negative_results}}, upsert=True)

    def get_size(self):
        return self.global_results_db.count()
