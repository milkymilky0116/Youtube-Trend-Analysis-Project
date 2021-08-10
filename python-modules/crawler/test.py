import requests
from selenium import webdriver as wd

from selenium import webdriver

import csv
import pandas as pd
import time
import os
df=pd.read_csv('files/video_data_{}_init.csv'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))))

print(df['video_info_views'])





