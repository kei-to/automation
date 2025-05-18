import sqlite3
from pathlib import Path

class DBManager:
    """SQLite 接続とテーブル自動生成を担う。初回起動時に全テーブルを作成する。"""

    def __init__(self, db_path: str = "youtube_analysis.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()

    # --- テーブル作成 ---
    def _create_tables(self):
        ddl = """
        CREATE TABLE IF NOT EXISTS channels (
            channel_id TEXT PRIMARY KEY,
            channel_name TEXT,
            subscriber_count INTEGER,
            view_count INTEGER,
            video_count INTEGER,
            ratio REAL,
            url TEXT
        );

        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            view_count INTEGER,
            channel_id TEXT,
            ratio REAL
        );

        CREATE TABLE IF NOT EXISTS comments (
            comment_id TEXT PRIMARY KEY,
            live_id TEXT,
            user_name TEXT,
            message TEXT,
            published TEXT
        );

        CREATE TABLE IF NOT EXISTS live_tokens (
            chat_id TEXT PRIMARY KEY,
            next_token TEXT,
            last_saved TIMESTAMP
        );
        """
        with self.conn:
            self.conn.executescript(ddl)

    # --- データ保存メソッド ---
    def save_channel(self, ch):
        with self.conn:
            self.conn.execute(
                """INSERT OR IGNORE INTO channels
                       (channel_id, channel_name, subscriber_count, view_count, video_count, ratio, url)
                       VALUES (?,?,?,?,?,?,?)""",
                (ch["id"], ch["title"], ch["subscriber_count"], ch["view_count"],
                 ch["video_count"], ch["ratio"], ch["url"])
            )

    def save_video(self, v):
        with self.conn:
            self.conn.execute(
                """INSERT OR IGNORE INTO videos
                       (video_id, title, view_count, channel_id, ratio)
                       VALUES (?,?,?,?,?)""",
                (v["id"], v["title"], v["view_count"], v["channel_id"], v["ratio"])
            )

    def save_comment(self, c):
        with self.conn:
            self.conn.execute(
                """INSERT OR IGNORE INTO comments
                       (comment_id, live_id, user_name, message, published)
                       VALUES (?,?,?,?,?)""",
                (c["id"], c["live_id"], c["user_name"], c["content"], c["timestamp"])
            )

    # --- nextPageToken の保持 ---
    def update_next_token(self, chat_id: str, token: str):
        with self.conn:
            self.conn.execute(
                """INSERT OR REPLACE INTO live_tokens
                       (chat_id, next_token, last_saved)
                       VALUES (?,?,CURRENT_TIMESTAMP)""",
                (chat_id, token)
            )

    def get_next_token(self, chat_id: str):
        row = self.conn.execute("SELECT next_token FROM live_tokens WHERE chat_id=?", (chat_id,)).fetchone()
        return row[0] if row else None

