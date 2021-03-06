
import requests
import time

URL_LANGUAGE_IDENTIFIER = "http://opener.olery.com/language-identifier"
#URL_LANGUAGE_IDENTIFIER = "http://192.168.101.127:1111"


URL_TOKENIZER = "http://opener.olery.com/tokenizer"
#URL_TOKENIZER = "http://192.168.101.127:2222"

URL_POSTAGGER = "http://opener.olery.com/pos-tagger"
#URL_POSTAGGER = "http://192.168.101.127:3333"

URL_CONSTITUENCY_PARSE = "http://opener.olery.com/constituent-parser"
#URL_CONSTITUENCY_PARSE = "http://192.168.101.127:4444"

URL_POLARITY_TAGGER = "http://opener.olery.com/polarity-tagger"
#URL_POLARITY_TAGGER = "http://192.168.101.127:5555"

URL_PROPERTY_TAGGER = "http://opener.olery.com/property-tagger"
#URL_POLARITY_TAGGER = "http://192.168.101.127:6666"

URL_OPINION_DETECTOR = "http://opener.olery.com/opinion-detector"
#URL_OPINION_DETECTOR = "http://192.168.101.127:7777"

'''Named Entity Recognition and Named Entity Disambiguation '''

URL_NER = "http://opener.olery.com/ner"
#URL_NER = "http://192.168.101.127:8888"

URL_NED = "http://opener.olery.com/ned"
#URL_NER = "http://192.168.101.127:8888"

URL_COREFERENCE = "http://opener.olery.com/coreference"
#URL_COREFERENCE = "http://192.168.101.127:9999"

URL_CONSTITUENT_PARSER = "http://opener.olery.com/constituent-parser"
#URL_CONSTITUENT_PARSER = "http://192.168.101.127:1010"

text = "el mundo se va a la mierda i aqui nadie hace nada maldito asco"

f_NER = open('QueryApp/Data/NER.kaf', 'w')

f_NED = open('QueryApp/Data/NED.kaf', 'w')

f_COREFERENCE = open('QueryApp/Data/COREFERENCE.kaf', 'w')

#f_CONSTITUENT_PARSER = open('QueryApp/Data/CONSTITUENT_PARSER.kaf', 'w')


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

    '''  '''


    result={}


    result["polarity"] = get_polarity(output_polarity_tagger)
    result["property"] = get_polarity(output_property_tagger)
    result["opinion"] = get_polarity(output_opinion_detector)

    return result

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

    print "Polarity tagger:"
    print get_polarity(output_polarity_tagger)

    print "Property tagger:"
    print get_polarity(output_property_tagger)

    print "Opinion tagger:"
    print get_polarity(output_opinion_detector)


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

    f_NER.close()
    f_NED.close()
    f_COREFERENCE.close()



    print "output_polarity_tagger result:"
    print get_polarity(output_polarity_tagger)

    print "output_property_tagger result:"
    print get_polarity(output_property_tagger)

    print "output_opinion_detector result:"
    print  get_polarity(output_opinion_detector)

'''
