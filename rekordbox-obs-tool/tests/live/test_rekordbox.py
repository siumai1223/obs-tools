from rekordbox_client.rekordbox_client import RekordboxClient
import time
import json

def test_rekordbox_live():
    """Rekordboxとの実際の接続をテストする"""
    # クライアントの初期化
    client = RekordboxClient()
    
    print("Rekordbox Client Test")
    print("===================")
    
    # データベース接続
    print("\n1. データベース接続テスト")
    assert client.connect(), "データベース接続に失敗"
    print("✅ データベースに接続成功")

    try:
        # 現在の曲情報を取得
        print("\n2. 現在の曲情報取得テスト")
        track = client.get_current_track()
        if track:
            print("✅ 曲情報の取得成功")
            print("\n取得した曲情報:")
            print(json.dumps(track, indent=2, ensure_ascii=False))
        else:
            print("ℹ️ 現在再生中の曲はありません")

        # 履歴情報を取得
        print("\n3. 再生履歴取得テスト")
        history = client.get_history(limit=5)  # 最新5曲を取得
        if history:
            print("✅ 履歴情報の取得成功")
            print("\n最近再生された曲:")
            for i, track in enumerate(history, 1):
                print(f"\n{i}. {track['title']} - {track['artist']}")
                print(f"   BPM: {track['bpm']}, Key: {track['key']}")
                print(f"   最終再生: {track['last_played']}")
        else:
            print("ℹ️ 履歴情報はありません")

        # リアルタイム監視テスト
        print("\n4. リアルタイム監視テスト（10秒間）")
        print("rekordboxで曲を再生または選択してください...")
        
        start_time = time.time()
        last_title = None
        
        while time.time() - start_time < 10:
            track = client.get_current_track()
            if track and track['title'] != last_title:
                last_title = track['title']
                print(f"\n新しい曲を検出: {track['title']} - {track['artist']}")
                print(f"BPM: {track['bpm']}, Key: {track['key']}")
            time.sleep(1)

    finally:
        # クリーンアップ
        client.close()
        print("\nテスト完了") 