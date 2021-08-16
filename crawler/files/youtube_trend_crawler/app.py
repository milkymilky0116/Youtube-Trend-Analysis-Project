from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from yt_trend_crawler import Youtube_Crawler
def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options
if __name__ == "__main__":
    chrome_options=set_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)
    keyword_list=['강아지','고양이','뉴스','여행','예능','축구','스마트폰','운동','게임','요리']
    Youtube_Crawler(keyword_list,'zofo3v8hwj',"uSaxHZaefo6WTQ2rwcdNJqVGnngg3QkjA10dvEw9","AIzaSyA8AVDeWVW2aEqMds7z51gjhr8o3ebRyik",driver)