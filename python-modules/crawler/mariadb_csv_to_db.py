import pymysql
import csv
import requests
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

    #sql문 테이블 생성
    sql="""CREATE TABLE IF NOT EXISTS youtube_test_data(video_id char(12) NOT NULL, 
            video_title varchar(100) NOT NULL, 
            publish_time char(20) NOT NULL, 
            channel_id char(30) NOT NULL, 
            channel_title varchar(100) NOT NULL, 
            category_id char(10) NOT NULL, 
            trending_date char(20) NOT NULL ,
            tags varchar(500) NULL,
            view_count char(10) NOT NULL,
            likes_count char(10) NOT NULL,
            dislikes_count char(10) NOT NULL,
            comment_count char(20) NOT NULL,
            thumbnail_link varchar(100) NOT NULL,
            description varchar(10000) NULL);"""
    cur.execute(sql)

    #PRIMARY KEY 에러 방지를 위한 AUTO INCREMENT문 실행
    sql="ALTER TABLE youtube_tmp_data AUTO_INCREMENT = 1;"
    cur.execute(sql)

    #csv Column들을 불러옴
    for row in csvReader:
        video_id=(row[0])
        video_title=(row[1])
        publish_time=(row[2])
        channel_id=(row[3])
        channel_title=(row[4])
        category_id=(row[5])
        trending_date=(row[6])
        tags=(row[7])
        view_count=(row[8])
        likes_count=(row[9])
        dislikes_count=(row[10])
        comment_count=(row[11])
        thumbnail_link=(row[12])
        description=(row[15])
        #데이터베이스에 csv의 데이터를 넣는 sql문 실행
        sql="INSERT INTO youtube_tmp_data(video_id , video_title, publish_time, channel_id, channel_title, category_id, trending_date,tags,view_count,likes_count,dislikes_count,comment_count,thumbnail_link,description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        cur.execute(sql,(video_id,video_title,publish_time,channel_id,channel_title,category_id,trending_date,tags,view_count,likes_count,dislikes_count,comment_count,thumbnail_link,description))
        conn.commit()

    f.close()
    conn.close()