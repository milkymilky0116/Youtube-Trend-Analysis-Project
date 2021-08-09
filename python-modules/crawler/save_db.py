import pymysql
import csv
import requests

conn=None
cur=None

sql=""

#Maria DB 서버와 연결
conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
#커넥터 연결
cur=conn.cursor()

#최초 생성떄만 실행
sql="""CREATE TABLE IF NOT EXISTS youtube_test_data(video_id char(12) NOT NULL, 
        video_title varchar(100) NOT NULL, 
        publish_time char(20) NOT NULL, 
        channel_title varchar(100) NOT NULL, 
        tags varchar(500) NULL,
        view_count char(10) NOT NULL,
        likes_count char(10) NOT NULL,
        dislikes_count char(10) NOT NULL,
        comment_count char(20) NOT NULL,
        thumbnail_link varchar(100) NOT NULL,
        description varchar(10000) NULL);"""
cur.execute(sql)
