# main.py  ── エントリーポイント
from modules.channel_filter import ChannelFilter
from modules.video_fetcher import VideoFetcher
from modules.comment_fetcher import CommentFetcher
import live_poller

def main():
    MENU = """
YouTube チャンネル分析ツール
  1. チャンネル情報フィルタリング
  2. 動画情報取得
  3. ライブチャット取得（単発）
  4. ライブチャット常時ポーリング（120 秒間隔）
選択してください (1/2/3/4): """
    choice = input(MENU).strip()

    if choice == "1":
        ChannelFilter().filter_channels()

    elif choice == "2":
        VideoFetcher().fetch_videos()

    elif choice == "3":
        CommentFetcher().fetch_comments()

    elif choice == "4":
        video_id = input("ライブ配信の動画 ID を入力: ").strip()
        # 120 秒間隔。変更したい場合は第 2 引数で指定
        live_poller.poll_live_chat(video_id, interval_sec=120)

    else:
        print("無効な選択です。")

if __name__ == "__main__":
    main()
