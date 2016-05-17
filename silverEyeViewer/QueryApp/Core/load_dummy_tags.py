# -*- coding: utf-8 -*-
from pymongo import MongoClient
import os
import sys
sys.path.append( os.path.dirname(os.path.dirname(__file__)) )
from DAO.DAOCollectionTags import DAOTags

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
            u"#AlbertPresidente",
            u"C's",
            u"Albert_Rivera"]

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
            u"#EH Bildu" ,
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
            u"#LeyDeImpunidad",
            u"Podemos",
            u"Pablo Iglesias"]

pp = [u"partidopopular" ,
            u"partido popular",
            u"pp",
            u"PP",
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
            u"Rajoy",
            u"@NNGG_Es"]

psoe = [u"psoe" ,
            u"psc" ,
            u"PsoE" ,
            u"@socialistes_cat" ,
            u"#FemForaRajoy" ,
            u"#SomLaSolucio" ,
            u"@carmechacon" ,
            u"@sanchezcastejon" ,
            u"@PSOE" ,
            u"#PSOE",
            u"PSOE",
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


if __name__ == "__main__":

    client = MongoClient('0.0.0.0', 27017, connect=True)
    database = "SilverEye"
    daoTags = DAOTags(client, database)

    daoTags.add_collection("ciudadanos")
    for tag in ciudadanos:
        daoTags.add_tag(tag, [])
        daoTags.add_tag_to_collection("ciudadanos", tag)

    daoTags.add_collection("democracia_llibertat")
    for tag in democracia_llibertat:
        daoTags.add_tag(tag, [])
        daoTags.add_tag_to_collection("democracia_llibertat", tag)

    daoTags.add_collection("ehbildu")
    for tag in ehbildu:
        daoTags.add_tag(tag, [])
        daoTags.add_tag_to_collection("ehbildu", tag)

    daoTags.add_collection("erc")
    for tag in erc:
        daoTags.add_tag(tag, [])
        daoTags.add_tag_to_collection("erc", tag)

    daoTags.add_collection("podemos")
    for tag in podemos:
        daoTags.add_tag(tag, [])
        daoTags.add_tag_to_collection("podemos", tag)

    daoTags.add_collection("pp")
    for tag in pp:
        daoTags.add_tag(tag, [])
        daoTags.add_tag_to_collection("pp", tag)

    daoTags.add_collection("psoe")
    for tag in psoe:
        daoTags.add_tag(tag, [])
        daoTags.add_tag_to_collection("psoe", tag)

    daoTags.add_collection("unio")
    for tag in unio:
        daoTags.add_tag(tag, [])
        daoTags.add_tag_to_collection("unio", tag)

    daoTags.add_collection("upyd")
    for tag in upyd:
        daoTags.add_tag(tag, [])
        daoTags.add_tag_to_collection("upyd", tag)
