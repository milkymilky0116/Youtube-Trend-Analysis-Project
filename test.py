import pymysql
import pandas as pd
from PyKomoran import Komoran
from konlpy.tag import Okt
from gensim.models.word2vec import Word2Vec
import ast
from gensim.models import KeyedVectors
from collections import Counter
import random
from pytube import YouTube

def get_query_data(keywords):
    
    conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
    cur=conn.cursor()
    sql="SELECT video_info_thumbnails FROM youtube_test_data WHERE video_info_title or video_info_keywords or video_info_description REGEXP %s ORDER BY video_info_rank"
    keywords="|".join(keywords)
    cur.execute(sql,(keywords,))
    result_set=cur.fetchall()

    result=[]
    for row in result_set[1:]:
        result.append(str(row[0]))

    return result

print(get_query_data(['고양이','강아지']))
    
