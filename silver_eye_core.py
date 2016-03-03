# -*- coding: utf-8 -*-

import opener

from pymongo import MongoClient
import time

ciudadanos = [u"@GirautaOficial" ,
            u"#AlbertRivera" ,
            u"@Albert_Rivera" ,
            u"@CiudadanosCs" ,
            u"#RutaCiudadana" ,
            u"#ConIlusion" ,
            u"@sdelcampocs" ,
            u"#Ilusión" ,
            u"#Ciudadanos" ,
            u"@InesArrimadas" ,
            u"#AlbertPresidente"]

democracia_llibertat = [u"@ConvergenciaCAT" ,
            u"@DemocratesCAT" ,
            u"@reagrupament" ,
            u"#possible" ,
            u"@20dl_cat" ,
            u"@joseprull" ,
            u"@joanbague" ,
            u"@peresalo68" ,
            u"@Ferran_Bel" ,
            u"@franceschoms"]

ehbildu = [u"@ehbildu" ,
            u"#BilduErabakira" ,
            u"#BilduErabakira" ,
            u"@ehbildu_legebil"]

erc = [u"ERC" ,
            u"#SomRepública" ,
            u"@Esquerra_ERC" ,
            u"@GabrielRufian" ,
            u"@Esquerra_ERC" ,
            u"@JoanTarda" ,
            u"@junqueras" ,
            u"@MartaRovira"]

podemos = [u"#UNPAISCONTIGO" ,
            u"@ahorapodemos" ,
            u"#Un6Dcontigo" ,
            u"#6DHagamosHistoria" ,
            u"@Pablo_Iglesias_" ,
            u"@AdaColau" ,
            u"@VickyRosell" ,
            u"#LeyDeImpunidad"]

pp = [u"partidopopular" ,
            u"partido popular",
            u"pp",
            u"#PP",
            u"#EspañaEnSerio",
            u"@marianorajoy",
            u"@AlfonsoAlonsoPP",
            u"@PPopular",
            u"#VotaPP",
            u"@Sorayapp",
            u"@mdcospedal",
            u"pablocasado_",
            u"#YoVotoPP",
            u"#EmpleoEnSerio",
            u"@NNGG_Es"]

psoe = [u"psoe" ,
            u"psc" ,
            u"@socialistes_cat" ,
            u"#FemForaRajoy" ,
            u"#SomLaSolucio" ,
            u"@carmechacon" ,
            u"@sanchezcastejon" ,
            u"@PSOE" ,
            u"#OrgulloSocialista" ,
            u"#VOTAPSOE" ,
            u"#PedroPresidente" ,
            u"#UnFuturoParaLaMayoría"]

unio = [u"@unio_cat" ,
            u"@DuranLleida" ,
            u"#Solucions!" ,
            u"@Marti_Barbera" ,
            u"@Ramon_Espadaler"]

upyd = [u"@UPYD" ,
            u"#VotaUPYD" ,
            u"#MásEspaña" ,
            u"@Herzogoff" ,
            u"@sryuriaguilar"]

def identify_sentiment_by_text_entities_and_user():
    client = MongoClient('0.0.0.0', 27017)

    db_origin = client.SilverEye['twitterPolitical']
    db_destiny_data = client.SilverEye['TestSentiment']
    db_destiny_user = client.SilverEye['TestSentimentUser']

    size = int(db_origin.count())

    max_set = 5;


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

    #print entities_collection

    for entity in user_entities:
        result_entities[entity] = 0

    for tweet_entity in entities_collection:
        for user in user_entities:
            for key in tweet_entity.keys():
                if user == key:
                    result_entities[user] += tweet_entity[user]

    return result_entities


def analyze_user(user_id):
    client = MongoClient('0.0.0.0', 27017)

    db_data = client.SilverEye['TestSentiment']
    db_user = client.SilverEye['TestSentimentUser']

    data = db_data.find({"user": user_id})

    result = get_result_of_set_of_data(data)

    db_user.update({"user": user_id}, {"$set": {"result": result}}, upsert=True)


