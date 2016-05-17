# -*- coding: utf-8 -*-
import unittest

from pymongo import MongoClient

from DAOCollectionTags import DAOTags

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


class TestDAOCollectionTags(unittest.TestCase):

    client = MongoClient("127.0.0.1", 27017, connect=True)
    database_name = "Test"

    def setUp(self):
        self.client[self.database_name]['Tags'].delete_many({})
        self.client[self.database_name]['CollectionsSet'].delete_many({})
        pass

    def add_tags_into_collection(self):

        daoTags = DAOTags(self.client, self.database_name)

        daoTags.add_collection("ciudadanos")
        for tag in ciudadanos:
            daoTags.add_tag(tag, [])
            daoTags.add_tag_to_collection("ciudadanos", tag)

        daoTags.add_collection("democracia_llibertat")
        for tag in democracia_llibertat:
            daoTags.add_tag(tag, [])
            daoTags.add_tag_to_collection("democracia_llibertat", tag)

        self.assertEqual(daoTags.get_size_collections(), 2)
        self.assertEqual(daoTags.get_size_tags(), len(ciudadanos) + len(democracia_llibertat))

        for collections in daoTags.get_all_collection():

            if collections['_id'] == "ciudadanos":
                self.assertEqual(len(collections["tags"]), len(ciudadanos))

            if collections['_id'] == "democracia_llibertat":
                self.assertEqual(len(collections["tags"]), len(democracia_llibertat))

    def test_get_classified_tags(self):

        daoTags = DAOTags(self.client, self.database_name)

        daoTags.add_tag("No classified", [])

        daoTags.add_collection("ciudadanos")
        for tag in ciudadanos:
            daoTags.add_tag(tag, [])
            daoTags.add_tag_to_collection("ciudadanos", tag)

        for collections in daoTags.get_all_collection():
            if collections['_id'] == "ciudadanos":
                self.assertEqual(len(collections["tags"]), len(ciudadanos))


if __name__ == '__main__':
    unittest.main()