import os
import sys
import socket
from curl_cffi import requests

def check_socks5_open(host="127.0.0.1", port=10808):
    """检测本地 SOCKS5 代理端口是否就绪"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def keep_alive():
    cookie = os.getenv("USER_COOKIE")
    bot_id = os.getenv("BOT_ID", "6037")
    proxy_url = os.getenv("PROXY_URL", "socks5://127.0.0.1:10808")

    if not cookie:
        print("❌ 错误: 未在 GitHub Secrets 中设置 USER_COOKIE！")
        sys.exit(1)

    # 自动检测本地代理是否在线
    proxies = None
    if check_socks5_open("127.0.0.1", 10808):
        print("🌐 检测到 sing-box 本地 SOCKS5 代理处于激活状态，将通过代理连接...")
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
    else:
        print("⚠️ 本地 SOCKS5 代理未启动，将直接使用 GitHub 直连发起请求...")

    # 伪装 Chrome 120 浏览器标头
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

    bots_page_url = "https://anikbothosting.de/"
    bot_detail_url = f"https://anikbothosting.de/bot-details.php?id={bot_id}"

    try:
        print("🚀 正在发送保活请求 (伪装 Chrome 120 TLS 指纹)...")

        # 请求 1: 访问 Bot 列表主页
        r1 = requests.get(
            bots_page_url,
            headers=headers,
            impersonate="chrome120",
            proxies=proxies,
            timeout=20
        )
        print(f"访问我的 Bot 列表页响应状态: {r1.status_code}")

        # 请求 2: 访问具体 Bot 详情页刷新活跃状态
        r2 = requests.get(
            bot_detail_url,
            headers=headers,
            impersonate="chrome120",
            proxies=proxies,
            timeout=20
        )
        print(f"访问 Bot [{bot_id}] 详情页响应状态: {r2.status_code}")

        if r1.status_code == 200 or r2.status_code == 200:
            print(f"✅ Bot [{bot_id}] 活跃状态成功刷新！已成功防止 4 天闲置删除。")
        elif r1.status_code == 403 or r2.status_code == 403:
            print("❌ 返回 403 Forbidden: 节点 IP 同样被 Cloudflare 拦截，或 Cookie 已失效。建议尝试更换节点或更新 Cookie。")
            sys.exit(1)
        else:
            print(f"⚠️ 响应状态码异常 ({r2.status_code})，请检查 BOT_ID 或 Cookie 是否正确。")

    except Exception as e:
        print(f"❌ 请求发生网络异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    keep_alive()
