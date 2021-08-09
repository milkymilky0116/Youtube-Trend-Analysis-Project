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
from fake_useragent import UserAgent
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def set_driver_remote():
    chrome_options=webdriver.ChromeOptions()
    ua=UserAgent()
    userag=ua.random
    print(userag)

    chrome_options.add_argument(f'user-agent={userag}')
    chrome_options.add_argument('headless') # headless 모드 설정
    chrome_options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
    chrome_options.add_argument("disable-gpu") 
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
    chrome_options.add_experimental_option('prefs', prefs)


    driver=webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME,
        options=chrome_options
    )

    return driver

def set_driver_local():
    driver=webdriver.Chrome('driver/chromedriver')

    return driver
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