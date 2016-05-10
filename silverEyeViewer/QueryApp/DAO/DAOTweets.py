import pymongo


class Tweets:

    def __init__(self, mongo_client, database):
        self.mongo_client = mongo_client
        self.tweets_db = self.mongo_client[database]['Tweets']

    def save_new_tweet(self, id, tweet):
        self.tweets_db.update({"_id": id}, {"tweet": tweet}, upsert=True)

    def get_tweet_by_dates(self, timestamp_init, timestamp_end):
        return self.tweets_db.find({"tweet.timestamp_ms": {"$gte": timestamp_init, "$lte": timestamp_end}})

    def get_size(self):
        return self.tweets_db.count()