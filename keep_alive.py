import os
import sys
import requests

def keep_alive():
    # 从 GitHub Secrets 获取环境变量
    cookie = os.getenv("USER_COOKIE")
    bot_id = os.getenv("BOT_ID", "6037") # 默认值 6037

    if not cookie:
        print("❌ 错误: 未设置 USER_COOKIE Secret！")
        sys.exit(1)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": cookie,
        "Referer": "https://anikbothosting.de/my-bots.php"
    }

    # 1. 刷新主控制台页面
    bots_page_url = "https://anikbothosting.de/my-bots.php"
    # 2. 访问具体的 Bot 详情页（模拟真实用户点击进入 Bot 页面）
    bot_detail_url = f"https://anikbothosting.de/bot-details.php?id={bot_id}"

    try:
        print("正在发送保活请求...")
        r1 = requests.get(bots_page_url, headers=headers, timeout=15)
        print(f"访问我的 Bot 列表页响应状态: {r1.status_code}")

        r2 = requests.get(bot_detail_url, headers=headers, timeout=15)
        print(f"访问 Bot [{bot_id}] 详情页响应状态: {r2.status_code}")

        if r1.status_code == 200 and r2.status_code == 200:
            print(f"✅ Bot [{bot_id}] 及账号活跃状态刷新成功！")
        else:
            print("⚠️ 响应状态异常，请检查 GitHub Secrets 中的 USER_COOKIE 是否过期或不完整。")

    except Exception as e:
        print(f"❌ 请求发生异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    keep_alive()
