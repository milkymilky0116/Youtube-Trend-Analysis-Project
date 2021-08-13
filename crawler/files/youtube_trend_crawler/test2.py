import pymysql

conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')
cur=conn.cursor()

sql="SHOW COLUMNS FROM youtube_test_data LIKE 'video_info_ran'"
cur.execute(sql)
result=cur.fetchall()
print(len(result))