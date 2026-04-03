<div align="center">

# 王澳楠 EVE · Skill

> *「大家好我是EVE！你的音乐止痛药！」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-通用-blue.svg)]()

</br>

说唱歌手、唱作人、竹笛+说唱的融合者。<br>
她的歌装过太多人的深夜，也治愈过无数个说不出口的时刻。

**王澳楠EVE的AI分身——用她的语气、她的方式，陪你聊音乐、聊情绪、聊那些说不出口的话。**

[项目结构](#项目结构) · [快速使用](#快速使用) · [效果示例](#效果示例) · [数据来源](#数据来源)

---

### 🌟 同类项目：[同事.skill](https://github.com/titanwings/colleague-skill) · [前任.skill](https://github.com/titanwings/ex-skill)

> 同事跑了用同事.skill，前任跑了用前任.skill，<br>
> 喜欢的歌手也可以数字化——**赛博追星一条龙** 🌟🌟🌟

</div>

---

## 是什么

**王澳楠 EVE**，1999.12.20 生，ENFP 说唱歌手，深圳大学 F.I.G 说唱社出身。

代表作《逐客令》《让他走》《请和这样的我恋爱吧》《我妈妈让我好好学习》。B站签名：**「大家好我是EVE！你的音乐止痛药！」**

这个 Skill 是她的数字分身——不只是语气模仿，是基于 72 首歌词 + 24 条微博 + 20 个 B 站视频构建的完整人格档案。

---

## 快速使用

### 方式一：配置 AI Agent（推荐）

```bash
# 克隆到本地
git clone https://github.com/yanghaoraneve/wang_aonan_eve_skill.git

# 将 persona.md 全文作为 system prompt 加载到你的 AI
# 知识库 knowledge/ 目录可按需挂载给 AI 读取
```

> SKILL.md 中有完整的人格配置说明、RAG 检索指令（让 AI 能读懂歌词/微博/B站数据）。

### 方式二：对话前端（开箱即用）

```bash
cd frontend
# 编辑 eve_server.py，填入你的 MiniMax API Key
python3 eve_server.py
# 浏览器打开 http://localhost:18799
```

---

## 效果示例

**场景一：聊音乐**

```
用户    ❯ EVE，你最代表的作品是哪首？
EVE     ❯ 嗯…《逐客令》应该大家都知道吧？
        竹笛那段我真的录了很久哈哈
        "欢迎所有人但是除了你" 那个感觉…
        就，很像我。

用户    ❯ 逐客令讲的什么？
EVE     ❯ 口是心非呗！
        就是那种"你走吧"但心里其实"别走"的感觉
        写的时候我自己也…（叹气）
        有些话说不出口嘛。
```

**场景二：日常互动**

```
用户    ❯ 你怎么这么晚还不睡？
EVE     ❯ omg你怎么也这么晚！
        我是夜猫子型哈哈～习惯深夜写歌
        白天脑子不清醒，一到晚上就…
        熬过去就是变强！💪
```

---

## 数据来源

| 来源 | 内容 |
|------|------|
| 网易云音乐 API | 72 首歌词（55 首完整 + 17 首伴奏/Live） |
| B站 API | 20 个视频详情 + 75 条热门评论 |
| 微博搜索（weibo-cli） | 24 条动态（2021-2026） |
| 公开资料整理 | 生日 / MBTI / 平台账号 / 经历 |

---

## 项目结构

```
wang_aonan_eve_skill/
├── SKILL.md              # Skill 配置入口（含 RAG 检索指令）
├── persona.md            # 完整人格档案（system prompt 用）
├── meta.json             # 艺人基本信息
├── README.md             # 本文件
├── frontend/
│   └── eve_server.py     # 对话前端（Python，MiniMax API）
└── knowledge/
    ├── lyrics/               # 95 个歌词文件（网易云）
    ├── song_list_full.json   # 51 首歌列表
    ├── weibo_posts_full.json # 24 条微博原文
    ├── video_details.json    # 20 个 B 站视频详情
    └── comments.json         # 75 条 B 站评论
```

---

## License

MIT License · 致谢与参考：

**本项目在构思与结构上参考了 [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill)**——「将冰冷的离别化为温暖的 Skill」，同系列还有 [前任.skill](https://github.com/titanwings/ex-skill)，赛博永生理念一致，深受启发。

