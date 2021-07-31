from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
import random
import json
import requests
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from util.sentence_tokenize import *
from tensorflow.keras.preprocessing.sequence import pad_sequences
test_title="머나먼 북극마을 대모험 - 세계여행(6)"
headers = {"content-type": "application/json"}
token_sentence=sentence_tokenize(test_title)
print(token_sentence)
with open('./model/tokenizer.pickle','rb') as handle:
    tokenizer=pickle.load(handle)
encode_sentence=tokenizer.texts_to_sequences([token_sentence])
pad_sentence=pad_sequences(encode_sentence, maxlen=30)
print(pad_sentence)
MODEL_URL='http://110.165.16.124:31830/v1/models/test:predict'

data=json.dumps({
    'instances':pad_sentence.tolist()
})
response=requests.post(MODEL_URL,data=data,headers=headers)
result=json.loads(response.text)
prediction=result['predictions']
print(np.argmax(prediction[0]))