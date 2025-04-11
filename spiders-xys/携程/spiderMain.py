from selenium import webdriver
from selenium.webdriver.chrome.service import Service # 新版selenium的service
from selenium.webdriver.common.by import By
from DrissionPage import ChromiumPage
import csv
import json
import os.path
import time
import django
import pandas as pd
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boss直聘.settings')#初始化django环境



dp = ChromiumPage()
dp.listen.start('json/HotelSearch?')
dp.get('https://hotels.ctrip.com/hotels/list?countryId=1&city=25&provinceId=0&checkin=2024/11/10&checkout=2024/11/11&optionId=25&optionType=City&directSearch=&display=%E5%8E%A6%E9%97%A8%2C%20%E7%A6%8F%E5%BB%BA%2C%20%E4%B8%AD%E5%9B%BD&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1&&highPrice=-1&barCurr=CNY&sort=6')
resp = dp.listen.wait()
json_data = resp.response.body
hotelList = json_data['Response']['hotelList']['list']
for index in hotelList:
    dit = {
        '酒店:':index['base']['hotelName'],
        '评论:':index['comment']['content'],
        '价格:':index['money']['price'],
        '地址:':index['position']['cityName']
    }
    print(dit)