from django.shortcuts import redirect
from django.shortcuts import render
from pymongo import MongoClient

from old.core import SilverEye

server = '127.0.0.1'

port = 27017

silver_eye_core =None


def silver_eye_status(request):
    client = MongoClient(server, port, connect=True)
    return render(request, 'status.html')


def get_last_tweet(request):
    client = MongoClient(server, port, connect=True)
    tweet = client.SilverEye.lasTweet.find()
    tweet = [i for i in tweet][0]
    request.last_tweet = tweet

    return render(request, 'last_tweet.html', {"last_tweet": tweet['tweet']['text']})


def init_twitter_extractor(request):
    silver_eye_core = SilverEye(server, port)
    silver_eye_core.start_extractor()

    return redirect('/query/manage/status')


def stop_twitter_extractor(request):
    if silver_eye_core is not None:
        silver_eye_core.stop_extractor()
    else:
        print "Error Stop"
    return redirect('/query/manage/status')


def restart_twitter_extractor(request):
    if silver_eye_core is not None:
        silver_eye_core.stop_extractor()
        init_twitter_extractor(request)
    else:
        print "Error restart"
    return redirect('/query/manage/status')