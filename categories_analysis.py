import csv
import os
import numpy as np
import pandas as pd
from PyKomoran import *
from gensim.models import word2vec
os.chdir('C:\youtube_trend\Youtube-Trend-Analysis-Project')
komoran=Komoran(DEFAULT_MODEL['FULL'])
komoran.set_user_dic('dataset\dic.user')
categories=["Film & Animation", "Autos & Vehicles" ,
           "Music" ,"Pets & Animals", "Sports","Short Movies" ,"Travel & Events"
           ,"Gaming","Videoblogging","People & Blogs","Comedy","Entertainment"
           "News & Politics", "Howto & Style","Education","Science & Technology",
           "Movies","Anime/Animation","Action/Adventure","Classics","Comedy","Documentary",
           "Drama","Family","Foreign","Horror","Sci-Fi/Fantasy","Thriller","Shorts","Shows","Trailers"]



data=pd.read_csv('dataset/KRvideos.csv', engine='python')
df=data[:]
for col in ['video_id', 'trending_date', 'channel_title', 'publish_time', 'views' ,'likes' , 'dislikes']:
    del df[col]

yt_title=df['title']
temp=[]

for i in range(100):
    sentence=yt_title[i]
    sentence_nouns=komoran.get_morphes_by_tags(sentence, tag_list=['NNG','NNP','NNB'])
    all_temp=[]
    temp.append(sentence_nouns)
    yt_category=df['category_id'][i]

    categories_number_dic={0 : "Film & Animation" , 1: "Autos & Vehicles" ,
           2: "Music"  ,3:"Pets & Animals" ,4: "Sports",5:"Short Movies" , 6:"Travel & Events" 
           ,7:"Gaming" ,8:"Videoblogging" ,9:"People & Blogs" ,10:"Comedy"  ,11 :"Entertainment" ,
           12:"News & Politics"  , 13 :"Howto & Style" ,14:"Education" ,15:"Science & Technology" ,
           16:"Movies" ,17:"Anime/Animation" ,18:"Action/Adventure",19:"Classics",20:"Comedy",21:"Documentary",
           22:"Drama",23:"Family",24:"Foreign",25:"Horror",26:"Sci-Fi/Fantasy",27:"Thriller",28:"Shorts",29:"Shows",30:"Trailers"}
    

print(temp)




