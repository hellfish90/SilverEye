from pymongo import MongoClient

from DAOTags import DAOTags


if __name__ == "__main__":
    client =  MongoClient('0.0.0.0', 27017, connect=True)
    daoTags = DAOTags(client)

    #daoTags.add_tag("#test",["#test1","@test2"])
    daoTags.add_tag("@test2",["#test1","@test2"])
    daoTags.add_tag("@test3",["#test3","@test3"])
    daoTags.add_collection("collection1")
    daoTags.add_collection("collection2")
    #daoTags.add_tag_to_collection("collection1","#test")
    daoTags.add_tag_to_collection("collection1","@test3")
    daoTags.add_tag_to_collection("collection2","@test2")
    #daoTags.update_related_tags_and_plus_repeat("#test",["#test1","#test1","#test1","#test2"])
    #daoTags.remove_tag_of_collection("collection1","#test")
    #print daoTags.get_collection_name_by_tag("#test")
    #print daoTags.get_unclassified_tags()
    #print daoTags.get_classified_tags("collection1")
    #print daoTags.get_all_classified_tags()
    #print daoTags.tag_exist("#test10")
