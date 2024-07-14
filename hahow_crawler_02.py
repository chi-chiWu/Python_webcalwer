# 匯入 requests 套件
import requests
# 匯入 BeautifulSoup 套件
from bs4 import BeautifulSoup
# 匯入 json 套件
import json
# 匯入 pandas 套件
import pandas as pd
# 匯入 time 套件
import time

url = "https://api.hahow.in/api/products/search?category=COURSE&filter=INCUBATING&limit=24&page=0&sort=INCUBATE_TIME"

# 設定 User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

courses = []
# 獲取JSON資料
response = requests.get(url, headers=headers)
if response.status_code == 200:
    courses = response.json()
    # print(courses)
    # 取得產品資料
    products = courses['data']['courseData']['products']

    # 以List儲存資料
    courses = []
    # 印出產品資料標題
    for product in products:
        # 利用字典方式儲存資料
        course_data = {
            'title': product['title'],
            'metaDescription': product['metaDescription'],
            'price': product['price'],
            'numSoldTickets': product['numSoldTickets'],
            'numRating': product['numRating'],
        }
        courses.append(course_data)
    print(courses)
else:
    print("請求失敗")

# 建立DataFrame

# 存成 EXCEL 檔案

# 最後的部分請大家自己嘗試