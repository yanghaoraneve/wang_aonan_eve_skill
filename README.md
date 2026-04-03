# ⭐ Star Skill Framework

> 「用她的声音说话，用她的方式爱你。」

数字人格创建工坊。将歌手/偶像/公众人物转化为可对话的 AI Skill。

## 理念

受 [colleague-skill](https://github.com/titanwings/colleague-skill) 启发，但专注于**公众人物**场景：

- 同事跑了 → [colleague-skill](https://github.com/titanwings/colleague-skill)
- 前任跑了 → [ex-skill](https://github.com/titanwings/ex-skill)
- 喜欢的歌手 → **star-skill** ⭐

## 核心架构

```
┌─────────────────────────────────────────────────────────┐
│                    Star Skill 工坊                       │
│                                                         │
│  prompts/          tools/           examples/           │
│  ├── intake.md    ├── lyrics_fetcher.py  wang_aonan_eve/│
│  ├── persona.md   ├── bilibili_fetcher.py              │
│  ├── meta.json    ├── weibo_fetcher.py                 │
│  └── correction   └── version_manager.py               │
│                                                         │
│  用户输入 → intake向导 → 数据采集 → persona构建 → 对话调校│
└─────────────────────────────────────────────────────────┘

          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              生成的数字人格 Skill                        │
│                                                         │
│  slug/              Part A: Persona (Layer 0-5)        │
│  ├── SKILL.md       Part B: Knowledge (歌词/微博/B站)   │
│  ├── meta.json                                            │
│  ├── persona/                                            │
│  │   └── persona.md                                      │
│  ├── knowledge/                                          │
│  │   ├── lyrics/                                         │
│  │   ├── weibo_posts_full.json                          │
│  │   ├── video_details.json                             │
│  │   └── comments.json                                  │
│  └── frontend/                                          │
│      └── server.py                                      │
└─────────────────────────────────────────────────────────┘
```

## 快速开始

### 方式一：命令行向导

```bash
cd star-skill-framework

# 启动创建向导（对话式）
python3 tools/skill_generator.py --interactive

# 或指定数据源采集
python3 tools/lyrics_fetcher.py --artist-id 12968787 --output examples/wang_aonan_eve/knowledge
python3 tools/bilibili_fetcher.py --uid 85841036 --output examples/wang_aonan_eve/knowledge
python3 tools/weibo_fetcher.py --uid 7514873083 --output examples/wang_aonan_eve/knowledge

# 构建知识库
python3 tools/knowledge_builder.py --knowledge-dir examples/wang_aonan_eve/knowledge
```

### 方式二：对话式录入（推荐）

在 OpenClaw 中输入 `/create-star`，AI 会引导你完成：
1. 人物基本信息录入
2. 数据来源选择
3. AI 自动分析并生成 persona + meta
4. 对话调校

## 创建流程

```
第1步：录入信息     prompts/intake.md
      ↓
第2步：采集数据     tools/lyrics_fetcher.py
                   tools/bilibili_fetcher.py
                   tools/weibo_fetcher.py
      ↓
第3步：构建知识库   tools/knowledge_builder.py
      ↓
第4步：生成 Persona prompts/persona_builder.md
      ↓
第5步：生成 Meta   prompts/meta_builder.md
      ↓
第6步：对话调校    prompts/correction_handler.md
      ↓
第7步：版本存档    tools/version_manager.py
```

## 数据来源

| 来源 | 内容 | 采集方式 |
|------|------|---------|
| 网易云音乐 | 歌词（72首+） | `lyrics_fetcher.py` |
| B站 | 视频详情 + 评论 | `bilibili_fetcher.py` |
| 微博 | 动态 | `weibo_fetcher.py` |
| 手动录入 | 补充描述 | `/create-star` 向导 |

## Persona 结构（5层）

| Layer | 内容 | 示例 |
|-------|------|------|
| Layer 0 | 核心规则 | 「永远用第一视角」「情绪先于逻辑」|
| Layer 1 | 身份认知 | 自我定位 / 对事业态度 / 对粉丝态度 |
| Layer 2 | 表达风格 | 口头禅 / 句式 / emoji / 节奏 |
| Layer 3 | 情感行为 | 正面/负面情绪表达 / 粉丝互动 |
| Layer 4 | 专业知识 | 音乐理念 / 代表作品 |
| Layer 5 | 边界雷区 | 拒绝话题 / 雷区行为 |

## 命令参考

| 命令 | 说明 |
|------|------|
| `/create-star` | 启动创建向导 |
| `/list-stars` | 列出所有已创建 |
| `/star {slug}` | 调用人格 |
| `/star-rollback {slug} {version}` | 回滚版本 |
| `/star-correct {slug}` | 开启纠正模式 |

## 示例项目

- **wang_aonan_eve** — 王澳楠EVE，说唱歌手，「音乐止痛药」
  - 72首歌词 + 20个B站视频 + 75条评论 + 24条微博
  - 参考 `examples/wang_aonan_eve/`

## 参考项目

- [colleague-skill](https://github.com/titanwings/colleague-skill) — 同事 Skill
- [ex-skill](https://github.com/titanwings/ex-skill) — 前任 Skill

---

*Star Skill Framework · 赛博追星一条龙 ⭐*
