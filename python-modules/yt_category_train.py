import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import urllib.request
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras.layers import Embedding, Dense, LSTM, Bidirectional, Concatenate, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras import Input, Model,optimizers
import pickle
import tensorflow as tf

from tensorflow.python.keras.backend import backend

class BahdanauAttention(tf.keras.Model):
  def __init__(self, units):
    super(BahdanauAttention, self).__init__()
    self.W1 = Dense(units)
    self.W2 = Dense(units)
    self.V = Dense(1)

  def call(self, values, query): # 단, key와 value는 같음
    # query shape == (batch_size, hidden size)
    # hidden_with_time_axis shape == (batch_size, 1, hidden size)
    # score 계산을 위해 뒤에서 할 덧셈을 위해서 차원을 변경해줍니다.
    hidden_with_time_axis = tf.expand_dims(query, 1)

    # score shape == (batch_size, max_length, 1)
    # we get 1 at the last axis because we are applying score to self.V
    # the shape of the tensor before applying self.V is (batch_size, max_length, units)
    score = self.V(tf.nn.tanh(
        self.W1(values) + self.W2(hidden_with_time_axis)))

    # attention_weights shape == (batch_size, max_length, 1)
    attention_weights = tf.nn.softmax(score, axis=1)

    # context_vector shape after sum == (batch_size, hidden_size)
    context_vector = attention_weights * values
    context_vector = tf.reduce_sum(context_vector, axis=1)

    return context_vector, attention_weights

urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt", filename="ratings_train.txt")
urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt", filename="ratings_test.txt")

okt=Okt()
train_data = pd.read_table('ratings_train.txt')
test_data = pd.read_table('ratings_test.txt')

document=train_data['document']
label=train_data['label']

train_data.drop_duplicates(subset = ['document'], inplace=True) 
train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") 
train_data['document'] = train_data['document'].str.replace('^ +', "") 
train_data['document'].replace('', np.nan, inplace=True) 
train_data = train_data.dropna(how='any')

print('전처리 후 테스트용 샘플의 개수 :',len(train_data))

test_data.drop_duplicates(subset = ['document'], inplace=True) 
test_data['document'] = test_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") 
test_data['document'] = test_data['document'].str.replace('^ +', "") 
test_data['document'].replace('', np.nan, inplace=True) 
test_data = test_data.dropna(how='any') 

print('전처리 후 테스트용 샘플의 개수 :',len(test_data))

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

x_train=[]
for sentence in train_data['document']:
    temp_x=okt.morphs(sentence, stem=True)
    temp_x=[word for word in temp_x if not word in stopwords]
    x_train.append(temp_x)

x_test=[]

for sentence in test_data['document']:
    temp_x=okt.morphs(sentence, stem=True)
    temp_x=[word for word in temp_x if not word in stopwords]
    x_test.append(temp_x)

tokenizer=Tokenizer()
tokenizer.fit_on_texts(x_train)
print(tokenizer.word_index)

threshold=3
total_cnt=len(tokenizer.word_index)
rare_cnt=0
total_freq=0
rare_freq=0

for key,value in tokenizer.word_counts.items():
    total_freq=total_freq+value

    if(value<threshold):
        rare_cnt=rare_cnt+1
        rare_freq=rare_freq+value


vocab_size=total_cnt-rare_cnt+1

tokenizer=Tokenizer(vocab_size)
tokenizer.fit_on_texts(x_train)
x_train=tokenizer.texts_to_sequences(x_train)
x_test=tokenizer.texts_to_sequences(x_test)

y_train=np.array(train_data['label'])
y_test=np.array(test_data['label'])

drop_train=[index for index,sentence in enumerate(x_train) if len(sentence)<1]

x_train=np.delete(x_train,drop_train,axis=0)
y_train=np.delete(y_train,drop_train,axis=0)

def below_threshold_len(max_len,nested_list):
    cnt=0
    for s in nested_list:
        if(len(s)<=max_len):
            cnt=cnt+1
max_len=30
x_train=pad_sequences(x_train,maxlen=max_len)
x_test=pad_sequences(x_test,maxlen=max_len)

sequence_input=Input(shape=(max_len,), dtype='int32')
embedded_sequences=Embedding(vocab_size,128,input_length=max_len, mask_zero=True)(sequence_input)
lstm=Bidirectional(LSTM(64, dropout=0.5, return_sequences=True))(embedded_sequences)
lstm, forward_h, forward_c, backward_h, backward_c=Bidirectional(LSTM(64,dropout=0.5,return_sequences=True, return_state=True))(lstm)

state_h = Concatenate()([forward_h, backward_h]) # 은닉 상태
state_c = Concatenate()([forward_c, backward_c]) # 셀 상태

attention = BahdanauAttention(64) # 가중치 크기 정의
context_vector, attention_weights = attention(lstm, state_h)

dense1 = Dense(20, activation="relu")(context_vector)
dropout = Dropout(0.5)(dense1)
output = Dense(1, activation="sigmoid")(dropout)
model = Model(inputs=sequence_input, outputs=output)

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(x_train, y_train, epochs = 3, batch_size = 256, validation_data=(x_test, y_test), verbose=1)

es=EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
mc=ModelCheckpoint('best_model.h5',monitor='val_acc', mode='max', verbose=1, save_best_only=True)

loaded_model=load_model('best_model.h5')
print(loaded_model.evaluate(x_test,y_test)[1])

with open('sentiment_token.pickle','wb') as handle:
    pickle.dump(tokenizer,handle,protocol=pickle.HIGHEST_PROTOCOL)