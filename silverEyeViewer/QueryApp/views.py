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
    client = MongoClient('192.168.101.73', 27017)

    #Prod
    #client = MongoClient('127.0.0.1', 27017)

    limitnumber = int(limitnumber)
    maxnumber = int(maxnumber)

    data = client.SilverEye.twitterUser.find()[limitnumber:maxnumber]

    #print data[0]['name']

    return render(request, 'listUsersTwitter.html', {'users': data})


def list_twitter_status(request, limitnumber=0, maxnumber=150):

    #Dev
    client = MongoClient('192.168.101.73', 27017)

    #Prod
    #client = MongoClient('127.0.0.1', 27017)

    limitnumber = int(limitnumber)
    maxnumber = int(maxnumber)

    data = client.SilverEye.twitterStatus.find()[limitnumber:maxnumber]

    print data[0]['text']

    return render(request, 'listStatusTwitter.html', {'status': data})