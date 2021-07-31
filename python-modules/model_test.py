import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import urllib.request
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
okt=Okt()
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
with open('sentiment_token.pickle','rb') as handle:
    tokenizer=pickle.load(handle)
loaded_model=load_model('best_model.h5')
def sentiment_predict(new_sentence):
    new_sentence=okt.morphs(new_sentence,stem=True)
    new_sentence=[word for word in new_sentence if not word in stopwords]
    encodeded=tokenizer.texts_to_sequences([new_sentence])
    pad_new=pad_sequences(encodeded,maxlen=30)
    score=float(loaded_model.predict(pad_new))
    if(score > 0.5):
        print("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
    else:
        print("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))

sentence="ㅋㅋㅋㅋㅋㅋㅋ ㄹㅇ 개웃기네"
sentiment_predict(sentence)