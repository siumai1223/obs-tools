import os
import json

def enable_debug_mode():
    """rekordboxのデバッグモードを有効にする"""
    appdata = os.getenv('APPDATA')
    if not appdata:
        print("Could not find APPDATA directory")
        return False

    config_dir = os.path.join(appdata, 'Pioneer', 'rekordbox')
    config_file = os.path.join(config_dir, 'config.json')

    try:
        # 既存の設定を読み込む
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {}

        # デバッグモードを有効にする
        config['debug'] = True
        config['verbose'] = True
        config['log_level'] = 'debug'

        # 設定を保存
        os.makedirs(config_dir, exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        print("Debug mode enabled. Please restart rekordbox.")
        return True
    except Exception as e:
        print(f"Error enabling debug mode: {e}")
        return False

if __name__ == "__main__":
    enable_debug_mode() 