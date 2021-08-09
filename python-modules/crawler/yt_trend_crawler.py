from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from util.crawling_method import set_driver_remote
import pandas as pd
#from util.crawling_method import set_driver_remote
from pytube import YouTube
from vis_word_map import make_word_map
import datetime
import os


def vid_info(keyword,driver):
    #filter_keyword(keyword,driver)
    search_keyword="%23"+keyword
    driver.get('https://www.youtube.com/results?search_query='+search_keyword+'&sp=CAMSBAgCEAE%253D')
    i=1
    j=1
    video_info_title=[]
    video_info_link=[]
    video_info_keywords=[]
    video_info_views=[]
    video_info_thumbnails=[]
    video_info_channelId=[]
    video_info_description=[]
    video_info_publish_date=[]
    video_info_author=[]

    get_info_avaliable=True
    while True:
        page=driver.page_source
        soup=BeautifulSoup(page,'lxml')

        all_video_sections=soup.select("#contents > ytd-item-section-renderer:nth-of-type({})".format(j))
        video_len=None
        for child in all_video_sections:
            all_videos=child.find_all(id='dismissible')
            section_views=[]
            for video in all_videos:
                video_len=len(all_videos)
                video_info=video.find(id='video-title')
                href=video_info.attrs['href']
                #view=[i.text for i in video.select('#metadata-line > span:nth-of-type(1)')][0]
                #view=string_int_filtering(view)
                #print(href)
                video_link="https://www.youtube.com"+href
                video_tube=YouTube(video_link)
                prev_view_avg=None
                if video_tube.views>1000:
                    
                    video_info_title.append(video_tube.title)
                    print(video_tube.title)
                    video_info_link.append(href)
                    keywords="|".join(video_tube.keywords)
                    video_info_keywords.append(keywords)
                    print(keywords)
                    video_info_views.append(video_tube.views)
                    video_info_thumbnails.append(video_tube.thumbnail_url)
                    video_info_author.append(video_tube.author)
                    video_info_channelId.append(video_tube.channel_id)
                    video_info_publish_date.append(video_tube.publish_date)
                    video_info_description.append(video_tube.description)

                    section_views.append(video_tube.views)
                    if len(video_info_link)>100:
                        break
                #prev_view_avg=sum(section_views)/len(section_views)
            print(len(video_info_link))
                
            if len(section_views)>3:
                driver.execute_script("window.scrollTo(0, 800*{});".format(video_len*2))
                j=j+1
                time.sleep(2)
            else:
                get_info_avaliable=False
                
                video_data=zip(
                    video_info_title,
                    video_info_link,
                    video_info_keywords,
                    video_info_views,
                    video_info_thumbnails,
                    video_info_author,
                    video_info_channelId,
                    video_info_publish_date,
                    video_info_description)

                df=pd.DataFrame(video_data, columns=['title','link','keywords','views','thumbnails','channel_name','channel_id','publish_date','description'])
                if not os.path.exists('video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time())))):
                    #새로 파일 작성
                    df.to_csv('video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))),mode='w', index=False, encoding='utf-8')
                else:
                    df.to_csv('video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))),mode='a', index=False, encoding='utf-8')
                    
                    datafile=pd.read_csv('video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))),sep=',')
                    datafile.drop_duplicates(['link'],keep='last',inplace=True)
                    datafile.to_csv('video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))),mode='w', index=False, encoding='utf-8')

                break
        if get_info_avaliable==False:
            break

def multiple_keyword_search(args):
    start=time.time()
    for i in range(len(args)):
        keyword_list=make_word_map(args[i])
        #driver=webdriver.Chrome('driver/chromedriver.exe')
        driver=set_driver_remote()
        for i in range(len(keyword_list)):
            vid_info(keyword_list[i],driver)
            print("complete:",keyword_list[i])
        driver.close()

    end=time.time()
    times = str(datetime.timedelta(seconds=start-end)).split(".")
    times = times[0]
    print(times)

    driver.quit()


keyword_list=['강아지','뉴스','여행']
#keyword_list=['뉴스']

multiple_keyword_search(keyword_list)

