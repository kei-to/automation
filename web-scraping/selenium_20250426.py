import requests
from bs4 import BeautifulSoup

# 1. ページにアクセス
url = 'https://www.youtube.com/'
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/114.0.0.0 Safari/537.36'
    )
}
response = requests.get(url, headers=headers)
response.raise_for_status()  # 念のためステータスコードをチェック

# 2. HTMLをパース
soup = BeautifulSoup(response.text, 'html.parser')

# 3. metaタグをすべて取得し、nameかproperty属性を持つものだけフィルター
meta_tags = soup.find_all('meta')
filtered = [
    tag for tag in meta_tags
    if tag.get('name') or tag.get('property')
]

# 4. 抜き出した情報を表示
for tag in filtered:
    key = tag.get('name') or tag.get('property')
    content = tag.get('content', '')
    print(f"{key}: {content}")