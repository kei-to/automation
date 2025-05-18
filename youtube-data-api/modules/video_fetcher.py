from database.db_manager import DBManager
from utils.helpers import fetch_video_info

class VideoFetcher:
    def __init__(self):
        self.db = DBManager()

    def fetch_videos(self):
        channel_id = input("チャンネルIDを入力: ")
        videos = fetch_video_info(channel_id)
        for video in videos:
            if video['ratio'] >= 20:
                print(f"動画取得: {video['title']}")
                self.db.save_video(video)
            else:
                print(f"比率不足: {video['title']}")
