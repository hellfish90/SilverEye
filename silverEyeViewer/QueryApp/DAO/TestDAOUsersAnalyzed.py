import time
import unittest

from DAOUsersAnalyzed import UsersAnalyzed
from pymongo import MongoClient


class TestDAOUsersAnalyzed(unittest.TestCase):

    database_name = "Test"

    def test_update_new_user(self):
        client = MongoClient("127.0.0.1", 27017, connect=True)

        usersAnalyzedDAO = UsersAnalyzed(client, self.database_name)
        usersAnalyzedDAO.save_update_users_analyzed(1212313131, {"PP": 1, "PSC": -1}, 25, int(time.time()), {"PP": 20, "PSC": 50})

        self.assertEqual(usersAnalyzedDAO.get_size(), 1)

    def test_update_two_times_new_user(self):
        client = MongoClient("127.0.0.1", 27017, connect=True)

        usersAnalyzedDAO = UsersAnalyzed(client, self.database_name)
        usersAnalyzedDAO.save_update_users_analyzed(1212313131, {"PP": 1, "PSC": -1}, 25, int(time.time()), {"PP": 20, "PSC": 50})
        usersAnalyzedDAO.save_update_users_analyzed(1212313131, {"PP": 50, "PSC": -1}, 50, int(time.time()), {"PP": 20, "PSC": 50})

        self.assertEqual(usersAnalyzedDAO.get_size(), 1)


if __name__ == '__main__':
    unittest.main()