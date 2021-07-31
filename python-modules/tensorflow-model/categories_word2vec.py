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
from categories_train import text_encoding
data=pd.read_csv('dataset/KRvideos.csv', engine='python')
df=data[:]
token=[]
yt_title=df['title']
yt_category=df['categoryId']
yt_description=df['description']
yt_tags=df['tags']
y_data=yt_category


temp=data_tokenize(yt_title)
token.append(temp)
token.append(yt_category)
print(token)

