import pymongo


class LastTweet:

    def __init__(self, mongo_client, database):
        self.mongo_client = mongo_client
        self.last_tweet_collection = self.mongo_client[database]['LastTweet']

    def get_last_tweet(self):
        return self.last_tweet_collection.find_one({'_id': "unique"})

    def update_last_tweet(self, tweet):
        self.last_tweet_collection.update_one({"_id": "unique"}, {"$set": {"tweet": tweet}}, upsert=True)

    def get_size(self):
        return self.last_tweet_collection.count()
