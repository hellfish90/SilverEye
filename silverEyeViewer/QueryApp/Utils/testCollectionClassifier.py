# -*- coding: utf-8 -*-
from pymongo import MongoClient
from collection_classifier import CollectionClassifier

if __name__ == "__main__":
    client = MongoClient('0.0.0.0', 27017, connect=True)
    daoTags = CollectionClassifier(client)

    text1 = "@test2 #test #test @lavida #sensepor jo també penso que no s'ha de tenir por"
    text2 = "@test2 #alegria que es festamajor"
    text3 = "@test3 #alegria que es festamajor"

    text4 = "Podemos puede con el pp"

    #daoTags.get_collection_by_tags(daoTags.get_tags_of_tweet(text1))
    #daoTags.get_collection_by_tags(daoTags.get_tags_of_tweet(text2))
    #daoTags.get_collection_by_tags(daoTags.get_tags_of_tweet(text3))
    daoTags.get_collection_by_tags(daoTags.get_tags_of_tweet(text4))

