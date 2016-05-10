# !/usr/bin/python

# -*- coding: utf-8 -*-

import requests
import time

import os

server_ip = "http://192.168.101.127"

#URL_LANGUAGE_IDENTIFIER = "http://opener.olery.com/language-identifier"
URL_LANGUAGE_IDENTIFIER = server_ip + ":1111"


#URL_TOKENIZER = "http://opener.olery.com/tokenizer"
URL_TOKENIZER = server_ip + ":2222"

#URL_POSTAGGER = "http://opener.olery.com/pos-tagger"
URL_POSTAGGER = server_ip + ":3333"

#URL_CONSTITUENCY_PARSE = "http://opener.olery.com/constituent-parser"
URL_CONSTITUENCY_PARSE = server_ip + ":4444"

#URL_POLARITY_TAGGER = "http://opener.olery.com/polarity-tagger"
URL_POLARITY_TAGGER = server_ip + ":5555"

URL_PROPERTY_TAGGER = "http://opener.olery.com/property-tagger"
#URL_PROPERTY_TAGGER = server_ip + ":6666"

URL_OPINION_DETECTOR = "http://opener.olery.com/opinion-detector"
#URL_OPINION_DETECTOR = server_ip + ":7777"

'''Named Entity Recognition and Named Entity Disambiguation '''

URL_NER = "http://opener.olery.com/ner"
#URL_NER = "http://192.168.101.127:8888"

URL_NED = "http://opener.olery.com/ned"
#URL_NER = "http://192.168.101.127:8888"

#URL_COREFERENCE = "http://opener.olery.com/coreference"
URL_COREFERENCE = "http://192.168.101.127:9999"

#URL_CONSTITUENT_PARSER = "http://opener.olery.com/constituent-parser"
URL_CONSTITUENT_PARSER = "http://192.168.101.127:1010"

text = "el mundo se va a la mierda i aqui nadie hace nada maldito asco"

f_NER = open(os.path.dirname(os.path.dirname(__file__)) +'/Core/Log/NER.kaf', 'w')

f_NED = open(os.path.dirname(os.path.dirname(__file__)) +'/Core/Log/NED.kaf', 'w')

f_COREFERENCE = open(os.path.dirname(os.path.dirname(__file__)) +'/Core/Log/COREFERENCE.kaf', 'w')

f_CONSTITUENT_PARSER = open(os.path.dirname(os.path.dirname(__file__)) +'/Core/Log/CONSTITUENT_PARSER.kaf', 'w')


def call_language_identifier(URL, data):
    session = requests.session()
    text= complementByInputKAFTrue(data)

    r = requests.post(URL, headers={}, data=text.encode('utf-8'), cookies={})

    return r._content

def call_tokenizer(URL, data):
    session = requests.session()
    text= complementByInputKAFTrue(data).replace('"ca"','"es"')

    r = requests.post(URL, headers={}, data=text, cookies={})
    return r._content


def call_pos_tagger(URL,data):
    session = requests.session()
    text= complementByInputKAFTrue(data).replace('"ca"','"es"')

    r = requests.post(URL, headers={}, data=text, cookies={})
    return r._content

def call_constituency_parse(URL,data):
    session = requests.session()
    text= complementByInputKAFTrue(data).replace('"es"','"ca"')

    r = requests.post(URL, headers={}, data=text, cookies={})
    return r._content

def call_polarity_tagger(URL,data):
    session = requests.session()
    text= complementByInputKAFTrue(data).replace('"ca"','"es"')

    r = requests.post(URL, headers={}, data=text, cookies={})
    return r._content

def call_property_tagger(URL,data):
    session = requests.session()
    text= complementByInputKAFTrue(data).replace('"ca"','"es"')

    r = requests.post(URL, headers={}, data=text, cookies={})
    return r._content


def call_opinion_detector(URL,data):
    session = requests.session()
    text= complementByInputKAFTrue(data).replace('"ca"','"es"')

    r = requests.post(URL, headers={}, data=text, cookies={})
    return r._content

def call_ner(URL,data):
    session = requests.session()
    text= complementByInputKAFTrue(data).replace('"ca"','"es"')

    r = requests.post(URL, headers={}, data=text, cookies={})
    return r._content

def call_ned(URL,data):
    session = requests.session()
    text= complementByInputKAFTrue(data).replace('"ca"','"es"')

    r = requests.post(URL, headers={}, data=text, cookies={})
    return r._content

def call_coreference(URL,data):
    session = requests.session()
    text= complementByInputKAFTrue(data).replace('"ca"','"es"')

    r = requests.post(URL, headers={}, data=text, cookies={})
    return r._content

def call_constituent_parser(URL,data):
    session = requests.session()
    text= complementByInputKAFTrue(data).replace('"ca"','"es"')

    r = requests.post(URL, headers={}, data=text, cookies={})
    return r._content


def complementByInputKAFTrue(text):
    return "input=" + text + "&kaf=true"


def print_polarity(data):
    print "Positive:" + str(data.count('positive'))
    print "Negative:" + str(data.count('negative'))
    print "Neutral:" + str(data.count('neutral'))
    print "--------------------------------------"

