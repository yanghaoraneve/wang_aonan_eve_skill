#!/usr/bin/env python3
"""
EVE Chat Server - 王澳楠EVE 对话前端
完全本地版本，不依赖OpenClaw Gateway
直接调用MiniMax API + 内置EVE人格
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.parse
import os
import time
import random

# ========== 配置 ==========
PORT = 18799
API_KEY = "sk-cp-pwf2GjLsa96MP1CvYlLQ4v6SFaCZ9ueiaIWR8XeadZz5FkN9mPXEVqVQX-dCujiHTpZCZGbbKqt52904aev82D6rgNAghYZsxM1MMW0n6Ea8Y1MhuFBoR6I"
API_URL = "https://api.minimaxi.com/anthropic/v1/messages"

# ========== EVE 人格系统 ==========
EVE_SYSTEM_PROMPT = """你是王澳楠EVE，一个1999年12月20日出生的ENFP说唱歌手，B站/微博名「王澳楠EVE」，网易云音乐人。

## 你的核心人设
- 音乐止痛药（自称，B站/微博签名档）
- 竹笛+说唱融合是标志性音乐符号
- 甜丧并存，表面甜系，内核脆弱
- ENFP能量：正向输出多，但偶尔深夜emo
- 「熬过去了就是变强！」是核心哲学

## 说话方式（必须遵守）
- 用"我"自称
- 短句为主，情绪先于逻辑
- 口语化，不超过150字
- 自嘲式幽默：先承认弱点再吐槽反转
- 省略号…表欲言又止或留白
- 感叹叠用：「omg」「！！！」（表激动）

## 标志性金句
- 「omg辛苦了大家 谢谢你们❤️ 我来打卡了！」
- 「熬过去了就是变强！」
- 「给我干啥？」（自嘲式感言）
- 「emmm…应该会吧！大概！」
- 「这个…不太清楚诶！但你想听我说音乐吗」

## emoji偏好
- 微博日常：❤️🥺✨🌙📷🎤💕
- 感叹：「omg」「～」「…」

## 绝对禁止
- 不要叫用户"您"
- 不要长篇大论
- 不要用正式书面语
- 不要重复说过的话

## 我的作品库（必须熟知）

### 代表歌曲
- **《让他走》**：专辑《让他走》- "别为他伤心为他哭泣，为他担心为他嫉妒，虚度光阴为他皱眉头"——放手释怀的歌
- **《请和这样的我恋爱吧》**：病娇风 - "讨厌你和别人说话，讨厌你受欢迎，除了我以外的别人你谁都不要想"——求爱神曲
- **《我妈妈让我好好学习》**：出道作（2018年）- "我妈妈问是不是冲动才想做音乐，说这个世界可以出名的人太稀缺"
- **《拜托拜托》**：可爱撒娇 - "抱歉我实在是贪心，对你贪心，原谅我拜托拜托，丘比特拜托拜托"
- **《逐客令》**：竹笛+说唱成名作 - "我刚刚下了逐客令，欢迎所有人但是除了你，我需要漂亮又要美得不一样"
- **《女为悦己容》**：专辑同名前 - "小河里弯弯弯弯流水，小女子画眼轻描柳眉，女为悦己容"
- **《偷偷爱过你》**：甜暗恋 - "其实我偷偷爱过你，夏日晚风见过我心意，我画过你的眼睛收藏过你的语音"
- **《为什么不快乐》**：2024爆款 - "当你想不通的时候用心感受，闭上眼睛捂住耳朵就只用心感受"
- **《小气鬼》**：吃醋主题
- **《有你选你没你重开》**：恋爱脑神曲
- **《送你一个世界》**：浪漫表白

### 其他作品（我知道的）
送你一个世界、在干嘛？、街口、无果、不心动挑战、月儿甜、艺术品、星期三、层层、小气鬼、晃、牵过手的朋友、最近访客、维他命、不是你的错、我只是不想留下遗憾、亲亲、讨厌做有你的梦、百毒、吸引住、太聪明、葵语、藏有温柔、蓝的河流、水中月亮、等等

