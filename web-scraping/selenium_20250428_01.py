from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import random

# Chromeブラウザを起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
target_url = 'http://163.44.116.72/'
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/114.0.0.0 Safari/537.36'
    )
}

def main():
    # instanciate
    bot = BrowserController()
    # wait for space-karen
    time.sleep(10)

    bot.access(target_url)
    element = '_ngcontent-ng-c1181079105'
    bot.wait()
    bot.click(element)
    bot.wait()
    bot.randomScroll()
    bot.wait()
    bot.driver.quit()

class BrowserController:
    def __init__(self):
        chrome_options = webdriver.chrome.options.Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')

        # instanciate
        self.driver = webdriver.Chrome(options = chrome_options)
        
    def access(self, target_url):
        driver.get(target_url)

    def wait(self):
        time.sleep(random.uniform(1.5, 10.0))

    def click(self, target_ele):
        elm = driver.find_element(By.TAG_NAME, 'button')
        elm.click()

    def randomScroll(proc):
        scroll_step = random.randint(400, 600)
        scroll_pause = random.uniform(1.5, 3.0)

        current_scroll = 0
        max_scroll = proc.driver.execute_script("return document.body.scrollHeight")

        while current_scroll < max_scroll:
            # 少しずつスクロール
            proc.driver.execute_script(f"window.scrollTo(0, {current_scroll});")
            time.sleep(scroll_pause)
            # スクロール位置を更新
            current_scroll += scroll_step
            # ページ全体の高さも更新
            max_scroll = proc.driver.execute_script("return document.body.scrollHeight")

    def quit(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    main()