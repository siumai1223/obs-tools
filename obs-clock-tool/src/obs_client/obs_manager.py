from obswebsocket import obsws, requests

class OBSManager:
    """OBS WebSocket接続とテキスト更新を管理するクラス"""
    
    def __init__(self, config):
        """
        Args:
            config: ConfigManagerインスタンス
        """
        self.config = config
        self.obs = None
        self.connected = False
    
    def connect(self):
        """OBSに接続"""
        try:
            print(f"OBSへの接続を試みています... (host: {self.config.obs_config['host']}, port: {self.config.obs_config['port']})")
            self.obs = obsws(
                host=self.config.obs_config["host"],
                port=self.config.obs_config["port"],
                password=self.config.obs_config["password"]
            )
            print("WebSocketクライアントを作成しました。接続を開始します...")
            self.obs.connect()
            self.connected = True
            print("OBSに正常に接続しました。")
            self._log_obs_info()
        except Exception as e:
            self.connected = False
            raise Exception(f"OBSへの接続に失敗しました: {str(e)}")
    
    def disconnect(self):
        """OBSから切断"""
        if self.obs:
            self.obs.disconnect()
            self.connected = False
    
    def update_text(self, text):
        """テキストソースを更新"""
        if not self.connected:
            return
        
        try:
            # まず、SetInputSettings を試す
            response = self.obs.call(requests.SetInputSettings(
                inputName=self.config.display_config["source_name"],
                inputSettings={"text": text}
            ))
            return response
        except Exception as e:
            print(f"SetInputSettings でのエラー: {type(e).__name__} - {str(e)}")
            try:
                # 失敗した場合は、SetTextFreetype2Properties を試す
                response = self.obs.call(requests.SetTextFreetype2Properties(
                    source=self.config.display_config["source_name"],
                    text=text
                ))
                return response
            except Exception as e:
                print(f"SetTextFreetype2Properties でのエラー: {type(e).__name__} - {str(e)}")
                try:
                    # 最後の手段として、SetSourceSettings を試す
                    response = self.obs.call(requests.SetSourceSettings(
                        sourceName=self.config.display_config["source_name"],
                        sourceSettings={"text": text}
                    ))
                    return response
                except Exception as e:
                    print(f"SetSourceSettings でのエラー: {type(e).__name__} - {str(e)}")
                    return None
    
    def _log_obs_info(self):
        """OBSの情報をログに出力"""
        try:
            # 利用可能なソースの一覧を取得
            scenes = self.obs.call(requests.GetSceneList())
            print("\n利用可能なシーン:")
            for scene in scenes.getScenes():
                print(f"シーン: {scene['sceneName']}")
                
            # 現在のシーンのソース一覧を取得
            current_scene = scenes.getCurrentScene()
            sources = self.obs.call(requests.GetSceneItemList(sceneName=current_scene))
            print(f"\n現在のシーン '{current_scene}' のソース一覧:")
            for source in sources.getSceneItems():
                print(f"ソース: {source['sourceName']}, 種類: {source.get('sourceKind', '不明')}")

            # テキストソースの情報を取得
            try:
                source_settings = self.obs.call(requests.GetInputSettings(
                    inputName=self.config.display_config["source_name"]
                ))
                print(f"\nテキストソース '{self.config.display_config['source_name']}' の設定:")
                print(source_settings)
            except Exception as e:
                print(f"\nテキストソース情報の取得に失敗: {str(e)}")
        except Exception as e:
            print(f"OBS情報の取得に失敗: {str(e)}") 