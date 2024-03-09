import locationtagger
from langdetect import detect, detect_langs
from deep_translator import GoogleTranslator #pip install -U deep-translator


def city(text): 
    place_entity = locationtagger.find_locations(text = text)
    return place_entity.cities
 
def translate(sentence, target_lang):
    sentence = GoogleTranslator(source='auto', target= target_lang ).translate(sentence) 
    return sentence
 
def detect_lang(sentence):
    detected_lang = detect_langs(sentence)
    lang_str = str(detected_lang[0])
    return lang_str[:2]

 
sentence = "hey hi"
lang = detect_lang(sentence)
context = translate(sentence, 'hi') #for example I'm translating it in Hindi

