# -*- coding: utf-8 -*-
import time
import unittest

from pymongo import MongoClient

from silverEyeViewer.QueryApp.Core.DAO import TwitterCounter


class TestDAOTwitterCounter(unittest.TestCase):

    client = MongoClient("127.0.0.1", 27017, connect=True)
    database_name = "Test"

    def setUp(self):
        self.client[self.database_name]['TwitterCounter'].delete_many({})
        pass

    def test_update_new_result(self):

        dao_twitter_counter = TwitterCounter(self.client, self.database_name)

        dao_twitter_counter.save_new_twitter_counter(int(time.time()), int(time.time())+1000, {"PP": 30, "PSC": -50},
                                                     12345, {"PP": 10, "PSC": -20})

        self.assertEqual(dao_twitter_counter.get_size(), 1)

    def test_update_two_new_result(self):

        dao_twitter_counter = TwitterCounter(self.client, self.database_name)

        dao_twitter_counter.save_new_twitter_counter(int(time.time()), int(time.time())+1000, {"PP": 30, "PSC": -50},
                                                     12345, {"PP": 10, "PSC": -20})

        dao_twitter_counter.save_new_twitter_counter(int(time.time()), int(time.time())+1000, {"PP": 30, "PSC": -50},
                                                     12345, {"PP": 10, "PSC": -20})

        self.assertEqual(dao_twitter_counter.get_size(), 2)

    def test_timestamp_query(self):

        dao_twitter_counter = TwitterCounter(self.client, self.database_name)

        dao_twitter_counter.save_new_twitter_counter(int(time.time()), int(time.time())+1000, {"PP": 30, "PSC": -50},
                                                     12345, {"PP": 10, "PSC": -20})
        time.sleep(1)
        start_query = int(time.time())



        dao_twitter_counter.save_new_twitter_counter(int(time.time()), int(time.time())+1000, {"PP": 30, "PSC": -50},
                                                     12345, {"PP": 10, "PSC": -20})

        dao_twitter_counter.save_new_twitter_counter(int(time.time()), int(time.time())+1000, {"PP": 30, "PSC": -50},
                                                     12345, {"PP": 10, "PSC": -20})

        dao_twitter_counter.save_new_twitter_counter(int(time.time()), int(time.time())+1000, {"PP": 30, "PSC": -50},
                                                     12345, {"PP": 10, "PSC": -20})



        dao_twitter_counter.save_new_twitter_counter(int(time.time()), int(time.time())+1000, {"PP": 30, "PSC": -50},
                                                     12345, {"PP": 10, "PSC": -20})
        end_query = int(time.time())
        time.sleep(1)

        dao_twitter_counter.save_new_twitter_counter(int(time.time()), int(time.time())+1000, {"PP": 30, "PSC": -50},
                                                     12345, {"PP": 10, "PSC": -20})

        result_size = dao_twitter_counter.get_twitter_counter_by_dates(start_query, end_query).count()

        self.assertEqual(dao_twitter_counter.get_size()-2, result_size)




if __name__ == '__main__':
    unittest.main()