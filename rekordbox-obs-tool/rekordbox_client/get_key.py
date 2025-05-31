import os
import sqlite3
import binascii

def get_database_path():
    """rekordboxデータベースのパスを取得する"""
    appdata = os.getenv('APPDATA')
    if not appdata:
        print("Could not find APPDATA directory")
        return None
    
    db_path = os.path.join(appdata, 'Pioneer', 'rekordbox', 'master.db')
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return None
    
    return db_path

def get_database_key():
    """rekordboxのデータベースキーを取得する"""
    db_path = get_database_path()
    if not db_path:
        return None

    try:
        # データベースファイルの先頭1024バイトを読み込む
        with open(db_path, 'rb') as f:
            header = f.read(1024)

        # SQLCipher4のヘッダーを探す
        if b'SQLite format 3' not in header:
            print("Not a valid SQLite database file")
            return None

        # ヘッダーの後の16バイトがキーの可能性がある
        key_data = header[100:116]  # SQLite header size is 100 bytes
        key = binascii.hexlify(key_data).decode()
        print(f"Found potential key: {key}")
        
        # キーが正しいかテストする
        try:
            conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
            conn.close()
            print("Warning: Database is not encrypted")
            return None
        except sqlite3.OperationalError:
            print("Database is encrypted (this is expected)")
            return key
    except Exception as e:
        print(f"Error: {e}")
    
    print("Could not find database key")
    print("Please make sure:")
    print("1. Rekordbox is not running")
    print("2. Run backup_db.py to backup and remove the current database")
    print("3. Start rekordbox to create a new database")
    print("4. Try running this script again")
    return None

if __name__ == "__main__":
    get_database_key() 