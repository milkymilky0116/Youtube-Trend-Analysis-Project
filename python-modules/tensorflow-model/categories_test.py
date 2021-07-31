from gensim.models import Word2Vec, word2vec
import pandas as pd
import tensorflow as tf
from util.sentence_tokenize import *
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences


model=tf.keras.models.load_model('model/predict_yt_category/1', compile=True)
print(model.summary())

test_title="굳이 데스크탑 사지마? 노트북을 마치 컴퓨터 본체처럼 쓰는 가장 쉬운 방법. 클램쉘 모드를 아시나요?"
token_sentence=sentence_tokenize(test_title)

with open('./model/tokenizer.pickle','rb') as handle:
    tokenizer=pickle.load(handle)
encode_sentence=tokenizer.texts_to_sequences([token_sentence])
pad_sentence=pad_sequences(encode_sentence, maxlen=30)
print(pad_sentence)

print(model.predict(pad_sentence).argmax())

