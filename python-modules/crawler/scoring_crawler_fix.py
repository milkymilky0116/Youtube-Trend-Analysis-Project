
from bs4 import BeautifulSoup
import requests
import re
import time
import os
from fake_useragent import UserAgent
base_url='https://www.google.co.kr/search'

keywords=['강아지', '고양이']
community={
    'dcinside':'dcinside.com',
    'fmkorea':'fmkorea.com',
    'dogdrip':'dogdrip.net'
}
def get_search_stat(keyword,site):
    user_agent=UserAgent()
    url='https://www.google.com/search?q={}&as_qdr=d&as_sitesearch={}'.format(keyword,site)
    headers = {
        "referer": "https://www.google.com/",
        "user-agent":user_agent.random
    }

    res=requests.get(url,headers=headers)

    soup=BeautifulSoup(res.text,'lxml')
    print(soup)
    try:
        number=soup.select_one('#result-stats').text
        number=number[:number.find('(')] 
        number="".join(re.findall("\d+",number))
        return int(number)
    except:
        return 0

def community_search(keywords,kwargs):
    result=[]
    start=time.time()
    for key in kwargs:
        for i in range(len(keywords)):
            result_stat=get_search_stat(keywords[i],kwargs[key])
            result.append(result_stat)

            time.sleep(10)
    
    print(result)
    print("시간: ", time.time()-start)

community_search(keywords,community)
