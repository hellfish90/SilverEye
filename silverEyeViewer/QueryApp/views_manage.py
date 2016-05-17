from django.shortcuts import redirect
from django.shortcuts import render
from Core.DAO.DAOLastTweet import LastTweet
from Core.Config.configuration import Configuration


def silver_eye_status(request):
    return render(request, 'status.html')


def get_last_tweet(request):
    configuration = Configuration()
    client = configuration.get_client()
    database_name = configuration.get_database_name()

    dao_last_tweet = LastTweet(client, database_name)

    tweet = dao_last_tweet.get_last_tweet()["tweet"]
    request.last_tweet = tweet

    return render(request, 'last_tweet.html', {"last_tweet": tweet['tweet']['text']})


def init_twitter_extractor(request):


    return redirect('/query/manage/status')


def stop_twitter_extractor(request):

    return redirect('/query/manage/status')


def restart_twitter_extractor(request):

    return redirect('/query/manage/status')