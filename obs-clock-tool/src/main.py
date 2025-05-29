import sys
from PyQt5.QtWidgets import QApplication
from config.config_manager import ConfigManager
from obs_client.obs_manager import OBSManager
from gui.clock_window import ClockWindow

def main():
    """アプリケーションのメインエントリーポイント"""
    app = QApplication(sys.argv)
    
    # 各マネージャーの初期化
    config_manager = ConfigManager()
    obs_manager = OBSManager(config_manager)
    
    # メインウィンドウの作成と表示
    window = ClockWindow(config_manager, obs_manager)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 