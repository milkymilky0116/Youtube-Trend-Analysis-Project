from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scoring_crawler_dump import community_search,get_search_stat
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(chrome_options=options, executable_path='driver/chromedriver')
driver.get("https://sslproxies.org/")
driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]"))))
ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]
driver.quit()
proxies = []

keywords=['펜트하우스줄거리', '펜트하우스3']
community={
    'dcinside':'dcinside.com',
    'fmkorea':'fmkorea.com',
    'dogdrip':'dogdrip.net'

}

for i in range(0, len(ips)):
    proxies.append(ips[i]+':'+ports[i])
print(proxies)


options = webdriver.ChromeOptions()
options.add_argument('--proxy-server={}'.format(proxies[1]))
driver = webdriver.Chrome(options=options, executable_path='driver/chromedriver')
driver.get('https://google.com')
