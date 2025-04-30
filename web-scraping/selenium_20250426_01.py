from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


import time

# 対象のチャンネルURL (例：@GoogleJapan のチャンネルページ）
channel_url = 'https://www.youtube.com/@Vtube_kei/videos'

# Chromeブラウザを起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # 指定チャンネルの「動画」タブにアクセス
    driver.get(channel_url)

    # ページを少し待つ（最低限）
    time.sleep(5)

    # 動画一覧が入っているコンテンツエリアを取得
    content_element = driver.find_element(By.ID, "contents")

    # outerHTMLで要素まるごとのHTMLを取得
    html = content_element.get_attribute('outerHTML')

    # ファイルに保存
    with open('channel_videos.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("動画一覧HTMLを保存しました！✅")

finally:
    # 最後にブラウザを閉じる
    driver.quit()

