from typing import Dict, List, Optional
import pyrekordbox
from pyrekordbox.db6 import Rekordbox6Database
import logging
import re
from datetime import datetime, timedelta

class RekordboxClient:
    def __init__(self, key: Optional[str] = None):
        self.db = None
        self.key = key
        self.logger = logging.getLogger(__name__)

    def connect(self) -> bool:
        """rekordboxデータベースに接続する"""
        try:
            self.db = Rekordbox6Database(key=self.key)
            self.logger.info("Successfully connected to rekordbox database")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to rekordbox database: {e}")
            return False

    def get_current_track(self) -> Optional[Dict]:
        """現在再生中の曲情報を取得する"""
        try:
            if not self.db:
                if not self.connect():
                    return None

            # 現在再生中の曲を取得
            content = self.db.get_content()
            if not content:
                return None

            # 最初の曲を返す（現在再生中の曲の情報は取得できないため）
            return self._format_track_info(content[0])
        except Exception as e:
            self.logger.error(f"Error getting current track: {e}")
            return None

    def _format_track_info(self, track) -> Dict:
        """曲情報を整形する"""
        try:
            # キー情報から名前部分を抽出
            key_str = str(track.Key) if hasattr(track, 'Key') and track.Key else ''
            key_match = re.search(r'Name=([^)]+)', key_str)
            key = key_match.group(1) if key_match else ''

            # BPM情報を取得（デバッグ情報を追加）
            bpm = 0
            if hasattr(track, 'BPM'):  # 大文字のBPMを試す
                try:
                    bpm_value = float(track.BPM)
                    # BPMは100倍の整数値として保存されているため、100で割る
                    bpm = round(bpm_value / 100, 2) if bpm_value > 0 else 0
                    self.logger.info(f"Raw BPM value for {track.Title}: {track.BPM}, Converted: {bpm}")
                except (ValueError, TypeError) as e:
                    self.logger.error(f"Error converting BPM for {track.Title}: {e}")
                    bpm = 0
            else:
                self.logger.warning(f"No BPM attribute found for track: {track.Title}")

            # 日付情報を取得（updated_atを使用）
            last_played = None
            if hasattr(track, 'updated_at'):
                try:
                    last_played = track.updated_at
                    self.logger.info(f"Last played date for {track.Title}: {last_played}")
                except Exception as e:
                    self.logger.error(f"Error getting updated_at for {track.Title}: {e}")
                    last_played = None
            else:
                self.logger.warning(f"No updated_at found for track: {track.Title}")

            # 利用可能な属性をログに出力
            self.logger.info(f"Available attributes for track {track.Title}:")
            for attr in dir(track):
                if not attr.startswith('_'):
                    try:
                        value = getattr(track, attr)
                        self.logger.info(f"  {attr}: {value}")
                    except Exception as e:
                        self.logger.error(f"Error getting attribute {attr}: {e}")

            return {
                "title": track.Title if hasattr(track, 'Title') else '',
                "artist": track.Artist.Name if hasattr(track, 'Artist') and track.Artist else '',
                "album": track.Album.Name if hasattr(track, 'Album') and track.Album else '',
                "genre": track.Genre.Name if hasattr(track, 'Genre') and track.Genre else '',
                "bpm": bpm,
                "key": key,
                "rating": track.Rating if hasattr(track, 'Rating') else 0,
                "comment": track.Comment if hasattr(track, 'Comment') else '',
                "duration": track.Duration if hasattr(track, 'Duration') else 0,
                "file_path": track.Path if hasattr(track, 'Path') else '',
                "last_played": last_played.strftime('%Y-%m-%d %H:%M:%S') if last_played else None,
                "play_count": track.DJPlayCount if hasattr(track, 'DJPlayCount') else 0
            }
        except Exception as e:
            self.logger.error(f"Error formatting track info: {e}")
            return {
                "title": "", "artist": "", "album": "", "genre": "",
                "bpm": 0, "key": "", "rating": 0, "comment": "",
                "duration": 0, "file_path": "", "last_played": None,
                "play_count": 0
            }

    def get_history(self, limit: int = 10, days: int = 7) -> List[Dict]:
        """最近再生した曲の履歴を取得する

        Args:
            limit (int): 取得する曲数の上限
            days (int): 何日前までの履歴を取得するか
        """
        try:
            if not self.db:
                if not self.connect():
                    return []

            content = self.db.get_content()
            if not content:
                return []

            # 一週間前の日時を計算
            week_ago = datetime.now() - timedelta(days=days)
            self.logger.info(f"Filtering tracks played after: {week_ago}")

            # updated_atを持つ曲をフィルタリング
            history = []
            for track in content:
                if hasattr(track, 'updated_at') and track.updated_at:
                    try:
                        # 一週間以内の曲のみを追加
                        if track.updated_at > week_ago:
                            history.append((track, track.updated_at))
                            self.logger.info(f"Found recent track: {track.Title} (updated at {track.updated_at})")
                    except Exception as e:
                        self.logger.error(f"Error checking updated_at for track {track.Title}: {e}")
                        continue

            # 日付でソートして最新順に並び替え
            history.sort(key=lambda x: x[1], reverse=True)
            self.logger.info(f"Found {len(history)} tracks in history")

            # 指定された数の曲情報を返す
            return [self._format_track_info(track) for track, _ in history[:limit]]
        except Exception as e:
            self.logger.error(f"Error getting history: {e}")
            return []

    def close(self):
        """データベース接続を閉じる"""
        if self.db:
            try:
                self.db.close()
                self.logger.info("Database connection closed")
            except Exception as e:
                self.logger.error(f"Error closing database connection: {e}") 