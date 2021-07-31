from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from collections import Counter
from time import sleep
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import re
import sys
import requests
import csv
from util.crawling_method import scroll_to_bottom
import pandas as pd
from collections import OrderedDict


driver=webdriver.Chrome('http://110.165.16.124:32341/')
driver.get('https://www.youtube.com/feed/explore')
driver.implicitly_wait(3)
"""
f=open('dataset/comment_data.csv','wt' , encoding='utf-8')
f.write('comment')
"""
#csvWriter=csv.writer(f)

scroll_to_bottom(driver)


time.sleep(1.5)


page=driver.page_source
soup=BeautifulSoup(page,'lxml')

all_videos=soup.find_all(id='dismissible')
title_url_list=[]
for video in all_videos:
    title=video.find(id='video-title')
    href=title.attrs['href']
    title_url_list.append(href)


def comment_crawler(title_url_list):
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

print(comment_crawler(title_url_list))



