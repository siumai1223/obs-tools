import json
import os

class ConfigManager:
    """設定ファイルの読み込みと管理を行うクラス"""
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self):
        """設定ファイルを読み込む"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            'config.json'
        )
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"設定ファイルの読み込みに失敗しました: {str(e)}")
    
    @property
    def obs_config(self):
        """OBS接続設定を取得"""
        return self.config.get('obs', {})
    
    @property
    def display_config(self):
        """表示設定を取得"""
        return self.config.get('display', {}) 