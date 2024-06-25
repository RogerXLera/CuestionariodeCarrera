#import goslate
import os
from definitions import * # classes Skill, Activity, TimePeriod, TimePeriodSequence, Job, User Preference
from read_file import *
import time
import translate
from libretranslatepy import LibreTranslateAPI
from textblob import TextBlob 
from googletrans import Translator
from deep_translator import GoogleTranslator



def translate_sentence_goslate(text,lan:str='es'):
    
    primary_text = text 
    #gs = goslate.Goslate()  
    #return gs.translate(primary_text, lan)
    return None 

def translate_sentence_google(text,lan:str='es'):
    
    primary_text = text
    translator = Translator()
    return translator.translate(primary_text, src='en',dest= lan).text
    #return None 

def translate_sentence(text,lan:str='es'):
    
    primary_text = text 
    translator = translate.Translator(to_lang=lan) 
    translation = translator.translate(primary_text)
    return translation

def translate_sentence_libre(text,lan:str='es'):
    
    primary_text = text
    lt = LibreTranslateAPI("https://translate.terraprint.co/")  
    translation = lt.translate(primary_text,source='en',target=lan)
    return translation

def translate_sentence_arcos(text,lan:str='es'):

    translation = from_lang.get_translation(to_lang)
    translatedText = translation.translate(text)
    return translatedText

def translate_sentence_textblob(text,lan:str='es'):

    blob = TextBlob(text) 
    print(blob.translate(to=lan)) 
    return None


def translate_sentence_deept(text,lan:str='es'):
    
    primary_text = text
    translator = GoogleTranslator(source='en', target=lan)
    return translator.translate(primary_text)
    #return None 

def translate_jobs(J,lan:str='es'):

    j_dict = {}
    for j_id,j in J.items():
        translation = translate_sentence_deept(j.name,lan)
        print(j.name,translation)
        j_dict.update({j_id:translation})

    return j_dict

def translate_queries(Q,lan:str='es'):

    q_dict = {}
    for q_id,q in Q.items():
        translation = translate_sentence(q.question,lan)
        print(q.question,translation)
        time.sleep(1)
        q_dict.update({q_id:translation})

    return q_dict

def install_arcos():

    import argostranslate.package
    import argostranslate.translate

    from_code = "en"
    to_code = "es"

    # Download and install Argos Translate package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    available_package = list(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )[0]
    download_path = available_package.download()
    argostranslate.package.install_from_path(download_path)

    # Translate
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = list(filter(
            lambda x: x.code == from_code,
            installed_languages))[0]
    to_lang = list(filter(
            lambda x: x.code == to_code,
            installed_languages))[0]

    return None
    


if __name__ == '__main__':

    import json
    


    wd_ = 'data'
    path_ = os.getcwd()
    lan = 'es'

    job_file_path = os.path.join(path_,wd_,"anzsco.xlsx")
    q_file_path = os.path.join(path_,wd_,"questions.json")

    J = read_jobs_a(job_file_path)
    Q = read_questions(q_file_path)

    print(len(J))



    #j_dict = translate_jobs(J,lan)
    #q_dict = translate_queries(Q,lan)


    #with open(os.path.join(path_,wd_,'anzsco_job_dict.json'),'w') as outputfile:
        #json.dump(j_dict,outputfile)

    #with open(os.path.join(path_,wd_,'questions_dict.json'),'w') as outputfile:
        #json.dump(q_dict,outputfile)
    
