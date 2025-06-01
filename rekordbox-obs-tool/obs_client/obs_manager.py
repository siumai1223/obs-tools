from obswebsocket import obsws, requests
import logging

class OBSManager:
    """OBS WebSocket接続とテキスト更新を管理するクラス"""
    
    def __init__(self, config):
        """
        Args:
            config: 設定情報を含む辞書
        """
        self.config = config
        self.obs = None
        self.connected = False
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        """OBSに接続"""
        try:
            self.logger.info(f"OBSへの接続を試みています... (host: {self.config['host']}, port: {self.config['port']})")
            self.obs = obsws(
                host=self.config["host"],
                port=self.config["port"],
                password=self.config["password"]
            )
            self.logger.info("WebSocketクライアントを作成しました。接続を開始します...")
            self.obs.connect()
            self.connected = True
            self.logger.info("OBSに正常に接続しました。")
            self._log_obs_info()
        except Exception as e:
            self.connected = False
            self.logger.error(f"OBSへの接続に失敗しました: {str(e)}")
            raise Exception(f"OBSへの接続に失敗しました: {str(e)}")
    
    def disconnect(self):
        """OBSから切断"""
        if self.obs:
            self.obs.disconnect()
            self.connected = False
            self.logger.info("OBSから切断しました。")
    
    def update_text(self, text):
        """テキストソースを更新"""
        if not self.connected:
            self.logger.warning("OBSに接続されていません。テキスト更新をスキップします。")
            return
        
        try:
            # まず、SetInputSettings を試す
            response = self.obs.call(requests.SetInputSettings(
                inputName=self.config["source_name"],
                inputSettings={"text": text}
            ))
            self.logger.debug(f"テキストソースを更新しました: {text}")
            return response
        except Exception as e:
            self.logger.error(f"SetInputSettings でのエラー: {type(e).__name__} - {str(e)}")
            try:
                # 失敗した場合は、SetTextFreetype2Properties を試す
                response = self.obs.call(requests.SetTextFreetype2Properties(
                    source=self.config["source_name"],
                    text=text
                ))
                self.logger.debug(f"テキストソースを更新しました（Freetype2）: {text}")
                return response
            except Exception as e:
                self.logger.error(f"SetTextFreetype2Properties でのエラー: {type(e).__name__} - {str(e)}")
                try:
                    # 最後の手段として、SetSourceSettings を試す
                    response = self.obs.call(requests.SetSourceSettings(
                        sourceName=self.config["source_name"],
                        sourceSettings={"text": text}
                    ))
                    self.logger.debug(f"テキストソースを更新しました（SourceSettings）: {text}")
                    return response
                except Exception as e:
                    self.logger.error(f"SetSourceSettings でのエラー: {type(e).__name__} - {str(e)}")
                    return None
    
    def _log_obs_info(self):
        """OBSの情報をログに出力"""
        try:
            # 利用可能なソースの一覧を取得
            scenes = self.obs.call(requests.GetSceneList())
            self.logger.info("\n利用可能なシーン:")
            for scene in scenes.getScenes():
                self.logger.info(f"シーン: {scene['sceneName']}")
                
            try:
                # 現在のシーンのソース一覧を取得
                current_scene = scenes.getCurrentScene()
                if current_scene:
                    sources = self.obs.call(requests.GetSceneItemList(sceneName=current_scene))
                    self.logger.info(f"\n現在のシーン '{current_scene}' のソース一覧:")
                    for source in sources.getSceneItems():
                        self.logger.info(f"ソース: {source['sourceName']}, 種類: {source.get('sourceKind', '不明')}")
                else:
                    self.logger.warning("現在のシーンが取得できませんでした。")
            except Exception as e:
                self.logger.warning(f"現在のシーン情報の取得に失敗: {str(e)}")

            # テキストソースの情報を取得
            try:
                source_settings = self.obs.call(requests.GetInputSettings(
                    inputName=self.config["source_name"]
                ))
                self.logger.info(f"\nテキストソース '{self.config['source_name']}' の設定:")
                self.logger.info(source_settings)
            except Exception as e:
                self.logger.error(f"\nテキストソース情報の取得に失敗: {str(e)}")
        except Exception as e:
            self.logger.error(f"OBS情報の取得に失敗: {str(e)}") 