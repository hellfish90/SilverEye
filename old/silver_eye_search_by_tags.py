# -*- coding: utf-8 -*-
__author__ = 'Marc'

import tweepy
import json
import logging
import datetime

logging.basicConfig(
    filename='search_by_user.log',
    level=logging.WARNING,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%d-%m-%y %H:%M')

# Configuration parameters
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""
database_name = ""


ciudadanos = [u"@GirautaOficial" + " OR "
            u"#AlbertRivera" + " OR "
            u"@Albert_Rivera" + " OR "
            u"@CiudadanosCs"  + " OR "
            u"#RutaCiudadana"  + " OR "
            u"#ConIlusion"  + " OR "
            u"@sdelcampocs"  + " OR "
            u"#Ilusión"  + " OR "
            u"#Ciudadanos"  + " OR "
            u"@InesArrimadas"  + " OR "
            u"#AlbertPresidente"]

democracia_llibertat = [u"@ConvergenciaCAT" + " OR "
            u"@DemocratesCAT" + " OR "
            u"@reagrupament" + " OR "
            u"#possible" + " OR "
            u"@20dl_cat" + " OR "
            u"@joseprull" + " OR "
            u"@joanbague" + " OR "
            u"@peresalo68" + " OR "
            u"@Ferran_Bel" + " OR "
            u"@franceschoms"]

ehbildu = [u"@ehbildu" + " OR "
            u"#BilduErabakira" + " OR "
            u"#BilduErabakira" + " OR "
            u"@ehbildu_legebil"]

erc = [u"ERC" + " OR "
            u"#SomRepública" + " OR "
            u"@Esquerra_ERC" + " OR "
            u"@GabrielRufian" + " OR "
            u"@Esquerra_ERC" + " OR "
            u"@JoanTarda" + " OR "
            u"@junqueras" + " OR "
            u"@MartaRovira"]

podemos = [u"#UNPAISCONTIGO" + " OR "
            u"@ahorapodemos" + " OR "
            u"#Un6Dcontigo" + " OR "
            u"#6DHagamosHistoria" + " OR "
            u"@Pablo_Iglesias_" + " OR "
            u"@AdaColau" + " OR "
            u"@VickyRosell" + " OR "
            u"#LeyDeImpunidad"]

pp = [u"partidopopular" + " OR "
            u"partido popular" + " OR "
            u"pp" + " OR "
            u"#PP" + " OR "
            u"#EspañaEnSerio" + " OR "
            u"@marianorajoy" + " OR "
            u"@AlfonsoAlonsoPP" + " OR "
            u"@PPopular" + " OR "
            u"#VotaPP" + " OR "
            u"@Sorayapp" + " OR "
            u"@mdcospedal" + " OR "
            u"pablocasado_" + " OR "
            u"#YoVotoPP" + " OR "
            u"#EmpleoEnSerio" + " OR "
            u"@NNGG_Es"]

psoe = [u"psoe" + " OR "
            u"psc"  + " OR "
            u"@socialistes_cat" + " OR "
            u"#FemForaRajoy"  + " OR "
            u"#SomLaSolucio"  + " OR "
            u"@carmechacon"  + " OR "
            u"@sanchezcastejon" + " OR "
            u"@PSOE"  + " OR "
            u"#OrgulloSocialista" + " OR "
            u"#VOTAPSOE"  + " OR "
            u"#PedroPresidente"  + " OR "
            u"#UnFuturoParaLaMayoría"]

unio = [u"@unio_cat" + " OR "
            u"@DuranLleida" + " OR "
            u"#Solucions!" + " OR "
            u"@Marti_Barbera" + " OR "
            u"@Ramon_Espadaler"]

upyd = [u"@UPYD" + " OR "
            u"#VotaUPYD" + " OR "
            u"#MásEspaña" + " OR "
            u"@Herzogoff" + " OR "
            u"@sryuriaguilar"]

keywords = ciudadanos + democracia_llibertat + ehbildu + erc + podemos + pp + psoe + unio + upyd

if __name__ == '__main__':
    logging.debug('silver_eye_twitter_streaming.py starting ...')
    logging.error(datetime.datetime.now())
    logging.debug("------------------")

    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
        access_token = config['access_token']
        access_token_secret = config['access_token_secret']
        consumer_key = config['consumer_key']
        consumer_secret = config['consumer_secret']
        database_name = config['database_name']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    stuff = tweepy.Cursor(api.search, q=keywords).items()

    for tweet in stuff:
        print tweet.created_at, tweet.text, tweet.lang

