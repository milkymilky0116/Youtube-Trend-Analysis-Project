from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
keywords=['펜트하우스줄거리', '펜트하우스3']
community={
    'dcinside':'dcinside.com',
    'fmkorea':'fmkorea.com',
    'dogdrip':'dogdrip.net'

}
chrome_options=webdriver.FirefoxOptions()
chrome_options.page_load_strategy='none'
chrome_options.headless=True
driver=webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.FIREFOX,
    options=chrome_options
)

def get_search_stat(driver,link):
    search_link='https://www.google.com/search?q='+link
    driver.get(search_link)
    page=driver.page_source
    tools_button=driver.find_element_by_xpath('//*[@id="hdtb-tls"]')
    tools_button.click()
    time.sleep(2)

    time_button=driver.find_element_by_xpath('//*[@id="hdtbMenus"]/span[2]/g-popup/div[1]/div')
    time_button.click()
    time.sleep(2)

    day_button=driver.find_element_by_xpath('//*[@id="lb"]/div/g-menu/g-menu-item[3]/div')
    day_button.click()
    time.sleep(2)

    tools_button=driver.find_element_by_xpath('//*[@id="hdtb-tls"]')
    tools_button.click()
    time.sleep(2)
    
    try:
        result_stat=driver.find_element_by_xpath('//*[@id="result-stats"]').text
        result_stat=result_stat[result_stat.find('About')+6:result_stat.rfind('results')-1].replace(',','')
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
