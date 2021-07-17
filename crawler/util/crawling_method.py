import time
import re
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
    text_count = re.findall(r'(\d+(?:\.\d+)?)',text)
    int_count=float(text_count[0])
    if text.find('만')!=-1:
        int_count=int_count*10000
    elif text.find('천')!=-1:
        int_count=int_count*1000
    return int(int_count)