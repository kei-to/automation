import aiohttp
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class TwitterAPIError(Exception): pass
class TwitterRateLimitError(TwitterAPIError): pass
class TwitterAuthError(TwitterAPIError): pass

class TwitterClient:
    def __init__(self):
        self.bearer_token = os.getenv("BEARER_TOKEN")
        if not self.bearer_token:
            raise RuntimeError("BEARER_TOKEN not set in environment variables.")
        self.base_url = "https://api.twitter.com/2/tweets/search/recent"

    async def fetch_latest_tweets(self, hashtag: str, max_results: int = 10) -> List[Dict]:
        headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }

        params = {
            "query": hashtag,
            "max_results": max_results,
            "tweet.fields": "id,text"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, headers=headers, params=params) as resp:
                print(resp.status, await resp.text())
                if resp.status == 429:
                    raise TwitterRateLimitError("Twitter API rate limit exceeded")
                elif resp.status == 401:
                    raise TwitterAuthError("Invalid or expired Bearer token")
                elif resp.status != 200:
                    raise TwitterAPIError(f"Twitter API error: {resp.status}")

                data = await resp.json()
                return data.get("data", [])  # list of tweets
