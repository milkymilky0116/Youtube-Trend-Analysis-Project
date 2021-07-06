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
from util.crawling_method import scroll_to_bottom
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

f=open('dataset/comment_data.csv','w')
f.write('comment')
driver=webdriver.Chrome('driver/chromedriver.exe')
driver.get('https://www.youtube.com/watch?v=3_DxLk2bii0')
time.sleep(2)
"""
time.sleep(2.0)
scroll_to_bottom(driver)
"""

driver.execute_script("window.scrollTo(0,300)")
comment_count=driver.find_element_by_xpath('//*[@id="count"]/yt-formatted-string/span[2]').text







