from database.db_manager import DBManager
from utils.helpers import fetch_live_comments

class CommentFetcher:
    def __init__(self):
        self.db = DBManager()

    def fetch_comments(self):
        live_id = input("ライブ配信IDを入力: ")
        comments = fetch_live_comments(live_id)

        if comments:
            print(f"取得コメント数: {len(comments)} 件")
            for comment in comments:
                print(f"[{comment['timestamp']}] {comment['user_name']}: {comment['content']}")
                self.db.save_comment(comment)
            print("コメント取得が完了しました。")
        else:
            print("コメントが見つかりませんでした。")
