import json
import os
from typing import Any, Dict, Optional

def load_config(config_path: str) -> Dict[str, Any]:
    """
    設定ファイルを読み込む

    Args:
        config_path (str): 設定ファイルのパス

    Returns:
        Dict[str, Any]: 設定データ

    Raises:
        FileNotFoundError: 設定ファイルが存在しない場合
        json.JSONDecodeError: JSONの解析に失敗した場合
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config_path: str, config_data: Dict[str, Any]) -> None:
    """
    設定ファイルを保存する

    Args:
        config_path (str): 設定ファイルのパス
        config_data (Dict[str, Any]): 保存する設定データ

    Raises:
        IOError: ファイルの書き込みに失敗した場合
    """
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)

def get_config_value(config: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    設定値を取得する

    Args:
        config (Dict[str, Any]): 設定データ
        key (str): 取得するキー（ドット区切りで階層指定可能）
        default (Any, optional): デフォルト値

    Returns:
        Any: 設定値、存在しない場合はデフォルト値
    """
    keys = key.split('.')
    value = config
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default
    return value

def validate_config(config: Dict[str, Any], required_keys: Dict[str, type]) -> bool:
    """
    設定値を検証する

    Args:
        config (Dict[str, Any]): 検証する設定データ
        required_keys (Dict[str, type]): 必須キーとその型の辞書

    Returns:
        bool: 検証結果（True: 成功、False: 失敗）
    """
    for key, expected_type in required_keys.items():
        value = get_config_value(config, key)
        if value is None or not isinstance(value, expected_type):
            return False
    return True 