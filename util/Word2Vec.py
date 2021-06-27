import csv
import os
import numpy as np
import pandas as pd
from PyKomoran import *
import gensim


class Word2Vec():
    def __init__(self):
        None
    def tokenize(self, txt):
        pos_tag=Komoran(DEFAULT_MODEL['LIGHT'])
        return ['/'.join(t) for t in pos_tag.pos(txt, norm=True, stem=True)]

    def read_data(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            data=[line.split('\t') for line in f.read().splitlines()]
        return data
    def Word2vec_model(self, model_name):
        model= gensim.models.word2vec.Word2Vec.load(model_name)
        return model
    def Convert2Vec(self, model_name, doc):
        word_vec=[]
        model=gensim.models.word2vec.Word2Vec.load(model_name)
        for sent in doc:
            sub=[]
            for word in sent:
                if word in model.wv.vocab:
                    sub.append(model.wv[word])
                else:
                    sub.append(np.random.uniform(-0.25,0.25,300))
            word_vec.append(sub)
        return word_vec
    def Zero_padding(self, train_batch_x, Batch_size, Maxseq_length, Vector_size):
        zero_pad=np.zeros((Batch_size,Maxseq_length,Vector_size))
        for i in range(Batch_size):
            zero_pad[i,:np.shape(train_batch_x[i])[0], :np.shape(train_batch_x[i])[1]]=train_batch_x[i]
        return zero_pad
    
    def One_hot(self,data):
        index_dict={value:index for index,value in enumerate(set(data))}
        result=[]

        for value in data:
            one_hot=np.zeros(len(index_dict))
            index=index_dict[value]
            one_hot[index]=1
            result.append(one_hot)
        return result
