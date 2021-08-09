from util.crawling_method import extract_keywords
import pandas as pd
import time
import math
import numpy as np
from csv import DictWriter
import csv
from nltk.tokenize import word_tokenize

data=pd.read_csv('video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))),encoding='utf-8')

title=list(data['title'])
data['keywords']=data['keywords'].fillna('')
data['description']=data['description'].fillna('')

keywords=list(data['keywords'])
description=list(data['description'])


with open('stopwords.txt','r',encoding='utf-8') as f:
    text=f.read().split('\n')

summary=[]
for i in range(len(title)):
    keyword=keywords[i].split('|')
    keyword=" ".join(keyword)
    key_info=title[i]+" "+keyword+" "+description[i]
    
    summary_data=extract_keywords(key_info,2)

    summary_data=" ".join(summary_data)

    print(summary_data)

    summary.append(summary_data)

data['summary']=summary

print(data)

data.to_csv('video_data_{}_summary.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))),mode='a',index=False, encoding='utf-8')


