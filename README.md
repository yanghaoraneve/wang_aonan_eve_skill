# 王澳楠 EVE · 数字人格 Skill

> 「大家好我是EVE！你的音乐止痛药！」

## 是什么

王澳楠EVE的AI数字人格，基于她公开资料（歌词/微博/B站/采访）构建。

## 快速使用

### 方式一：直接配置AI Agent

将 `persona.md` 全文作为 **system prompt** 加载到任意AI应用即可。

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
├── meta.json              # 艺人基本信息（UID/平台/生日/MBTI）
├── persona.md             # 完整人格档案（AI system prompt用）
├── SKILL.md               # Skill配置说明
├── README.md               # 本文件
├── frontend/
│   └── eve_server.py      # 对话前端（独立Python服务器）
└── knowledge/
    ├── lyrics/            # 95个歌词文件（网易云）
    ├── song_list_full.json    # 51首歌列表
    ├── weibo_posts_full.json # 24条微博原文
    ├── bilibili/
    │   ├── video_details.json   # 20个B站视频详情
    │   └── comments.json        # 75条B站评论
    └── meta.json           # 数据源说明
```

## 人格亮点

- **MBTI**: ENFP（快乐小狗）
- **音乐定位**: 音乐止痛药
- **风格**: 甜丧/病娇/竹笛说唱
- **核心金句**: 「熬过去了就是变强！」
- **标志作品**: 竹笛版《逐客令》127万播放

## 数据来源

| 来源 | 内容 |
|------|------|
| 网易云音乐API | 72首歌词（55首完整+17首伴奏/Live） |
| B站API | 20个视频详情+75条热门评论 |
| 微博搜索 | 24条动态（2021-2026） |
| 公开资料整理 | 生日/MBTI/平台账号/代表作 |

## License

MIT
