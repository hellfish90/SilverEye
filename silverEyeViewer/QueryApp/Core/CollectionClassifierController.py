#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from DAO.DAOCollectionTags import DAOTags


class CollectionClassifierController:

    def __init__(self, client, database):
        self.dao_tags = DAOTags(client, database)

    def get_tags_of_tweet(self, text):

        try:
            text = text.replace(".", " ")
            text = text.replace(":", " ")
            text = text.replace(",", " ")

            tags_in_text = []

            split_text = text.split(' ')
            tags = self.dao_tags.get_all_tags()

            for tag in tags:
                if tag["_id"] in text:
                    tags_in_text.append(tag["_id"])

            if split_text[0] == "RT":
                del split_text[0]
                del split_text[1]

            for word in split_text:
                if len(word) > 1 and word[0] == "@":
                    if word not in tags_in_text:
                        tags_in_text.append(word)
                if len(word) > 1 and word[0] == "#":
                    if word not in tags_in_text:
                        tags_in_text.append(word)

            return tags_in_text

        except Exception as exception:
            # Oh well, reconnect and keep trucking
            raise Exception("get_tags_of_tweets->CollectionClassifierController" + exception.message)

    def get_collection_by_tags(self, input_tags):

        collection_in_tag = {}

        unclassified_tags = list(input_tags)
        identified_tags = []

        try:
            for tag in input_tags:
                if self.dao_tags.tag_exist(tag):
                    collection = self.dao_tags.get_the_collection_name_of_tag(tag)
                    if collection is not None:
                        collection = collection['_id']
                        if collection_in_tag.has_key(collection):
                            collection_in_tag[collection] += collection_in_tag[collection] + 1
                        else:
                            collection_in_tag[collection] = 1
                        try:
                            unclassified_tags.remove(tag)
                            identified_tags.append(tag)
                        except ValueError:
                            continue

            self.add_or_update_unclassified_tags(unclassified_tags, input_tags)
            self.update_classified_tags(identified_tags, input_tags)
            return collection_in_tag

        except Exception as exception:
            # Oh well, reconnect and keep trucking
            raise Exception("get_collection_by_tags->CollectionClassifierController" + exception.message)

    def update_classified_tags(self, classified_tags, related_tags):
        for classified_tag in classified_tags:
            self.dao_tags.update_related_tags_and_plus_repeat(classified_tag, related_tags)

    def add_or_update_unclassified_tags(self, unclassified_tags, related_tags):
        for unclassified_tag in unclassified_tags:
            if self.dao_tags.tag_exist(unclassified_tag):
                self.dao_tags.update_related_tags_and_plus_repeat(unclassified_tag, related_tags)
            else:
                self.dao_tags.add_tag(unclassified_tag, related_tags)
