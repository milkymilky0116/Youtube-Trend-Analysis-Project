import pymysql

conn=None
cur=None

sql=""

conn=pymysql.connect(host="110.165.16.124",port=32305, user='root', password='1234', db='test', charset='utf8')
cur=conn.cursor()

sql="CREATE TABLE IF NOT EXISTS usertable (id char(4), userName char(10), email char(15), birthYear int)"
cur.execute(sql)

conn.commit()
conn.close()