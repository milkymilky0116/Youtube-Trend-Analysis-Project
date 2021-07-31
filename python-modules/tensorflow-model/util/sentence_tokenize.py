from PyKomoran import *
import pandas as pd
komoran=Komoran("EXP")
komoran.set_user_dic('dataset/dic.user')
def data_tokenize(df):
    temp=[]
    for i in range(len(df)):
        sentence=df[i]
        sentence_nouns=komoran.get_morphes_by_tags(sentence, tag_list=['NNG','NNP'])
        temp.append(sentence_nouns)
    return temp
def sentence_tokenize(sentence):
    sentence_nouns=komoran.get_morphes_by_tags(sentence, tag_list=['NNP'])
    return sentence_nouns

