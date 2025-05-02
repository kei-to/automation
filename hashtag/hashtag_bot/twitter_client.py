# bot/twitter_client.py

import aiohttp
import os

class TwitterClient:
    def __init__(self):
        self.bearer_token = os.getenv("BEARER_TOKEN")
        self.base_url = "https://api.twitter.com/2/tweets/search/recent"

    async def fetch_latest_tweets(self, hashtag, max_results=5):
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
        }

        params = {
            "query": hashtag,
            "max_results": max_results,
            "tweet.fields": "id,text",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    raise Exception(f"Twitter API error: {resp.status}")
                data = await resp.json()
                return data.get("data", [])  # list of tweets
