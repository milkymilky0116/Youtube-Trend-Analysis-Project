import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from collections import OrderedDict
from pytube import YouTube
import requests
import csv

data=pd.read_csv('KR_youtube_trending_data.csv', engine='python')
df=data[:]

yt_video_id=df['video_id']
yt_title=df['title']

title_url_list=yt_video_id.tolist()
chrome_options=webdriver.FirefoxOptions()
def comment_crawler(title_url_list):
    driver=webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.FIREFOX,
    options=chrome_options)

    all_comments=[]
    for i in range(0,len(title_url_list)):
        time.sleep(5)
        link='https://youtu.be/'+title_url_list[i]
        avaliable_link='http://i.ytimg.com/vi/{}/0.jpg'.format(title_url_list[i])
        if requests.get(avaliable_link).status_code==404:
            pass
        else:
            driver.get(link)
            html = driver.find_element_by_tag_name('html')

            driver.execute_script("window.scrollTo(0,500)")

            time.sleep(5)

            #scroll_to_bottom(driver)
            """
            comment_count=driver.find_element_by_xpath('//*[@id="count"]/yt-formatted-string/span[2]').text
            comment_count=comment_count.replace(',','')
            print(comment_count)
            SCROLL_PAUSE_TIME = 2
            CYCLES = int(comment_count) * 1/150
            CYCLES= int(CYCLES)
            print(CYCLES)
            """

            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(5)


            """"
            for i in range(1):
                html.send_keys(Keys.END)
                time.sleep(SCROLL_PAUSE_TIME)
            """

            comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
            temp=[]
            k=0
            for elem in comment_elems:
                comment=elem.text.replace('\n','').replace('\r','')
                if k==2:
                    break
                else:
                    temp.append(comment)
                k+=1
            print(temp)
            print(len(temp))
            #all_comments = [elem.text.replace('\n','').replace('\r','') for elem in comment_elems]
            for i in range(len(temp)):
                all_comments.append(temp[i])
    return all_comments

comment_data=comment_crawler(title_url_list)
data_frame=pd.DataFrame({"comment":comment_data})
data_frame.to_csv('comment_data.csv',index=None)
