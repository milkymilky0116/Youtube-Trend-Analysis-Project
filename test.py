import pymysql
import pandas as pd
def get_query_data(keyword):
    conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
    cur=conn.cursor()
    sql="SELECT video_info_thumbnails FROM youtube_test_data WHERE video_info_title or video_info_keywords or video_info_description REGEXP %s"
    #keyword=["고양이","강아지"]
    #keyword="|".join(keyword)
    cur.execute(sql,(keyword,))
    result_set=cur.fetchall()

    result=[]
    for row in result_set[1:]:
        result.append(list(row))
    

    return df