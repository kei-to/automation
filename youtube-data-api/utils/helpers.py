import json
import os
from googleapiclient.discovery import build

# APIキーの読み込み
def load_api_key():
    config_path = "config/settings.json"
    with open(config_path, 'r') as file:
        settings = json.load(file)
    return settings["api_key"]

# YouTube API クライアントの初期化
api_key = load_api_key()
youtube = build("youtube", "v3", developerKey=api_key)

# チャンネル情報の取得
def fetch_channel_info(channel_id):
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()
    if "items" in response and len(response["items"]) > 0:
        item = response["items"][0]
        return {
            "id": item["id"],
            "title": item["snippet"]["title"],
            "subscriber_count": int(item["statistics"].get("subscriberCount", 0)),
            "view_count": int(item["statistics"].get("viewCount", 0)),
            "video_count": int(item["statistics"].get("videoCount", 0)),
            "ratio": float(item["statistics"].get("viewCount", 0)) / max(int(item["statistics"].get("subscriberCount", 1)), 1),
            "url": f"https://www.youtube.com/channel/{item['id']}"
        }
    return {}

# 動画情報の取得
def fetch_video_info(channel_id):
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=50,
        type="video",
        order="viewCount"
    )
    response = request.execute()
    videos = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        videos.append({
            "id": video_id,
            "title": item["snippet"]["title"],
            "view_count": 0,  # 後で動画詳細から取得
            "channel_id": channel_id,
            "ratio": 0
        })
    return videos

# ライブ配信コメントの取得
def fetch_live_comments(live_chat_id):
    comments = []
    next_page_token = None

    while True:
        request = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part="snippet,authorDetails",
            maxResults=500,
            pageToken=next_page_token
        )
        response = request.execute()

        # コメントの追加
        for item in response.get("items", []):
            comments.append({
                "id": item["id"],
                "live_id": live_chat_id,
                "channel_id": item["authorDetails"]["channelId"],
                "user_id": item["authorDetails"]["channelId"],
                "user_name": item["authorDetails"]["displayName"],
                "content": item["snippet"]["textMessageDetails"]["messageText"],
                "timestamp": item["snippet"]["publishedAt"],
                "created_at": item["snippet"]["publishedAt"]
            })

        # 次ページトークンの取得
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return comments

