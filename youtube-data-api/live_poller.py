import time, json, sqlite3, signal, sys
from googleapiclient.discovery import build

API_KEY = json.load(open("config/settings.json"))["api_key"]
youtube = build("youtube", "v3", developerKey=API_KEY)

DB = sqlite3.connect("youtube_analysis.db", check_same_thread=False)
DB.execute("""CREATE TABLE IF NOT EXISTS live_tokens (
                 chat_id TEXT PRIMARY KEY,
                 next_token TEXT,
                 last_saved TIMESTAMP
             )""")
DB.execute("""CREATE TABLE IF NOT EXISTS comments (
                 comment_id TEXT PRIMARY KEY,
                 live_id TEXT,
                 user_name TEXT,
                 message  TEXT,
                 published TEXT
             )""")

STOP = False
for sig in (signal.SIGINT, signal.SIGTERM):
    signal.signal(sig, lambda *_: globals().update(STOP=True))

def fetch_live_chat_id(video_id: str):
    """動画 ID から activeLiveChatId を取得 (ライブ中のみ有効)"""
    resp = youtube.videos().list(part="liveStreamingDetails", id=video_id).execute()
    items = resp.get("items", [])
    if not items:
        print("動画IDが見つかりません")
        return None
    live_chat_id = items[0]["liveStreamingDetails"].get("activeLiveChatId")
    if not live_chat_id:
        print("チャットが無効、または配信前/終了後です")
    return live_chat_id

def poll_live_chat(video_id: str, interval_sec: int = 120):
    chat_id = fetch_live_chat_id(video_id)
    if not chat_id:
        return

    # 途中再開トークン
    row = DB.execute("SELECT next_token FROM live_tokens WHERE chat_id=?", (chat_id,)).fetchone()
    token = row[0] if row else None

    while not STOP:
        try:
            resp = youtube.liveChatMessages().list(
                liveChatId=chat_id,
                part="snippet,authorDetails",
                maxResults=200,
                pageToken=token
            ).execute()

            rows = [(item["id"],  # comment_id 主キーで重複防止
                     chat_id,
                     item["authorDetails"]["displayName"],
                     item["snippet"]["textMessageDetails"]["messageText"],
                     item["snippet"]["publishedAt"])
                    for item in resp.get("items", [])]
            if rows:
                with DB:
                    DB.executemany("""INSERT OR IGNORE INTO comments
                                      (comment_id, live_id, user_name, message, published)
                                      VALUES (?, ?, ?, ?, ?)""", rows)
                print(f"保存: {len(rows)} 件 (dup は除外)")

            token = resp.get("nextPageToken")
            with DB:
                DB.execute("""INSERT OR REPLACE INTO live_tokens
                              (chat_id, next_token, last_saved)
                              VALUES (?, ?, CURRENT_TIMESTAMP)""", (chat_id, token))

            time.sleep(max(interval_sec, 1))  # 120秒間隔 (最小 1s セーフガード)
        except Exception as e:
            print("API エラー", e)
            time.sleep(30)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python live_poller.py <LIVE_VIDEO_ID>")
        sys.exit(1)
    poll_live_chat(sys.argv[1])