import requests
from selenium import webdriver as wd
from selenium import webdriver
print(requests.get('http://i.ytimg.com/vi/9d7jNUjBoss/0.jpg'))
print(requests.get('http://i.ytimg.com/vi/9d7jNUjBoss/0.jpg').status_code==404)

print(requests.get('http://110.165.16.124:4444/').status_code)