import time
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import re
import pandas as pd
from collections import OrderedDict
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def scroll_to_bottom(driver):

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight );")
        time.sleep(2.0)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
def string_int_filtering(text):
    text_count = re.findall(r'(\d+(?:\.\d+)?)',text)
    int_count=float(text_count[0])
    if text.find('만')!=-1:
        int_count=int_count*10000
    elif text.find('천')!=-1:
        int_count=int_count*1000
    return int(int_count)

def comment_crawler(title_url_list,driver):
    all_comments=[]
    for i in range(1,len(title_url_list)):
        time.sleep(10)
        driver.get('https://youtube.com'+title_url_list[i])
        html = driver.find_element_by_tag_name('html')

        driver.execute_script("window.scrollTo(0,500)")

        time.sleep(20)

        #scroll_to_bottom(driver)
        
        comment_count=driver.find_element_by_xpath('//*[@id="count"]/yt-formatted-string/span[2]').text
        comment_count=comment_count.replace(',','')
        print(comment_count)
        SCROLL_PAUSE_TIME = 2
        CYCLES = int(comment_count) * 1/150
        CYCLES= int(CYCLES)
        print(CYCLES)

        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(SCROLL_PAUSE_TIME * 2)

        for i in range(CYCLES):
            html.send_keys(Keys.END)
            time.sleep(SCROLL_PAUSE_TIME)

        comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
        temp=[]
        for elem in comment_elems:
            comment=elem.text.replace('\n','').replace('\r','')
            temp.append(comment)
            if len(temp)>800:
                print(len(temp))
                break
        #all_comments = [elem.text.replace('\n','').replace('\r','') for elem in comment_elems]
        for i in range(len(temp)):
            all_comments.append(temp[i])
    comment_orderd_dict=OrderedDict([
        ('comment', all_comments)
    ])
    return comment_orderd_dict


def extract_keywords(key_info,n):
    ngram_range=(1,1)
    count=CountVectorizer(ngram_range=ngram_range).fit([key_info])
    candidates=count.get_feature_names()
    model=SentenceTransformer('distilbert-base-nli-mean-tokens')
    doc_embedding=model.encode([key_info])
    candidates_embedding=model.encode(candidates)

    top_n=n
    distance=cosine_similarity(doc_embedding,candidates_embedding)
    keywords=[candidates[index] for index in distance.argsort()[0][-top_n:]]

    return keywords