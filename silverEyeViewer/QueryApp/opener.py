
import requests
import sys

URL_LANGUAGE_IDENTIFIER = "http://opener.olery.com/language-identifier"
#URL_LANGUAGE_IDENTIFIER = "http://192.168.101.127:1111"


URL_TOKENIZER = "http://opener.olery.com/tokenizer"
#URL_TOKENIZER = "http://192.168.101.127:2222"

URL_POSTAGGER = "http://opener.olery.com/pos-tagger"
#URL_POSTAGGER = "192.168.101.127:3333"

URL_CONSTITUENCY_PARSE = "http://opener.olery.com/constituent-parser"
#URL_CONSTITUENCY_PARSE = "192.168.101.127:4444"

URL_POLARITY_TAGGER = "http://opener.olery.com/polarity-tagger"
#URL_POLARITY_TAGGER = "192.168.101.127:5555"

URL_PROPERTY_TAGGER = "http://opener.olery.com/property-tagger"
#URL_POLARITY_TAGGER = "192.168.101.127:6666"

URL_OPINION_DETECTOR = "http://opener.olery.com/opinion-detector"
#URL_OPINION_DETECTOR = "192.168.101.127:7777"

text = "el mundo se va a la mierda i aqui nadie hace nada maldito asco"



def call_language_identifier(URL, data):
    session = requests.session()
    text= complementByInputKAFTrue(data)

    r = requests.post(URL, headers={}, data=text, cookies={})
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

def complementByInputKAFTrue(text):
    return "input=" + text + "&kaf=true"



def print_polarity(data):
    print "Positive:" + str(data.count('positive'))
    print "Negative:" + str(data.count('negative'))
    print "Neutral:" + str(data.count('neutral'))
    print "--------------------------------------"

def get_polarity(data):
    positive = "Positive:" + str(data.count('positive'))
    negative = "Negative:" + str(data.count('negative'))
    neutral = "Neutral:" + str(data.count('neutral'))
    return {"positive": positive, "negative": negative, "neutral": neutral}



def analyze_text(text):

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


    result={}


    result["polarity"] = get_polarity(output_polarity_tagger)
    result["property"] = get_polarity(output_property_tagger)
    result["opinion"] = get_polarity(output_opinion_detector)

    return result

if __name__ == '__main__':

    text = raw_input("Introdueix el text a analitzar\n")

    print "--------------------------------------"

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


    print "output_polarity_tagger result:"
    print get_polarity(output_polarity_tagger)

    print "output_property_tagger result:"
    print get_polarity(output_property_tagger)

    print "output_opinion_detector result:"
    print  get_polarity(output_opinion_detector)
