import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
import re
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from fake_useragent import UserAgent
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from langdetect.lang_detect_exception import LangDetectException
from langdetect import detect
from urllib.error import HTTPError
import urllib.request
import re
import json
import collections
from googleapiclient.discovery import build
from konlpy.tag import Okt
from PyKomoran import Komoran
import twitter
from collections import Counter
from twitter.error import TwitterError

twitter_consumer_key = "3GMcnn0TU3LJ7OzYI1l06kmdY"
twitter_consumer_secret = "ll8ZiXwfE8RPyDCHm23Mzm66XFwaXdHBpb4AojTBqGkNGQodYA"  
twitter_access_token = "1405566672522465281-8I81m6mU5VGPKBpCIsgDYFQyEvOtZw"
twitter_access_secret = "AlT8zhRYvEPxKH5uuieqbifmoj0SwN7B9tOXUpWBG7p3V"
twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                          consumer_secret=twitter_consumer_secret, 
                          access_token_key=twitter_access_token, 
                          access_token_secret=twitter_access_secret)


komoran=Komoran('EXP')
komoran.set_user_dic('files/dic.user')

def set_driver_remote():
    chrome_options=webdriver.ChromeOptions()
    ua=UserAgent()
    userag=ua.random
    print(userag)

    chrome_options.add_argument(f'user-agent={userag}')
    chrome_options.add_argument('headless') # headless 모드 설정
    chrome_options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
    chrome_options.add_argument("disable-gpu") 
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
    chrome_options.add_experimental_option('prefs', prefs)


    driver=webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME,
        options=chrome_options
    )

    return driver

def set_driver_local():
    driver=webdriver.Chrome('driver/chromedriver')

    return driver
def scroll_to_bottom(driver):

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight );")
        time.sleep(2.0)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
def string_int_filtering(text):
    #text_count ="".join(re.findall(r'(\d+(?:K+)?)',text))
    try:
        text_count=text[:text.find(' ')]
        result=None
        if 'K' in text_count:
            place=text_count.find('K')
            int_part=float(text_count[:place])
            result=int_part*1000
            return result
        else:
            return int(text_count)
    except:
        return 0
"""
def comment_crawler(driver,url):
    link='https://youtu.be'+url
    driver.get(link)
    all_comment=[]
    youtube_comments=None
    i=0
    j=0
    while True:
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'lxml')
        youtube_comments = soup.select('yt-formatted-string#content-text')
        if len(youtube_comments)>0:
            element=driver.find_element_by_tag_name('body')
            element.send_keys(Keys.END)
            if i==3:
                break
            i+=1
        else:
            element=driver.find_element_by_tag_name('body')
            element.send_keys(Keys.END)
            if j>5:
                break
            j+=1
    if len(youtube_comments)<30:
        return None
    else:
        for i in range(len(youtube_comments)):
            string=str(youtube_comments[i].text)
            string = string.replace('\n', '') 
            string = string.replace('\t', '')
            if len(all_comment)>30:
                return all_comment
            all_comment.append(string)
"""
def comment_crawler(api_key,video_link):
    try:
        youtube = build('youtube', 'v3',developerKey=api_key)

        #/watch?v=hEqJLnEWVKk

        video_link=video_link[video_link.find("=")+1:]

        video_id=video_link
    
        video_response=youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=30
        ).execute()
        result=[]
        while True:
            for item in video_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                cleaner=re.compile('<.*?>')
                comment=re.sub(cleaner,'',comment)         
                result.append(comment)
            if len(video_response['items'])<30:
                if len(result)==len(video_response['items']):
                    break
            if len(result)==30:
                break
        return result
    except:
        return None

def keyword_nouns(keywords):
    result=[]
    for i in range(len(keywords)):
        nouns=komoran.get_morphes_by_tags(keywords[i],tag_list=['NNP','NNG'])
        for j in range(len(nouns)):
            result.append(nouns[j])
    return result

def twitter_search(search_query):
    keyword_noun=keyword_nouns(search_query)
    try:
        for i in range(len(keyword_noun)):
            query=keyword_noun[i]
            status=twitter_api.GetSearch(term=query,count=10)
            result=[]
            for item in status:
                for tag in item.hashtags:
                    result.append(tag.text)
            count=Counter(result).most_common(20)
            result_count=0
            for i in range(len(count)):
                query_count=count[i][1]
                result_count+=query_count
            if result_count==None:
                return 0
            else:
                return result_count
    except TwitterError as e:
        return 0

