import pymysql
import csv
import pandas as pd
import numpy as np
import pytube
from pytube.exceptions import MembersOnly, VideoPrivate, VideoRegionBlocked, VideoUnavailable
import requests
import ast
import random
from collections import Counter
from datetime import datetime
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

    conn=pymysql.connect(host="",port=30141, user='', password='', db='', charset='utf8mb4')
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

    sql="SELECT video_info_sentiment_list,video_info_title,video_info_comment FROM youtube_test_data WHERE video_info_link=%s"
    cur.execute(sql,link)
    sentiment_result=cur.fetchall()

    video_title=sentiment_result[0][1]

    sentiment_dict=ast.literal_eval(sentiment_result[0][0])

    sentiment_label=[]
    sentiment_rate=[]
    
    comment_context=[]
    comment_sentiment=[]

    try:
        for key,value in sentiment_dict.items():
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

    comment=sentiment_result[0][2]
    if comment!='None':
        comment=ast.literal_eval(comment)
        for key,value in comment.items():
            comment_context.append(key)
            comment_sentiment.append(value)
    comment_result={}
    comment_result['comment']=comment_context[:10]
    comment_result['sentiment']=comment_sentiment



    

    return line_chart_dict,pie_chart_dict,comment_result




def get_youtube_data(query_num,*args):
    conn=pymysql.connect(host="",port=30141, user='', password='', db='', charset='utf8mb4')
    cur=conn.cursor()
    elements=[]
    for i in args:
        elements.append(i)
    
    query=','.join(elements)
    select_query=''.join("SELECT {} FROM youtube_test_data ORDER BY video_info_rank".format(query))
    cur.execute(select_query)
    if query_num=='all':
        result_set=cur.fetchall()
    else:
        result_set=cur.fetchmany(query_num)
    print(len(result_set))
    result=[]
    

    for row in result_set[:]:
        result.append(list(row))
    
    df=pd.DataFrame(columns=elements, data=result)

    cur.close()
    return df
def get_random_keyword():

    conn=pymysql.connect(host="",port=30141, user='', password='', db='', charset='utf8mb4')
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
    count_list=Counter(word_list)
    count_list={ x: count for x, count in count_list.items() if count >=2}
    count_word_list=[]
    for key,value in count_list.items():
        count_word_list.append(key)
    random_list=random.sample(count_word_list,10)
    return random_list
def get_social_weather():
    conn=pymysql.connect(host="",port=30141, user='', password='', db='', charset='utf8mb4')
    cur=conn.cursor()
    current_time=datetime.today().strftime("%Y%m%d%H%M%S")
    sql='SELECT video_info_sentiment_result FROM youtube_test_data WHERE video_info_publish_date < %s'
    cur.execute(sql,(current_time,))
    result_set=cur.fetchall()
    comment_sentiment=[]
    for i in range(len(result_set)):
        comment_sentiment.append(result_set[i][0])
    sentiment_counter=Counter(comment_sentiment)
    sentiment_ratio=[]
    for key,value in sentiment_counter.items():
        ratio=(value/len(result_set))*100
        sentiment_counter[key]=ratio
        sentiment_ratio.append(ratio)
    social_sentiment=sentiment_counter.most_common(1)[0][0]
    social_sentiment_ratio=sentiment_counter.most_common(1)[0][1]
    social_weather=''
    if social_sentiment=='negative' and social_sentiment_ratio < 50:
        social_weather='rain'
    elif social_sentiment=='negative' and social_sentiment_ratio >50:
        social_weather='Typhoon'
    elif social_sentiment=='None' and social_sentiment_ratio <50:
        social_weather='Cloudy'
    elif social_sentiment=='None' and social_sentiment_ratio >50:
        social_weather='Drizzling'
    elif social_sentiment=='positive' and social_sentiment_ratio <50:
        social_weather='little Cloudy'
    elif social_sentiment=='None' and social_sentiment_ratio >50:
        social_weather='Sunny'
    return social_weather,social_sentiment_ratio,social_sentiment
get_social_weather()
def get_query_data(keywords):
    
    conn=pymysql.connect(host="",port=30141, user='', password='', db='', charset='utf8mb4')
    cur=conn.cursor()
    sql="SELECT video_info_thumbnails,video_info_link,video_info_title FROM youtube_test_data WHERE video_info_title or video_info_keywords REGEXP %s ORDER BY video_info_rank"
    query_keyword=[]
    for i in range(len(keywords)):
        if keywords[i]!=None:
            query_keyword.append(keywords[i])
    keywords="|".join(query_keyword)
    cur.execute(sql,(keywords,))
    result_set=cur.fetchall()

    thumbnails=[]
    link=[]
    title=[]
    for i in range(len(result_set)):
        thumbnails.append(result_set[i][0])
        link.append(result_set[i][1])
        title.append(result_set[i][2])
    result_dict={}
    result_dict['thumbnails']=thumbnails
    result_dict['link']=link
    result_dict['title']=title

    return result_dict

