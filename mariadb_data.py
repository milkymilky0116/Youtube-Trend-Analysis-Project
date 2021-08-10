import pymysql
import csv
import pandas as pd
import numpy as np
import pytube
from pytube.exceptions import MembersOnly, VideoPrivate, VideoRegionBlocked, VideoUnavailable
import requests

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
        link='https://youtu.be/'+id
        result.append(link)
    return result

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
    for row in result_set[1:]:
        result.append(list(row))
    df=pd.DataFrame(columns=elements, data=result)

    cur.close()
    return df
