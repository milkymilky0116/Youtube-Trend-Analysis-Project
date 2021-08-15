import pymysql
import csv
import pandas as pd
import numpy as np
import pytube
from pytube.exceptions import MembersOnly, VideoPrivate, VideoRegionBlocked, VideoUnavailable
import requests
import ast
import random
conn=None
cur=None



def convert_resolution(res,link):
    result=[]
    
    for row in link:
        row=row.replace('/default.jpg','/{}default.jpg'.format(res))
        result.append(row)
    return result
def convert_link(video_id):
    result=[]
    for id in video_id:
        link='https://youtu.be'+id
        result.append(link)
    return result
def convert_id(link):
    link=str(link)
    result=link[link.find('=')+1:]

    return result
def get_analysis_data(data):
    line_chart_dict={}
    pie_chart_dict={}

    conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
    cur=conn.cursor()
    link=(data['value'],)

    

    sql="SELECT date,views FROM youtube_view_data WHERE link=%s"
    cur.execute(sql,link)
    result=cur.fetchall()
    result=result[len(result)-5:]
    print(result)
    view_date=[]
    view_rate=[]
    for i in range(len(result)):
        view_date.append(result[i][0])
        view_rate.append(result[i][1])

    sql="SELECT video_info_sentiment_list,video_info_title FROM youtube_test_data WHERE video_info_link=%s"
    cur.execute(sql,link)
    sentiment_result=cur.fetchall()

    video_title=sentiment_result[0][1]
    """

    """
    print(sentiment_result)
    sentiment_result=ast.literal_eval(sentiment_result[0][0])

    sentiment_label=[]
    sentiment_rate=[]

    try:
        for key,value in sentiment_result.items():
            sentiment_label.append(key)
            sentiment_rate.append(value*100)
    except:
        pass
        
    line_chart_dict['date']=view_date
    line_chart_dict['rate']=view_rate

    line_chart_dict['title']=video_title
    line_chart_dict['id']=convert_id(data['value'])

    pie_chart_dict['sentiment']=sentiment_label
    pie_chart_dict['rate']=sentiment_rate

    return line_chart_dict,pie_chart_dict




def get_youtube_data(query_num,*args):
    conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
    cur=conn.cursor()
    elements=[]
    for i in args:
        elements.append(i)
    
    query=','.join(elements)
    select_query=''.join("SELECT {} FROM youtube_test_data".format(query))
    cur.execute(select_query)
    if query_num=='all':
        result_set=cur.fetchall()
    else:
        result_set=cur.fetchmany(query_num)
    result=[]
    

    for row in result_set[:]:
        result.append(list(row))
    
    df=pd.DataFrame(columns=elements, data=result)

    cur.close()
    return df
def get_random_keyword():

    conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
    cur=conn.cursor()
    sql="SELECT video_info_keywords FROM youtube_test_data ORDER BY video_info_rank"
    #keyword=["고양이","강아지"]
    #keyword="|".join(keyword)
    cur.execute(sql)
    result_set=cur.fetchall()
    word_list=[]
    for i in range(len(result_set)):
        words=result_set[i][0].split('|')
        for j in range(len(words)):
            word_list.append(words[j])
    random_list=random.sample(word_list,10)
    return random_list
def get_query_data(keyword):
    
    conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
    cur=conn.cursor()
    sql="SELECT video_info_thumbnails FROM youtube_test_data WHERE video_info_title or video_info_keywords or video_info_description REGEXP %s ORDER BY video_info_rank"
    #keyword=["고양이","강아지"]
    #keyword="|".join(keyword)
    cur.execute(sql,(keyword,))
    result_set=cur.fetchall()

    result=[]
    for row in result_set[1:]:
        result.append(str(row[0]))

    return result
def get_related_data(keyword):
    
    conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
    cur=conn.cursor()
    sql="SELECT video_info_keywords,video_info_title,video_info_summary_data,video_info_comment FROM youtube_test_data WHERE video_info_title or video_info_keywords or video_info_description REGEXP %s ORDER BY video_info_rank"
    #keyword=["고양이","강아지"]
    #keyword="|".join(keyword)
    cur.execute(sql,(keyword,))
    result_set=cur.fetchall()

    result=[]
    for row in result_set[1:]:
        result.append(str(row[0]))

    return result

