from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
import time
keywords=['펜트하우스줄거리', '펜트하우스3']
community={
    'dcinside':'dcinside.com',
    'fmkorea':'fmkorea.com',
    'dogdrip':'dogdrip.net'

}

chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument('headless') # headless 모드 설정
chrome_options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
chrome_options.add_argument("disable-gpu") 
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")

prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
chrome_options.add_experimental_option('prefs', prefs)

driver=webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME,
    options=chrome_options
)

#driver=webdriver.Chrome('driver/chromedriver')
def get_search_stat(driver,link):
    
    search_link='https://www.google.com/search?q='+link
    driver.get(search_link)
    page=driver.page_source


    tools_button=driver.find_element_by_xpath('//*[@id="hdtb-tls"]')
    driver.implicitly_wait(2)
    AC(driver).move_to_element(tools_button).click(tools_button).perform()
    #wait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="hdtb-tls"]'))).click()

    time_button=driver.find_element_by_xpath('//*[@id="hdtbMenus"]/span[2]/g-popup/div[1]/div')
    #wait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="hdtbMenus"]/span[2]/g-popup/div[1]/div'))).click()
    driver.implicitly_wait(2)
    AC(driver).move_to_element(tools_button).click(time_button).perform()

    day_button=driver.find_element_by_xpath('//*[@id="lb"]/div/g-menu/g-menu-item[3]/div')
    
    #wait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="lb"]/div/g-menu/g-menu-item[3]/div'))).click()
    driver.implicitly_wait(2)
    AC(driver).move_to_element(tools_button).click(day_button).perform()

    tools_button=driver.find_element_by_xpath('//*[@id="hdtb-tls"]')
    #wait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="hdtb-tls"]'))).click()
    driver.implicitly_wait(2)
    AC(driver).move_to_element(tools_button).click(tools_button).perform()
    try:
        #result_stat=driver.find_element_by_xpath('//*[@id="result-stats"]').text
        result_stat=wait(driver,5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="result-stats"]'))).text
        result_stat=result_stat[result_stat.find('(')
        return result_stat
    except:
        return 0
    


def community_search(keywords,driver,kwargs):
    for key in kwargs:
        for i in range(len(keywords)):
            search_word=keywords[i]
            search_link=keywords[i]+' '+'site:'+kwargs[key]
            print(get_search_stat(driver,search_link))

            


community_search(keywords,driver,community)
driver.quit()