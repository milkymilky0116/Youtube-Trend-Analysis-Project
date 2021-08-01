from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver=webdriver.Remote(
    command_executor='http://110.165.16.124:31549/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME,
    options=chrome_options
)

driver.get('https://google.com')
driver.quit()