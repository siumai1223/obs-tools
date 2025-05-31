from datetime import datetime
import pytest
from utils.time_utils import format_duration, parse_duration, format_timestamp, parse_timestamp

def test_format_duration():
    """format_duration関数のテスト"""
    # 基本的な変換
    assert format_duration(3661) == "01:01:01"  # 1時間1分1秒
    assert format_duration(7200) == "02:00:00"  # 2時間
    assert format_duration(65) == "00:01:05"    # 1分5秒
    assert format_duration(45) == "00:00:45"    # 45秒
    
    # 小数点の処理
    assert format_duration(3661.5) == "01:01:01"  # 小数点は切り捨て
    
    # ゼロの処理
    assert format_duration(0) == "00:00:00"

def test_parse_duration():
    """parse_duration関数のテスト"""
    # 基本的な変換
    assert parse_duration("01:01:01") == 3661  # 1時間1分1秒
    assert parse_duration("02:00:00") == 7200  # 2時間
    assert parse_duration("00:01:05") == 65    # 1分5秒
    assert parse_duration("00:00:45") == 45    # 45秒
    
    # 不正な形式
    assert parse_duration("1:1:1") is None        # 桁数不足
    assert parse_duration("01:01") is None        # 部分不足
    assert parse_duration("aa:bb:cc") is None     # 数字以外
    assert parse_duration("") is None             # 空文字
    assert parse_duration("24:00:00") == 86400    # 24時間

def test_format_timestamp():
    """format_timestamp関数のテスト"""
    # 特定の日時でテスト
    test_dt = datetime(2024, 1, 1, 12, 34, 56)
    
    # デフォルトフォーマット
    assert format_timestamp(test_dt) == "2024-01-01 12:34:56"
    
    # カスタムフォーマット
    assert format_timestamp(test_dt, "%Y/%m/%d") == "2024/01/01"
    assert format_timestamp(test_dt, "%H:%M:%S") == "12:34:56"
    assert format_timestamp(test_dt, "%Y年%m月%d日") == "2024年01月01日"
    
    # 現在時刻のテスト（厳密な値は比較できないので、形式のみ確認）
    current = format_timestamp()
    assert len(current) == 19  # "YYYY-MM-DD HH:MM:SS"の長さ
    assert current[4] == "-" and current[7] == "-"  # 区切り文字の確認

def test_parse_timestamp():
    """parse_timestamp関数のテスト"""
    # 基本的な変換
    expected_dt = datetime(2024, 1, 1, 12, 34, 56)
    assert parse_timestamp("2024-01-01 12:34:56") == expected_dt
    
    # カスタムフォーマット
    assert parse_timestamp("2024/01/01", "%Y/%m/%d") == datetime(2024, 1, 1)
    assert parse_timestamp("12:34:56", "%H:%M:%S") == datetime(1900, 1, 1, 12, 34, 56)
    assert parse_timestamp("2024年01月01日", "%Y年%m月%d日") == datetime(2024, 1, 1)
    
    # 不正な形式
    assert parse_timestamp("invalid") is None
    assert parse_timestamp("2024-13-01 12:34:56") is None  # 存在しない月
    assert parse_timestamp("2024-01-32 12:34:56") is None  # 存在しない日
    assert parse_timestamp("") is None  # 空文字 