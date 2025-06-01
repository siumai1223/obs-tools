import os
import sys
import sqlite3
from sqlalchemy import inspect

# プロジェクトルートをPythonパスに追加
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from rekordbox_client.rekordbox_client import RekordboxClient
import json
import logging
from datetime import datetime, timedelta

# ロガーの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def inspect_track_details(track):
    """トラック情報の詳細を調査"""
    details = []
    for attr in dir(track):
        if not attr.startswith('_'):  # プライベート属性を除外
            try:
                value = getattr(track, attr)
                details.append(f"{attr}: {value}")
            except Exception as e:
                details.append(f"{attr}: [Error: {e}]")
    return details

def inspect_database_structure(client):
    """データベースの構造を調査"""
    results = []
    results.append("\n=== データベーステーブル一覧 ===")
    
    try:
        # SQLAlchemyのインスペクターを使用
        inspector = inspect(client.db._connection.engine)
        
        # テーブル一覧を取得
        tables = inspector.get_table_names()
        
        for table_name in tables:
            results.append(f"\nテーブル: {table_name}")
            
            # テーブルの構造を取得
            columns = inspector.get_columns(table_name)
            results.append(f"{table_name}テーブルの構造:")
            for column in columns:
                col_name = column['name']
                col_type = str(column['type'])
                is_nullable = "NULL" if column.get('nullable', True) else "NOT NULL"
                is_pk = "PRIMARY KEY" if column.get('primary_key', False) else ""
                results.append(f"  - {col_name} ({col_type}) {is_nullable} {is_pk}".strip())
            
            # インデックス情報を取得
            indexes = inspector.get_indexes(table_name)
            if indexes:
                results.append("\nインデックス:")
                for index in indexes:
                    results.append(f"  - {index['name']}: {', '.join(index['column_names'])}")
            
            # 外部キー情報を取得
            foreign_keys = inspector.get_foreign_keys(table_name)
            if foreign_keys:
                results.append("\n外部キー:")
                for fk in foreign_keys:
                    results.append(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
            
            # レコード数を取得
            try:
                count = client.db._connection.execute(f"SELECT COUNT(*) FROM {table_name}").scalar()
                results.append(f"\nレコード数: {count}")
            except Exception as e:
                results.append(f"レコード数の取得に失敗: {e}")
            
            results.append("")
            
    except Exception as e:
        results.append(f"テーブル情報の取得に失敗: {e}")
        logger.exception("データベース構造の取得中にエラー:")
    
    return results

def test_database_inspection():
    """Rekordboxデータベースの詳細な調査を行う"""
    client = RekordboxClient()
    results = []
    
    results.append("Rekordbox Database Debug")
    results.append("=======================")
    
    assert client.connect(), "データベース接続に失敗"

    try:
        # データベースから直接コンテンツを取得
        content = list(client.db.get_content())  # イテレータをリストに変換
        results.append(f"\n取得したトラック総数: {len(content)}")

        # 最近更新された曲を探す
        recent_tracks = []
        for track in content:
            if hasattr(track, 'updated_at') and track.updated_at:
                # 過去24時間以内の曲を対象に
                if track.updated_at > datetime.now() - timedelta(days=1):
                    recent_tracks.append(track)

        results.append(f"\n過去24時間以内に更新された曲数: {len(recent_tracks)}")
        
        if recent_tracks:
            results.append("\n=== 最近更新された曲の詳細 ===")
            for i, track in enumerate(sorted(recent_tracks, key=lambda x: x.updated_at, reverse=True)[:5], 1):
                results.append(f"\n--- 曲 {i} ---")
                results.append(f"タイトル: {track.Title}")
                results.append(f"アーティスト: {track.Artist.Name if hasattr(track.Artist, 'Name') else 'N/A'}")
                results.append(f"更新日時: {track.updated_at}")
                results.append(f"解析状態: {track.Analysed if hasattr(track, 'Analysed') else 'N/A'}")
                results.append(f"再生回数: {track.DJPlayCount if hasattr(track, 'DJPlayCount') else 'N/A'}")
                results.append(f"最終再生: {track.LastPlayed if hasattr(track, 'LastPlayed') else 'N/A'}")
                
                # 詳細な属性情報を取得
                results.append("\n=== トラック詳細情報 ===")
                details = inspect_track_details(track)
                results.extend(details)

        # データベース構造の調査
        results.extend(inspect_database_structure(client))

    except Exception as e:
        results.append(f"データ取得中にエラーが発生: {e}")
        logger.exception("詳細なエラー情報:")

    finally:
        client.close()
        results.append("\nデバッグ完了")
        
    return results

if __name__ == "__main__":
    # テストを実行
    results = test_database_inspection()
    
    # 結果をファイルに保存
    output_file = os.path.join(project_root, "database_inspection_results.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    
    # 結果を画面にも表示
    print("\n".join(results)) 