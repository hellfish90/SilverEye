# -*- coding: utf-8 -*-
import unittest

from pymongo import MongoClient

from silverEyeViewer.QueryApp.Core.DAO import Tweets

example_tweet2 = {
    "_id" : "5645b9c0af705318078b35a8",
    "contributors" : None,
    "truncated" : False,
    "text" : "Buen diaa,a seguir durmiendo!",
    "is_quote_status" : False,
    "in_reply_to_status_id" : None,
    "id" : 665112333916721152,
    "favorite_count" : 0,
    "source" : "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>",
    "retweeted" : False,
    "coordinates" : None,
    "timestamp_ms" : "22222222222",
    "entities" : {
        "user_mentions" : [],
        "symbols" : [],
        "hashtags" : [],
        "urls" : []
    },
    "in_reply_to_screen_name" : None,
    "id_str" : "665112333916721152",
    "retweet_count" : 0,
    "in_reply_to_user_id" : None,
    "favorited" : False,
    "user" : {
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
    },
    "geo" : None,
    "in_reply_to_user_id_str" : None,
    "lang" : "es",
    "created_at" : "Fri Nov 13 10:21:52 +0000 2015",
    "filter_level" : "low",
    "in_reply_to_status_id_str" : None,
    "place" : {
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
        "name" : "Mar de Ajó"
    }
}

example_tweet2 = {
    "_id" : "5645b9c0af705318078b35a8",
    "contributors" : None,
    "truncated" : False,
    "text" : "Buen diaa,a seguir durmiendo!",
    "is_quote_status" : False,
    "in_reply_to_status_id" : None,
    "id" : 665112333916721152,
    "favorite_count" : 0,
    "source" : "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>",
    "retweeted" : False,
    "coordinates" : None,
    "timestamp_ms" : "4444444444444",
    "entities" : {
        "user_mentions" : [],
        "symbols" : [],
        "hashtags" : [],
        "urls" : []
    },
    "in_reply_to_screen_name" : None,
    "id_str" : "665112333916721152",
    "retweet_count" : 0,
    "in_reply_to_user_id" : None,
    "favorited" : False,
    "user" : {
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
    },
    "geo" : None,
    "in_reply_to_user_id_str" : None,
    "lang" : "es",
    "created_at" : "Fri Nov 13 10:21:52 +0000 2015",
    "filter_level" : "low",
    "in_reply_to_status_id_str" : None,
    "place" : {
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
        "name" : "Mar de Ajó"
    }
}

example_tweet = {
    "_id" : "5645b9c0af705318078b35a8",
    "contributors" : None,
    "truncated" : False,
    "text" : "Buen diaa,a seguir durmiendo!",
    "is_quote_status" : False,
    "in_reply_to_status_id" : None,
    "id" : 665112333916721152,
    "favorite_count" : 0,
    "source" : "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>",
    "retweeted" : False,
    "coordinates" : None,
    "timestamp_ms" : "333333333333",
    "entities" : {
        "user_mentions" : [],
        "symbols" : [],
        "hashtags" : [],
        "urls" : []
    },
    "in_reply_to_screen_name" : None,
    "id_str" : "665112333916721152",
    "retweet_count" : 0,
    "in_reply_to_user_id" : None,
    "favorited" : False,
    "user" : {
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
    },
    "geo" : None,
    "in_reply_to_user_id_str" : None,
    "lang" : "es",
    "created_at" : "Fri Nov 13 10:21:52 +0000 2015",
    "filter_level" : "low",
    "in_reply_to_status_id_str" : None,
    "place" : {
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
        "name" : "Mar de Ajó"
    }
}


class TestDAOTweets(unittest.TestCase):

    client = MongoClient("127.0.0.1", 27017, connect=True)
    database_name = "Test"

    def setUp(self):
        #self.client[self.database_name]['TwitterTweets'].delete_many({})
        pass

    def test_update_new_result(self):

        dao_twitter_user = Tweets(self.client, self.database_name)
        dao_twitter_user.save_new_tweet(1234, example_tweet)

        self.assertEqual(dao_twitter_user.get_size(), 1)

    def test_update_two_new_result(self):

        dao_twitter_user = Tweets(self.client, self.database_name)
        dao_twitter_user.save_new_tweet(1234, example_tweet)
        dao_twitter_user.save_new_tweet(4567, example_tweet2)

        self.assertEqual(dao_twitter_user.get_size(), 2)

    def test_update_two_new_result(self):

        dao_twitter_user = Tweets(self.client, self.database_name)
        dao_twitter_user.save_new_tweet(1234, example_tweet)
        dao_twitter_user.save_new_tweet(1234, example_tweet)

        self.assertEqual(dao_twitter_user.get_size(), 1)

    def test_query_timestamp(self):

        dao_twitter_user = Tweets(self.client, self.database_name)
        result_size = dao_twitter_user.get_tweet_by_dates("22222222222", "4444444444444").count()

        self.assertEqual(result_size, 1)


if __name__ == '__main__':
    unittest.main()