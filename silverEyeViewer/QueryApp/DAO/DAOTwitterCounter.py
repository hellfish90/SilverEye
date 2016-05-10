import pymongo


class TwitterCounter:

    def __init__(self, mongo_client, database):
        self.mongo_client = mongo_client
        self.twitter_counter_db = self.mongo_client[database]['TwitterCounter']

    def save_new_twitter_counter(self, timestamp_init, timestamp_end, result_collections, tweets_num, collection_counter):
        self.twitter_counter_db.insert_one({"timestamp_init": timestamp_init, "timestamp_end": timestamp_end,
                                            "result_collections": result_collections, "tweets_num": tweets_num,
                                            "collection_counter": collection_counter})

    def get_twitter_counter_by_dates(self, timestamp_init, timestamp_end):
        return self.twitter_counter_db.find({"timestamp_init": {"$gte": timestamp_init, "$lte": timestamp_end}})

    def get_size(self):
        return self.twitter_counter_db.count()