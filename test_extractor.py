from twitter_extractor import Extractor
from pymongo import MongoClient

if __name__ == "__main__":

    client = MongoClient('0.0.0.0', 27017, connect=True)

    extractor = Extractor(client)

    print extractor.get_all_tags()