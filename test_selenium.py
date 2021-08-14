from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
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

driver.get('https://naver.com')

print(driver.page_source)