def extract_keywords(key_info,n):
    okt=Okt()
    ngram_range=(1,1)
    count=CountVectorizer(ngram_range=ngram_range).fit([key_info])
    candidates=count.get_feature_names()
    model=SentenceTransformer('distilbert-base-nli-mean-tokens')
    doc_embedding=model.encode([key_info])
    candidates_embedding=model.encode(candidates)

    top_n=n
    distance=cosine_similarity(doc_embedding,candidates_embedding)
    keywords=[candidates[index] for index in distance.argsort()[0][-top_n:]]


    return keywords

def keyword_nouns(keywords):
    result=[]
    for i in range(len(keywords)):
        nouns=komoran.get_morphes_by_tags(keywords[i],tag_list=['NNP','NNG'])
        for j in range(len(nouns)):
            result.append(nouns[j])
    return result




def sentiment_analyse(sentence_list,client_id,client_secret):
    if sentence_list==None or len(sentence_list)<10:
        return None,None,None,None
    result_sentiment=[]
    comment_sentiment={}
    for i in range(len(sentence_list)):
        sentence=sentence_list[i]
        try:
            if detect(sentence)=='ko' or detect(sentence)=='en':
                client_id = client_id
                client_secret = client_secret
                url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze";
                body={
                        'content':sentence
                    }
                body=json.dumps(body)
                request = urllib.request.Request(url)
                request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
                request.add_header("X-NCP-APIGW-API-KEY",client_secret)
                request.add_header("Content-Type","application/json")
                response = urllib.request.urlopen(request, data=body.encode("utf-8"))
                rescode = response.getcode()
                if(rescode==200):
                    response_body = response.read()
                    text=response_body.decode('utf-8')
                    text=text[text.find('sentiment'):text.find('confidence')]
                    sentiment_text= re.sub(r"[^a-zA-Z0-9:]","",text)
                    sentiment_text=sentiment_text[sentiment_text.find(':')+1:]
                    comment_sentiment[sentence]=sentiment_text
                    result_sentiment.append(sentiment_text)
                else:
                    errcode="Error Code:" + rescode
                    return errcode
            else:
                return None,None,None,None
        except LangDetectException:
            i+=1
        except HTTPError:
            i+=1
        except:
            i+=1
    frequency=collections.Counter(result_sentiment)
    sentiment_result=frequency.most_common(3)[0][0]
    sentiment_value=0

    print(comment_sentiment)

    result_dict={}
    for item in frequency:
        result_dict[item]=frequency[item]/len(result_sentiment)
    if sentiment_result=='positive': 
        sentiment_value=1
    elif sentiment_result=="netural":
        sentiment_value=0
    elif sentiment_result=="negative":
        sentiment_value=-1
    
    return result_dict,sentiment_result,sentiment_value

def vid_info(keyword,driver,tm):
        #filter_keyword(keyword,driver)
        search_keyword="%23"+keyword
        driver.get('https://www.youtube.com/results?search_query='+search_keyword+'&sp=CAMSBAgCEAE%253D')
        j=1
        video_info_link=[]
        get_info_avaliable=True
        while True:
            page=driver.page_source
            soup=BeautifulSoup(page,'lxml')
            all_video_sections=soup.select("#contents > ytd-item-section-renderer:nth-of-type({})".format(j))
            video_len=None
            for child in all_video_sections:
                all_videos=child.find_all(id='dismissible')
                section_views=[]
                for video in all_videos:
                    video_len=len(all_videos)
                    video_info=video.find(id='video-title')
                    href=video_info.attrs['href']
                    view=[i.text for i in video.select('#metadata-line > span:nth-of-type(1)')][0]
                    view=string_int_filtering(view)
                    if view>1000:
                        video_info_link.append(href)
                        print(href)
                        section_views.append(view)
                    #prev_view_avg=sum(section_views)/len(section_views)
                if len(section_views)>3:
                    #driver.execute_script("window.scrollTo(0, 800*{});".format(video_len*2))
                    element=driver.find_element_by_tag_name('body')
                    element.send_keys(Keys.END)
                    j=j+1
                    time.sleep(1)
                else:
                    get_info_avaliable=False
                    with open('files/dataset_init_{}.txt'.format(tm),'a',encoding='utf-8') as f:
                        for line in video_info_link:
                            f.write(line)
                            f.write('\n')
                    break   
            if get_info_avaliable==False:
                break
        return video_info_link
    
