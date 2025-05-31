import logging
import argparse
from rekordbox_client import RekordboxClient
from pyrekordbox.db6 import Rekordbox6Database

# ロギングの設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    try:
        # デフォルトのキー取得方法を使用
        db = Rekordbox6Database()
        print("Successfully connected to database")
        db.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return

    # テストクライアントを実行
    client = RekordboxClient()
    
    # データベースに接続
    if not client.connect():
        print("Failed to connect to rekordbox database")
        return

    try:
        # 現在再生中の曲を取得
        current_track = client.get_current_track()
        if current_track:
            print("\nCurrently playing:")
            print(f"Title: {current_track['title']}")
            print(f"Artist: {current_track['artist']}")
            print(f"BPM: {current_track['bpm']}")
            print(f"Key: {current_track['key']}")
            if current_track['last_played']:
                print(f"Last played: {current_track['last_played']}")
        else:
            print("\nNo track is currently playing")

        # 最近再生した曲の履歴を取得（直近1週間）
        print("\nRecent history (last 7 days):")
        history = client.get_history(limit=10, days=7)
        for i, track in enumerate(history, 1):
            print(f"\n{i}. {track['title']} - {track['artist']}")
            print(f"   BPM: {track['bpm']}, Key: {track['key']}")
            if track['last_played']:
                print(f"   Last played: {track['last_played']}")

    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main() 