# HomeSV-Alert

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
その後、 main.py を実行してください。
</details>

# メッセージ

<img width="587" height="196" alt="image" src="https://github.com/user-attachments/assets/610e8ed3-7494-40d2-8a5e-01ff846298cf" />