def get_polarity(data):
    positive = data.count('positive')
    negative = data.count('negative')
    neutral = data.count('neutral')
    return {"positive": positive, "negative": negative, "neutral": neutral}


def analyze_text_and_get_polarity(text):

    try:
        sentiment = analyze_text(text)
        polarity_aprox = get_aprox_polarity(sentiment)
        return polarity_aprox

    except Exception as exception:
            # Oh well, reconnect and keep trucking
            raise Exception("analyze_text_and_get_polarity->SentimentAnalysisController" +
                                exception.message + str(exception.__class__)+"\nText:"+text)

def analyze_text(text):

    try:
        output_language_identifier = call_language_identifier(URL_LANGUAGE_IDENTIFIER, text)
        #print output_language_identifier
    except Exception as exception:
                # Oh well, reconnect and keep trucking
                raise Exception("SentimentAnalysisController->analyze_text->call_language_identifier" +
                                exception.message + str(exception.__class__)+"\nText:"+text)
    try:
        output_tokenizer = call_tokenizer(URL_TOKENIZER, output_language_identifier)
        #print output_tokenizer

        output_pos_tagger = call_pos_tagger(URL_POSTAGGER,output_tokenizer)
        #print output_pos_tagger

        output_constituency_parse = call_constituency_parse(URL_CONSTITUENCY_PARSE,output_pos_tagger)
        #print output_constituency_parse


        ''' Sentiment Analysis '''

        output_polarity_tagger = call_polarity_tagger(URL_POLARITY_TAGGER,output_constituency_parse)
        #print output_polarity_tagger

        output_property_tagger = call_property_tagger(URL_PROPERTY_TAGGER,output_constituency_parse)
        #print output_property_tagger

        output_opinion_detector = call_opinion_detector(URL_OPINION_DETECTOR,output_constituency_parse)
        #print output_opinion_detector

        '''  '''


        result={}


        result["polarity"] = get_polarity(output_polarity_tagger)
        result["property"] = get_polarity(output_property_tagger)
        result["opinion"] = get_polarity(output_opinion_detector)

        return result
    except Exception as exception:
                # Oh well, reconnect and keep trucking
                raise Exception("analyze_text->SentimentAnalysisController->" + exception.message + str(exception.__class__))


def get_aprox_polarity(sentiment):

    try:
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
    except Exception as exception:
                # Oh well, reconnect and keep trucking
                raise Exception("get_aprox_polarity->SentimentAnalysisController" + exception.message)

if __name__ == '__main__':

    text = raw_input("Introdueix el text a analitzar\n")

    print "--------------------------------------"
    start_time = time.time()

    #print uncurl.parse("curl -d \"input=this is an english text&kaf=true\" http://localhost:9393 ")

    output_language_identifier = call_language_identifier(URL_LANGUAGE_IDENTIFIER, complementByInputKAFTrue(text))
    #print output_language_identifier

    output_tokenizer = call_tokenizer(URL_TOKENIZER, output_language_identifier)
    #print output_tokenizer

    output_pos_tagger = call_pos_tagger(URL_POSTAGGER,output_tokenizer)
    #print output_pos_tagger

    output_constituency_parse = call_constituency_parse(URL_CONSTITUENCY_PARSE,output_pos_tagger)
    #print output_constituency_parse


    ''' Sentiment Analysis '''

    output_polarity_tagger = call_polarity_tagger(URL_POLARITY_TAGGER,output_constituency_parse)
    #print output_polarity_tagger

    output_property_tagger = call_property_tagger(URL_PROPERTY_TAGGER,output_constituency_parse)
    #print output_property_tagger

    output_opinion_detector = call_opinion_detector(URL_OPINION_DETECTOR,output_constituency_parse)
    #print output_opinion_detector


    print_polarity(output_opinion_detector)

    print "-------------------"

    print("--- %s seconds ---" % (time.time() - start_time))

    ''' Named Entity Recognition and Named Entity Disambiguation '''

'''
    output_ner = call_ner(URL_NER,output_constituency_parse)
    print output_ner
    f_NER.write(output_ner)

    output_ned = call_ned(URL_NED,output_ner)
    print output_ned
    f_NED.write(output_ned)

    output_coreference = call_coreference(URL_COREFERENCE,output_ned)
    print output_coreference
    f_COREFERENCE.write(output_coreference)

    output_constituent_parser = call_constituent_parser(URL_CONSTITUENT_PARSER,output_coreference)
    print output_constituent_parser
    f_CONSTITUENT_PARSER.write(output_constituent_parser)

    f_NER.close()
    f_NED.close()
    f_COREFERENCE.close()
    f_CONSTITUENT_PARSER.close()
'''

'''
    print "output_polarity_tagger result:"
    print get_polarity(output_polarity_tagger)

    print "output_property_tagger result:"
    print get_polarity(output_property_tagger)

    print "output_opinion_detector result:"
    print  get_polarity(output_opinion_detector)
'''