import requests
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv('credentials.env')

# 環境変数からトークン取得
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')


class TwitterClient:
    def __init__(self, env_path='credentials.env'):
        # 認証情報ロード
        load_dotenv(env_path)
        self.bearer_token = os.getenv('BEARER_TOKEN')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.base_url = 'https://api.twitter.com/2'

    def post_tweet(text):
        url = 'https://api.twitter.com/2/tweets'
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        payload = {
            'text': text
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            print('ツイート成功！')
            print(response.json())
        else:
            print('ツイート失敗')
            print(response.status_code, response.text)

    def get_latest_tweets(user_id):
        url = f'https://api.twitter.com/2/users/{user_id}/tweets'
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}',
        }
        params = {
            'max_results': 5
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            tweets = response.json()
            print('最新ツイート取得成功！')
            for tweet in tweets.get('data', []):
                print(tweet['text'])
        else:
            print('取得失敗')
            print(response.status_code, response.text)

    def get_direct_messages():
        url = 'https://api.twitter.com/2/dm_events'
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
        }
        params = {
            'max_results': 5
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            dms = response.json()
            print('DM一覧：')
            for event in dms.get('data', []):
                print(event)
        else:
            print('DM取得失敗')
            print(response.status_code, response.text)