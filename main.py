import os
import json
import aiohttp
import asyncio
import datetime
from ping3 import ping
from dotenv import load_dotenv
from gpiozero import OutputDevice

# Load .env file
load_dotenv()
HOSTS_STR = os.getenv("HOSTS")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
HOSTS = [host.strip() for host in HOSTS_STR.split(",")] # カンマ区切りで複数のホストをリストに変換＆空白除去

# GPIO define
RELAY01 = 2
RELAY02 = 3

# Relay define
relay01 = OutputDevice(RELAY01, active_high=False)
relay02 = OutputDevice(RELAY02, active_high=False)

# Discord通知関数
async def send_discord_notification(down_hosts):
    if not WEBHOOK_URL:
        print("WEBHOOK_URL is not set. Skipping Discord notification.")
        return

    if down_hosts:
        title = "Down alert!"
        description = "Some hosts have gone offline"
    
    # Discord通知本文
    payload = {
        "username": "HomeSV-Alert",
        "avatar_url": "https://raw.githubusercontent.com/yukugura/homesv-alert/refs/heads/main/icon.png",
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": 0xFF0000, # 赤色
                "fields": [
                    {
                        "name": "Hosts",
                        "value": f"{', '.join(down_hosts)}",
                        "inline": False
                    }
                ],
                "timestamp": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=payload) as response:
            if response.status == 204:
                print("Discord通知が送信されました。")
            else:
                print(f"Discord通知の送信に失敗しました。ステータスコード: {response.status}")

# hostがアクティブかどうかを確認する関数
async def is_active(host):
    try:
        # pingコマンドを実行
        response_time = await asyncio.to_thread(ping, host, timeout=1)
        return response_time is not False and response_time is not None
    except Exception as e:
        print(f"pingエラー: {host} - {e}")
        return False

# 指定したhostにpingを送信し失敗した場合、リトライする関数
async def is_host_up_with_retry(host, max_retry=5):
    for i in range(max_retry + 1):
        if await is_active(host):
            # ping成功時
            return True
        else:
            # ping失敗時
            if i < max_retry:
                await asyncio.sleep(1)  # 1秒待ってからリトライ
    return False

# リレー制御関数
def control_relay(state):
    if state == 'green':
        relay01.off()
        relay02.off()
    elif state == 'yellow':
        relay01.on()
        relay02.off()
    elif state == 'red':
        relay01.on()
        relay02.on()
    else:
        print("Invalid state. Use 'green', 'yellow', or 'red'.")
        return False
    return True

# メイン関数
async def main():
    # 機器を監視するメインループ
    print("ネットワーク監視プログラムを開始します。Ctrl + Cで停止します。")
    print(f"監視対象ホスト: {', '.join(HOSTS)}")
    try:
        while True:
            tasks = [is_host_up_with_retry(host) for host in HOSTS]
            results = await asyncio.gather(*tasks)

            # 状態判定
            all_ok = all(results)
            any_down = not all_ok and any(not res for res in results)

            if all_ok:
                # すべてのホストがアクティブな場合
                control_relay('green')
            elif any_down:
                # いずれかのホストが非アクティブな場合
                control_relay('red')
                down_hosts = [HOSTS[i] for i, res in enumerate(results) if not res]
                await send_discord_notification(down_hosts)
                print(f"いくつかのホストがダウンしています: {', '.join(down_hosts)}")
            else:
                # すべてのホストが非アクティブな場合
                control_relay('red')
                print("すべてのホストがダウンしています！")
            await asyncio.sleep(CHECK_INTERVAL)

    except asyncio.CancelledError:
        print("ネットワーク監視プログラムを停止します。")
        control_relay('yellow')  # 停止時にリレーをOFFにする
    finally:
        control_relay('green')  # 停止時にリレーをOFFにする

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("プログラムがユーザーによって中断されました。")