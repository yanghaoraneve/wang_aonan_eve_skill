# 王澳楠 EVE · 数字人格 Skill

> 「大家好我是EVE！你的音乐止痛药！」

## 是什么

王澳楠EVE（1999.12.20，ENFP）的AI数字人格，基于72首歌词+24条微博+20个B站视频+公开采访构建。

## 快速使用

### 方式一：配置AI Agent（推荐）

1. 将 `persona.md` 全文作为 **system prompt** 加载
2. （可选）将 `knowledge/` 目录挂载给AI读取歌词/微博/B站数据
3. 加载 `SKILL.md` 获取完整配置说明

### 方式二：启动对话前端

```bash
cd frontend
# 编辑 eve_server.py，替换 API_KEY 为你的MiniMax Key
python3 eve_server.py
# 浏览器打开 http://localhost:18799
```

## 目录结构

```
wang_aonan_eve/
├── SKILL.md              # Skill配置说明（含RAG检索指令）
├── persona.md            # 完整人格档案（system prompt用）
├── meta.json             # 艺人基本信息
├── README.md             # 本文件
├── frontend/
│   └── eve_server.py     # 对话前端（Python独立服务器，MiniMax API）
└── knowledge/
    ├── lyrics/               # 95个歌词文件（网易云）
    ├── song_list_full.json   # 51首歌列表
    ├── weibo_posts_full.json # 24条微博原文
    ├── video_details.json    # 20个B站视频详情
    └── comments.json         # 75条B站评论
```

## 数据来源

| 来源 | 内容 |
|------|------|
| 网易云音乐API | 72首歌词（55首完整+17首伴奏/Live） |
| B站API | 20个视频详情+75条热门评论 |
| 微博搜索 | 24条动态（2021-2026） |
| 公开资料 | 生日/MBTI/平台账号/代表作 |

## License

MIT
