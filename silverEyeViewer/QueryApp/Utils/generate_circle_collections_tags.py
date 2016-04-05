
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from collection_manager import Extractor

def generate_flare():
    with open('QueryApp/templates/flare.json', 'w') as outfile:

        client = MongoClient('0.0.0.0', 27017, connect=True)
        extractor = Extractor(client)
        lines = []

        collections = [a for a in extractor.get_all_collections()]
        last_collection = len(collections)

        outfile.write("{\"name\":\"SilverEye\",\n")
        outfile.write("\"children\":[")

        for collection in collections:
            outfile.write("{\n")
            outfile.write("\"name\":\""+collection["_id"]+"\",\n")
            outfile.write("\"children\": [\n")
            if "tags" in collection:
                print collection["tags"]
                last_tag = len(collection["tags"])

                for tag in collection["tags"]:
                    if last_tag > 1:
                        outfile.write("{\"name\": \""+tag.encode("utf-8")+"\", \"size\": 555},\n")
                    else:
                        outfile.write("{\"name\": \""+tag.encode("utf-8")+"\", \"size\": 555}\n")
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