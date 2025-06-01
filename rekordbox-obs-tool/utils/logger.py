import logging
import logging.handlers
import os
from typing import Optional

def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    max_bytes: int = 1024 * 1024,  # 1MB
    backup_count: int = 3
) -> logging.Logger:
    """
    ロガーを設定する

    Args:
        name (str): ロガー名
        log_file (Optional[str]): ログファイルパス
        level (int): ログレベル
        format_string (Optional[str]): ログフォーマット
        max_bytes (int): ログファイルの最大サイズ
        backup_count (int): 保持するバックアップファイル数

    Returns:
        logging.Logger: 設定済みのロガー
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format_string)

    # コンソールハンドラーの設定
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # ファイルハンドラーの設定（指定された場合）
    if log_file:
        # ログディレクトリの作成
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def get_log_level(level_name: str) -> int:
    """
    ログレベル名から数値を取得する

    Args:
        level_name (str): ログレベル名

    Returns:
        int: ログレベル数値
    """
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    return level_map.get(level_name.upper(), logging.INFO) 