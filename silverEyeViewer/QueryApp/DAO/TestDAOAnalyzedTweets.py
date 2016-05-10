# -*- coding: utf-8 -*-
import time
import unittest

from pymongo import MongoClient

from silverEyeViewer.QueryApp.DAO import AnalyzedTweets

place_example = {
    "full_name" : "Mar de Ajó, Argentina",
    "url" : "https://api.twitter.com/1.1/geo/id/003090295e0dcbe4.json",
    "country" : "Argentina",
    "place_type" : "city",
    "bounding_box" : {
        "type" : "Polygon",
        "coordinates" : [
            [
                [
                    -56.704345,
                    -36.759377
                ],
                [
                    -56.704345,
                    -36.692663
                ],
                [
                    -56.673212,
                    -36.692663
                ],
                [
                    -56.673212,
                    -36.759377
                ]
            ]
        ]
    },
    "country_code" : "AR",
    "attributes" : {},
    "id" : "003090295e0dcbe4",
    "name": "Mar de Ajó"
}


class TestDAOAnalyzedTweets(unittest.TestCase):

    client = MongoClient("127.0.0.1", 27017, connect=True)
    database_name = "Test"

    def setUp(self):
        self.client[self.database_name]['AnalyzedTweets'].delete_many({})
        pass

    def test_update_new_result(self):

        dao_analyzed_tweets = AnalyzedTweets(self.client, self.database_name)

        dao_analyzed_tweets.save_new_analyzed_tweet(1234, 1234, ["PP", "PSOE"], ["@mariano", "@rajoy"],
                                                {"type": "Point", "coordinates": [-77.01944444, -12.12083333]},
                                                int(time.time()), place_example, 0,
                                                "esto es una fiesta @mariano @rajoy")

        self.assertEqual(dao_analyzed_tweets.get_size(), 1)

    def test_update_two_new_result(self):

        dao_analyzed_tweets = AnalyzedTweets(self.client, self.database_name)

        dao_analyzed_tweets.save_new_analyzed_tweet(1234, 1234, ["PP", "PSOE"], ["@mariano", "@rajoy"],
                                                {"type": "Point", "coordinates": [-77.01944444, -12.12083333]},
                                                int(time.time()), place_example, 0,
                                                "esto es una fiesta @mariano @rajoy")

        dao_analyzed_tweets.save_new_analyzed_tweet(1234, 1234, ["PP", "PSOE"], ["@mariano", "@rajoy"],
                                                {"type": "Point", "coordinates": [-77.01944444, -12.12083333]},
                                                int(time.time()), place_example, 1,
                                                "esto es una fiesta @mariano @rajoy")

        self.assertEqual(dao_analyzed_tweets.get_size(), 1)

    def test_timestamp_query(self):

        dao_analyzed_tweets = AnalyzedTweets(self.client, self.database_name)

        dao_analyzed_tweets.save_new_analyzed_tweet(1111, 1111, ["PP", "PSOE"], ["@mariano", "@rajoy"],
                                                {"type": "Point", "coordinates": [-77.01944444, -12.12083333]},
                                                int(time.time()), place_example, 0,
                                                "esto es una fiesta @mariano @rajoy")
        time.sleep(1)
        start_query = int(time.time())



        dao_analyzed_tweets.save_new_analyzed_tweet(2222, 2222, ["PP", "PSOE"], ["@mariano", "@rajoy"],
                                                {"type": "Point", "coordinates": [-77.01944444, -12.12083333]},
                                                int(time.time()), place_example, 1,
                                                "esto es una fiesta @mariano @rajoy")

        dao_analyzed_tweets.save_new_analyzed_tweet(3333, 3333, ["PP", "PSOE"], ["@mariano", "@rajoy"],
                                                {"type": "Point", "coordinates": [-77.01944444, -12.12083333]},
                                                int(time.time()), place_example, 1,
                                                "esto es una fiesta @mariano @rajoy")

        dao_analyzed_tweets.save_new_analyzed_tweet(4444, 4444, ["PP", "PSOE"], ["@mariano", "@rajoy"],
                                                {"type": "Point", "coordinates": [-77.01944444, -12.12083333]},
                                                int(time.time()), place_example, 1,
                                                "esto es una fiesta @mariano @rajoy")



        dao_analyzed_tweets.save_new_analyzed_tweet(5555, 5555, ["PP", "PSOE"], ["@mariano", "@rajoy"],
                                                {"type": "Point", "coordinates": [-77.01944444, -12.12083333]},
                                                int(time.time()), place_example, 1,
                                                "esto es una fiesta @mariano @rajoy")
        end_query = int(time.time())
        time.sleep(1)

        dao_analyzed_tweets.save_new_analyzed_tweet(6666, 6666, ["PP", "PSOE"], ["@mariano", "@rajoy"],
                                                {"type": "Point", "coordinates": [-77.01944444, -12.12083333]},
                                                int(time.time()), place_example, 1,
                                                "esto es una fiesta @mariano @rajoy")

        result_size = dao_analyzed_tweets.get_analyzed_tweets_by_dates(start_query, end_query).count()

        self.assertEqual(dao_analyzed_tweets.get_size()-2, result_size)




if __name__ == '__main__':
    unittest.main()