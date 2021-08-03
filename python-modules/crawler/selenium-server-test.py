from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
chrome_options=webdriver.FirefoxOptions()

driver=webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.FIREFOX,
    options=chrome_options
)

driver.get('https://google.com')
driver.quit()