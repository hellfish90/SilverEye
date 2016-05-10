import pymongo


class LimitNotice:

    def __init__(self, mongo_client, database):
        self.mongo_client = mongo_client
        self.limit_notice_db = self.mongo_client[database]['TwitterLimitNotice']

    def save_new_twitter_counter(self, timestamp, track):
        self.limit_notice_db.insert_one({"timestamp": timestamp, "track": track})

    def get_limit_notice_by_dates(self, timestamp_init, timestamp_end):
            return self.limit_notice_db.find({"timestamp_init": {"$gte": timestamp_init, "$lt": timestamp_end}})

    def get_size(self):
        return self.limit_notice_db.count()