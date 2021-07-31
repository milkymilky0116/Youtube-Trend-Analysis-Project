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
import pandas as pd
from util.crawling_method import scroll_to_bottom, string_int_filtering
from collections import OrderedDict
from pytube import YouTube


driver=webdriver.Chrome('driver/chromedriver.exe')
def filter_keyword(keyword):
    #keyword="고양이"
    search_keyword="%23"+keyword
    driver.get('https://www.youtube.com/results?search_query='+search_keyword)
    driver.implicitly_wait(3)

    filter_button=driver.find_element_by_xpath("//*[@id='container']/ytd-toggle-button-renderer/a")
    filter_button.click()

    time.sleep(5)

    today_button=driver.find_element_by_xpath("//ytd-search-filter-renderer[2]//a[@id='endpoint']")
    sort_by_button=driver.find_element_by_xpath("//ytd-search-filter-group-renderer[5]//ytd-search-filter-renderer[3]//a[@id='endpoint']")
    today_button.click()

    time.sleep(5)

    filter_button.click()

    time.sleep(5)
    sort_by_button.click()

filter_keyword("강아지")
i=1
j=1

time.sleep(5)
video_info_title=[]
video_info_link=[]
video_info_keywords=[]
video_info_views=[]
video_info_thumbnails=[]
while True:
    print(j)
    page=driver.page_source
    soup=BeautifulSoup(page,'lxml')

    all_video_sections=soup.select("#contents > ytd-item-section-renderer:nth-of-type({})".format(j))
    video_len=None
    for child in all_video_sections:
        all_videos=child.find_all(id='dismissible')
        for video in all_videos:
            video_len=len(all_videos)
            video_info=video.find(id='video-title')
            href=video_info.attrs['href']
            #view=[i.text for i in video.select('#metadata-line > span:nth-of-type(1)')][0]
            #view=string_int_filtering(view)
            #print(href)
            
            video_link="https://www.youtube.com"+href
            video_tube=YouTube(video_link)

            video_info_title.append(video_tube.title)
            video_info_link.append(href)
            video_info_keywords.append(video_tube.keywords)
            video_info_views.append(video_tube.views)
            video_info_thumbnails.append(video_tube.thumbnail_url)
            print(video_tube.title)
            print(video_tube.keywords)
            print(video_tube.views)
            print(video_tube.thumbnail_url)


    driver.execute_script("window.scrollTo(0, 400*{});".format(video_len*2))
    j=j+1
    time.sleep(5)


