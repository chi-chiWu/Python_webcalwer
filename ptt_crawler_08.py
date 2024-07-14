# 匯入 requests 套件
import requests
# 匯入 BeautifulSoup 套件
from bs4 import BeautifulSoup
# 匯入 json 套件
import json
# 匯入 pandas 套件 -處理資料、數據分析
#處理一維與二維陣列
import pandas as pd

# 使用 requests.get 方法下載 PTT 棒球版首頁
url = 'https://www.ptt.cc/bbs/Baseball/index.html'

# 設定 User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}
# 帶入 headers 參數
response = requests.get(url, headers=headers)

# 使用 BeautifulSoup 解析 HTML 程式碼
soup = BeautifulSoup(response.text, 'html.parser')

# 儲存標題、作者、日期、人氣的列表
post_data = []
# 利用find_all方法找出所有class為r-ent的div標籤
divs = soup.find_all('div', class_='r-ent')
# 逐一檢視每個div標籤
for div in divs:
    # 找出作者
    author = div.find('div', class_='author').text
    # 找出日期
    date = div.find('div', class_='date').text
    # 找出人氣
    nrec = div.find('div', class_='nrec').text
    # 找出標題
    title = div.find('div', class_='title').text.strip()

    # 將作者、日期、人氣、標題輸出成列表
    post_data.append([author, date, nrec, title])

# 存成 EXCEL 檔案
#                               資料    欄位名稱 
df = pd.DataFrame(post_data, columns=['作者', '日期', '人氣', '標題'])
df.to_excel('index.xlsx', index=False)
