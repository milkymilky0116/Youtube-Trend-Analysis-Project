import pymysql
import csv
import requests
import time
def db_save(csvfile):
    conn=None
    cur=None

    sql=""

    #Maria DB 서버와 연결
    conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
    #커넥터 연결
    cur=conn.cursor()
    #csv 파일 오픈
    f=open(csvfile,'r', encoding='utf-8')
    csvReader=csv.reader(f)

    """
    title,link,keywords,summary,views,thumbnails,channel_name,channel_id,publish_date,description
    """



    #sql문 테이블 생성
    sql="""CREATE TABLE IF NOT EXISTS youtube_test_data(
            video_info_title varchar(100) NOT NULL,
            video_info_link varchar(100) NOT NULL,
            video_info_keywords varchar(500) NULL,
            video_info_views char(50) NOT NULL,
            video_info_thumbnails varchar(100) NOT NULL,
            video_info_author varchar(100) NOT NULL,
            video_info_channelId varchar(100) NOT NULL,
            video_info_publish_date char(20) NOT NULL ,
            video_info_description varchar(10000) NULL,
            video_info_summary_data varchar(100) NULL
            );"""
    cur.execute(sql)

    #PRIMARY KEY 에러 방지를 위한 AUTO INCREMENT문 실행
    sql="ALTER TABLE youtube_tmp_data AUTO_INCREMENT = 1;"
    cur.execute(sql)

    #csv Column들을 불러옴
    for row in csvReader:

        video_info_title=(row[0])
        video_info_link=(row[1])
        video_info_keywords=(row[2])
        video_info_views=(row[3])
        video_info_thumbnails=(row[4])
        video_info_author=(row[5])
        video_info_channelId=(row[6])
        video_info_publish_date=(row[7])
        video_info_description=(row[8])
        video_info_summary_data=(row[9])
        
        #데이터베이스에 csv의 데이터를 넣는 sql문 실행
        sql="INSERT INTO youtube_test_data(video_info_title,video_info_link,video_info_keywords,video_info_views,video_info_thumbnails,video_info_author,video_info_channelId,video_info_publish_date,video_info_description,video_info_summary_data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        cur.execute(sql,(video_info_title,video_info_link,video_info_keywords,video_info_views,video_info_thumbnails,video_info_author,video_info_channelId,video_info_publish_date,video_info_description,video_info_summary_data))
        conn.commit()

    f.close()
    conn.close()

db_save('files/video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))))