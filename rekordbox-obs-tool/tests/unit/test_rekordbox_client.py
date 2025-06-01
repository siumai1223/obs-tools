import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from rekordbox_client.rekordbox_client import RekordboxClient

class TestRekordboxClient:
    @pytest.fixture
    def mock_track(self):
        track = Mock()
        track.Title = "Test Track"
        track.Artist = Mock(Name="Test Artist")
        track.Album = Mock(Name="Test Album")
        track.Genre = Mock(Name="Test Genre")
        track.BPM = 12800  # 128.00 BPM
        track.Key = "Name=Cm"
        track.Rating = 5
        track.Comment = "Test Comment"
        track.Duration = 180
        track.Path = "/path/to/track"
        track.DJPlayCount = 10
        track.updated_at = datetime.now()
        return track

    @pytest.fixture
    def client(self):
        return RekordboxClient()

    def test_get_current_track_basic(self, client, mock_track):
        # モックデータベースの設定
        mock_db = Mock()
        mock_db.get_content.return_value = [mock_track]
        client.db = mock_db

        # テスト実行
        result = client.get_current_track()

        # 結果の検証
        assert result is not None
        assert result["title"] == "Test Track"
        assert result["artist"] == "Test Artist"
        assert result["bpm"] == 128.00
        assert result["key"] == "Cm"
        assert result["play_count"] == 10

    def test_get_current_track_multiple_tracks(self, client, mock_track):
        # 複数の曲を用意（異なる更新時刻）
        older_track = Mock()
        older_track.Title = "Old Track"
        older_track.Artist = Mock(Name="Old Artist")
        older_track.updated_at = datetime.now() - timedelta(minutes=30)

        newer_track = Mock()
        newer_track.Title = "New Track"
        newer_track.Artist = Mock(Name="New Artist")
        newer_track.updated_at = datetime.now()

        # モックデータベースの設定
        mock_db = Mock()
        mock_db.get_content.return_value = [older_track, newer_track]
        client.db = mock_db

        # テスト実行
        result = client.get_current_track()

        # 結果の検証（最新の曲が選択されることを確認）
        assert result is not None
        assert result["title"] == "New Track"
        assert result["artist"] == "New Artist"

    def test_get_current_track_cache_behavior(self, client, mock_track):
        # モックデータベースの設定
        mock_db = Mock()
        mock_db.get_content.return_value = [mock_track]
        client.db = mock_db

        # 1回目の呼び出し
        result1 = client.get_current_track()
        assert result1 is not None
        assert result1["title"] == "Test Track"

        # 同じ曲で2回目の呼び出し
        result2 = client.get_current_track()
        assert result2 is not None
        assert result2["title"] == "Test Track"
        assert result1 == result2  # キャッシュが使用されていることを確認

        # 異なる曲での呼び出し
        new_track = mock_track
        new_track.Title = "New Track"
        new_track.updated_at = datetime.now()
        mock_db.get_content.return_value = [new_track]

        result3 = client.get_current_track()
        assert result3 is not None
        assert result3["title"] == "New Track"
        assert result1 != result3  # 新しい曲情報が取得されていることを確認

    def test_database_connection(self, client):
        """データベース接続のテスト"""
        # 正常な接続
        mock_db = Mock()
        with patch('rekordbox_client.rekordbox_client.Rekordbox6Database', return_value=mock_db):
            assert client.connect() is True

        # 接続エラー
        with patch('rekordbox_client.rekordbox_client.Rekordbox6Database', side_effect=Exception("Connection failed")):
            assert client.connect() is False

    def test_get_current_track_error_cases(self, client):
        """エラーケースのテスト"""
        # データベース未接続の状態を作成
        client.db = None
        with patch.object(client, 'connect', return_value=False):
            assert client.get_current_track() is None

        # 空のコンテンツ
        mock_db = Mock()
        mock_db.get_content.return_value = []
        client.db = mock_db
        assert client.get_current_track() is None

        # データベースエラー
        mock_db.get_content.side_effect = Exception("Database error")
        assert client.get_current_track() is None

    def test_format_track_info_error_cases(self, client):
        """曲情報フォーマットのエラーケースのテスト"""
        # 最小限の属性しか持たない曲
        minimal_track = Mock()
        minimal_track.Title = "Minimal Track"
        minimal_track.Artist = None
        minimal_track.Album = None
        minimal_track.Genre = None
        minimal_track.BPM = None
        minimal_track.Key = None
        minimal_track.Rating = None
        minimal_track.Comment = None
        minimal_track.Duration = None
        minimal_track.Path = None
        minimal_track.DJPlayCount = None
        minimal_track.updated_at = None
        
        result = client._format_track_info(minimal_track)
        assert result["title"] == "Minimal Track"
        assert result["artist"] == ""
        assert result["album"] == ""
        assert result["genre"] == ""
        assert result["bpm"] == 0
        assert result["key"] == ""

        # 無効なBPM値
        invalid_bpm_track = Mock()
        invalid_bpm_track.Title = "Invalid BPM Track"
        invalid_bpm_track.BPM = "invalid"
        invalid_bpm_track.Artist = None
        invalid_bpm_track.Album = None
        invalid_bpm_track.Genre = None
        invalid_bpm_track.Key = None
        invalid_bpm_track.Rating = None
        invalid_bpm_track.Comment = None
        invalid_bpm_track.Duration = None
        invalid_bpm_track.Path = None
        invalid_bpm_track.DJPlayCount = None
        invalid_bpm_track.updated_at = None
        
        result = client._format_track_info(invalid_bpm_track)
        assert result["title"] == "Invalid BPM Track"
        assert result["bpm"] == 0 