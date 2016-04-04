

class GroupClassifier:

    def __init__(self, extractor, client):
        self.extractor = extractor
        self.client = client

    def get_entities_by_tweet(self, text):
        text = text.replace(".", " ")
        text = text.replace(":", " ")
        text = text.replace(",", " ")

        entities = []

        for entity in self.extractor.ciudadanos:
            if entity.encode('utf8') in text:
                entities.append(entity)

        for entity in self.extractor.democracia_llibertat:
            if entity.encode('utf8') in text:
                entities.append(entity)

        for entity in self.extractor.ehbildu:
            if entity.encode('utf8') in text:
                entities.append(entity)

        for entity in self.extractor.erc:
            if entity.encode('utf8') in text:
                entities.append(entity)

        for entity in self.extractor.podemos:
            if entity.encode('utf8') in text:
                entities.append(entity)

        for entity in self.extractor.pp:
            if entity.encode('utf8') in text:
                entities.append(entity)

        for entity in self.extractor.psoe:
            if entity.encode('utf8') in text:
                entities.append(entity)

        for entity in self.extractor.unio:
            if entity.encode('utf8') in text:
                entities.append(entity)

        split_text = text.split(' ')

        if split_text[0] == "RT":
            del split_text[0]
            del split_text[1]

        for word in split_text:
            if len(word) > 0 and word[0] == "@":
                if word not in entities:
                    entities.append(word)
            if len(word) > 0 and word[0] == "#":
                if word not in entities:
                    entities.append(word)

        return entities

    def get_political_party_counter_by_entities(self, entities):

        political = {}

        no_reconized_entities = []

        for entity in entities:

            classified_entity = False

            if entity in self.extractor.ciudadanos:
                if political.has_key('ciudadanos'):
                    political['ciudadanos'] += political['ciudadanos']
                else:
                    political['ciudadanos'] = 1
                classified_entity = True

            if entity in self.extractor.democracia_llibertat:
                if political.has_key('democracia_llibertat'):
                    political['democracia_llibertat'] += political['democracia_llibertat']
                else:
                    political['democracia_llibertat'] = 1
                classified_entity = True

            if entity in self.extractor.ehbildu:
                if political.has_key('ehbildu'):
                    political['ehbildu'] += political['ehbildu']
                else:
                    political['ehbildu'] = 1
                classified_entity = True

            if entity in self.extractor.erc:
                if political.has_key('erc'):
                    political['erc'] += political['erc']
                else:
                    political['erc'] = 1
                classified_entity = True

            if entity in self.extractor.podemos:
                if political.has_key('podemos'):
                    political['podemos'] += political['podemos']
                else:
                    political['podemos'] = 1
                classified_entity = True

            if entity in self.extractor.pp:
                if political.has_key('pp'):
                    political['pp'] += political['pp']
                else:
                    political['pp'] = 1
                classified_entity = True

            if entity in self.extractor.psoe:
                if political.has_key('psoe'):
                    political['psoe'] += political['psoe']
                else:
                    political['psoe'] = 1
                classified_entity = True

            if entity in self.extractor.unio:
                if political.has_key('unio'):
                    political['unio'] += political['unio']
                else:
                    political['unio'] = 1
                classified_entity = True

            if entity in self.extractor.upyd:
                if political.has_key('upyd'):
                    political['upyd'] += political['upyd']
                else:
                    political['upyd'] = 1
                classified_entity = True

            if not classified_entity:

                no_reconized_entities.append(entity)


        db_data = self.client.SilverEye.UnclassifiedEntities
        #Save no recognized entities
        for no_rec_ent in no_reconized_entities:
            db_data.update({'entity': str(no_rec_ent)}, {'$inc': {'repeat': 1}},upsert=True)
            for entity in entities:
                db_data.update({'entity': str(no_rec_ent)}, {"$addToSet": {"entities": entity}}, upsert=True)

        return political