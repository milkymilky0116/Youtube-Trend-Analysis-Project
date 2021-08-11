
import time
import pymysql
from util.crawling_method import *

import pandas as pd

from pytube import YouTube
from util.vis_word_map import make_word_map
from sqlalchemy import create_engine

class Youtube_Crawler:
    def __init__(self,keywords,client_id,client_secret,google_api):
        self.video_info_title=[]
        self.video_info_link=[]
        self.video_info_keywords=[]
        self.video_info_views=[]
        self.video_info_thumbnails=[]
        self.video_info_channelId=[]
        self.video_info_description=[]
        self.video_info_publish_date=[]
        self.video_info_author=[]
        self.video_info_summary_data=[]
        self.video_info_sentiment=[]

        self.video_data=None
        self.video_dataframe=None

        self.__client_id=client_id
        self.__client_secret=client_secret

        self.__google_api=google_api

        self.keywords=keywords

        self.tm=time.strftime('%Y-%m-%d-%I %M-%S-%p', time.localtime(time.time()))
        
        self.crawling()
    
    def get_client_id(self):
        return self.__client_id
    def get_google_api_key(self):
        return self.__google_api

    def get_client_secret(self):
        return self.__client_secret
    def get_video_dataframe(self):
        return self.video_dataframe
    def set_driver(self,statement):
        if statement=="local":
            driver=set_driver_local()
        elif statement=="server":
            driver=set_driver_remote()
        return driver

    def collect_data(self,driver,args):
        start=time.time()
        for i in range(len(args)):
            keyword_list=make_word_map(args[i])
            for i in range(len(keyword_list)):
                vid_info(keyword_list[i],driver,self.tm)
                print("complete:",keyword_list[i])
            driver.quit()
        end=time.time()
        print((end-start)/60)
    def parsing_data(self):
        start=time.time()
        with open('files/dataset_init_{}.txt'.format(self.tm),'rt',encoding='utf-8') as f:
            links=f.readlines()
            for link in links:
                link=link[:link.find("\n")]
                video_link="https://www.youtube.com"+link
                video_tube=YouTube(video_link)
                self.video_info_link.append(link)
                self.video_info_title.append(video_tube.title)
                print("Title:",video_tube.title)
                keywords="|".join(video_tube.keywords)
                self.video_info_keywords.append(keywords)
                self.video_info_views.append(video_tube.views)
                self.video_info_thumbnails.append(video_tube.thumbnail_url)
                self.video_info_author.append(video_tube.author)
                self.video_info_channelId.append(video_tube.channel_id)
                self.video_info_publish_date.append(video_tube.publish_date)
                self.video_info_description.append(video_tube.description)
        end=time.time()
        print((end-start)/60)

    def summary_data(self):
        start=time.time()
        for i in range(len(self.video_info_link)):
            keywords=self.video_info_keywords[i]
            title=self.video_info_title[i]
            description=self.video_info_description[i]

            sep_keyword=keywords.split("|")
            sep_keyword=" ".join(sep_keyword)

            key_info=title+" "+sep_keyword+" "+description

            summary_data=extract_keywords(key_info,2)

            summary_data=" ".join(summary_data)

            self.video_info_summary_data.append(summary_data)
            print("Summary:",summary_data)

        end=time.time()
        print("Data Analyse Complete")
        print((end-start)/60)

    def comment_analysis(self,driver):
        self.id=self.get_client_id()
        self.key=self.get_client_secret()
        self.api=self.get_google_api_key()
        for i in range(len(self.video_info_link)):

            print('Title:',self.video_info_title[i])

            #comment_list=comment_crawler(driver,self.video_info_link[i])
            comment_list=comment_crawler(self.api,self.video_info_link[i])
            print(comment_list)
            sentiment_list=sentiment_analyse(comment_list,self.id,self.key)
            print(sentiment_list)
            self.video_info_sentiment.append(str(sentiment_list))
        #driver.quit()


    def save_df(self):
        self.video_data=zip(
            self.video_info_title,
            self.video_info_link,
            self.video_info_keywords,
            self.video_info_views,
            self.video_info_thumbnails,
            self.video_info_channelId,
            self.video_info_description,
            self.video_info_publish_date,
            self.video_info_author,
            self.video_info_summary_data,
            self.video_info_sentiment,
        )
        self.video_dataframe=pd.DataFrame(self.video_data, columns=[
            "video_info_title",
            "video_info_link",
            "video_info_keywords",
            "video_info_views",
            "video_info_thumbnails",
            "video_info_channelId",
            "video_info_description",
            "video_info_publish_date",
            "video_info_author",
            "video_info_summary_data",
            "video_info_sentiment"])
        return self.video_dataframe

    def save_df_to_db(self,ip,port,user,pw,db_name):
        self.video_dataframe=self.save_df()

        print(self.video_dataframe)

        conn=None
        cur=None

        sql=""

        #Maria DB 서버와 연결
        #conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
        conn=pymysql.connect(host=ip,port=port, user=user, password=pw, db=db_name, charset='utf8mb4')
        #커넥터 연결
        cur=conn.cursor()

        df=self.get_video_dataframe()
        
        #sql문 테이블 생성
        """
        sql="CREATE TABLE IF NOT EXISTS youtube_test_data(
                video_info_title varchar(100) NOT NULL,
                video_info_link varchar(100) NOT NULL,
                video_info_keywords varchar(500) NULL,
                video_info_views char(50) NOT NULL,
                video_info_thumbnails varchar(100) NOT NULL,
                video_info_author varchar(100) NOT NULL,
                video_info_channelId varchar(100) NOT NULL,
                video_info_publish_date char(20) NOT NULL ,
                video_info_description varchar(10000) NULL,
                video_info_summary_data varchar(100) NULL,
                video_info_sentiment varchar(10) NULL
                );"
        cur.execute(sql)

        #PRIMARY KEY 에러 방지를 위한 AUTO INCREMENT문 실행
        sql="ALTER TABLE youtube_test_data AUTO_INCREMENT = 1;"
        cur.execute(sql)
        """
        engine=create_engine('mysql+mysqlconnector://root:sjlee3423@110.165.16.124:30141/Youtube_Trend_Server')

        df.to_sql(name='youtube_test_data',con=engine,index=False)

    def crawling(self):

        print("="*50)
        print("Stage 1: Collecting Data")
        print("="*50)
        driver=self.set_driver('server')
        self.collect_data(driver,self.keywords)

        print("="*50)
        print("Stage 2: Parsing Data")
        print("="*50)
        self.parsing_data()

        print("="*50)
        print("Stage 3: Summary Data")
        print("="*50)
        self.summary_data()

        print("="*50)
        print("Stage 4: Comment Sentiment Analysis")
        print("="*50)
        #driver=self.set_driver('server')
        self.comment_analysis(driver)
        

        print("="*50)
        print("Stage 5: Save Data to Maria DB")
        print("="*50)
        self.save_df_to_db("110.165.16.124",30141,'root','sjlee3423','Youtube_Trend_Server')

if __name__=="__main__":
    keyword_list=['여행']
    Youtube_Crawler(keyword_list,"zofo3v8hwj","uSaxHZaefo6WTQ2rwcdNJqVGnngg3QkjA10dvEw9","AIzaSyA8AVDeWVW2aEqMds7z51gjhr8o3ebRyik")