import csv
import os
from re import M
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
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
os.chdir('C:\youtube_trend\Youtube-Trend-Analysis-Project')
komoran=Komoran(DEFAULT_MODEL['FULL'])
komoran.set_user_dic('dataset\dic.user')


data=pd.read_csv('dataset/KRvideos.csv', engine='python')
df=data[:]
for col in ['video_id', 'trending_date', 'channelTitle', 'publishedAt', 'view_count' ,'likes']:
    del df[col]

yt_title=df['title']
yt_category=df['categoryId']
yt_description=df['description']
yt_tags=df['tags']
y_data=yt_category

temp=data_tokenize(yt_title)
x_data=temp
tokenizer=Tokenizer()
tokenizer.fit_on_texts(x_data)
x_data=tokenizer.texts_to_sequences(x_data)
x_data=pad_sequences(x_data, maxlen=30)

y_data=to_categorical(y_data)

x_train, x_test, y_train, y_test= train_test_split(x_data, y_data, test_size=0.3, random_state=777, stratify=y_data)

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

model=Sequential()
model.add(Embedding(25000, 128))
model.add(LSTM(128))
model.add(Dense(30, activation='softmax'))


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model_dir = './model'
if not os.path.exists(model_dir):
    os.mkdir(model_dir)
model_path = model_dir + "/predict_yt_category.model"
checkpoint = ModelCheckpoint(filepath=model_path, monitor="val_loss", verbose=1, save_best_only=True)
early_stopping = EarlyStopping(monitor='val_loss', patience=7)

history=model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test), callbacks=[checkpoint, early_stopping]) 

category_list={
    1:'Film & Animation',
    2:'Autos & Vehicles',
    10:"Music",
    15:"Pets & Animals",
    17:"Sports",
    18:"Short Movies",
    19:"Travel & Events",
    20:"Gaming",
    21:"Videoblogging",
    22:"People & Blogs",
    23:"Comedy",
    24:"Entertainment",
    25:"News & Politics",
    26:"Howto & Style",
    27:"Education",
    28:"Science & Technology",
    30:"Movies",
    31:"Anime/Animation",
    32:"Action/Adventure",
    33:"Classics",
    34:"Comedy",
    35:"Documentary",
    36:"Drama",
    37:"Family",
    38:"Foreign",
    39:"Horror",
    40:"Sci-Fi/Fantasy",
    41:"Thriller",
    42:"Shorts",
    43:"Shows",
    44:"Trailers"
}

test_title="당신도 프로입니까? 아이패드 프로 12.9 (5세대) 리뷰 [4K]"
token_sentence=sentence_tokenize(test_title)
encode_sentence=tokenizer.texts_to_sequences([token_sentence])
pad_sentence=pad_sequences(encode_sentence, maxlen=30)

score=model.predict(pad_sentence)
print(category_list[score.argmax()], score[0,score.argmax()])