def analyze_political_sentiment_by_entities(user_id):
    client = MongoClient('0.0.0.0', 27017)

    db_user = client.SilverEye['TestSentimentUser']

    ciudadanos_tag = []
    democracia_llibertat_tag = []
    ehbildu_tag = []
    erc_tag = []
    podemos_tag = []
    pp_tag = []
    psoe_tag = []
    unio_tag = []
    upyd_tag = []

    ciudadanos_total = 0
    democracia_llibertat_total = 0
    ehbildu_total = 0
    erc_total = 0
    podemos_total = 0
    pp_total = 0
    psoe_total = 0
    unio_total = 0
    upyd_total = 0


    data = db_user.find({"user": user_id})[0]

    print data
    print data['result']


    for key, value in data['result'].items():
        if key in ciudadanos:
            ciudadanos_tag.append(value)

        if key in democracia_llibertat:
            democracia_llibertat_tag.append(value)

        if key in ehbildu:
            ehbildu_tag.append(value)

        if key in erc:
            erc_tag.append(value)

        if key in podemos:
            podemos_tag.append(value)

        if key in pp:
            pp_tag.append(value)

        if key in psoe:
            psoe_tag.append(value)

        if key in unio:
            unio_tag.append(value)

        if key in upyd:
            upyd_tag.append(value)

    for value in ciudadanos_tag:
        ciudadanos_total = value +ciudadanos_total

    for value in democracia_llibertat_tag:
        democracia_llibertat_total = value + democracia_llibertat_total

    for value in ehbildu_tag:
        ehbildu_total = value + ehbildu_total

    for value in erc_tag:
        erc_total = value + erc_total

    for value in podemos_tag:
        podemos_total = value + podemos_total

    for value in pp_tag:
        pp_total = value + pp_total

    for value in psoe_tag:
        psoe_total += value

    for value in unio_tag:
        unio_total += value

    for value in upyd_tag:
        upyd_total += value

    result = {"ciudadanos":ciudadanos_total,"democracia_llibertat":democracia_llibertat_total, "ehbildu":ehbildu_total, \
              "erc":erc_total, "podemos":podemos_total, "pp":pp_total, "psoe":psoe_total, "unio":unio_total, "upyd":upyd_total }

    db_user.update({"user": user_id}, {"$set": {"result_political": result}}, upsert=True)


def analyze_all_users():
    client = MongoClient('0.0.0.0', 27017)
    db_user = client.SilverEye['TestSentimentUser']

    for user in db_user.find():
        print user
        analyze_user(user['user'])
        analyze_political_sentiment_by_entities(user['user'])


def global_results():
    client = MongoClient('0.0.0.0', 27017)
    db_user = client.SilverEye['TestSentimentUser']

    ciudadanos_total = 0
    democracia_llibertat_total = 0
    ehbildu_total = 0
    erc_total = 0
    podemos_total = 0
    pp_total = 0
    psoe_total = 0
    unio_total = 0
    upyd_total = 0

    for user in db_user.find():

        if user['result_political'] is not None:

            for key, value in user['result_political'].items():
                if key == "ciudadanos":
                    ciudadanos_total = ciudadanos_total +value
                if key == "democracia_llibertat":
                    democracia_llibertat_total = democracia_llibertat_total +value
                if key == "ehbildu":
                    ehbildu_total = ehbildu_total +value
                if key == "erc":
                    erc_total = erc_total +value
                if key == "podemos":
                    podemos_total = podemos_total +value
                if key == "pp":
                    pp_total = pp_total +value
                if key == "unio":
                    unio_total = unio_total +value
                if key == "upyd":
                    upyd_total = upyd_total +value
                if key == "psoe":
                    psoe_total = psoe_total +value

    print ciudadanos_total
    print democracia_llibertat_total
    print ehbildu_total
    print erc_total
    print podemos_total
    print pp_total
    print psoe_total
    print unio_total
    print upyd_total


if __name__ == '__main__':
    start_time = time.time()

    #identify_sentiment_by_text_entities_and_user()
    # analyze_user(117702124)
    # analyze_all_users()

    global_results()
    print("--- %s seconds ---" % (time.time() - start_time))

