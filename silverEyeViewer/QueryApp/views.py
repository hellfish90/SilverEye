# !/usr/bin/python

# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

from pymongo import MongoClient


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
