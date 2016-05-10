import pymongo


class TemporalTwitterAnalysis:

    def __init__(self, mongo_client, database):
        self.mongo_client = mongo_client
        self.twitter_counter_db = self.mongo_client[database]['TemporalTwitterAnalysis']

    def save_new_twitter_counter(self, timestamp_init, timestamp_end, result_collections, num_tweets,
                                    timestamp_last_update, collection_counter, collection_global_positive_results,
                                    collection_global_neutral_results, collection_global_negative_results):

        self.twitter_counter_db.insert_one({"timestamp_init": timestamp_init, "timestamp_end": timestamp_end,
                                            "result_collections": result_collections, "num_tweets": num_tweets,
                                            "timestamp_last_update": timestamp_last_update,
                                            "collection_counter": collection_counter,
                                            "collection_global_positive_results": collection_global_positive_results,
                                            "collection_global_neutral_results": collection_global_neutral_results,
                                            "collection_global_negative_results": collection_global_negative_results})

    def get_twitter_counter_by_dates(self, timestamp_init, timestamp_end):
        return self.twitter_counter_db.find({"timestamp_init": {"$gte": timestamp_init, "$lte": timestamp_end}})

    def get_size(self):
        return self.twitter_counter_db.count()

    def remove_all(self):
        self.twitter_counter_db.delete_many({})
