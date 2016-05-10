# -*- coding: utf-8 -*-
import unittest

from pymongo import MongoClient

from silverEyeViewer.QueryApp.DAO import LastTweet

example_tweet = {
    "contributors" : None,
    "truncated" : False,
    "text" : "@Netzai_Sandoval ¿podemos hablar? Saludos",
    "is_quote_status" : False,
    "in_reply_to_status_id" : 725132642132226048,
    "id" : 725324852484182016,
    "favorite_count" : 0,
    "source" : "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
    "retweeted" : False,
    "coordinates" : None,
    "timestamp_ms" : "1461765895373",
    "entities" : {
        "user_mentions" : [
            {
                "id" : 82728445,
                "indices" : [
                    0,
                    16
                ],
                "id_str" : "82728445",
                "screen_name" : "Netzai_Sandoval",
                "name" : "Netzaí Sandoval"
            }
        ],
        "symbols" : [],
        "hashtags" : [],
        "urls" : []
    },
    "in_reply_to_screen_name" : "Netzai_Sandoval",
    "id_str" : "725324852484182016",
    "retweet_count" : 0,
    "in_reply_to_user_id" : 82728445,
    "favorited" : False,
    "user" : {
        "follow_request_sent" : None,
        "profile_use_background_image" : True,
        "default_profile_image" : False,
        "id" : 55367373,
        "verified" : False,
        "profile_image_url_https" : "https://pbs.twimg.com/profile_images/715253540357218304/vcxH600o_normal.jpg",
        "profile_sidebar_fill_color" : "FFFFFF",
        "profile_text_color" : "333333",
        "followers_count" : 1505,
        "profile_sidebar_border_color" : "FFFFFF",
        "id_str" : "55367373",
        "profile_background_color" : "1A1B1F",
        "listed_count" : 46,
        "profile_background_image_url_https" : "https://pbs.twimg.com/profile_background_images/441733157771939841/efNtniLm.jpeg",
        "utc_offset" : -18000,
        "statuses_count" : 1918,
        "description" : "Reportera @Reforma,\nmultimedia journalism @SussexUni, estudios en migración @elcolef",
        "friends_count" : 1499,
        "location" : "México DF",
        "profile_link_color" : "E31C4D",
        "profile_image_url" : "http://pbs.twimg.com/profile_images/715253540357218304/vcxH600o_normal.jpg",
        "following" : None,
        "geo_enabled" : False,
        "profile_banner_url" : "https://pbs.twimg.com/profile_banners/55367373/1401204733",
        "profile_background_image_url" : "http://pbs.twimg.com/profile_background_images/441733157771939841/efNtniLm.jpeg",
        "name" : "Silvia Garduño",
        "lang" : "es",
        "profile_background_tile" : True,
        "favourites_count" : 48,
        "screen_name" : "silvielena",
        "notifications" : None,
        "url" : None,
        "created_at" : "Thu Jul 09 21:25:00 +0000 2009",
        "contributors_enabled" : False,
        "time_zone" : "Mexico City",
        "protected" : False,
        "default_profile" : False,
        "is_translator" : False
    },
    "geo" : None,
    "in_reply_to_user_id_str" : "82728445",
    "lang" : "es",
    "created_at" : "Wed Apr 27 14:04:55 +0000 2016",
    "filter_level" : "low",
    "in_reply_to_status_id_str" : "725132642132226048",
    "place" : None
}


class TestDAOLastTweet(unittest.TestCase):

    database_name = "Test"

    def test_update_new_tweet(self):
        client = MongoClient("127.0.0.1", 27017, connect=True)

        dao_last_tweet = LastTweet(client, self.database_name)
        dao_last_tweet.update_last_tweet({"tweet": example_tweet})

        self.assertEqual(dao_last_tweet.get_size(), 1)

    def test_update_two_times_new_user(self):
        client = MongoClient("127.0.0.1", 27017, connect=True)

        dao_last_tweet = LastTweet(client, self.database_name)
        dao_last_tweet.update_last_tweet({"tweet": example_tweet})
        dao_last_tweet.update_last_tweet({"tweet": {}})

        self.assertEqual(dao_last_tweet.get_size(), 1)
        self.assertNotEqual(example_tweet, dao_last_tweet.get_last_tweet())


if __name__ == '__main__':
    unittest.main()