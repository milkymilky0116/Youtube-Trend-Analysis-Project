import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import re
import urllib.request

from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt", filename="dataset/ratings_train.txt")
urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt", filename="dataset/ratings_test.txt")


train_data=pd.read_table('dataset/ratings_train.txt')
test_data=pd.read_table('dataset/ratings_test.txt')

train_data['document'].nunique(), train_data['label'].nunique()
train_data.drop_duplicates(subset=['document'], inplace=True)


train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

train_data['document'] = train_data['document'].str.replace('^ +', "")
train_data['document'].replace('', np.nan, inplace=True)

train_data=train_data.dropna(how='any')

test_data.drop_duplicates(subset = ['document'], inplace=True)
test_data['document'] = test_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") 
test_data['document'] = test_data['document'].str.replace('^ +', "") 
test_data['document'].replace('', np.nan, inplace=True) 
test_data = test_data.dropna(how='any')

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

x_train=[]
okt=Okt()
for sentence in train_data['document']:
    sentence=sentence.lower()
    temp_x=okt.morphs(sentence, stem=True)
    temp_x=[word for word in temp_x if not word in stopwords]
    x_train.append(x_train)

for sentence in train_data['document']:
    sentence=sentence.lower()
    temp_x=okt.morphs(sentence, stem=True)
    temp_x=[word for word in temp_x if not word in stopwords]
    x_train.append(x_train)

tokenizer=Tokenizer()
tokenizer.fit_on_texts(x_train)

print(tokenizer.word_index)