> 原文：https://github.com/benjiyaya/Minimax-H3-Prompt-AgentSkill （README，中文翻译）

# 🎬 MiniMax H3 视频提示词 Agent Skill

一个 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 技能，把粗略的视频创意 + 参考图片/音频转化为生产级的 **MiniMax H3** 视频生成提示词。

## 功能说明

当你附加图片、视频或音频并描述一个视频概念时，本技能会：

1. **自动检测 H3 模式**（Ref2VA、T2VA、I2VA、FL2VA、L2VA）
2. 在 7 个电影化维度上对创意进行**创造性增强**
3. **输出精确的 H3 格式** —— 可直接粘贴进 ComfyUI

## 支持的 H3 模式

| 模式 | 适用场景 | 输出格式 |
|---|---|---|
| **Ref2VA** | 角色/风格/声音参考素材 | 6 段式结构化提示词 |
| **T2VA** | 文生视频（无图片） | 带时间戳的多镜头时间线 |
| **I2VA** | 1 张图作为首帧 | 指令行 + 时间线 |
| **FL2VA** | 2 张图（首帧 + 尾帧） | 指令行 + 时间线 |
| **L2VA** | 1 张图作为尾帧 | 指令行 + 时间线 |

## 创造性增强维度

每条提示词都会在以下维度上得到丰富：

- 🎥 **镜头身份（Camera Identity）** — 物理相机类型、瑕疵、格式美学
- 🎨 **视觉质感（Visual Texture）** — 颗粒、色彩基调、灯光设计、曝光特性
- ⚡ **节奏弧线（Pacing Arc）** — 能量推进、剪辑节奏、铺垫模式
- 👤 **角色细节（Character Detail）** — 外貌特征、服装、标志性视觉色彩
- 🧭 **空间地理（Spatial Geography）** — 屏幕方向、动作矢量、环境布局
- 🔄 **连续性推进（Continuity Progression）** — 状态追踪、损伤累积、情绪弧线
- 🔊 **声音设计（Sound Design）** — 环境音、音效、剧情内/剧情外音乐映射

## 安装

### Hermes Agent 用户

把技能文件夹复制到你的 Hermes 技能目录：

```bash
# Linux/macOS
cp -r h3-video-prompt-enhancer ~/.hermes/skills/creative/

# Windows
xcopy h3-video-prompt-enhancer %LOCALAPPDATA%\\hermes\\skills\\creative\\ /E /I
```

重启 Hermes Agent。当你附加媒体素材并描述视频创意时，技能会自动触发。

### 其他 Agent 框架（Claude、Codex 等）

`SKILL.md` 和参考文件都是标准 Markdown —— 在任何支持基于文件指令的 Agent 中，把它们作为系统上下文或项目规则加载即可。

## 文件结构

```
h3-video-prompt-enhancer/
├── README.md                              # 你正在看的文件
├── SKILL.md                               # 技能主文件 — 工作流、规则、验证
└── references/
    ├── ref2va-format.md                   # 完整的 Ref2VA 6 段式格式规范
    ├── base-multishot-format.md           # T2VA / I2VA / FL2VA / L2VA 格式规范
    └── creative-showcase.md               # 高级长篇提示词模式与基准示例
```

## 使用示例

### Ref2VA（角色参考）

```
📎 Attach: character_sheet.png, voice_sample.mp3
💬 "A woman matching this character walks through a neon-lit Tokyo street at night, 
    stops at a ramen stand, says hi to the cook"
```

→ 输出包含 `subject_definitions`、`summary`、`retention_analysis`、`detailed_description`、`overall_soundscape`、`non_diegetic_music` 的 6 段式结构化提示词。

### I2VA（图生视频）

```
📎 Attach: first_frame.png
💬 "A baker opening his shop before sunrise, proud of the first loaf"
```

→ 输出以首帧图片为锚点的带时间戳多镜头时间线。

### FL2VA（首帧 + 尾帧）

```
📎 Attach: first_frame.png, last_frame.png
💬 "Day to night transition over a city skyline"
```

→ 输出从首帧到尾帧的连续插值提示词。

## 关键格式规则

- 输出为**纯结构化文本** —— 不加 markdown 代码围栏，不加前言
- 所有时间戳使用 `MM:SS.mmm` 格式，严格递增
- 每个镜头只有一个主导动作 —— 绝不塞进多个动作
- 镜头运动用自然英语书写（例如 *"The camera pushes in with small amplitude at slow speed"*）
- 对白原样保留在 `<d>[Language] ...</d>` 标签内
- 参考标签（`<Subject N>`、`<Picture N>`、`<Video N>`、`<Audio N>`）在所有段落中保持一致

## ComfyUI 集成

```
LLM Node (with system prompt) → text output → H3 Ref2VA / H3 Base node prompt input
```

保持 ASSETS 列表顺序与参考输入的物理接线顺序一致 —— 标签按位置映射（Image 1 → 第一个图片接口，以此类推）。

## 出处

为 [MiniMax H3](https://github.com/MiniMax-AI) 全模态视频模型而构建。Ref2VA 与 Base MultiShot 格式规范源自 MiniMax 官方的 H3-Context-IR 预处理器文档。

## 许可证

MIT
