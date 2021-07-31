from flask import Flask, render_template
import mariadb_data
from urllib.parse import quote_plus
import pandas as pd
import requests
import pytube
app=Flask(__name__)
app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)
@app.route('/')
def index():
    df=mariadb_data.get_youtube_data(50,'video_id','video_title','thumbnail_link')
    df_img=df['thumbnail_link']
    df_link=df['video_id']
    df_title=df['video_title']
    df_img=df_img.values.tolist()
    df_img=mariadb_data.convert_resolution('hq',df_img)
    df_link=mariadb_data.convert_link(df_link)


    return render_template('index.html', img_data=df_img, link_data=df_link, title_data=df_title)
    
if __name__=="__main__":
    app.run('0.0.0.0')