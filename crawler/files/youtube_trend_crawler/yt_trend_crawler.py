
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


#유니코드 설정: DB에 저장할때 이모티콘도 깨지지 않게 저장될 수 있도록 utf8mb4로 지정해주었습니다.
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)

class Youtube_Crawler:
    #크롤러 클래스
    def __init__(self,keywords,client_id,client_secret,google_api):

        #DB에 저장할 데이터들
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


        #API 키 입력
        #client id와 client secret은 네이버 클라우드 플랫폼에서 받을수 있는 고유 키입니다. 클래스를 생성할 떄 자신의 API 키를 입력해주세요.
        self.__client_id=client_id
        self.__client_secret=client_secret

        #google api키는 Youtube Data v3 API의 키입니다.
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
        #크롬드라이버를 로컬에서 실행할지, docker에서 실행되는 Grid서버에서 실행할 것인지에 대한 여부를 지정할 수 있습니다.
        if statement=="local":
            driver=set_driver_local()
        elif statement=="server":
            driver=set_driver_remote()
        return driver

    def collect_data(self,driver,args):
        #데이터를 수집합니다.
        start=time.time()
        for i in range(len(args)):
            keyword_list=make_word_map(args[i])
            #키워드들에 대한 연관 검색어를 불러옵니다. ex) 강아지-> 개,고양이,애완동물,반려견....
            for i in range(len(keyword_list)):
                #키워드들에 대한 동영상 검색 결과를 저장합니다. 저장된 결과값은 files안에 로그로 저장이 됩니다.
                vid_info(keyword_list[i],driver,self.tm)
                print("complete:",keyword_list[i])

        driver.quit()
        end=time.time()
        print((end-start)/60)
    def parsing_data(self):
        #collect data에서 수집한 동영상 정보들을 파싱합니다.
        start=time.time()
        with open('files/dataset_init_{}.txt'.format(self.tm),'rt',encoding='utf-8') as f: #저장된 데이터를 불러옵니다.
            links=f.readlines()
            for link in links:
                link=link[:link.find("\n")]
                video_link="https://www.youtube.com"+link
                video_tube=YouTube(video_link) #데이터를 파싱하기 위해 pytube 객체를 생성합니다.

                if link not in self.video_info_link: #링크 중복을 방지해주는 조건문입니다. (중복되는 결과값이 있을수 있으므로.)
                    try:
                        #데이터를 파싱합니다.
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
                    except: #예기치 못한 에러는 패스합니다. (ex. 동영상이 비공개 처리가 되었을경우.)
                        pass
        
        end=time.time()
        print((end-start)/60)

    def summary_data(self):
        #수집된 데이터를 두 단어로 요약합니다.
        start=time.time()
        for i in range(len(self.video_info_link)):
            keywords=self.video_info_keywords[i]
            title=self.video_info_title[i]
            description=self.video_info_description[i]

            sep_keyword=keywords.split("|")
            sep_keyword=" ".join(sep_keyword)

            key_info=title+" "+sep_keyword+" "+description
            #동영상의 자연어 정보는 제목+태그+설명란의 조합으로 이루어집니다.

            summary_data=extract_keywords(key_info,2)
            #자연어 정보를 Tensorflow 모델을 통해 요약을 수행합니다.

            summary_data=" ".join(summary_data)
            #데이터베이스에 저장하기 편하도록 str으로 변환합니다.

            self.video_info_summary_data.append(summary_data)
            print("Summary:",summary_data)
        end=time.time()
        print("Data Analyse Complete")
        print((end-start)/60)

    def scoring_video(self,ip,port,user,pw,db_name):

        #수집된 데이터를 통해 동영상에 점수를 매깁니다.

        conn=pymysql.connect(host=ip,port=port, user=user, password=pw, db=db_name, charset='utf8mb4')
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
            #테이블이 존재하는지에 대한 여부를 얻는 sql문을 실행합니다.

            print(ava_val)

            if ava_val[0][0]!=0: #존재한다면 다음과 같이 실행합니다. (0: 테이블이 없음 1: 존재함)
                sql="SELECT video_info_link,video_info_views FROM {} WHERE video_info_link=%s".format(db_name)
                cur.execute(sql,link)
                result=cur.fetchall()

                print(result)
                if len(result)>0:
                    sql='DELETE FROM {} WHERE video_info_link=%s'.format(db_name)
                    cur.execute(sql,link)
                    conn.commit()
                    #테이블의 중복을 제거하는 sql문을 실행합니다.

                    past_result=result[0][1]
                    change_rate=int((int(current_view)-past_result)/past_result *100)
                    change_value=int(current_view)-past_result
                    #데이터가 이전에 존재한다면 이전의 조회수와 현재의 조회수를 비교해 증가량과 비율을 계산합니다.
            
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
        
        engine=create_engine('mysql+mysqlconnector://user:pw@host:port/db_name?charset=utf8mb4')

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

        self.scoring_video("ip",'port','user','pw','db_name')

        print("="*50)
        print("Stage 6: Save Data to Maria DB")
        print("="*50)
        self.save_df_to_db("ip",'port','user','pw','db_name')

        print("="*50)
        print("Stage 7: Ranking Videos")
        print("="*50)

        self.ranking_data("ip",'port','user','pw','db_name')


if __name__=="__main__":
    keyword_list=['강아지','고양이','뉴스','여행','예능','축구','스마트폰','운동','게임','요리']
    #keyword_list=['여행']
    Youtube_Crawler(keyword_list,'client_api',"client_secret","google-api")