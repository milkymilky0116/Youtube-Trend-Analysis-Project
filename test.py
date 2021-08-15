import pymysql
import pandas as pd
from PyKomoran import Komoran
from konlpy.tag import Okt
from gensim.models.word2vec import Word2Vec
import ast
from gensim.models import KeyedVectors
from collections import Counter
import random
def get_random_keyword():
    okt=Okt()
    conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
    cur=conn.cursor()
    sql="SELECT video_info_keywords FROM youtube_test_data ORDER BY video_info_rank"
    #keyword=["고양이","강아지"]
    #keyword="|".join(keyword)
    cur.execute(sql)
    result_set=cur.fetchall()
    word_list=[]
    for i in range(len(result_set)):
        words=result_set[i][0].split('|')
        for j in range(len(words)):
            word_list.append(words[j])
    random_list=random.sample(word_list,10)
    return random_list

    
