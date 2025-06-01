import pytest
import time
import os
import json
from pathlib import Path
from obs_client.obs_manager import OBSManager

def load_test_config():
    """テスト用の設定を読み込む"""
    # 環境変数からパスワードを取得
    obs_password = os.getenv("OBS_WEBSOCKET_PASSWORD", "")
    
    # テスト設定ファイルの読み込み
    config_path = Path(__file__).parent.parent / "test_config.json"
    example_path = Path(__file__).parent.parent / "test_config.json.example"
    
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        with open(example_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    
    # 環境変数のパスワードで上書き
    config["obs"]["password"] = obs_password
    return config

def test_obs_integration():
    """OBSとの実際の接続テスト"""
    # 設定の読み込み
    config = load_test_config()
    
    if not config["obs"]["password"]:
        pytest.skip("OBS WebSocket password not set in environment variables")
    
    # OBSマネージャーの初期化
    obs_manager = OBSManager(config["obs"])
    
    try:
        print("\n1. OBS接続テスト")
        obs_manager.connect()
        assert obs_manager.connected, "OBSへの接続に失敗"
        print("✅ OBSに接続成功")

        # テキストソースの更新テスト
        print("\n2. テキストソース更新テスト")
        test_messages = [
            "接続テスト - メッセージ1",
            "接続テスト - メッセージ2 (特殊文字: あいうえお)",
            "接続テスト - メッセージ3 (記号: !@#$%^&*())"
        ]
        
        for message in test_messages:
            print(f"\nテスト: {message}")
            response = obs_manager.update_text(message)
            assert response is not None, f"テキストの更新に失敗: {message}"
            print("✅ テキスト更新成功")
            time.sleep(2)  # 更新を目視確認するための待機

        # 長いテキストのテスト
        print("\n3. 長いテキストのテスト")
        long_message = "これは非常に長いテキストメッセージです。" * 5
        response = obs_manager.update_text(long_message)
        assert response is not None, "長いテキストの更新に失敗"
        print("✅ 長いテキスト更新成功")
        time.sleep(2)

        # 空のテキストのテスト
        print("\n4. 空テキストのテスト")
        response = obs_manager.update_text("")
        assert response is not None, "空テキストの更新に失敗"
        print("✅ 空テキスト更新成功")
        time.sleep(2)

    finally:
        # クリーンアップ
        print("\n5. 切断テスト")
        obs_manager.disconnect()
        print("✅ OBSから切断成功")

if __name__ == "__main__":
    print("OBS接続テストを開始します...")
    print("注意: このテストを実行する前に、以下を確認してください：")
    print("1. OBSが起動していること")
    print("2. 'NowPlaying'という名前のテキストソースが作成されていること")
    print("3. 環境変数 OBS_WEBSOCKET_PASSWORD が設定されていること")
    
    try:
        test_obs_integration()
        print("\n✅ すべてのテストが成功しました！")
    except Exception as e:
        print(f"\n❌ テスト中にエラーが発生しました: {str(e)}")
        raise 