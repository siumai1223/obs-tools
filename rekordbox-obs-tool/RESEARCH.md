# Rekordbox Database Research

## Phase 1: 調査・設計フェーズ

### 1. rekordboxの曲情報取得方法の調査

#### データベースの仕様
- rekordbox 7は暗号化されたSQLite3データベースを使用
- SQLCipher4で暗号化されている
- データベースファイルの場所: `C:\Users\[ユーザー名]\AppData\Roaming\Pioneer\rekordbox\master.db`

#### データベースの暗号化
1. **暗号化方式**: SQLCipher4
2. **キーの取得方法**:
   - Fridaを使用してプロセスメモリから直接取得
   - pyrekordboxライブラリを使用して自動的に取得
   - rekordlocksmithツールを使用して取得

#### 推奨実装方法
- **選定ライブラリ**: pyrekordbox
- **選定理由**:
  - rekordbox 7に対応
  - データベースの暗号化キーを自動的に取得
  - データベース構造が整理されている
  - Pythonネイティブのライブラリ

### 2. OBS WebSocket APIの調査
- OBS 28.0.0以降では標準でWebSocket APIが組み込み済み
- デフォルトポート: 4455

### 次のステップ
1. pyrekordboxを使用したデータベースアクセスの実装
2. 必要なテーブルとカラムの特定
3. OBS WebSocket APIとの連携実装 