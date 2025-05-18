from database.db_manager import DBManager
from utils.helpers import fetch_channel_info

class ChannelFilter:
    def __init__(self):
        self.db = DBManager()

    def filter_channels(self):
        channel_ids = input("チャンネルIDをカンマ区切りで入力: ").split(",")
        threshold = int(input("登録者数の上限を指定 (デフォルト: 10000): ") or 10000)
        
        for channel_id in channel_ids:
            info = fetch_channel_info(channel_id.strip())
            if info['subscriber_count'] <= threshold:
                print(f"フィルタ通過: {info['title']}")
                self.db.save_channel(info)
            else:
                print(f"フィルタ除外: {info['title']}")
