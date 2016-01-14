
import requests
import uncurl



URL_LANGUAGE_IDENTIFIER = "http://opener.olery.com/language-identifier"

text = "hola hem dic marc i parlo catala"

text_complet = "input=" + text + "&kaf=true"

payload = {

}

headers = {'input': text_complet}

def call_language_identifier():

    r = requests.get(URL_LANGUAGE_IDENTIFIER, input=text_complet)
    print r.status_code
    print r.headers['content-type']
    print r.encoding
    print r.text
    print r.json()

def call_language_identifier2():
    session = requests.session()
    r = requests.post(URL_LANGUAGE_IDENTIFIER, headers={}, data=text_complet, cookies={})
    print r._content

if __name__ == '__main__':

    #print uncurl.parse("curl -d \"input=this is an english text&kaf=true\" http://localhost:9393 ")

    call_language_identifier2()

