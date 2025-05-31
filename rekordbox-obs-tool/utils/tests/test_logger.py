import logging
import os
import pytest
from utils.logger import setup_logger, get_log_level

@pytest.fixture
def temp_log_file(tmp_path):
    """一時的なログファイルパスを提供するフィクスチャ"""
    return str(tmp_path / "test.log")

def test_setup_logger_console_only():
    """コンソール出力のみのロガー設定テスト"""
    logger = setup_logger("test_console")
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)

def test_setup_logger_with_file(temp_log_file):
    """ファイル出力を含むロガー設定テスト"""
    logger = setup_logger("test_file", log_file=temp_log_file)
    assert isinstance(logger, logging.Logger)
    assert len(logger.handlers) == 2
    
    # ハンドラーの種類を確認
    handlers = logger.handlers
    assert any(isinstance(h, logging.StreamHandler) for h in handlers)
    assert any(isinstance(h, logging.handlers.RotatingFileHandler) for h in handlers)
    
    # ログファイルが作成されたことを確認
    assert os.path.exists(temp_log_file)

def test_setup_logger_custom_level():
    """カスタムログレベルの設定テスト"""
    logger = setup_logger("test_level", level=logging.DEBUG)
    assert logger.level == logging.DEBUG

def test_setup_logger_custom_format():
    """カスタムフォーマットの設定テスト"""
    custom_format = '%(levelname)s - %(message)s'
    logger = setup_logger("test_format", format_string=custom_format)
    
    # 最初のハンドラーのフォーマッターを確認
    formatter = logger.handlers[0].formatter
    assert formatter._fmt == custom_format

def test_get_log_level():
    """ログレベル変換のテスト"""
    assert get_log_level("DEBUG") == logging.DEBUG
    assert get_log_level("INFO") == logging.INFO
    assert get_log_level("WARNING") == logging.WARNING
    assert get_log_level("ERROR") == logging.ERROR
    assert get_log_level("CRITICAL") == logging.CRITICAL
    
    # 小文字でも動作することを確認
    assert get_log_level("debug") == logging.DEBUG
    assert get_log_level("info") == logging.INFO
    
    # 不正な値の場合はINFOを返すことを確認
    assert get_log_level("INVALID") == logging.INFO
    assert get_log_level("") == logging.INFO 