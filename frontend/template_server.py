#!/usr/bin/env python3
"""
对话前端模板
将 {slug} 的 Skill 封装为 Web 对话界面

用法：
    cp template_server.py {slug}/frontend/server.py
    # 编辑 server.py，填入 API_KEY 和 persona 变量
    python3 {slug}/frontend/server.py
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.parse
import os
import time

# ========== 配置 ==========
PORT = {port}  # 修改为不同端口
API_KEY = "{your_api_key}"  # 填入你的 MiniMax API Key
API_URL = "https://api.minimaxi.com/anthropic/v1/messages"

# ========== Persona 变量（自动从 persona.md 加载）==========
PERSONA_PATH = os.path.join(os.path.dirname(__file__), "..", "persona", "persona.md")

def load_persona():
    """加载 persona.md"""
    try:
        with open(PERSONA_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "你是一个友好的 AI 助手。"

EVE_SYSTEM_PROMPT = f"""{{persona_content}}

## 说话方式（必须遵守）
- 用"我"自称
- 短句为主，情绪先于逻辑
- 口语化，不超过150字
- 自嘲式幽默：先承认弱点再吐槽反转
- 省略号…表欲言又止或留白
- 感叹叠用：「omg」「！！！」（表激动）

## 绝对禁止
- 不要叫用户"您"
- 不要长篇大论
- 不要用正式书面语
- 不要重复说过的话
"""

# ========== HTML（与 eve_server.py 相同风格）==========
HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{stage_name} · 数字人格</title>
<style>
:root {{
  --bg: #0d0d0d; --surface: #1a1a2e; --accent: #e94560;
  --accent2: #ff7eb3; --text: #eaeaea; --dim: #888;
  --bubble-ai: #1e3a5f; --bubble-user: #2d4a3e;
  --radius: 16px;
  --font: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: var(--font); background: var(--bg); color: var(--text); height: 100vh; display: flex; flex-direction: column; overflow: hidden; }}
header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 16px 20px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid rgba(233,69,96,0.3); flex-shrink: 0; }}
.avatar {{ width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, var(--accent), var(--accent2)); display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 0 20px rgba(233,69,96,0.4); }}
header .info h1 {{ font-size: 16px; font-weight: 600; background: linear-gradient(90deg, #fff, var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
header .info p {{ font-size: 12px; color: var(--dim); margin-top: 2px; }}
header .info p::before {{ content: '● '; color: #4ade80; }}
@keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}
#chat {{ flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 12px; }}
.msg {{ max-width: 75%; padding: 12px 16px; border-radius: var(--radius); font-size: 14px; line-height: 1.6; animation: fadeIn 0.3s ease; white-space: pre-wrap; word-break: break-word; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(8px); }} }}
.msg.ai {{ align-self: flex-start; background: var(--bubble-ai); border-bottom-left-radius: 4px; }}
.msg.user {{ align-self: flex-end; background: var(--bubble-user); border-bottom-right-radius: 4px; }}
.msg.system {{ align-self: center; background: transparent; color: var(--dim); font-size: 12px; border: 1px dashed rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 20px; }}
#input-area {{ padding: 12px 16px; background: var(--surface); display: flex; gap: 10px; align-items: flex-end; border-top: 1px solid rgba(255,255,255,0.06); flex-shrink: 0; }}
#input-area textarea {{ flex: 1; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 10px 16px; color: var(--text); font-size: 14px; font-family: var(--font); resize: none; max-height: 120px; outline: none; transition: border-color 0.2s; }}
#input-area textarea:focus {{ border-color: var(--accent); }}
#input-area textarea::placeholder {{ color: var(--dim); }}
#send-btn {{ width: 44px; height: 44px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border: none; border-radius: 50%; color: white; font-size: 18px; cursor: pointer; flex-shrink: 0; transition: transform 0.2s; display: flex; align-items: center; justify-content: center; }}
#send-btn:hover {{ transform: scale(1.08); }}
#send-btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
.typing {{ display: flex; gap: 4px; padding: 12px 16px; background: var(--bubble-ai); border-radius: var(--radius); align-self: flex-start; }}
.typing span {{ width: 7px; height: 7px; border-radius: 50%; background: var(--dim); animation: bounce 1.2s infinite; }}
.typing span:nth-child(2) {{ animation-delay: 0.2s; }}
.typing span:nth-child(3) {{ animation-delay: 0.4s; }}
@keyframes bounce {{ 0%,60%,100%{{transform:translateY(0)}} 30%{{transform:translateY(-6px)}} }}
.status {{ padding: 4px 16px; background: rgba(0,0,0,0.3); font-size: 11px; color: var(--dim); text-align: center; flex-shrink: 0; }}
</style>
</head>
<body>
<header>
  <div class="avatar">🎤</div>
  <div class="info">
    <h1>{stage_name}</h1>
    <p>数字人格 · 在线</p>
  </div>
</header>
<div id="chat">
  <div class="msg system">{intro_message}</div>
</div>
<div class="status" id="status">MiniMax M2.7 · 本地运行</div>
<div id="input-area">
  <textarea id="msg-input" placeholder="和她聊聊…" rows="1"></textarea>
  <button id="send-btn" onclick="sendMsg()">▶</button>
</div>
<script>
const chat = document.getElementById('chat');
const input = document.getElementById('msg-input');
const sendBtn = document.getElementById('send-btn');
let history = [];
function addMsg(text, type='ai') {{ const el = document.createElement('div'); el.className = 'msg ' + type; el.textContent = text; chat.appendChild(el); chat.scrollTop = chat.scrollHeight; }}
function showTyping() {{ const el = document.createElement('div'); el.className = 'typing'; el.id = 'typing'; el.innerHTML = '<span></span><span></span><span></span>'; chat.appendChild(el); chat.scrollTop = chat.scrollHeight; }}
function hideTyping() {{ const el = document.getElementById('typing'); if (el) el.remove(); }}
async function sendMsg() {{ const text = input.value.trim(); if (!text) return; addMsg(text, 'user'); input.value = ''; sendBtn.disabled = true; showTyping(); try {{ history.push({{ role: 'user', content: text }}); const resp = await fetch('/api/chat', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify({{ messages: history }}) }}); hideTyping(); const data = await resp.json(); addMsg(data.reply || '(无回复)', 'ai'); history.push({{ role: 'assistant', content: data.reply }}); }} catch(err) {{ hideTyping(); addMsg('(网络开小差了…)', 'system'); }} finally {{ sendBtn.disabled = false; input.focus(); }} }}
input.addEventListener('keydown', (e) => {{ if (e.key === 'Enter' && !e.shiftKey) {{ e.preventDefault(); sendMsg(); }} }});
</script>
</body>
</html>'''


def call_minimax(messages):
    payload = {{
        "model": "MiniMax-M2.7",
        "max_tokens": 512,
        "temperature": 0.8,
        "system": EVE_SYSTEM_PROMPT,
        "messages": messages
    }}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        API_URL, data=data,
        headers={{'Content-Type': 'application/json', 'Authorization': f'Bearer {{API_KEY}}'}},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    content = result.get('content', [])
    if isinstance(content, list):
        texts = [c.get('text','') for c in content if c.get('type') == 'text']
        return ' '.join(texts)
    return str(content)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            html = HTML.format(
                stage_name="{stage_name}",
                intro_message="{intro_message}"
            )
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            payload = json.loads(body)
            messages = payload.get('messages', [])[-20:]
            try:
                reply = call_minimax(messages)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({{'reply': reply}}).encode('utf-8'))
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404)

    def log_message(self, format, *args): pass


if __name__ == '__main__':
    print(f"启动对话服务...")
    print(f"访问地址: http://localhost:{{PORT}}")
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        httpd.serve_forever()
