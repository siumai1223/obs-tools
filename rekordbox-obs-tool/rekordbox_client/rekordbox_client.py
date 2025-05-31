from typing import Dict, List, Optional
import pyrekordbox
from pyrekordbox.db6 import Rekordbox6Database
import logging
import re

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

            return {
                "title": track.Title if hasattr(track, 'Title') else '',
                "artist": track.Artist.Name if hasattr(track, 'Artist') and track.Artist else '',
                "album": track.Album.Name if hasattr(track, 'Album') and track.Album else '',
                "genre": track.Genre.Name if hasattr(track, 'Genre') and track.Genre else '',
                "bpm": track.Bpm if hasattr(track, 'Bpm') else 0,
                "key": key,
                "rating": track.Rating if hasattr(track, 'Rating') else 0,
                "comment": track.Comment if hasattr(track, 'Comment') else '',
                "duration": track.Duration if hasattr(track, 'Duration') else 0,
                "file_path": track.Path if hasattr(track, 'Path') else ''
            }
        except Exception as e:
            self.logger.error(f"Error formatting track info: {e}")
            return {
                "title": "", "artist": "", "album": "", "genre": "",
                "bpm": 0, "key": "", "rating": 0, "comment": "",
                "duration": 0, "file_path": ""
            }

    def get_history(self, limit: int = 10) -> List[Dict]:
        """最近再生した曲の履歴を取得する"""
        try:
            if not self.db:
                if not self.connect():
                    return []

            content = self.db.get_content()
            if not content:
                return []

            # 最新の曲を返す（履歴情報は取得できないため）
            return [self._format_track_info(track) for track in content[:limit]]
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