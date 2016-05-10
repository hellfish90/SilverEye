from pymongo import MongoClient

from DAOAnalyzedTweets import AnalyzedTweets

client = MongoClient("127.0.0.1", 27017, connect=True)
database_name = "Test"
dao_analyzed_tweets = AnalyzedTweets(client, database_name)

result = dao_analyzed_tweets.get_first_and_last_timestamp()

print result