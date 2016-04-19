
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from extractor_manager import Extractor
from collection_classifier import CollectionClassifier


def generate_flare():
    with open('QueryApp/templates/flare.json', 'w') as outfile:

        client = MongoClient('0.0.0.0', 27017, connect=True)
        collections = CollectionClassifier(client)
        lines = []

        collections = [a for a in collections.get_all_collections()]
        last_collection = len(collections)

        outfile.write("{\"name\":\"SilverEye\",\n")
        outfile.write("\"children\":[")

        for collection in collections:
            collection_name =list(collection)[0]
            #print collection
            outfile.write("{\n")
            outfile.write("\"name\":\""+collection_name+"\",\n")
            outfile.write("\"children\": [\n")

            if len(collection[collection_name])>0:

                last_tag = len(collection[collection_name])

                for tag in collection[collection_name]:
                    if last_tag > 1:
                        outfile.write("{\"name\": \""+tag["_id"].encode("utf-8")+"\", \"size\": "+str((tag["repeat"]*100)+100)+"},\n")
                    else:
                        outfile.write("{\"name\": \""+tag["_id"].encode("utf-8")+"\", \"size\": "+str((tag["repeat"]*100)+100)+"}\n")
                    last_tag -= 1

                outfile.write("]\n")
            else:
                outfile.write("]\n")

            if last_collection>1:
                outfile.write("},\n")
            else:
                outfile.write("}\n")
            last_collection -=1
        outfile.write("]}")