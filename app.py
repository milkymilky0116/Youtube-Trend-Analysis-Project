from flask import Flask, json, render_template, jsonify, request
import mariadb_data
from urllib.parse import quote_plus
from collections import Counter
app = Flask(__name__)
app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)


@app.route('/')
def index():
    df = mariadb_data.get_youtube_data(
        50, 'video_info_link', 'video_info_thumbnails', 'video_info_title', 'video_info_sentiment_result')
    print(len(df))
    df_img = df['video_info_thumbnails']
    df_link = df['video_info_link']
    df_title = df['video_info_title']

    weather, ratio, sentiment = mariadb_data.get_social_weather()
    ratio = sentiment+":"+"%.2f%%" % ratio
    print(ratio)

    df_img = df_img.values.tolist()
    df_img = mariadb_data.convert_resolution('hq', df_img)
    df_id = mariadb_data.convert_id(df_link)
    random_keyword = mariadb_data.get_random_keyword()

    #df_link = mariadb_data.convert_link(df_link)

    return render_template('index.html', img_data=df_img, link_data=df_link, title_data=df_title, id_data=df_id, trend_keyword=random_keyword, weather=weather, ratio=ratio)


@app.route('/show_result', methods=['POST'])
def show_result():
    data = request.get_json()

    line_chart_dict, pie_chart_dict, comment_result = mariadb_data.get_analysis_data(
        data)

    return jsonify(view_result=line_chart_dict, sentiment_result=pie_chart_dict, comment_result=comment_result)


@app.route('/show_search', methods=['POST'])
def show_search():
    data = request.get_json()
    search_list = data['value']
    query_result = mariadb_data.get_query_data(search_list)

    return jsonify(query_result=query_result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
