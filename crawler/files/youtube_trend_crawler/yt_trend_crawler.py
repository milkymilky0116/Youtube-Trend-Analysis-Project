
import time
import pymysql
from util.crawling_method import *

import pandas as pd

from pytube import YouTube
from util.vis_word_map import make_word_map
from sqlalchemy import create_engine
from skcriteria import Data, MIN, MAX
from skcriteria.madm import closeness,simple
import codecs

codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)

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
        self.video_info_comment=[]
        self.video_info_sentiment_list=[]
        self.video_info_sentiment_result=[]
        self.video_info_sentiment_value=[]
        self.video_info_change_rate=[]
        self.video_info_change_value=[]
        self.video_info_sns_score=[]
        self.video_info_rank=[]

        
        self.video_data=None
        self.video_dataframe=None

        self.__client_id=client_id
        self.__client_secret=client_secret

        self.__google_api=google_api

        self.keywords=keywords

        self.tm=time.strftime('%Y-%m-%d-%I %M-%p', time.localtime(time.time()))
        
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

                if link not in self.video_info_link:
                    try:
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
                    except:
                        pass
        
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

    def scoring_video(self,ip,port,user,pw,db_name):

        #conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
        conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
        cur=conn.cursor()
        for i in range(len(self.video_info_link)):
            change_rate=0
            sns_count=0
            change_value=0

            current_view=self.video_info_views[i]
            link=(self.video_info_link[i],)

            check="SELECT COUNT(*) FROM Information_schema.tables WHERE table_name= %s"

            cur.execute(check,(db_name))
            ava_val=cur.fetchall()

            print(ava_val)

            if ava_val[0][0]!=0:
                sql="SELECT video_info_link,video_info_views FROM {} WHERE video_info_link=%s".format(db_name)
                cur.execute(sql,link)
                result=cur.fetchall()

                print(result)
                if len(result)>0:
                    sql='DELETE FROM {} WHERE video_info_link=%s'.format(db_name)
                    cur.execute(sql,link)
                    conn.commit()

                    past_result=result[0][1]
                    change_rate=int((int(current_view)-past_result)/past_result *100)
                    change_value=int(current_view)-past_result
            
            keyword=self.video_info_keywords[i].split(' ')

            sns_count=twitter_search(keyword)

            print('change_rate:',change_rate)
            print('change value:',change_value)
            print('sns score:',sns_count)
            
            self.video_info_change_rate.append(change_rate)
            self.video_info_sns_score.append(sns_count)
            self.video_info_change_value.append(change_value)



    def comment_analysis(self,driver):
        self.id=self.get_client_id()
        self.key=self.get_client_secret()
        self.api=self.get_google_api_key()
        for i in range(len(self.video_info_link)):

            print('Title:',self.video_info_title[i])

            #comment_list=comment_crawler(driver,self.video_info_link[i])
            comment_list=comment_crawler(self.api,self.video_info_link[i])
            comment_data=""
            if isinstance(comment_list,list):
                comment_data=",".join(comment_list)
            print(comment_data)
            self.video_info_comment.append(comment_data)
            sentiment_list,sentiment_result,sentiment_value=sentiment_analyse(comment_list,self.id,self.key)
            print(sentiment_list)
            self.video_info_sentiment_list.append(str(sentiment_list))
            print(sentiment_result)
            print(sentiment_value)
            self.video_info_sentiment_result.append(sentiment_result)
            self.video_info_sentiment_value.append(sentiment_value)
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
            self.video_info_comment,
            self.video_info_sentiment_list,
            self.video_info_sentiment_result,
            self.video_info_sentiment_value,
            self.video_info_change_rate,
            self.video_info_change_value,
            self.video_info_sns_score,
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
            "video_info_comment",
            "video_info_sentiment_list",
            "video_info_sentiment_result",
            "video_info_sentiment_value",
            "video_info_change_rate",
            "video_info_change_value",
            "video_info_sns_score"],index=None)
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
        
        engine=create_engine('mysql+mysqlconnector://root:sjlee3423@110.165.16.124:30141/Youtube_Trend_Server?charset=utf8mb4')

        df.to_sql(name='youtube_test_data',if_exists='append',con=engine,index=False)
    def ranking_data(self,ip,port,user,pw,db_name):

        conn=pymysql.connect(host=ip,port=port, user=user, password=pw, db=db_name, charset='utf8mb4')
        cur=conn.cursor()

        sql="SELECT video_info_views,video_info_change_value,video_info_sns_score,video_info_sentiment_value FROM youtube_test_data "
        cur.execute(sql)
        result=cur.fetchall()


        rank_data=pd.DataFrame(list(result),columns=['views','change_value','sns_score','sentiment_value'])
        rank_data['sns_score'].fillna(0,inplace=True)
        rank_data['sentiment_value'].fillna(0,inplace=True)

        views=rank_data['views'].tolist()
        change_value=rank_data['change_value'].tolist()
        sns_score=rank_data['sns_score'].tolist()
        sentiment_value=rank_data['sentiment_value'].tolist()

        tmp_data=list(zip(views,change_value,sns_score,sentiment_value))

        criteria=[MAX,MAX,MAX,MAX]

        ranking_data=Data(tmp_data,criteria,weights=[.4,.15,.3,.15],cnames=['view','view_increase','sns_count','sentiment'])
        dm=simple.WeightedProduct()
        dec=dm.decide(ranking_data)
        rank=list(dec.rank_)

        sql="SHOW COLUMNS FROM youtube_test_data LIKE 'video_info_rank'"
        cur.execute(sql)
        column_exists=cur.fetchall()

        if len(column_exists)==0:
            sql='ALTER TABLE youtube_test_data ADD COLUMN video_info_rank int'
            cur.execute(sql)

        sql="SELECT video_info_link FROM youtube_test_data "
        cur.execute(sql)
        result=cur.fetchall()
        link_data=[value[0] for value in result]


        for i in range(len(rank)):
            sql='UPDATE youtube_test_data SET video_info_rank=%s where video_info_link=%s'
            value=int(rank[i])
            cur.execute(sql,(value,link_data[i]))
            conn.commit()
        print(rank)
        conn.close()


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
        print("Stage 5: Scoring Video")
        print("="*50)

        self.scoring_video("110.165.16.124",30141,'root','sjlee3423','Youtube_Trend_Server')

        print("="*50)
        print("Stage 6: Save Data to Maria DB")
        print("="*50)
        self.save_df_to_db("110.165.16.124",30141,'root','sjlee3423','Youtube_Trend_Server')

        print("="*50)
        print("Stage 7: Ranking Videos")
        print("="*50)

        self.ranking_data("110.165.16.124",30141,'root','sjlee3423','Youtube_Trend_Server')


if __name__=="__main__":
    keyword_list=['강아지','고양이','뉴스','여행','예능','축구','스마트폰','운동','게임','요리']
    #keyword_list=['여행']
    Youtube_Crawler(keyword_list,"zofo3v8hwj","uSaxHZaefo6WTQ2rwcdNJqVGnngg3QkjA10dvEw9","AIzaSyA8AVDeWVW2aEqMds7z51gjhr8o3ebRyik")