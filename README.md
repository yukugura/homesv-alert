# HomeSV-Alert

対象機器に対して ping を使用して定期的に死活監視を行います。  
５回連続で失敗した場合、ダウン状態だと判断し指定のURLにDiscord-Webhookを送信します。

# リリース
すべてのリリースは以下の場所にあります。

・github：https://github.com/yukugura/homesv-alert/releases/

# 動作環境
### RaspberryPi4 ModelB 8

# How to setup

<details>
<summary>手順 １ [.envファイルの初期設定]</summary>
プロジェクトを実行するには、環境変数の設定が必要です。`.env.sample`ファイルをコピーし、`.env`という名前で保存してください。  
その後、 `CHECK_INTERVAL` `WEBHOOK_URL` `HOSTS` の３つを変更して上書きしてください。

<summary>  </summary>

</details>

<details>
<summary>手順 ２ [ボット・サーバーのセットアップ]</summary>

Pythonインストール後、ライブラリをインストールします。仮想環境での運用をおすすめします。  
```
pip install python-dotenv
```  
```
pip install aiohttp
```  
```
pip install ping3
```
```
pip install lgpio
```  
その後、 main.py を実行してください。
</details>

# メッセージ

<img width="587" height="196" alt="image" src="https://github.com/user-attachments/assets/610e8ed3-7494-40d2-8a5e-01ff846298cf" />
