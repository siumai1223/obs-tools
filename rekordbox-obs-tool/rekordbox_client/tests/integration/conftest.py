import os
import pytest
import json

@pytest.fixture
def db_path():
    """rekordboxデータベースのパスを提供するfixture"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config["rekordbox"]["database_path"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        # CIテスト用のダミーパス
        return os.path.join(os.path.dirname(__file__), 'test_data', 'test.db') 