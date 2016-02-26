# !/usr/bin/python

# -*- coding: utf-8 -*-

import opener

from pymongo import MongoClient


def identify_sentiment_by_text_entities_and_user():
    client = MongoClient('0.0.0.0', 1234)

    db_origin = client.SilverEye['twitterPolitical']
    db_destiny_data = client.SilverEye['TestSentiment']
    db_destiny_user = client.SilverEye['TestSentimentUser']

    size = int(db_origin.count())

    max_set = 5;

    size = 20

    data_analyzed = 0;

    while data_analyzed < size:
        init = data_analyzed + 1
        final = max_set + data_analyzed + 1

        data_set = db_origin.find()[init:final]
        analyze_set_of_tweets(data_set, db_destiny_data, db_destiny_user)

        data_analyzed = final


def analyze_set_of_tweets(data_set, destiny_data, destiny_user):
    for data in data_set:
        text = data['text'].encode('utf8')
        user = data['user']['id']
        coordinates = data['coordinates']
        political = data['Political']

        entities = get_entities(text)
        polarity = opener.analyze_text(text)
        polarity = get_color_by_sentiment(polarity)

        destiny_data.update({'user': user, 'text': text}, {'user': user, "text": text, "coordinates": coordinates,\
                                                           'entities': entities, 'polarity': polarity,\
                                                           'political': political}, upsert=True)
        destiny_user.update({'user': user}, {'user': user}, upsert=True)


def get_entities(text):
    text = text.replace(".", " ")

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


def get_color_by_sentiment(sentiment):
    negative = int(sentiment['opinion']['negative'])
    negative = negative + int(sentiment['polarity']['negative'])

    positive = int(sentiment['opinion']['positive'])
    positive = positive + int(sentiment['polarity']['positive'])

    if negative == positive:
        return 0
    elif negative > positive:
        return -1
    elif negative < positive:
        return 1


def get_result_of_set_of_data(data_set):
    entities_collection = []

    user_entities = []

    result_entities = {}

    # Optimize
    for data in data_set:
        data_entities = data['entities']
        entities = {}
        for entity in set(data_entities):
            entities[entity] = int(data["polarity"])
            if entity not in user_entities:
                user_entities.append(entity)

        entities_collection.append(entities)

    print entities_collection

    for entity in user_entities:
        result_entities[entity] = 0

    for tweet_entity in entities_collection:
        for user in user_entities:
            for key in tweet_entity.keys():
                if user == key:
                    result_entities[user] += tweet_entity[user]

    return result_entities


def analyze_user(user_id):
    client = MongoClient('0.0.0.0', 1234)

    db_data = client.SilverEye['TestSentiment']
    db_user = client.SilverEye['TestSentimentUser']

    data = db_data.find({"user": user_id})

    result = get_result_of_set_of_data(data)

    db_user.update({"user": user_id}, {"$set": {"result": result}}, upsert=True)


def analyze_all_users():
    client = MongoClient('0.0.0.0', 1234)
    db_user = client.SilverEye['TestSentimentUser']

    for user in db_user.find():
        print user
        analyze_user(user['user'])


if __name__ == '__main__':
    identify_sentiment_by_text_entities_and_user()
    # analyze_user(117702124)
    analyze_all_users()