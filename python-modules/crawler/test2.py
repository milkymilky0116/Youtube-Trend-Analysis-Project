import pandas as pd
import pymysql
import numpy as np
from sqlalchemy import create_engine

conn=pymysql.connect(host="110.165.16.124",port=30141, user='root', password='sjlee3423', db='Youtube_Trend_Server', charset='utf8mb4')

engine=create_engine('mysql+mysqlconnector://root:sjlee3423@110.165.16.124:30141/Youtube_Trend_Server')

dict={1:1}
print(str(dict))


