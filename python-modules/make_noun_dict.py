import json
import pandas as pd
import ijson
from konlpy.tag import Okt
from pandas.io.json import json_normalize
from namuwiki.extractor import extract_text
from PyKomoran import Komoran
from gensim.models import word2vec
from py4j.protocol import Py4JError, Py4JJavaError
import math
import multiprocessing as mp
komoran=Komoran("EXP")
komoran.set_user_dic('dic.user')
okt=Okt()
def analysis_text(sentence):
  sentence_nouns=okt.nouns(sentence)
  return sentence_nouns


capture_values = [
    ("item.namespace", "string"),
    ("item.title", "string"),
    ("item.text", "string")
]
def parse_namuwiki_json(limit = -1, debug=False):
  i = 0
  doc = {}
  with open('namu_wiki.json', encoding='utf-8') as f:
    for prefix, event, value in ijson.parse(f):
      
      if debug:
        print(prefix, event, value)

      if (prefix, event) in capture_values:
        doc[prefix[5:]] = value
      if (prefix, event, value) == ("item", "end_map", None):
        yield doc    
        doc = {}
        i += 1

        if limit > 0 and i >= limit:
          break

import re

cleaning_first_patterns = [
  r"\[\*[^\]]+\]",
  r"~~[^~]+~~"
]
cleaning_first_patterns = [re.compile(pattern, re.IGNORECASE | re.MULTILINE) for pattern in cleaning_first_patterns]

cleaning_patterns = [
  r"\([^\)]+\)"
]
cleaning_patterns = [re.compile(pattern, re.IGNORECASE | re.MULTILINE) for pattern in cleaning_patterns]

replace_patterns = {
    '\\n': "\n",
    "\\'": "",
    "\\-": "",
    "\\.": ""
}

def clean_text(text):
  for regex in cleaning_first_patterns:
    text = re.sub(regex, "", text)
   
  text = extract_text(text)

  for regex in cleaning_patterns:
    text = re.sub(regex, "", text)

  text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
  return text
title=[]

def worker(data):
    with open('process_data.txt', 'w', encoding='utf-8') as output:
      for i, doc in enumerate(data):
        clean_context=clean_text(doc['text'])
        if clean_context=="":
          pass
        else:
          context_noun=analysis_text(clean_context)
          output.write(','.join(context_noun))
          output.write('\n')
        if i%100==0:
          print('progress :',i)



if __name__ =='__main__':
  worker(parse_namuwiki_json())













"""
def namu_word2vec():
  context=[]
  for i, doc in enumerate(parse_namuwiki_json()):
    title_text=clean_text(doc['title'])
    title.append(title_text)
    context_text=clean_text(doc['text'])
    try:
      context_noun=analysis_text(context_text)
      context.append(context_noun)
    except Py4JJavaError as e:
      pass
    
    if i%100==0:
      print('progress :',i)
  return context





embedding = word2vec.Word2Vec(namu_word2vec(), vector_size=350, window=5, batch_words=10000, min_count=10, iter=10 , sg=1, workers=multiprocessing.cpu_count())
embedding.save('post.embedding')
"""
  

"""
with open("dic.user", "w", encoding='utf-8') as out:
  for i in range(len(title)):
    out.write(title[i]+'\t'+'NNP')
    out.write('\n')
"""

  
  
  