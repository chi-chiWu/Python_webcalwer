# 匯入 requests 套件
import requests

# 使用 requests.get 方法下載 PTT 棒球版首頁
url = 'https://www.ptt.cc/bbs/Baseball/index.html'
response = requests.get(url)

# 輸出回傳之狀態值與內容
print(f"狀態值: {response.status_code}, 內容: {response.text}")


