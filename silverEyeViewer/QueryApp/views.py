# !/usr/bin/python

# -*- coding: utf-8 -*-

from django.shortcuts import render

from .forms import AnalysisForm


# Create your views here.

from pymongo import MongoClient
import opener


def text_analysis(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AnalysisForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            results = opener.analyze_text(form.data['data'])
            print results

            return render(request, 'sentimentQuery.html', {'form': form, 'results': results, 'text': form.data['data']})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnalysisForm()

    return render(request, 'sentimentQuery.html', {'form': form})


def list_twitter_users(request, limitnumber=0, maxnumber=150):

    #Dev
    client = MongoClient('192.168.101.128', 27017)

    #Prod
    #client = MongoClient('127.0.0.1', 27017)

    limitnumber = int(limitnumber)
    maxnumber = int(maxnumber)

    data = client.SilverEye.twitterUser.find()[limitnumber:maxnumber]


    return render(request, 'listUsersTwitter.html', {'users': data})


def list_twitter_status(request, limitnumber=0, maxnumber=150):

    #Dev
    client = MongoClient('192.168.101.128', 27017)

    #Prod
    #client = MongoClient('127.0.0.1', 27017)

    limitnumber = int(limitnumber)
    maxnumber = int(maxnumber)

    data = client.SilverEye.twitterPolitical.find()[limitnumber:maxnumber]

    dataSend = []

    for tweet in data:
        print tweet['text']
        print tweet['place']

        text = tweet['text'].encode('utf8')

        sentiment = opener.analyze_text(text)
        #print sentiment
        color = get_color_by_sentiment(sentiment)
        entities = get_entities(text)
        relevantTweet = {'tweet':tweet['text'], 'sentiment':sentiment, 'place':tweet['place'], 'color':color, 'entities': entities}

        dataSend.append(relevantTweet)

    return render(request, 'listStatusTwitter.html', {'status': dataSend})

def list_twitter_users_analized(request, limitnumber=0, maxnumber=150):

    #Dev
    client = MongoClient('0.0.0.0', 1234)

    db_destiny_user = client.SilverEye['TestSentimentUser']


    limitnumber = int(limitnumber)
    maxnumber = int(maxnumber)

    data = db_destiny_user.find()[limitnumber:maxnumber]


    return render(request, 'listUsersAnalized.html', {'users': data})




def user_analized(request, id=0):

    client = MongoClient('0.0.0.0', 1234)

    db_data = client.SilverEye.TestSentiment
    db_user = client.SilverEye.TestSentimentUser

    user = db_user.find_one({"user": int(id)})
    data = db_data.find({"user": int(id)})

    return render(request, 'userAnalized.html', {'user': user, 'data_set':data})

########

def get_color_by_sentiment(sentiment):

    negative = int(sentiment['opinion']['negative'])
    negative = negative + int(sentiment['polarity']['negative'])

    positive = int(sentiment['opinion']['positive'])
    positive = positive + int(sentiment['polarity']['positive'])

    if negative == positive:
        return 0
    elif negative > positive:
        return 1
    elif negative < positive:
        return 2


def get_entities(text):
    splited_text = text.split(' ')

    users = []

    if splited_text[0] == "RT":
        del splited_text[0]
        del splited_text[1]

    for word in splited_text:
        if len(word) > 0 and word[0] == "@":
            users.append(word)
        if len(word) > 0 and word[0] == "#":
            users.append(word)

    return users



