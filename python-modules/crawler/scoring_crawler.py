from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import re
import requests
keywords=['펜트하우스줄거리', '펜트하우스3']
community={
    'dcinside':'dcinside.com',
    'fmkorea':'fmkorea.com',
    'dogdrip':'dogdrip.net'
}

#driver=webdriver.Chrome('driver/chromedriver')
def get_search_stat(driver,link):
    search_link='https://www.google.com/search?q='+link+'&as_qdr=d'
    
    driver.implicitly_wait(5)

    driver.get(search_link)

    wait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="hdtb-tls"]'))).click()

    try:
        
        #result_stat=driver.find_element_by_xpath('//*[@id="result-stats"]').text
        result_stat=wait(driver,5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="result-stats"]'))).text
        result_stat=result_stat[:result_stat.find('(')] 
        result_stat="".join(re.findall("\d+",result_stat))
        print(result_stat)
        return int(result_stat)
    except:
        return 0
    


def community_search(keywords,driver,kwargs):
    result=[]
    start=time.time()
    for key in kwargs:
        for i in range(len(keywords)):
            search_link=keywords[i]+' '+'site:'+kwargs[key]
            result_stat=get_search_stat(driver,search_link)
            result.append(result_stat)
    
    print(result)
    print("시간: ", time.time()-start)

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

chrome_options.add_argument("--user-data-dir=chrome-data")

prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
chrome_options.add_experimental_option('prefs', prefs)


driver=webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME,
    options=chrome_options
)

#driver=webdriver.Chrome('driver/chromedriver.exe')

community_search(keywords,driver,community)
driver.quit()