# 匯入 requests 套件
import requests
# 匯入 BeautifulSoup 套件
from bs4 import BeautifulSoup, NavigableString
# 匯入 json 套件
import json
# 匯入 pandas 套件
import pandas as pd
# 匯入 re 套件
import re
# 匯入 urllib 套件
from urllib.parse import urlencode, urljoin
# 匯入 time 套件
import time

# 設定 User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# 加上 cookies
cookies = {
    'over18': '1'
}

# 設定查詢字串
query_keyword = "大谷翔平"

# 使用 urlencode 方法將字典轉換為查詢字串
encoding_title = urlencode({'q': query_keyword})
query_url = 'https://www.ptt.cc/bbs/Gossiping/search?{}'.format(encoding_title)
# print(query_url)

# 獲取查詢結果並進行解析
resp_article_list = requests.get(query_url, headers=headers, cookies=cookies)
soup_article_list = BeautifulSoup(resp_article_list.text, 'html.parser')

# 印出 HTML 程式碼
print(soup_article_list.prettify())

# 列出所有文章並爬取
def article_crawler(url):
    # 使用 requests.get 方法下載文章頁面
    response = requests.get(url, headers=headers, cookies=cookies)
    # 若網頁回應不是 200 OK，則返回
    if response.status_code != 200:
        return
    
    # 使用 BeautifulSoup 解析 HTML 程式碼
    soup = BeautifulSoup(response.text, 'html.parser')

    # 輸出提示內容，讓使用者知道目前爬取的文章
    print("=" * 30)
    print("爬取 " + url + " 文章內容，並暫停 1 秒")
    print("=" * 30)
    # 建立文章資訊字典
    article = {
        'author_id': '',
        'author_nickname': '',
        'title': '',
        'timestamp': '',
        'contents': '',
        'ip': ''
    }
    # 文章內容
    article_body = soup.find(id='main-content')

    # 文章標頭
    article_head = article_body.findAll('div', class_='article-metaline')
    # 依序檢視文章標頭
    for metaline in article_head:
        # 作者、標題、時間
        meta_tag = metaline.find(class_='article-meta-tag').text
        # 作者、標題、時間的值
        meta_value = metaline.find(class_='article-meta-value').text
        # 依照 meta_tag 的值，將 meta_value 存入 article 字典
        if meta_tag == '作者':
            # 利用正規表達式找出作者 ID及暱稱
            compile_nickname = re.compile('\((.*)\)').search(meta_value)
            article['author_id'] = meta_value.split('(')[0].strip(' ')
            article['author_nickname'] = compile_nickname.group(1) if compile_nickname else ''
        elif meta_tag == '標題':
            article['title'] = meta_value
        elif meta_tag == '時間':
            article['timestamp'] = meta_value

    # 文章內容，去除掉標頭及推文
    # <class 'bs4.element.NavigableString'>
    contents = [expr for expr in article_body.contents if isinstance(expr, NavigableString)]
    contents = [re.sub('\n', '', expr) for expr in contents]
    contents = [i for i in contents if i]
    contents = '\n'.join(contents)
    article['contents'] = contents

    # 文章發布IP
    article_ip = article_body.find(class_='f2').text
    # 利用正規表達式找出 IP
    compile_ip = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}').search(article_ip)
    article['ip'] = compile_ip.group(0) if compile_ip else ''

    time.sleep(1)

    print("=" * 30)
    print("爬取 " + url + " 留言內容，並暫停 1 秒")
    print("=" * 30)
    comments = []
    # 依序檢視留言
    for comment in article_body.findAll('div', class_='push'):
        # 推文標籤、留言者 ID、留言內容、留言 IP、留言時間
        tag = comment.find(class_='push-tag').text
        guest_id = comment.find(class_='push-userid').text
        guest_content = comment.find(class_='push-content').text
        guest_ipdatetime = comment.find(class_='push-ipdatetime').text
        compile_ip = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}').search(guest_ipdatetime)
        guest_ip = compile_ip.group(0) if compile_ip else ''
        guest_timestamp = re.sub(guest_ip, '', guest_ipdatetime).strip()
        comments.append({
            'tag': tag,
            'id': guest_id,
            'content': guest_content,
            'ip': guest_ip,
            'timestamp': guest_timestamp
        })

    time.sleep(1)

    article['comments'] = comments
    article['url'] = url
    return article

data = []
# 逐一檢視每個文章
for article_line in soup_article_list.findAll('div', class_='r-ent'):
    title_tag = article_line.find('div', class_='title')
    article_url = title_tag.find('a')['href']
    article_url = urljoin(resp_article_list.url, article_url)
    # 爬取文章
    article_data = article_crawler(article_url)
    data.append(article_data)

with open('search_results_by_keyword.json', 'w+', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)