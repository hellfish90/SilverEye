import pymongo


class AnalyzedTweets:

    def __init__(self, mongo_client, database):
        self.mongo_client = mongo_client
        self.analyzed_tweets = self.mongo_client[database]['AnalyzedTweets']

    def save_new_analyzed_tweet(self, user_id, tweet_id, collections, tags, coordinates,
                                timestamp, place, polarity, text):

        self.analyzed_tweets.update({"user_id": user_id, "tweet_id": tweet_id}, {"$set": {"collections": collections}}, upsert=True)
        self.analyzed_tweets.update({"user_id": user_id, "tweet_id": tweet_id}, {"$set": {"tags": tags}}, upsert=True)
        self.analyzed_tweets.update({"user_id": user_id, "tweet_id": tweet_id}, {"$set": {"coordinates": coordinates}}, upsert=True)
        self.analyzed_tweets.update({"user_id": user_id, "tweet_id": tweet_id}, {"$set": {"timestamp": timestamp}}, upsert=True)
        self.analyzed_tweets.update({"user_id": user_id, "tweet_id": tweet_id}, {"$set": {"place": place}}, upsert=True)
        self.analyzed_tweets.update({"user_id": user_id, "tweet_id": tweet_id}, {"$set": {"polarity": polarity}}, upsert=True)
        self.analyzed_tweets.update({"user_id": user_id, "tweet_id": tweet_id}, {"$set": {"text": text}}, upsert=True)

    def get_analyzed_tweets(self):
        return self.analyzed_tweets.find().sort("timestamp", pymongo.ASCENDING)

    def get_size(self):
        return self.analyzed_tweets.count()

    # TODO not work well....
    def get_analyzed_tweets_by_dates(self, timestamp_init, timestamp_end):
        return self.analyzed_tweets.find({"timestamp": {"$gte": str(timestamp_init), "$lte": str(timestamp_end)}})

    def get_tweets_by_user(self, user_id):
        return self.analyzed_tweets.find({"user_id": {"$eq": user_id}})

    def get_first_and_last_timestamp(self):

        last = list(self.analyzed_tweets.find().sort("timestamp", pymongo.DESCENDING))[0]
        last = last["timestamp"]

        first = list(self.analyzed_tweets.find().sort("timestamp", pymongo.ASCENDING))[0]
        first = first["timestamp"]

        return {"first": first, "last": last}

