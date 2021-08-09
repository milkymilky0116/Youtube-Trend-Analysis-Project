import requests
from selenium import webdriver as wd
from selenium import webdriver
from pytube import YouTube
from PyKomoran import Komoran
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from selenium import webdriver

def extract_keywords(key_info,n):
    ngram_range=(1,1)
    count=CountVectorizer(ngram_range=ngram_range).fit([key_info])
    candidates=count.get_feature_names()
    model=SentenceTransformer('distilbert-base-nli-mean-tokens')
    doc_embedding=model.encode([key_info])
    candidates_embedding=model.encode(candidates)

    top_n=n
    distance=cosine_similarity(doc_embedding,candidates_embedding)
    keywords=[candidates[index] for index in distance.argsort()[0][-top_n:]]

    return keywords
    
komoran=Komoran('EXP')
komoran.set_user_dic('dic.user')

link="https://youtu.be/eHYDwEeJUf8"
video_info=YouTube(link)
keywords_list=video_info.keywords

keywords=" ".join(keywords_list)

title=video_info.title
key_info=title+' '+keywords


print("키워드 :",keywords)
print("title :",title)
print("키워드 추출 :",extract_keywords(key_info,2))
print('\n'*3)

link="https://youtu.be/YazigoBQBKE"
video_info=YouTube(link)
keywords_list=video_info.keywords
keywords=" ".join(keywords_list)

title=video_info.title
key_info=title+' '+keywords


print("키워드 :",keywords)
print("title :",title)
print("키워드 추출 :",extract_keywords(key_info,2))
print('\n'*3)

link="https://youtu.be/BsbmOe6F77A"
video_info=YouTube(link)
keywords_list=video_info.keywords
keywords=" ".join(keywords_list)

title=video_info.title
key_info=title+' '+keywords


print("키워드 :",keywords)
print("title :",title)
print("키워드 추출 :",extract_keywords(key_info,2))
print('\n'*3)

link="https://youtu.be/ZCKlRY14iFM"
video_info=YouTube(link)
keywords_list=video_info.keywords
keywords=" ".join(keywords_list)

title=video_info.title
title=komoran.get_morphes_by_tags(title,tag_list=['NNP','NNG'])
title=" ".join(title)
key_info=title+' '+keywords


print("키워드 :",keywords)
print("title :",title)
print("키워드 추출 :",extract_keywords(key_info,2))
print('\n'*3)


