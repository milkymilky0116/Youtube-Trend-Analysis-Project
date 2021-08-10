from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.action_chains import ActionChains
from util.crawling_method import set_driver_remote, string_int_filtering, extract_keywords
from selenium.webdriver.common.keys import Keys
import pandas as pd

from pytube import YouTube
from vis_word_map import make_word_map
import datetime
import os


def vid_info(keyword,driver):
    #filter_keyword(keyword,driver)
    search_keyword="%23"+keyword
    driver.get('https://www.youtube.com/results?search_query='+search_keyword+'&sp=CAMSBAgCEAE%253D')
    j=1

    video_info_link=[]
    
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
                view=[i.text for i in video.select('#metadata-line > span:nth-of-type(1)')][0]
                view=string_int_filtering(view)

                if view>1000:
                    video_info_link.append(href)
                    print(href)
                    section_views.append(view)
                #prev_view_avg=sum(section_views)/len(section_views)
            

                
            if len(section_views)>3:
                #driver.execute_script("window.scrollTo(0, 800*{});".format(video_len*2))
                element=driver.find_element_by_tag_name('body')
                element.send_keys(Keys.END)
                j=j+1
                time.sleep(1)
            else:
                get_info_avaliable=False
                with open('files/dataset_init_{}.txt'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))),'a',encoding='utf-8') as f:
                    for line in video_info_link:
                        f.write(line)
                        f.write('\n')

                break
            
        if get_info_avaliable==False:
            break
    return video_info_link

def multiple_keyword_search(args):

    start=time.time()

    video_info_title=[]
    video_info_link=[]
    video_info_keywords=[]
    video_info_views=[]
    video_info_thumbnails=[]
    video_info_channelId=[]
    video_info_description=[]
    video_info_publish_date=[]
    video_info_author=[]
    video_info_summary_data=[]


    print("="*50)
    print("Stage 1: Collecting Data")
    print("="*50)

    for i in range(len(args)):
        keyword_list=make_word_map(args[i])
        #driver=webdriver.Chrome('driver/chromedriver.exe')
        driver=set_driver_remote()
        for i in range(len(keyword_list)):
            vid_info(keyword_list[i],driver)
            print("complete:",keyword_list[i])
        driver.quit()

    end=time.time()

    print((end-start)/60)


    print("="*50)
    print("Stage 2: Parsing Data")
    print("="*50)

    start=time.time()
    prev_data=None
    """
    prev_data_link=None
    if os.path.exists('files/dataset_init_{}.txt'.format(time.strftime('%Y-%m-%d', time.localtime(time.time())))):
        prev_data=pd.read_csv('files/dataset_init_{}.txt'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))))
        prev_data_link=prev_data['link']
    """

        

    with open('files/dataset_init_{}.txt'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))),'rt',encoding='utf-8') as f:
        links=f.readlines()
        for link in links:
            link=link[:link.find("\n")]
            video_link="https://www.youtube.com"+link
            video_tube=YouTube(video_link)
            video_info_link.append(link)
            video_info_title.append(video_tube.title)
            print("Title:",video_tube.title)
            keywords="|".join(video_tube.keywords)
            video_info_keywords.append(keywords)
            video_info_views.append(video_tube.views)
            video_info_thumbnails.append(video_tube.thumbnail_url)
            video_info_author.append(video_tube.author)
            video_info_channelId.append(video_tube.channel_id)
            video_info_publish_date.append(video_tube.publish_date)
            video_info_description.append(video_tube.description)
    end=time.time()


    
    print("Data Parsing Complete")

    print((end-start)/60)

    print("="*50)
    print("Stage 3: Analyse Data")
    print("="*50)

    start=time.time()
    for i in range(len(video_info_link)):
        keywords=video_info_keywords[i]
        title=video_info_title[i]
        description=video_info_description[i]

        sep_keyword=keywords.split("|")
        sep_keyword=" ".join(sep_keyword)

        key_info=title+" "+sep_keyword+" "+description

        summary_data=extract_keywords(key_info,2)

        summary_data=" ".join(summary_data)

        video_info_summary_data.append(summary_data)
                
        print("Summary:",summary_data)

    print("Data Analyse Complete")

    print(end-start)

    print("="*50)
    print("Stage 4: Write CSV & Update DB")
    print("="*50)

    start=time.time()


    video_data=zip(video_info_title,
                    video_info_link,
                    video_info_keywords,
                    video_info_views,
                    video_info_thumbnails,
                    video_info_author,
                    video_info_channelId,
                    video_info_publish_date,
                    video_info_description,
                    video_info_summary_data)
    
    df=pd.DataFrame(video_data, columns=['video_info_title','video_info_link','video_info_keywords','video_info_views','video_info_thumbnails','video_info_author','video_info_channelId','video_info_publish_date','video_info_description','video_info_summary_data'])
    df.head(5)
    if not os.path.exists('files/video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time())))):
        #새로 파일 작성
        df.to_csv('files/video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))),mode='w', index=False, encoding='utf-8')

    else:
        df.to_csv('files/video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))),mode='a', index=False, encoding='utf-8')
                    
        datafile=pd.read_csv('files/video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))),sep=',')
        datafile.drop_duplicates(['link'],keep='last',inplace=True)
        datafile.to_csv('files/video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))),mode='w', index=False, encoding='utf-8')

    end=time.time()
    print((end-start)/60)

keyword_list=['강아지','뉴스','여행']


multiple_keyword_search(keyword_list)

