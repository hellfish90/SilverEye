#tot el de collection manager cap aqui (DAO)
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from DAOTags import DAOTags


class CollectionClassifier:

    def __init__(self, client):
        self.client = client
        self.dao_tags = DAOTags(self.client)

    def get_all_collection_names(self):
        return self.dao_tags.get_all_collection_name()

    def add_collection(self, collection_name):
        self.dao_tags.add_collection(collection_name)

    def remove_collection(self, collection_name):
        self.dao_tags.remove_collection(collection_name)

    def remove_tag_of_collection(self, collection, tag_name):
        self.dao_tags.remove_tag_of_collection(collection,tag_name)

    def add_tag_to_collection(self, collection_name, tag_name):
        self.dao_tags.add_tag_to_collection(collection_name, tag_name)

    def delete_tag_to_collection(self, collection_name, tag_name):
        self.dao_tags.remove_tag_of_collection(collection_name,tag_name)

    def get_all_tags(self):
        return self.dao_tags.get_all_classified_tags()

    def get_all_collections(self):
        return self.dao_tags.get_all_classified_tags()

    def get_all_unclassified_tags(self):
        return self.dao_tags.get_unclassified_tags()

    def get_all_classified_tags_name(self):
        return self.dao_tags.get_all_classified_tags_name()

    def get_tags_of_tweet(self, text):

        text = text.replace(".", " ")
        text = text.replace(":", " ")
        text = text.replace(",", " ")

        tags_in_text = []

        split_text = text.split(' ')
        collection_tags = self.dao_tags.get_all_classified_tags()

        for collections in collection_tags:
                for collection in collections:
                    for tags in collections[collection]:
                        if tags["_id"] in text.decode('utf-8'):
                            tags_in_text.append(tags["_id"])

        if split_text[0] == "RT":
            del split_text[0]
            del split_text[1]

        for word in split_text:
            if len(word) > 0 and word[0] == "@":
                if word not in tags_in_text:
                    tags_in_text.append(word)
            if len(word) > 0 and word[0] == "#":
                if word not in tags_in_text:
                    tags_in_text.append(word)

        print tags_in_text

        return tags_in_text

    def get_collection_by_tags(self, input_tags):

        collection_in_tag = {}

        unclassified_tags = list(input_tags)
        identified_tags = []

        collection_tags = self.dao_tags.get_all_classified_tags()

        for tag in input_tags:
            for collections in collection_tags:
                for collection in collections:
                    for tags in collections[collection]:
                        if tag in tags["_id"]:
                            if collection_in_tag.has_key(collection):
                                collection_in_tag[collection] += collection_in_tag[collection] + 1
                            else:
                                collection_in_tag[collection] = 0
                            try:
                                unclassified_tags.remove(tag)
                                identified_tags.append(tag)
                            except ValueError:
                                continue

        self.add_or_update_unclassified_tags(unclassified_tags, input_tags)
        self.update_classified_tags(identified_tags, input_tags)
        return collection_in_tag

    def update_classified_tags(self, classified_tags, related_tags):
        for classified_tag in classified_tags:
            self.dao_tags.update_related_tags_and_plus_repeat(classified_tag, related_tags)

    def add_or_update_unclassified_tags(self, unclassified_tags, related_tags):
        for unclassified_tag in unclassified_tags:
            if self.dao_tags.tag_exist(unclassified_tag):
                self.dao_tags.update_related_tags_and_plus_repeat(unclassified_tag, related_tags)
            else:
                self.dao_tags.add_tag(unclassified_tag, related_tags)
