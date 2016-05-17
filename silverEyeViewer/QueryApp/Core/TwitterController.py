# -*- coding: utf-8 -*-
import json
import tweepy
import threading

from TwitterListener import TwitterStream
import os

class TwitterController:

    def __init__(self, silver_eye_core):
        self.silver_eye_core = silver_eye_core
        self.twitter_stream = None

    def start(self, keywords):
        self.twitter_stream = self.TwitterStreamingThread(self, keywords)
        self.twitter_stream.start()
        pass

    def stop(self):
        self.twitter_stream.stop()

    def on_tweet_received(self, tweet):
        if self.silver_eye_core is None:
            print tweet["text"]
        else:
            self.silver_eye_core.analyze_tweet(tweet)

    def on_error(self, error):
        ##TODO guardar errors
        print "ERROR:"+error
        print "\n"

    def on_limit_notice(self, notice):
        ##TODO guardar limit noticia
        print "Limit:"+notice

    class TwitterStreamingThread (threading.Thread):

            def __init__(self, twitter_controller, keywords):
                threading.Thread.__init__(self)
                self.twitter_listener = None
                self.search = True
                self.twitter_controller = twitter_controller
                self.keywords = keywords

            def run(self):
                self.init_twitter_extractor()

            def init_twitter_extractor(self):
                with open(os.path.dirname(os.path.dirname(__file__)) +'/Core/Config/config.json', 'r') as f:
                    config = json.load(f)
                    access_token = config['access_token']
                    access_token_secret = config['access_token_secret']
                    consumer_key = config['consumer_key']
                    consumer_secret = config['consumer_secret']

                    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                    auth.set_access_token(access_token, access_token_secret)
                    api = tweepy.API(auth)

                    while self.search:
                        try:
                            self.twitter_listener = tweepy.streaming.Stream(auth, TwitterStream(api, self.twitter_controller))
                            self.twitter_listener.filter(track=self.keywords)

                        except Exception as e:
                            self.twitter_controller.on_error("TwitterStreamingThread->"+e.message)
                            continue

            def stop(self):
                self.search = False
                self.twitter_listener.disconnect()

            def stopped(self):
                return self._stop.isSet()


if __name__ == "__main__":
    twitter_controller = TwitterController(None)
    twitter_controller.start(["hello"])
    my_input = raw_input("Please press enter to stop")
    twitter_controller.stop()
    my_input = raw_input("Please press enter to stop")
    twitter_controller.start(["hello"])
