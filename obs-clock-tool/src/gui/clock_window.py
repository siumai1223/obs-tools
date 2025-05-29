from datetime import datetime
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QPushButton, QSpinBox, QComboBox, 
                           QCheckBox, QGroupBox, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class ClockWindow(QMainWindow):
    """メインウィンドウのGUIクラス"""
    
    def __init__(self, config_manager, obs_manager):
        """
        Args:
            config_manager: ConfigManagerインスタンス
            obs_manager: OBSManagerインスタンス
        """
        super().__init__()
        self.config = config_manager
        self.obs_manager = obs_manager
        self.setup_ui()
        
        # OBSに接続
        try:
            self.obs_manager.connect()
        except Exception as e:
            QMessageBox.warning(self, "警告", str(e) + "\n時計の表示のみ続行します。")
    
    def setup_ui(self):
        """UIの初期設定"""
        self.setWindowTitle("OBS Clock Tool")
        self.setMinimumSize(400, 300)
        
        # メインウィジェットとレイアウトの設定
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # プレビュー表示エリア
        preview_group = QGroupBox("プレビュー")
        preview_layout = QVBoxLayout()
        self.preview_label = QLabel("00:00:00")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setFont(QFont(
            self.config.display_config["font"],
            self.config.display_config["font_size"]
        ))
        preview_layout.addWidget(self.preview_label)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # 設定エリア
        settings_group = QGroupBox("設定")
        settings_layout = QVBoxLayout()
        
        # フォント設定
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("フォント:"))
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Times New Roman", "Helvetica"])
        self.font_combo.setCurrentText(self.config.display_config["font"])
        font_layout.addWidget(self.font_combo)
        settings_layout.addLayout(font_layout)
        
        # フォントサイズ設定
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("サイズ:"))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(12, 72)
        self.size_spin.setValue(self.config.display_config["font_size"])
        size_layout.addWidget(self.size_spin)
        settings_layout.addLayout(size_layout)
        
        # 表示オプション
        self.show_date_check = QCheckBox("日付を表示")
        self.show_date_check.setChecked(self.config.display_config["show_date"])
        settings_layout.addWidget(self.show_date_check)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # コントロールエリア
        control_layout = QHBoxLayout()
        self.start_button = QPushButton("開始")
        self.stop_button = QPushButton("停止")
        self.stop_button.setEnabled(False)
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        layout.addLayout(control_layout)
        
        # タイマーの設定
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        
        # ボタンのイベント接続
        self.start_button.clicked.connect(self.start_timer)
        self.stop_button.clicked.connect(self.stop_timer)
        
        # 設定変更のイベント接続
        self.font_combo.currentTextChanged.connect(self.update_preview)
        self.size_spin.valueChanged.connect(self.update_preview)
        self.show_date_check.stateChanged.connect(self.update_preview)
        
        # 初期表示の更新
        self.update_preview()
    
    def update_time(self):
        """時間表示を更新"""
        current_time = datetime.now()
        if self.show_date_check.isChecked():
            time_text = current_time.strftime(
                f"{self.config.display_config['date_format']} {self.config.display_config['format']}"
            )
        else:
            time_text = current_time.strftime(self.config.display_config['format'])
        
        # プレビューの更新
        self.preview_label.setText(time_text)
        
        # OBSのテキストソースを更新
        self.obs_manager.update_text(time_text)
    
    def update_preview(self):
        """プレビュー表示を更新"""
        font = QFont(self.font_combo.currentText(), self.size_spin.value())
        self.preview_label.setFont(font)
        self.update_time()
    
    def start_timer(self):
        """タイマーを開始"""
        self.timer.start(int(self.config.display_config["update_interval"] * 1000))
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
    
    def stop_timer(self):
        """タイマーを停止"""
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    
    def closeEvent(self, event):
        """ウィンドウが閉じられるときの処理"""
        self.obs_manager.disconnect()
        event.accept() 