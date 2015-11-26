from django.shortcuts import render

# Create your views here.

from pymongo import MongoClient


def list_twitter_users(request):

    #Dev
    client = MongoClient('192.168.101.73', 27017)

    #Prod
    #client = MongoClient('127.0.0.1', 27017)

    data = client.SilverEye.twitterUser.find()

    print data[0]['name']

    return render(request, 'listUsersTwitter.html', {'users': data})
