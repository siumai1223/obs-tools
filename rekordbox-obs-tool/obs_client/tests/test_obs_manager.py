import pytest
from unittest.mock import Mock, patch
from obs_client.obs_manager import OBSManager

@pytest.fixture
def config():
    return {
        "host": "localhost",
        "port": 4455,
        "password": "",
        "source_name": "NowPlaying"
    }

@pytest.fixture
def obs_manager(config):
    return OBSManager(config)

def test_init(obs_manager, config):
    """初期化のテスト"""
    assert obs_manager.config == config
    assert obs_manager.obs is None
    assert obs_manager.connected is False

def test_connect_success(obs_manager):
    """接続成功のテスト"""
    mock_obs = Mock()
    with patch('obs_client.obs_manager.obsws', return_value=mock_obs):
        obs_manager.connect()
        assert obs_manager.connected is True
        assert obs_manager.obs == mock_obs
        mock_obs.connect.assert_called_once()

def test_connect_failure(obs_manager):
    """接続失敗のテスト"""
    with patch('obs_client.obs_manager.obsws', side_effect=Exception("Connection failed")):
        with pytest.raises(Exception) as exc_info:
            obs_manager.connect()
        assert "OBSへの接続に失敗しました" in str(exc_info.value)
        assert obs_manager.connected is False

def test_disconnect(obs_manager):
    """切断のテスト"""
    mock_obs = Mock()
    obs_manager.obs = mock_obs
    obs_manager.connected = True
    
    obs_manager.disconnect()
    assert obs_manager.connected is False
    mock_obs.disconnect.assert_called_once()

def test_update_text_not_connected(obs_manager):
    """未接続時のテキスト更新テスト"""
    assert obs_manager.update_text("test") is None

def test_update_text_success(obs_manager):
    """テキスト更新成功のテスト"""
    mock_obs = Mock()
    obs_manager.obs = mock_obs
    obs_manager.connected = True
    
    obs_manager.update_text("test")
    mock_obs.call.assert_called_once()

def test_update_text_fallback(obs_manager):
    """テキスト更新フォールバックのテスト"""
    mock_obs = Mock()
    mock_obs.call.side_effect = [
        Exception("First method failed"),
        Exception("Second method failed"),
        Mock()  # 3番目の方法は成功
    ]
    obs_manager.obs = mock_obs
    obs_manager.connected = True
    
    result = obs_manager.update_text("test")
    assert result is not None
    assert mock_obs.call.call_count == 3 