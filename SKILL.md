---
name: create-star-skill
description: 创建明星/偶像/公众人物数字人格 Skill 的工坊框架。将歌手/演员/网红等转化为可对话的 AI 数字分身。
version: "1.0"
triggers:
  - /create-star
  - /star-wizard
  - /build-star-skill
user-invocable: true
read:
  - README.md
  - prompts/intake.md
---

# ⭐ Star Skill 工坊

> 「用她的声音说话，用她的方式爱你。」

## 是什么

Star Skill 是一个**数字人格创建框架**，用于将真实明星/偶像/公众人物转化为可对话的 AI Skill。

基于 `colleague-skill`（by titanwings）理念演进，但专注于**公众人物**场景：
- 歌手 → 音乐止痛药
- 演员 → 角色百科全书
- 网红 → 赛博追星搭子

---

## 快速开始

```bash
# 进入工坊
cd star-skill-framework

# 启动创建向导
/create-star

# 按提示输入：
# 1. 人物基本信息（姓名、平台、MBTI等）
# 2. 选择数据来源（网易云/B站/微博/手动描述）
# 3. 等待 AI 分析并生成 persona + knowledge
# 4. 对话调校，纠正偏差
```

---

## 架构总览

```
star-skill-framework/
├── SKILL.md                   # 本文件，工坊入口
├── README.md                  # 详细文档
│
├── prompts/                   # Prompt 模板
│   ├── intake.md             # 信息录入向导
│   ├── persona_builder.md    # Persona Layer 0-5 生成模板
│   ├── meta_builder.md       # meta.json 生成模板
│   ├── knowledge_router.md   # 知识库路由配置
│   └── correction_handler.md # 对话纠正处理
│
├── tools/                     # Python 工具
│   ├── lyrics_fetcher.py     # 歌词采集（网易云）
│   ├── weibo_fetcher.py      # 微博采集（weibo-cli）
│   ├── bilibili_fetcher.py   # B站视频/评论采集
│   ├── knowledge_builder.py   # 知识库构建工具
│   ├── skill_generator.py     # Skill 文件生成
│   └── version_manager.py     # 版本管理
│
└── star/                      # ⚡ 框架生成产物（运行 /create-star 后生成）
    ├── SKILL.md
    ├── meta.json
    ├── persona/
    │   └── persona.md
    ├── knowledge/
    │   ├── lyrics/
    │   ├── song_list_full.json
    │   ├── weibo_posts_full.json
    │   ├── video_details.json
    │   └── comments.json
    └── frontend/
│
└── docs/
    └── PRC.md                # 项目需求文档
```

---

## 生成的 Skill 结构

每个创建的数字人格 Skill 包含两部分：

| 部分 | 内容 |
|------|------|
| **Part A — Persona** | 5层性格结构：核心规则 → 身份认知 → 表达风格 → 情感行为 → 边界雷区 |
| **Part B — Knowledge** | 知识库路由：歌词/微博/视频/评论，按类型索引 |

**运行逻辑**：接收消息 → Persona 判断身份/风格 → Knowledge 检索 → 用她的语气输出

---

## 数据来源

| 来源 | 内容 | 采集工具 |
|------|------|---------|
| 网易云音乐 | 歌词（按歌曲ID抓取） | `lyrics_fetcher.py` |
| B站 | 视频详情 + 评论 | `bilibili_fetcher.py` |
| 微博 | 动态 + 评论 | `weibo_fetcher.py` |
| 手动描述 | 补充信息 | 人工录入 |

---

## 调校命令

| 命令 | 说明 |
|------|------|
| `/create-star` | 启动创建向导 |
| `/list-stars` | 列出所有已创建的数字人格 |
| `/star {slug}` | 调用完整 Skill |
| `/star-{slug}-persona` | 仅人格部分 |
| `/star-{slug}-knowledge` | 仅知识库 |
| `/star-rollback {slug} {version}` | 回滚到历史版本 |
| `/star-correct {slug}` | 开启纠正模式 |

---

## 参考项目

- [colleague-skill](https://github.com/titanwings/colleague-skill) by @titanwings
- [ex-skill](https://github.com/titanwings/ex-skill) by @titanwings

---
