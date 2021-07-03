import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import urllib.request
from PyKomoran import *
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from util.sentence_tokenize import sentence_tokenize
komoran=Komoran(DEFAULT_MODEL['FULL'])
train_data=pd.read_table('dataset/ratings_train.txt')
test_data=pd.read_table('dataset/ratings_test.txt')

train_data.drop_duplicates(subset=['document'], inplace=True)

print(train_data.isnull().values.any())

train_data['document']=train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
train_data['document'] = train_data['document'].str.replace('^ +', "")
train_data['document'].replace('', np.nan, inplace=True)

train_data=train_data.dropna(how='any')

test_data.drop_duplicates(subset = ['document'], inplace=True)
test_data['document'] = test_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") 
test_data['document'] = test_data['document'].str.replace('^ +', "") 
test_data['document'].replace('', np.nan, inplace=True) 

test_data = test_data.dropna(how='any') 

x_train=[]
for sentence in train_data['document']:
    sentence_token=sentence_tokenize('sentence')
    print(sentence_token)


"""
tokenizer=Tokenizer()
tokenizer.fit_on_text(x_train)


print(tokenizer.word_index)
"""