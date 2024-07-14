# 匯入 requests 套件
import requests
# 匯入 BeautifulSoup 套件
from bs4 import BeautifulSoup
# 匯入 json 套件
import json
# 匯入 pandas 套件
import pandas as pd

url = "https://hahow.in/courses/6630cb930d1fdd8ee45819d3"

# 設定 User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# 帶入 headers 參數
response = requests.get(url, headers=headers)

# 印出response status code
print(response.status_code)

# 使用 BeautifulSoup 解析 HTML 程式碼
soup = BeautifulSoup(response.text, 'html.parser')

# 印出 HTML 程式碼
print(soup.prettify())

# 存成 HTML 檔案
with open('hahow_crawler_01.html', 'w', encoding='utf-8') as f:
    f.write(response.text)