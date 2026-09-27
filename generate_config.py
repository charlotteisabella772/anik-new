import sys
import os
import json
import base64
import urllib.parse

def generate_singbox_config():
    node = os.getenv('V2RAY_NODE', '').strip()
    if not node:
        print("⚠️ 未检测到 V2RAY_NODE 变量，跳过配置生成。")
        sys.exit(0)

    outbound = None

    # 解析 VMess 节点
    if node.startswith('vmess://'):
        b64_data = node[8:]
        # 补全 base64 padding
        b64_data += '=' * (-len(b64_data) % 4)
        info = json.loads(base64.b64decode(b64_data).decode('utf-8'))

        outbound = {
            'type': 'vmess',
            'tag': 'proxy',
            'server': info['add'],
            'server_port': int(info['port']),
            'uuid': info['id'],
            'security': info.get('scy', 'auto'),
            'alter_id': int(info.get('aid', 0))
        }
        if info.get('net') == 'ws':
            outbound['transport'] = {
                'type': 'ws',
                'path': info.get('path', '/'),
                'headers': {'Host': info.get('host', info['add'])}
            }
        if info.get('tls') == 'tls':
            outbound['tls'] = {
                'enabled': True,
                'server_name': info.get('host', info['add']),
                'insecure': True
            }

    # 解析 VLESS 节点
    elif node.startswith('vless://'):
        url = urllib.parse.urlparse(node)
        query = urllib.parse.parse_qs(url.query)
        outbound = {
            'type': 'vless',
            'tag': 'proxy',
            'server': url.hostname,
            'server_port': url.port,
            'uuid': url.username,
            'flow': query.get('flow', [''])[0]
        }
        if query.get('type', [''])[0] == 'ws':
            outbound['transport'] = {
                'type': 'ws',
                'path': query.get('path', ['/'])[0],
                'headers': {'Host': query.get('host', [url.hostname])[0]}
            }
        if query.get('security', [''])[0] in ['tls', 'reality']:
            outbound['tls'] = {
                'enabled': True,
                'server_name': query.get('sni', [url.hostname])[0],
                'insecure': True
            }

    if outbound:
        config = {
            'inbounds': [{
                'type': 'socks',
                'tag': 'socks-in',
                'listen': '127.0.0.1',
                'listen_port': 10808
            }],
            'outbounds': [outbound]
        }

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print('✅ config.json 配置文件成功生成！')
    else:
        print("❌ 无法解析该节点格式，仅支持 vmess:// 和 vless:// 节点。")
        sys.exit(1)

if __name__ == '__main__':
    generate_singbox_config()
