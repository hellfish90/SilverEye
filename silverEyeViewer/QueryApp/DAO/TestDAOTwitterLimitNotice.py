# -*- coding: utf-8 -*-
import time
import unittest

from pymongo import MongoClient

from silverEyeViewer.QueryApp.DAO.DAOLimitNotice import LimitNotice


class TestDAOTwitterLimitNotice(unittest.TestCase):

    client = MongoClient("127.0.0.1", 27017, connect=True)
    database_name = "Test"

    def setUp(self):
        self.client[self.database_name]['TwitterLimitNotice'].delete_many({})
        pass

    def test_update_new_result(self):

        dao_twitter_counter = LimitNotice(self.client, self.database_name)

        dao_twitter_counter.save_new_twitter_counter(int(time.time()), 2)

        self.assertEqual(dao_twitter_counter.get_size(), 1)

    def test_update_two_new_result(self):

        dao_twitter_counter = LimitNotice(self.client, self.database_name)

        dao_twitter_counter.save_new_twitter_counter(int(time.time()), 2)

        dao_twitter_counter.save_new_twitter_counter(int(time.time()), 3)

        self.assertEqual(dao_twitter_counter.get_size(), 2)

if __name__ == '__main__':
    unittest.main()