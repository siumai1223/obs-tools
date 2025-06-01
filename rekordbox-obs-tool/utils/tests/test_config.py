import json
import os
import pytest
from utils.config import load_config, save_config, get_config_value, validate_config

@pytest.fixture
def temp_config_file(tmp_path):
    """一時的な設定ファイルを作成するフィクスチャ"""
    config_data = {
        "obs": {
            "host": "localhost",
            "port": 4444,
            "password": os.getenv("TEST_OBS_PASSWORD", "")  # 環境変数から取得
        },
        "display": {
            "font_size": 12,
            "color": "#FFFFFF"
        }
    }
    config_file = tmp_path / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_data, f)
    return str(config_file)

def test_load_config(temp_config_file):
    """load_config関数のテスト"""
    config = load_config(temp_config_file)
    assert isinstance(config, dict)
    assert config["obs"]["host"] == "localhost"
    assert config["obs"]["port"] == 4444
    assert config["display"]["font_size"] == 12

def test_load_config_file_not_found():
    """存在しないファイルを読み込もうとした場合のテスト"""
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_file.json")

def test_save_config(tmp_path):
    """save_config関数のテスト"""
    config_file = tmp_path / "new_config.json"
    config_data = {"test": "data"}
    save_config(str(config_file), config_data)
    
    # 保存したファイルを読み込んで検証
    with open(config_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data == config_data

def test_get_config_value(temp_config_file):
    """get_config_value関数のテスト"""
    config = load_config(temp_config_file)
    
    # 存在する値の取得
    assert get_config_value(config, "obs.host") == "localhost"
    assert get_config_value(config, "display.font_size") == 12
    
    # 存在しない値の取得（デフォルト値を使用）
    assert get_config_value(config, "non.existent.key", default="default") == "default"
    
    # 階層が途中で切れる場合
    assert get_config_value(config, "obs.non_existent", default="default") == "default"

def test_validate_config():
    """validate_config関数のテスト"""
    config = {
        "server": {
            "host": "localhost",
            "port": 8080
        },
        "timeout": 30
    }
    
    # 正しい型の検証
    required_keys = {
        "server.host": str,
        "server.port": int,
        "timeout": int
    }
    assert validate_config(config, required_keys) is True
    
    # 誤った型の検証
    wrong_types = {
        "server.host": int,
        "server.port": str
    }
    assert validate_config(config, wrong_types) is False
    
    # 存在しないキーの検証
    non_existent_keys = {
        "non.existent.key": str
    }
    assert validate_config(config, non_existent_keys) is False 