from flask import Flask, json, render_template,jsonify,request
import mariadb_data
from urllib.parse import quote_plus
import pandas as pd
import pymysql
import ast
from util.vis_word_map import make_word_map
app = Flask(__name__)
app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)
search_csv=pd.read_csv('util/edge_data.csv')

@app.route('/')
def index():
    df = mariadb_data.get_youtube_data(
    50, 'video_info_link', 'video_info_thumbnails', 'video_info_title')
    df_img = df['video_info_thumbnails']
    df_link = df['video_info_link']
    df_title = df['video_info_title']
    df_img = df_img.values.tolist()
    df_img = mariadb_data.convert_resolution('hq', df_img)
    df_id=mariadb_data.convert_id(df_link)
    #df_link = mariadb_data.convert_link(df_link)

    return render_template('index.html', img_data=df_img, link_data=df_link, title_data=df_title, id_data=df_id)

@app.route('/show_result', methods=['POST'])
def show_result():
    data = request.get_json()
    dict={}
    dict2={}

    line_chart_dict,pie_chart_dict=mariadb_data.get_analysis_data(data)
    print(line_chart_dict)
    print(pie_chart_dict)

    return jsonify(view_result=line_chart_dict, sentiment_result=pie_chart_dict)
@app.route('/show',methods=['POST'])
def show_related():
    data=request.get_json()
    result={}
    type(data)
    result['result']=make_word_map(data)
    return jsonify(search_result=result)

if __name__ == "__main__":
    app.run()
