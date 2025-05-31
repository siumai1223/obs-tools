from datetime import datetime, timedelta
from typing import Optional, Union

def format_duration(seconds: Union[int, float]) -> str:
    """
    秒数を「HH:MM:SS」形式に変換する

    Args:
        seconds (Union[int, float]): 秒数

    Returns:
        str: フォーマットされた時間文字列
    """
    duration = timedelta(seconds=int(seconds))
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def parse_duration(duration_str: str) -> Optional[int]:
    """
    「HH:MM:SS」形式の文字列を秒数に変換する

    Args:
        duration_str (str): 時間文字列

    Returns:
        Optional[int]: 秒数（変換失敗時はNone）
    """
    try:
        parts = duration_str.split(':')
        if len(parts) != 3:
            return None
            
        # 各部分が2桁であることを確認
        if not all(len(part) == 2 for part in parts):
            return None
            
        hours, minutes, seconds = map(int, parts)
        if minutes >= 60 or seconds >= 60:  # 分と秒は60未満であることを確認
            return None
        return hours * 3600 + minutes * 60 + seconds
    except (ValueError, TypeError):
        return None

def format_timestamp(dt: Optional[datetime] = None, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    datetimeオブジェクトを指定フォーマットの文字列に変換する

    Args:
        dt (Optional[datetime]): 日時オブジェクト（Noneの場合は現在時刻）
        format_str (str): 出力フォーマット

    Returns:
        str: フォーマットされた日時文字列
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime(format_str)

def parse_timestamp(timestamp_str: str, format_str: str = '%Y-%m-%d %H:%M:%S') -> Optional[datetime]:
    """
    日時文字列をdatetimeオブジェクトに変換する

    Args:
        timestamp_str (str): 日時文字列
        format_str (str): 入力フォーマット

    Returns:
        Optional[datetime]: 日時オブジェクト（変換失敗時はNone）
    """
    try:
        return datetime.strptime(timestamp_str, format_str)
    except ValueError:
        return None 