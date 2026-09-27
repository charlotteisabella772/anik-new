import os
import sys
from curl_cffi import requests

def keep_alive():
    cookie = os.getenv("USER_COOKIE")
    bot_id = os.getenv("BOT_ID", "6037")

    if not cookie:
        print("❌ 错误: 未设置 USER_COOKIE Secret！")
        sys.exit(1)

    # 模拟真实 Chrome 120 浏览器的完整 Header
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cookie": cookie,
        "referer": "https://anikbothosting.de/my-bots.php",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    bots_page_url = "https://anikbothosting.de/my-bots.php"
    bot_detail_url = f"https://anikbothosting.de/bot-details.php?id={bot_id}"

    try:
        print("正在发送保活请求 (伪装 Chrome 浏览器指纹)...")
        
        # impersonate="chrome120" 可以完美模仿 Chrome 的 TLS/JA3 指纹
        r1 = requests.get(bots_page_url, headers=headers, impersonate="chrome120", timeout=15)
        print(f"访问我的 Bot 列表页响应状态: {r1.status_code}")

        r2 = requests.get(bot_detail_url, headers=headers, impersonate="chrome120", timeout=15)
        print(f"访问 Bot [{bot_id}] 详情页响应状态: {r2.status_code}")

        if r1.status_code == 200 or r2.status_code == 200:
            print(f"✅ Bot [{bot_id}] 状态刷新成功！")
        else:
            print(f"⚠️ 响应异常 ({r2.status_code})，请检查 Cookie 是否包含 cf_clearance 或已经过期。")

    except Exception as e:
        print(f"❌ 请求发生异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    keep_alive()
