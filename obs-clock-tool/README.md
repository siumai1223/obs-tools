# OBS Clock Tool

OBS Studio用のカスタマイズ可能な時計表示ツールです。GUIインターフェースでリアルタイムに時計の表示をカスタマイズし、OBS Studioに反映することができます。

## 機能

- リアルタイムな時刻表示
  - 時刻のみ表示（HH:MM:SS）
  - 日付と時刻の表示（YYYY-MM-DD HH:MM:SS）
- GUIによる表示カスタマイズ
  - フォント選択（Arial、Times New Roman、Helvetica）
  - フォントサイズ調整（12pt-72pt）
  - 日付表示の切り替え
- OBS Studio連携
  - テキストソースのリアルタイム更新
  - フォント設定の同期
- プレビュー機能
  - 設定変更のリアルタイムプレビュー
  - 開始/停止制御

## 必要条件

- Python 3.8以上
- OBS Studio 28.0.0以上（obs-websocket 5.0.0以上）
- 必要なPythonパッケージ：
  - PyQt5 5.15.9
  - obs-websocket-py 1.0.0
  - python-dateutil 2.8.2
  - pytz 2024.1

## インストール方法

1. リポジトリをクローンまたはダウンロードします
2. 必要なパッケージをインストールします：
   ```
   pip install -r requirements.txt
   ```

## 初期設定

### OBS Studioの設定

1. OBS Studioを起動します
2. メニューから「ツール」→「WebSocket Server Settings」を開きます
3. 以下の設定を行います：
   - 「Enable WebSocket server」にチェック
   - Server Port: 4455（デフォルト）
   - パスワードを設定（任意）
4. 「Apply」→「OK」をクリックします
5. シーンに新しいテキストソース（GDI+）を追加：
   - ソース名を「Clock」に設定（変更する場合はconfig.jsonも更新）
   - 「OK」をクリックして作成

### アプリケーションの設定

1. `config.json`を編集します：
   ```json
   {
       "obs": {
           "host": "localhost",
           "port": 4455,
           "password": "your_password_here"  // OBSで設定したパスワード
       },
       "display": {
           "source_name": "Clock",  // OBSのテキストソース名
           "format": "%H:%M:%S",
           "date_format": "%Y-%m-%d",
           "update_interval": 1.0,
           "font": "Arial",
           "font_size": 48,
           "show_date": false
       }
   }
   ```

## 使用方法

1. アプリケーションを起動します：
   ```
   python src/main.py
   ```

2. GUIウィンドウの操作：
   - **プレビュー**: 現在の設定での表示をリアルタイムで確認
   - **設定**:
     - フォント: ドロップダウンから選択
     - サイズ: スピンボックスで調整（12-72pt）
     - 日付表示: チェックボックスでオン/オフ
   - **コントロール**:
     - 開始: 時計の更新を開始
     - 停止: 時計の更新を停止

3. OBS Studioでの表示：
   - 追加したテキストソースに時計が表示されます
   - GUIでの設定変更が即座に反映されます

## トラブルシューティング

### 1. OBS接続エラー

#### 症状
- "Empty response to Identify, password may be incorrect"というエラーメッセージ
- OBSへの接続が失敗する

#### 解決方法
1. OBS Studioが起動しているか確認
2. WebSocketサーバーの設定を確認：
   - ツール → WebSocket Server Settings
   - Enable WebSocket serverがチェックされているか
   - パスワードが`config.json`の設定と一致しているか
3. ポート番号（4455）が他のアプリケーションと競合していないか確認

### 2. テキストソースの更新エラー

#### 症状
- テキストソースが更新されない
- "SetInputSettings failed"などのエラーメッセージ

#### 解決方法
1. テキストソースの設定を確認：
   - ソースが「テキスト (GDI+)」として作成されているか
   - ソース名が正確に`config.json`の`source_name`と一致しているか
2. テキストソースを再作成：
   - 既存のソースを削除
   - 新しいテキストソース（GDI+）を作成
   - 名前を「Clock」に設定

