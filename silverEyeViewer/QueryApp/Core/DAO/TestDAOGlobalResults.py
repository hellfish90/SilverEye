import time
import unittest

from pymongo import MongoClient

from silverEyeViewer.QueryApp.Core.DAO.DAOGlobalResults import GlobalResults


class TestDAOGlobalResults(unittest.TestCase):

    database_name = "Test"

    def test_update_new_result(self):
        client = MongoClient("127.0.0.1", 27017, connect=True)

        daoGlobalesults = GlobalResults(client, self.database_name)

        daoGlobalesults.update_global_results({"PP": 80, "PSC": -10}, 20000, 2000, int(time.time()),
                                              {"PP": 20, "PSC": 30})

        self.assertEqual(daoGlobalesults.get_size(), 1)

    def test_update_two_new_result(self):
        client = MongoClient("127.0.0.1", 27017, connect=True)

        daoGlobalesults = GlobalResults(client, self.database_name)

        daoGlobalesults.update_global_results({"PP": 80, "PSC": -10}, 20000, 2000, int(time.time()),
                                              {"PP": 20, "PSC": 30})
        daoGlobalesults.update_global_results({"CIUDADANOS": 80, "PSC": -10}, 201000, 20100, int(time.time()),
                                              {"PP": 20, "PSC": 50})

        self.assertEqual(daoGlobalesults.get_size(), 1)


if __name__ == '__main__':
    unittest.main()