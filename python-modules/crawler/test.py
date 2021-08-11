import requests
from selenium import webdriver as wd

from selenium import webdriver

import csv
import pandas as pd
import time
import os
import re
import json
import collections
from langdetect import detect

text='{"document":{"sentiment":"positive","confidence":{"negative":0.042479347,"positive":99.95143,"neutral":0.0060882084}},"sentences":[{"content":"사랑해요","offset":0,"length":4,"sentiment":"positive","confidence":{"negative":0.002548761,"positive":0.997086,"neutral":3.652925E-4},"highlights":[{"offset":0,"length":4}]}]}'
text=text[text.find('sentiment'):text.find('confidence')]
print(text)
new_string = re.sub(r"[^a-zA-Z0-9:]"," ",text)
print(new_string)

body={
    'content':'사랑합니다'
}

jsonString=json.dumps(body)

print(jsonString)

sentence="what's your hobby"
print(detect(sentence)=='en')

sentiment_list=['positive','positive','negative','positive','netural']
frquency=collections.Counter(sentiment_list)

list1=[1,2,3]
list2=[4,5,6]

list=zip(list1,list2)

df=pd.DataFrame(list,columns=[1,2])
print(df[1])

print(time.localtime(time.time()))

print(time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime(time.time())))