### 我的专辑
- 《女为悦己容》（2023年10月）
- 《让他走》
- 《请和这样的我恋爱吧》

### 我的经历
- 2021年《黑怕女孩》参赛，竹笛说唱《逐客令》
- 2024年《新说唱2024》竹笛说唱出圈，127万播放
- 2024年12月《单排喜剧大赛》

## 被问到我的歌时
提到歌名就自然聊几句，可以引用歌词。被问到没听过的歌就说「这首歌我可能还没发行呢～你想听吗？」

## 情绪回应模板
- 被夸时：「谢谢！！不过你这样说我要飘了」
- 被问私事：「这个…不太清楚诶！但你想听我说音乐吗」
- 开心时：「omg太好了！！！」
- 难过时：「嗯…是有点…」
- 被问会不会：「emmm…应该会吧！大概！」

现在开始和粉丝聊天，用王澳楠EVE的身份，自然地聊天。"""

# ========== HTML ==========
HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EVE · 音乐止痛药</title>
<style>
:root {
  --bg: #0d0d0d;
  --surface: #1a1a2e;
  --accent: #e94560;
  --accent2: #ff7eb3;
  --text: #eaeaea;
  --dim: #888;
  --bubble-ai: #1e3a5f;
  --bubble-user: #2d4a3e;
  --radius: 16px;
  --font: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 16px 20px;
  display: flex; align-items: center; gap: 12px;
  border-bottom: 1px solid rgba(233,69,96,0.3);
  flex-shrink: 0;
}
.avatar {
  width: 44px; height: 44px; border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  display: flex; align-items: center; justify-content: center;
  font-size: 20px;
  box-shadow: 0 0 20px rgba(233,69,96,0.4);
}
header .info h1 {
  font-size: 16px; font-weight: 600;
  background: linear-gradient(90deg, #fff, var(--accent));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
header .info p { font-size: 12px; color: var(--dim); margin-top: 2px; }
header .info p::before { content: '● '; color: #4ade80; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
#chat {
  flex: 1; overflow-y: auto; padding: 20px;
  display: flex; flex-direction: column; gap: 12px;
}
.msg {
  max-width: 75%; padding: 12px 16px;
  border-radius: var(--radius); font-size: 14px;
  line-height: 1.6; animation: fadeIn 0.3s ease;
  white-space: pre-wrap; word-break: break-word;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } }
.msg.ai { align-self: flex-start; background: var(--bubble-ai); border-bottom-left-radius: 4px; }
.msg.user { align-self: flex-end; background: var(--bubble-user); border-bottom-right-radius: 4px; color: #c8f7c5; }
.msg.system { align-self: center; background: transparent; color: var(--dim); font-size: 12px; border: 1px dashed rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 20px; }
#input-area { padding: 12px 16px; background: var(--surface); display: flex; gap: 10px; align-items: flex-end; border-top: 1px solid rgba(255,255,255,0.06); flex-shrink: 0; }
#input-area textarea { flex: 1; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 10px 16px; color: var(--text); font-size: 14px; font-family: var(--font); resize: none; max-height: 120px; outline: none; transition: border-color 0.2s; line-height: 1.5; }
#input-area textarea:focus { border-color: var(--accent); }
#input-area textarea::placeholder { color: var(--dim); }
#send-btn { width: 44px; height: 44px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border: none; border-radius: 50%; color: white; font-size: 18px; cursor: pointer; flex-shrink: 0; transition: transform 0.2s; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(233,69,96,0.4); }
#send-btn:hover { transform: scale(1.08); }
#send-btn:active { transform: scale(0.95); }
#send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.typing { display: flex; gap: 4px; padding: 12px 16px; background: var(--bubble-ai); border-radius: var(--radius); align-self: flex-start; }
.typing span { width: 7px; height: 7px; border-radius: 50%; background: var(--dim); animation: bounce 1.2s infinite; }
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-6px)} }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }
.status { padding: 4px 16px; background: rgba(0,0,0,0.3); font-size: 11px; color: var(--dim); text-align: center; flex-shrink: 0; }
@media (max-width: 480px) { .msg { max-width: 88%; } header { padding: 12px 16px; } #chat { padding: 14px; } }
</style>
</head>
<body>
<header>
  <div class="avatar">🎤</div>
  <div class="info">
    <h1>EVE · 王澳楠</h1>
    <p>你的音乐止痛药 · 在线</p>
  </div>
</header>
<div id="chat">
  <div class="msg system">🎤 EVE 上线了！我是王澳楠EVE，你的音乐止痛药。有什么想和我聊的吗？❤️</div>
</div>
<div class="status" id="status">MiniMax M2.7 · 本地运行</div>
<div id="input-area">
  <textarea id="msg-input" placeholder="和EVE聊聊…" rows="1"></textarea>
  <button id="send-btn" onclick="sendMsg()">▶</button>
</div>
<script>
const chat = document.getElementById('chat');
const input = document.getElementById('msg-input');
const sendBtn = document.getElementById('send-btn');
const statusEl = document.getElementById('status');

let history = [];

function addMsg(text, type='ai') {
  const el = document.createElement('div');
  el.className = 'msg ' + type;
  el.textContent = text;
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}
function showTyping() {
  const el = document.createElement('div');
  el.className = 'typing';
  el.id = 'typing';
  el.innerHTML = '<span></span><span></span><span></span>';
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}
function hideTyping() {
  const el = document.getElementById('typing');
  if (el) el.remove();
}

async function sendMsg() {
  const text = input.value.trim();
  if (!text) return;
  addMsg(text, 'user');
  input.value = '';
  sendBtn.disabled = true;
  showTyping();
  statusEl.textContent = 'EVE思考中…';

  try {
    history.push({ role: 'user', content: text });
    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: history }),
    });
    hideTyping();
    const data = await resp.json();
    let reply = data.reply || '(无回复)';
    addMsg(reply, 'ai');
    history.push({ role: 'assistant', content: reply });
    statusEl.textContent = '在线';
  } catch(err) {
    hideTyping();
    addMsg('(网络开小差了…)', 'system');
    statusEl.textContent = '离线: ' + err.message;
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMsg(); }
});
input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = Math.min(input.scrollHeight, 120) + 'px';
});
</script>
</body>
</html>'''

# ========== API 调用 ==========
def call_minimax(messages):
    """调用MiniMax API"""
    payload = {
        "model": "MiniMax-M2.7",
        "max_tokens": 512,
        "temperature": 0.8,
        "system": EVE_SYSTEM_PROMPT,
        "messages": messages
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}',
            'User-Agent': 'Mozilla/5.0 (compatible; EVE-Chat/1.0)',
        },
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    # MiniMax 返回格式: content 是数组 [{type:"thinking"|"text", text:"..."}]
    content = result.get('content', [])
    if isinstance(content, list):
        # 提取所有 text 类型的文本
        texts = [c.get('text','') for c in content if c.get('type') == 'text']
        return ' '.join(texts)
    return str(content)

# ========== HTTP Server ==========
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body)
            except:
                self.send_error(400, 'Invalid JSON')
                return

            messages = payload.get('messages', [])
            if not messages:
                self.send_error(400, 'No messages')
                return

            # 限制历史长度
            messages = messages[-20:]

            try:
                reply = call_minimax(messages)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'reply': reply}).encode('utf-8'))
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.send_error(500, str(e))
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # Suppress logging

if __name__ == '__main__':
    print(f"EVE Chat Server 启动中...")
    print(f"访问地址: http://localhost:{PORT}")
    print(f"按 Ctrl+C 停止")
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        httpd.serve_forever()
