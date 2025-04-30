from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Chromeブラウザを自動セットアップ＆起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 適当なページにアクセスしてみる
driver.get('https://www.google.com')

# 少し待ってからブラウザを閉じる
import time
time.sleep(5)
driver.quit()