### 3. フォント関連の問題

#### 症状
- フォントが正しく表示されない
- フォント設定が反映されない

#### 解決方法
1. システムにフォントがインストールされているか確認
2. OBS Studioでフォントが使用可能か確認
3. フォント名が正確に一致しているか確認

## 技術的な注意点

### OBS WebSocket APIの利用

本ツールはOBS WebSocket APIを使用してOBS Studioと通信します。APIの仕様により、以下の点に注意が必要です：

1. テキスト更新の方法
   - 複数のAPI呼び出し方法（SetInputSettings, SetTextGDIPlusProperties, SetSourceSettings）
   - 環境によって動作する方法が異なる可能性
   - エラーハンドリングと再試行メカニズムの実装

2. 接続管理
   - 接続状態の監視
   - 自動再接続機能
   - エラー時のフォールバック動作

3. パフォーマンス考慮
   - 更新間隔の適切な設定
   - 不要な更新の防止
   - エラー時のリソース解放

## ライセンス

MIT License

## 開発者向け情報

### 既知の問題と対処法

1. OBS WebSocket APIのバージョン互換性
   - 異なるバージョンのOBSで動作が異なる可能性
   - APIメソッドの可用性の確認が必要
   - 複数の更新メソッドをフォールバックとして実装

2. テキストソース更新の信頼性
   - 更新コマンドが失敗する可能性
   - 複数の更新方法を試行
   - エラーログの詳細な記録

3. 設定の永続化
   - 設定変更の保存機能
   - 設定ファイルの検証
   - エラー時のデフォルト値の使用

## プロジェクト構造

```
obs-clock-tool/
├── src/
│   ├── config/
│   │   └── config_manager.py  # 設定ファイルの管理
│   ├── obs_client/
│   │   └── obs_manager.py     # OBS WebSocket通信の管理
│   ├── gui/
│   │   └── clock_window.py    # メインウィンドウのGUI
│   └── main.py               # アプリケーションのエントリーポイント
├── config.json              # アプリケーション設定ファイル
├── requirements.txt        # 依存パッケージリスト
└── README.md              # ドキュメント
```

## コードの説明

### メインモジュール

- `main.py`: アプリケーションのエントリーポイント。各コンポーネントの初期化と接続を行う。

### 設定管理

- `config_manager.py`:
  - `ConfigManager`: 設定ファイルの読み込みと管理を行うクラス
  - `load_config()`: 設定ファイルを読み込む
  - `obs_config`: OBS接続設定を取得するプロパティ
  - `display_config`: 表示設定を取得するプロパティ

### OBS通信

- `obs_manager.py`:
  - `OBSManager`: OBS WebSocket接続とテキスト更新を管理するクラス
  - `connect()`: OBSに接続
  - `disconnect()`: OBSから切断
  - `update_text()`: テキストソースを更新
  - `_log_obs_info()`: OBSの情報をログに出力

### GUI

- `clock_window.py`:
  - `ClockWindow`: メインウィンドウのGUIクラス
  - `setup_ui()`: UIの初期設定
  - `update_time()`: 時間表示を更新
  - `update_preview()`: プレビュー表示を更新
  - `start_timer()`: タイマーを開始
  - `stop_timer()`: タイマーを停止

## 主要な機能と対応するコード

1. 設定管理
   - 設定ファイルの読み込み: `ConfigManager.load_config()`
   - 設定値の取得: `ConfigManager.obs_config`, `ConfigManager.display_config`

2. OBS連携
   - 接続管理: `OBSManager.connect()`, `OBSManager.disconnect()`
   - テキスト更新: `OBSManager.update_text()`
   - 情報取得: `OBSManager._log_obs_info()`

3. GUI操作
   - 時計表示: `ClockWindow.update_time()`
   - 設定反映: `ClockWindow.update_preview()`
   - タイマー制御: `ClockWindow.start_timer()`, `ClockWindow.stop_timer()` 