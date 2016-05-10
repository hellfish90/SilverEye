# -*- coding: utf-8 -*-
import unittest

from pymongo import MongoClient

from silverEyeViewer.QueryApp.DAO import TwitterUsers

example_user = {
    "_id" : "5645b9c0af705318078b35a9",
    "follow_request_sent" : None,
    "profile_use_background_image" : True,
    "default_profile_image" : False,
    "id" : 2251285345,
    "verified" : False,
    "profile_image_url_https" : "https://pbs.twimg.com/profile_images/661270232321929217/zQAp37ny_normal.jpg",
    "profile_sidebar_fill_color" : "EFEFEF",
    "profile_text_color" : "333333",
    "followers_count" : 673,
    "profile_sidebar_border_color" : "EEEEEE",
    "id_str" : "2251285345",
    "profile_background_color" : "131516",
    "listed_count" : 1,
    "profile_background_image_url_https" : "https://abs.twimg.com/images/themes/theme14/bg.gif",
    "utc_offset" : -7200,
    "statuses_count" : 20455,
    "description" : "Club Atletico River Plate (L  #14\n05/08/15 ||\nLa banda del perdido #Promo15 #Brc #Up#222",
    "friends_count" : 459,
    "location" : "San Bernardo, Argentina",
    "profile_link_color" : "009999",
    "profile_image_url" : "http://pbs.twimg.com/profile_images/661270232321929217/zQAp37ny_normal.jpg",
    "following" : None,
    "geo_enabled" : True,
    "profile_banner_url" : "https://pbs.twimg.com/profile_banners/2251285345/1444951621",
    "profile_background_image_url" : "http://abs.twimg.com/images/themes/theme14/bg.gif",
    "name" : "Ramiro❕",
    "lang" : "es",
    "profile_background_tile" : True,
    "favourites_count" : 2544,
    "screen_name" : "RamiiroDamian",
    "notifications" : None,
    "url" : "https://www.facebook.com/Rrramiro.16",
    "created_at" : "Wed Dec 18 02:29:00 +0000 2013",
    "contributors_enabled" : False,
    "time_zone" : "Brasilia",
    "protected" : False,
    "default_profile" : False,
    "is_translator" : False
}


class TestDAOTwitterUsers(unittest.TestCase):

    client = MongoClient("127.0.0.1", 27017, connect=True)
    database_name = "Test"

    def setUp(self):
        self.client[self.database_name]['TwitterUsers'].delete_many({})
        pass

    def test_update_new_result(self):

        dao_twitter_user = TwitterUsers(self.client, self.database_name)
        dao_twitter_user.save_new_user(1234, example_user)

        self.assertEqual(dao_twitter_user.get_size(), 1)

    def test_update_two_new_result(self):

        dao_twitter_user = TwitterUsers(self.client, self.database_name)
        dao_twitter_user.save_new_user(1234, example_user)
        dao_twitter_user.save_new_user(4567, example_user)

        self.assertEqual(dao_twitter_user.get_size(), 2)

    def test_update_two_new_result(self):

        dao_twitter_user = TwitterUsers(self.client, self.database_name)
        dao_twitter_user.save_new_user(1234, example_user)
        dao_twitter_user.save_new_user(1234, example_user)

        self.assertEqual(dao_twitter_user.get_size(), 1)

if __name__ == '__main__':
    unittest.main()