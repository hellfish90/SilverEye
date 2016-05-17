
# -*- coding: utf-8 -*-
import os
import sys
from pymongo import MongoClient

sys.path.append( os.path.dirname(os.path.dirname(__file__)) )
from QueryApp.Core.DAO.DAOCollectionTags import DAOTags
from QueryApp.Core.Config.configuration import Configuration



def generate_flare():

    configuration = Configuration()
    client = configuration.get_client()
    database_name = configuration.get_database_name()
    tags_collection_dao = DAOTags(client, database_name)


    with open('QueryApp/templates/flare.json', 'w') as outfile:
        lines = []

        collections = tags_collection_dao.get_all_collection()
        last_collection = len(collections)

        outfile.write("{\"name\":\"SilverEye\",\n")
        outfile.write("\"children\":[")

        for collection in collections:

            collection_name = str(collection["_id"])

            outfile.write("{\n")
            outfile.write("\"name\":\""+collection_name+"\",\n")
            outfile.write("\"children\": [\n")

            if len(collection["tags"]) > 0:

                last_tag = len(collection["tags"])

                for tag in collection["tags"]:

                    if last_tag > 1:
                        outfile.write("{\"name\": \""+tag["_id"].encode("utf-8")+"\", \"size\": "+str((tag["repeat"]*100)+100)+"},\n")
                    else:
                        outfile.write("{\"name\": \""+tag["_id"].encode("utf-8")+"\", \"size\": "+str((tag["repeat"]*100)+100)+"}\n")
                    last_tag -= 1

                outfile.write("]\n")
            else:
                outfile.write("]\n")

            if last_collection > 1:
                outfile.write("},\n")
            else:
                outfile.write("}\n")
            last_collection -= 1
        outfile.write("]}")
