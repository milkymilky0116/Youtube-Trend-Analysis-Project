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

import twitter
twitter_consumer_key = "3GMcnn0TU3LJ7OzYI1l06kmdY"
twitter_consumer_secret = "ll8ZiXwfE8RPyDCHm23Mzm66XFwaXdHBpb4AojTBqGkNGQodYA"  
twitter_access_token = "1405566672522465281-8I81m6mU5VGPKBpCIsgDYFQyEvOtZw"
twitter_access_secret = "AlT8zhRYvEPxKH5uuieqbifmoj0SwN7B9tOXUpWBG7p3V"
twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                          consumer_secret=twitter_consumer_secret, 
                          access_token_key=twitter_access_token, 
                          access_token_secret=twitter_access_secret)

    
query = "카불"
statuses = twitter_api.GetSearch(term=query, result_type='recent',count=20)
twitter_result=[]
for status in statuses:
    twitter_result.append(status.text)
print(twitter_result)