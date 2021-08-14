from multiprocessing.spawn import freeze_support
import pandas as pd
import pymysql
import time
from pytube import YouTube
from multiprocessing import Manager, Process
from sqlalchemy import create_engine
import pandas as pd
import codecs

codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)

def main():
    tm=time.strftime('%Y-%m-%d %I:%M %p', time.localtime(time.time()))
    start=time.time()
    conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='')
    cur=conn.cursor()
    sql="SELECT video_info_link FROM youtube_test_data"
    cur.execute(sql)
    search_query=cur.fetchall()
    link_result=[]
    date_result=[]
    result=[]
    for i in range(len(search_query)):
        link=search_query[i]
        yt_link=link[0]
        link_result.append(yt_link)
        date_result.append(tm)


    for i in range(len(link_result)):
        video_link="https://www.youtube.com"+link_result[i]
        video_info=YouTube(video_link)
        try:
            result.append(video_info.views)
        except:
            pass
 
    data=zip(date_result,link_result,result)
    df=pd.DataFrame(data,columns=['date','link','views'])
    engine=create_engine('mysql+mysqlconnector://root:sjlee3423@110.165.16.124:30141/Youtube_Trend_Server?charset=utf8mb4')
    df.to_sql(name='youtube_view_data',con=engine,if_exists='append',index=False)
    end=time.time()
    print(tm)
    
if __name__=="__main__":
    main()