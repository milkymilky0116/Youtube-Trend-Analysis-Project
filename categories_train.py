import csv
import os
from numpy.core.defchararray import title
import tensorflow as tf
import numpy as np
import pandas as pd
from PyKomoran import *
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding,LSTM,Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences
from util.sentence_tokenize import *

os.chdir('C:\youtube_trend\Youtube-Trend-Analysis-Project')
komoran=Komoran(DEFAULT_MODEL['FULL'])
komoran.set_user_dic('dataset\dic.user')


data=pd.read_csv('dataset/KRvideos.csv', engine='python')
df=data[:]
for col in ['video_id', 'trending_date', 'channel_title', 'publish_time', 'views' ,'likes' , 'dislikes']:
    del df[col]

yt_title=df['title']
yt_category=df['category_id']
y_data=yt_category

"""
temp=[]
for i in range(len(df)):
    sentence=yt_title[i]
    sentence_nouns=komoran.get_morphes_by_tags(sentence, tag_list=['NNG','NNP','NNB','NP','NR','VV','VA','VC','MM','MA'])
    temp.append(sentence_nouns)
"""
temp=data_tokenize(yt_title)
x_data=temp
tokenizer=Tokenizer()
tokenizer.fit_on_texts(x_data)
x_data=tokenizer.texts_to_sequences(x_data)
x_data=pad_sequences(x_data, maxlen=45)

y_data=to_categorical(y_data)

x_train, x_test, y_train, y_test= train_test_split(x_data, y_data, test_size=0.3, random_state=777, stratify=y_data)

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

model=Sequential()
model.add(Embedding(25000, 128))
model.add(LSTM(128))
model.add(Dense(45, activation='softmax'))

##########모델 학습

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=50, validation_data=(x_test, y_test)) 


test_title="[포켓몬 유나이트] 롤, 히오스 같은 포켓몬스터 게임 (Pokémon UNITE)"
token_sentence=sentence_tokenize(test_title)
encode_sentence=tokenizer.texts_to_sequences([token_sentence])
pad_sentence=pad_sequences(encode_sentence, maxlen=45)

score=model.predict(pad_sentence)
print(score.argmax(), score[0,score.argmax()])