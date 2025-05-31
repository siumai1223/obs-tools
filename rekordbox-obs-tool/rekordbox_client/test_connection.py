import os
import json
import sqlite3
import subprocess

def load_config():
    """設定ファイルを読み込む"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def test_database_connection(db_path):
    """データベースへの接続をテストする"""
    try:
        # データベースファイルの存在確認
        if not os.path.exists(db_path):
            print(f"エラー: データベースファイルが見つかりません: {db_path}")
            return

        print(f"データベースファイルを確認: {db_path}")
        print("ファイルは存在します。")
        
        # ファイルサイズを確認
        file_size = os.path.getsize(db_path)
        print(f"データベースファイルサイズ: {file_size / (1024*1024):.2f} MB")
        
        # SQLiteデータベースとして開いてみる
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # テーブル一覧を取得
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if tables:
                print("\nデータベーステーブル一覧:")
                for table in tables:
                    print(f"- {table[0]}")
                    
                    # テーブルのスキーマを表示
                    cursor.execute(f"PRAGMA table_info({table[0]})")
                    columns = cursor.fetchall()
                    print("  カラム:")
                    for col in columns:
                        print(f"    - {col[1]} ({col[2]})")
            else:
                print("\n警告: テーブルが見つかりません。データベースが暗号化されている可能性があります。")
            
        except sqlite3.DatabaseError as e:
            print(f"\n警告: SQLiteデータベースとして読み取れません: {e}")
            print("データベースが暗号化されている可能性があります。")
        finally:
            if 'conn' in locals():
                conn.close()

    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    # 設定を読み込む
    config = load_config()
    rekordbox_config = config["rekordbox"]
    
    # 接続テストを実行
    test_database_connection(rekordbox_config["database_path"]) 