> 原文：https://github.com/SlavaSexton/ComfyUI-Agent-Kit （README，中文翻译）

<div align="center">

<img src="docs/assets/cover.png" width="880" alt="ComfyUI skill for AI coding agents, by AI VFX NEWS">

# ComfyUI-Agent-Kit

**为每一个 AI 编程智能体（Claude Code、Codex、Gemini CLI、Qwen Code）打造的本地优先 ComfyUI。**
<br>
**你的 GPU，你的模型，无需云端，无需账号。**

**由 [AI VFX NEWS](https://aivfxnews.com/) 出品。**

让 Claude Code、Codex、Gemini CLI 或 Qwen Code 在你自己的机器上全速驱动 **ComfyUI**——生成图像、视频和音频，构建并运行工作流，挑选适合*你的*硬件的模型变体，并**在你自己的 ComfyUI 画布中实时查看图谱**。没有托管服务，没有按次生成的计费：一个安装器把同一套技术栈接入你运行的每一个智能体，之后你还可以用一条命令把整套配置移交给别人。

![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-FFD27D.svg)
![ComfyUI](https://img.shields.io/badge/ComfyUI-driven-5BAEE3.svg)
![Agents](https://img.shields.io/badge/Claude_·_Codex_·_Gemini_·_Qwen-9aa3b2.svg)
![Platforms](https://img.shields.io/badge/Windows_·_Linux_·_macOS-supported-9aa3b2.svg)

</div>

---

这是一个可移植、与机器无关、**多智能体**版本的可运行 ComfyUI 配置。一个共享核心（知识库 + MCP 驱动器）加上每个智能体一个轻量适配器。克隆仓库、运行安装器，你的每个智能体都会获得同一套技术栈，接入*你的*硬件。GLM（z.ai）通过 Claude Code 运行的情况由 `claude` 适配器覆盖。每个智能体如何接入，见 **[docs/AGENTS.md](docs/AGENTS.md)**。

**本地优先，既适合专家也适合日常用户。** 它的能力范围从一条命令生成图像/视频，一直到专业级 VFX 调色流程：v2 内置了 **[ComfyUI-OCIO](https://github.com/SlavaSexton/ComfyUI-OCIO)**（九个 Nuke 风格的 OpenColorIO 节点——读取序列、在 ACES 中调色、输出 ProRes、在节点内播放器上预览，全程色彩管理），以及一份构建自定义节点的实战指南。

> **设计上就是本地优先。** 更偏好云端？官方的 **Comfy Cloud MCP** 可以在 Comfy 的 GPU 上运行你的工作流，无需本地配置。本工具包是它的本地优先对应物：一切运行在*你*控制的硬件上，没有账号、没有按次生成的费用，模型选择器会根据你的 VRAM 为每个任务匹配规格，而且它同时服务四个智能体，而不是一个。哪个合适用哪个。

## 它能做什么

- **用四个智能体（Claude Code、Codex、Gemini CLI、Qwen Code）驱动 ComfyUI**，共享同一个核心。GLM 通过 Claude Code 运行也已被覆盖。([docs/AGENTS.md](docs/AGENTS.md))
- **约 90 个工具的 MCP 驱动器。** 智能体直接操作 ComfyUI：生成、构建/编辑/校验图谱、排队、下载模型、管理 VRAM、读取日志、诊断。
- **每个模型的"超级大脑"：** 75 条提示词配方条目，覆盖 68 个具名模型，从**官方来源**（图像、视频、音频、3D）提炼而成，按家族拆分，每个文件一次调用即可完整读取；当你说出一个模型名，智能体会自动调取对应配方，用该模型自己的"方言"来写提示词。
- **知道每个模型在哪里运行：** 全部 163 个库内模型（配方/实用工具/仅模板、本地 vs API）的[完整索引](docs/MODEL_INDEX.md)。
- **硬件感知的模型选择：** 检测你的 VRAM、RAM 和可用磁盘，推荐适合的变体（fp8/offload/多 GPU/量化），并在浪费带宽之前拒绝放不下的下载。
- **18 个增强与实用工具：** 超分/修复（Real-ESRGAN、SUPIR、SeedVR2）、插帧（FILM、RIFE）、分割/深度/姿态（SAM3、BiRefNet、Depth Anything），以及修复链。
- **581 个模板的模板库**（外加 **94 个官方 Subgraph Blueprint**，即可复用的子图积木）作为事实来源，还有**按 hash 拉取任意已分享工作流**和**模型擂台赛**（用提示词跑多个小规格模型，选出胜者再放大规模）。
- **从部件组装新工作流：** 把任务分解为阶段，混搭模板与 blueprint 子图，并正确连线（按类型从输出接到输入，必要时加转换节点），运行前先对照 `/object_info` 校验。它不是一个预设运行器。
- **专业调色 + 自定义节点（v2 新增）：** 内置 **[ComfyUI-OCIO](https://github.com/SlavaSexton/ComfyUI-OCIO)**——九个 Nuke 风格的 OpenColorIO 节点（读取/写入单帧、序列或视频，在 ACES 中调色，输出 ProRes/EXR，在节点内播放器上预览，全程色彩管理）——而且智能体知道每个节点的输入输出，并配有*构建*自定义节点包的实战指南。([docs/NODE_LIBRARY/ocio.md](docs/NODE_LIBRARY/ocio.md), [docs/BUILDING_NODES.md](docs/BUILDING_NODES.md))
- **替你启动 ComfyUI：** 当服务器未运行时，智能体会以后台 headless 方式启动它并直接生成（无需先打开应用）；想看看的话，在浏览器打开 `http://127.0.0.1:8188`。对于无人值守流程，启动策略可按项目配置（环境变量或 `.comfyui-agent.json`），因此它绝不会卡在交互提示上。
- **GUI 桥接 + 持久化：** 智能体把图谱写入你的 ComfyUI 画布，并把它构建或运行的每个工作流保存到 ComfyUI 的工作流文件夹，之后你可以从 Workflows 侧边栏打开（纯 API 生成不会在画布上留下任何痕迹）。
- **自动保持最新：** `check_updates.py` 对模板仓库做 diff 并读取博客 RSS；可选的每周任务会为新模型补充配方并推送。([docs/UPDATING.md](docs/UPDATING.md))
- **三个也能在 ComfyUI 之外使用的模型技能：`seedance`、`minimax-h3`、`krea`。** 同样适用于厂商自家应用或 API 的厂商提示词知识，以独立技能的形式提供，而不是埋在 ComfyUI 参考文档里。`minimax-h3` 掌握 H3 三段式提示词格式、`<d>` 对话以及量化与加速阶梯；`krea` 掌握 Krea 托管 API 与其开放权重（FLUX.1 Krea Dev）之间的分岔，以及为什么 Krea Realtime 唯一的 ComfyUI 包只是一个 0 星线索而非通路。其中第一个是 `seedance`：字节跳动的 Seedance 视频模型除了在 ComfyUI 中，也可在 Dreamina、即梦和 BytePlus API 上运行，因此其提示词知识以独立技能提供：三种任务类型及切换它们的那一个关键词、参考标签语法、时间戳分镜、真人角色公式，以及面部漂移、角色重复和延展接缝的故障排查表。提炼自字节跳动官方指南。([shared/seedance/SKILL.md](shared/seedance/SKILL.md))
- **可移植且幂等：** 一个安装器，自动检测你的智能体，可重复运行。Apache-2.0，不内置任何第三方代码（所有大件在安装时拉取）。

## 四层技术栈

<div align="center">

<img src="docs/assets/architecture.png" width="880" alt="The four-layer stack: knowledge + client, MCP driver, in-graph Claude nodes, node-building skills, plus the template library and GUI bridge">

</div>

<br>

| 层 | 内容 | 安装形式 |
|------:|------|--------------|
| 1 | **知识 + 客户端**：操作手册和一个零依赖 HTTP 客户端 | 智能体的 skill / extension 目录 |
| 2 | **MCP 驱动器**：约 90 个结构化工具，让智能体直接操作 ComfyUI | `comfyui-mcp` (npm) + 按智能体注册 MCP |
| 3 | **图内 Claude 节点**：把 LLM 作为工作流中的一个步骤（提示词增强、视觉 QA） | ComfyUI `custom_nodes` |
| 4 | **节点构建技能**：用于编写/修改自定义节点（V3 API） | 智能体的 skill 目录（Claude/Codex） |
| + | **模板库**：官方 500+ 工作流模板，事实来源 | sparse git clone + 快速索引 |

外加一个 **GUI 桥接**：智能体把图谱写入 `<ComfyUI>/user/default/workflows/`，你在内置 Workflows 侧边栏打开并调整。无需额外的"智能体面板"节点。

每一层的详情见 [docs/LAYERS.md](docs/LAYERS.md)，各智能体矩阵见 [docs/AGENTS.md](docs/AGENTS.md)。

## 模板库是事实来源

本工具包克隆官方的 [Comfy-Org/workflow_templates](https://github.com/Comfy-Org/workflow_templates) 并构建紧凑的查找索引，让智能体能把任何请求匹配到正确的模板。581 个模板（外加 **94 个官方 Subgraph Blueprint**，可复用的子图积木）覆盖所有任务类型——图像、视频、3D、音频、实用工具：

<div align="center">

<img src="docs/assets/templates_by_category.png" width="880" alt="Workflow templates by category: 160 video, 158 image, 103 use cases, 72 utility, 33 3D, 31 audio, 17 LLM, 7 node basics">

</div>

## 它懂每个模型的方言

每个生成式模型各自奖励不同的提示词写法：SDXL 要逗号标签，FLUX 要自然语言句子，视频模型要镜头与运动方向，音频模型要流派/节奏/乐器，负面提示词的支持程度也千差万别。本工具包内置 **[`MODELS.md`](shared/comfyui/MODELS.md)**，一份从**官方来源**（各厂商文档和模型卡、docs.comfy.org，以及 `anthropic-claude` 节点的各模型模板）提炼的逐模型提示词参考。当你在请求或工作流中提到某个模型，智能体会先读取该模型的条目，再正确地写提示词。

当前覆盖（75 条配方条目，68 个具名模型）：FLUX.1/.2 + Kontext, Z-Image, Boogu, Mage-Flow, Qwen-Image/Edit, SDXL, SD1.5/3.5, HiDream, Ideogram, Nano Banana Pro/2, Seedream, Recraft, GPT-Image, Grok, Reve, Kandinsky, BRIA, OmniGen, Chroma, Krea 1/2, ERNIE-Image, FireRed/LongCat/ChronoEdit/JoyAI Image Edit（编辑）, Capybara, Bernini-R, Anima, NewBie, PixelDiT, Ovis-Image, Lens, Quiver, Wan 2.1-2.7, LTX-2.3/2 Pro, Hunyuan Video, SVD, Kling, Veo, Sora, Seedance, Luma, Runway, MiniMax, PixVerse, Vidu, Pika, HeyGen（数字人视频）, HappyHorse, HuMo, SCAIL-2, Stable Audio, ACE-Step, ElevenLabs, ChatterBox, Sonilo, Hunyuan3D, Tripo, Rodin, Meshy。另有独立的**增强与实用工具**章节（非提示词驱动，是设置而非提示词）：超分与修复（Real-ESRGAN、SUPIR、SeedVR2、FlashVSR、Topaz、Magnific）、插帧（FILM、RIFE）、条件辅助（SAM3、BiRefNet、Depth Anything、DWPose、MoGe、IP-Adapter、LivePortrait、Mediapipe）以及视频物体移除（VOID）。其余情况回退到模板库。

<div align="center">

<img src="docs/assets/models_by_modality.png" width="880" alt="Per-model prompt recipes by modality: 43 image, 25 video, 6 audio, 4 3D, 78 total, split local/open-weight vs API, plus 18 enhancement and utility tools">

</div>

**完整模型索引**：库中每个模型以及本工具包对它有什么（配方/实用工具/仅模板）：**[docs/MODEL_INDEX.md](docs/MODEL_INDEX.md)**。

### 覆盖表：每个模型及提示词配方是否就绪

`✅ recipe` = 一份专门的、保持更新的提示词指南，通过 [MODELS.md](shared/comfyui/MODELS.md) 中的索引到达，索引会指出 `shared/comfyui/MODELS/` 下承载它的家族文件。`🔧 tool` = 一条增强/实用工具说明（是设置，不是提示词）。**表格最后复核：2026-08-06。**

一张表，列宽对齐最宽的行（视频模型）。

| 模态 | 模型 / 工具 | 提示词配方 | 运行方式 |
|---|---|:---:|---|
| Image | FLUX.1 / FLUX.2 / Kontext | ✅ | local + API |
| Image | Z-Image-Turbo | ✅ | local |
| Image | Qwen-Image / Edit | ✅ | local |
| Image | SDXL · SD 1.5 · SD 3.5 | ✅ | local |
| Image | HiDream-I1 | ✅ | local |
| Image | BRIA 3.x | ✅ | local |
| Image | OmniGen v1/v2 | ✅ | local |
| Image | Chroma | ✅ | local |
| Image | Krea 2 / FLUX.1 Krea Dev | ✅ | local |
| Image | ERNIE-Image | ✅ | local |
| Image | Capybara (image+video) | ✅ | local |
| Image | Bernini-R (relight) | ✅ | local |
| Image | Anima (anime, + ControlNet-LLLite) | ✅ | local |
| Image | NewBie (anime, XML prompts) | ✅ | local |
| Image | PixelDiT | ✅ | local |
| Image | Ovis-Image (text rendering) | ✅ | local |
| Image | Lens / Lens Turbo | ✅ | local |
| Image | Quiver (text to SVG) | ✅ | API |
| Image | Ideogram 2/3 | ✅ | API |
| Image | Nano Banana Pro / 2 | ✅ | API |
| Image | Seedream 4/5 | ✅ | API |
| Image | Recraft V3 | ✅ | API |
| Image | GPT-Image | ✅ | API |
| Image | Grok Image | ✅ | API |
| Image | Reve | ✅ | API |
| Image | Kandinsky 3.x | ✅ | local + API |
| Image edit | FireRed / LongCat / ChronoEdit | ✅ | local |
| Image edit | JoyAI Image Edit (JD) | ✅ | local |
| Video | Wan 2.1-2.7 (+VACE/Animate v1/Animate 2/ATI) | ✅ | local + API |
| Video | LTX-2.3 / LTX-2 Pro | ✅ | local |
| Video | Hunyuan Video | ✅ | local |
| Video | SVD (image-to-video) | ✅ | local |
| Video | HuMo (lip-sync) | ✅ | local |
| Video | SCAIL-2 (character) | ✅ | local |
| Video | HappyHorse 1.1 (synced audio) | ✅ | API |
| Video | Kling (1.6-3.0, O1/O3) | ✅ | API |
| Video | Veo 3/3.1 | ✅ | API |
| Video | Sora 2 | ✅ | API |
| Video | Seedance 1.0/1.5/2.0 (4K) | ✅ | API |
| Video | Luma Ray · Runway Gen-4/4.5 | ✅ | API |
| Video | MiniMax/Hailuo · PixVerse · Vidu · Pika | ✅ | API |
| Video | HeyGen (avatar, talking photo, translate) | ✅ | API |
| Audio | Stable Audio · ACE-Step · ChatterBox | ✅ | local |
| Audio | ElevenLabs · Sonilo | ✅ | API |
| 3D | Hunyuan3D | ✅ | local |
| 3D | Tripo · Rodin · Meshy | ✅ | API |
| Enhance / utility | Real-ESRGAN, SUPIR, SeedVR2, FlashVSR (upscale/restore) | 🔧 settings | local |
| Enhance / utility | Topaz, Magnific (upscale) | 🔧 settings | API |
| Enhance / utility | FILM, RIFE (frame interpolation) | 🔧 settings | local |
| Enhance / utility | SAM3, BiRefNet (segmentation/matting) | 🔧 settings | local |
| Enhance / utility | Depth Anything v2/v3, MoGe (depth/geometry) | 🔧 settings | local |
| Enhance / utility | DWPose, Mediapipe (pose/landmarks) | 🔧 settings | local |
| Enhance / utility | IP-Adapter, LivePortrait (conditioning/portrait) | 🔧 settings | local |
| Enhance / utility | VOID (video object removal) | 🔧 settings | local |

尚无配方的冷门模型（太新、文档少）会从其模板运行并借用最接近家族的写法；完整的逐变体明细见 [docs/MODEL_INDEX.md](docs/MODEL_INDEX.md)。

## 前置条件

- PATH 上有一个或多个智能体 CLI：[Claude Code](https://claude.com/claude-code)（`claude`）、[Codex](https://developers.openai.com/codex)（`codex`）、[Gemini CLI](https://github.com/google-gemini/gemini-cli)（`gemini`）、[Qwen Code](https://github.com/QwenLM/qwen-code)（`qwen`）
- [Node.js](https://nodejs.org)（`node` + `npm`）
- [git](https://git-scm.com)、[Python 3](https://python.org)
- 本地安装的 **ComfyUI**（Desktop 或源码版），[comfy.org](https://www.comfy.org/)

## 安装

### Claude Code：一条命令的插件

Claude Code 用户可以直接从 marketplace 添加本工具包，无需克隆：

```
/plugin marketplace add SlavaSexton/ComfyUI-Agent-Kit
/plugin install comfyui@comfyui-agent-kit
```

这会注册本地 `comfyui-mcp` 驱动器（用 `npx` 启动，无需手动 npm 步骤）并加载完整的 `comfyui` 技能（75 条配方的大脑 + 文档）。你仍需要本地的 ComfyUI 运行在 `http://127.0.0.1:8188`；技能会在第一个任务时填充你的机器信息块。插件仅限 Claude Code，因此 **Codex / Gemini CLI / Qwen Code** 请使用下面的多智能体安装器。

### 所有智能体：安装器

Windows (PowerShell)：

```powershell
git clone https://github.com/SlavaSexton/ComfyUI-Agent-Kit.git
cd ComfyUI-Agent-Kit
./install.ps1 -ComfyUIPath "E:\path\to\ComfyUI"   # installs for every agent CLI found on PATH
```

Linux / macOS：

```bash
git clone https://github.com/SlavaSexton/ComfyUI-Agent-Kit.git
cd ComfyUI-Agent-Kit
./install.sh --comfyui-path /path/to/ComfyUI       # installs for every agent CLI found on PATH
```

安装器先运行一次共享的机器配置（MCP 包、模板、图内节点），然后**自动检测**安装了 `claude` / `codex` / `gemini` / `qwen` 中的哪些并逐一接入。它是**幂等的**，随时可以重跑。用 `-Agents claude,gemini` / `--agents claude,gemini` 限定目标。可用标志：`-SkipTemplates` / `--skip-templates`（跳过约 900MB 的模板克隆）、`-SkipNodes` / `--skip-nodes`。各智能体详情及 GLM 说明见 **[docs/AGENTS.md](docs/AGENTS.md)**。

## 新机器上的首次运行

安装后，启动 ComfyUI，然后在智能体会话中让它运行一次 **bootstrap**（[docs/BOOTSTRAP.md](docs/BOOTSTRAP.md)）：它会通过 MCP 的 `health_check` 检测你的 GPU、VRAM、RAM、可用磁盘、路径和已装模型，填充技能中的机器信息块，并做一次冒烟测试生成。之后直接要作品就行。在 Claude/Codex 上，技能遇到 ComfyUI 关键词会自动激活；在 Gemini/Qwen 上，知识作为扩展的上下文加载。

## 可选：图内 LLM key

仅当你希望工作流在**没有**智能体参与的情况下增强提示词（例如无人值守流程）时才需要：

```powershell
setx CLAUDE_API_KEY "sk-ant-..."   # then restart ComfyUI
```

见 [docs/NODES.md](docs/NODES.md)。当是你在驾驶时，智能体直接写提示词，效果更好而且免费。

## 目录结构

```
ComfyUI-Agent-Kit/
├── install.ps1 / install.sh         top-level: shared setup + auto-detect agents + run adapters
├── shared/
│   ├── comfyui/                     SKILL.md + MODELS.md + comfy_client.py  (one source of truth)
│   └── tools/gen_quick_index.py     rebuild the template lookup index
├── agents/
│   ├── claude/   install.ps1/.sh    -> ~/.claude/skills/comfyui + claude mcp add + CLAUDE.md
│   ├── codex/    install.ps1/.sh    -> ~/.agents/skills/comfyui + ~/.codex/config.toml
│   ├── gemini/   install.ps1/.sh    -> ~/.gemini/extensions/comfyui (gemini-extension.json + GEMINI.md)
│   └── qwen/     install.ps1/.sh    -> ~/.qwen/extensions/comfyui (qwen-extension.json + QWEN.md)
├── docs/AGENTS.md                   per-agent matrix (how each connects) + GLM note
├── docs/MODEL_INDEX.md              every model in the library and what the kit has for it
├── docs/EXAMPLE_WORKFLOWS.md        notable shared workflows (model shootouts, restoration) + fetch helper
├── docs/UPDATING.md                 stay current: check_updates.py (templates diff + blog RSS) + the loop
├── docs/BOOTSTRAP.md / LAYERS.md / NODES.md
├── ATTRIBUTION.md                   credits for fetched third-party pieces
├── CHANGELOG.md                     curated history of notable changes (Keep a Changelog)
├── CONTRIBUTING.md                  what the kit accepts, the Teaching standard, house rules
├── LICENSE                          Apache-2.0 (this kit's original files)
└── NOTICE                           attribution + trademark notice (Apache-2.0 section 4d)
```

## 本仓库里有什么、没什么

仓库内（原创内容，Apache-2.0）：技能、客户端、安装器、索引生成器、文档、生成的配图。安装时从各自来源拉取（不在本仓库再分发）：`comfyui-mcp` 包、节点构建技能、工作流模板和图内 Claude 节点。

## 致谢与感谢

**我们自己的配套节点包：** **[ComfyUI-OCIO](https://github.com/SlavaSexton/ComfyUI-OCIO)**——九个 Nuke 风格的 OpenColorIO 节点——出自 **Slava Sexton**，即本工具包作者（Apache-2.0）。凡本工具包使用、推荐或基于它构建之处均已注明；见 **[ATTRIBUTION.md](ATTRIBUTION.md)**。

本工具包建立在出色的开源工作之上。它只是这些项目之上的一层薄接线，重活都是他们干的。特别感谢：

- **[ComfyUI](https://github.com/comfyanonymous/ComfyUI)**，作者 comfyanonymous / Comfy-Org，一切运行所依赖的引擎。
- **[comfyui-mcp](https://github.com/artokun/comfyui-mcp)**，作者 [artokun](https://github.com/artokun)，让智能体用结构化工具操作 ComfyUI 的 MCP 驱动器（第 2 层）。
- **[comfyui-custom-node-skills](https://github.com/jtydhr88/comfyui-custom-node-skills)**，作者 [jtydhr88 / Terry Jia](https://github.com/jtydhr88)，节点构建技能（第 4 层）。
- **[workflow_templates](https://github.com/Comfy-Org/workflow_templates)**，Comfy-Org 出品，作为事实来源的模板库。
- **[comfy-skills](https://github.com/Comfy-Org/comfy-skills)**，Comfy-Org 出品，本工具包在 SKILL.md 和 ADVANCED.md 中（为本地栈）改编了其输出节点校验护栏和多参考合成技术。
- **[comfyui-anthropic-claude](https://github.com/alexmunteanu/comfyui-anthropic-claude)**，作者 [alexmunteanu](https://github.com/alexmunteanu)；以及 **[comfyui_claude_prompt_generator](https://github.com/PauldeLavallaz/comfyui_claude_prompt_generator)**，作者 [PauldeLavallaz](https://github.com/PauldeLavallaz)，图内 Claude 节点（第 3 层）。

v1.1.0 建立在更多出色工作之上。同时感谢：

- **[Prompt Relay](https://github.com/GordonChen19/Prompt-Relay)**，作者 Gordon Chen、Ziqi Huang、Ziwei Liu（S-Lab, NTU），免训练的时序提示词路由方法（arXiv 2604.10030）。
- **[ComfyUI-PromptRelay](https://github.com/kijai/ComfyUI-PromptRelay)** 和 **[ComfyUI-SUPIR](https://github.com/kijai/ComfyUI-SUPIR)**，作者 [kijai](https://github.com/kijai)，本工具包推荐并驱动的 ComfyUI 移植版。
- **[LTX Director 2.0](https://github.com/WhatDreamsCost/WhatDreamsCost-ComfyUI)**，WhatDreamsCost 出品，LTX-2.3 的时间线编辑节点。
- **[Z-Image-Turbo Fun-ControlNet-Union](https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1)**，alibaba-pai（PAI）出品，以及 [Lightricks](https://huggingface.co/Lightricks) 的 **LTX-2.3** 模型和 **HDR IC-LoRA**。
- **[Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)**，作者 Xintao Wang 及 BasicSR 团队；以及 XPixel Group（Fanghua Yu 等）的 **SUPIR**，超分与修复模型。注意：SUPIR 权重为非商用。

社区广泛使用的实战技术还依赖：

- **[KJNodes](https://github.com/kijai/ComfyUI-KJNodes)**，作者 [kijai](https://github.com/kijai)（LTX-2.3 NAG、GGUF 加载、分块前馈、多引导）；**[ComfyUI-CacheDiT](https://github.com/Jasonzzt/ComfyUI-CacheDiT)**，作者 Jasonzzt（推理缓存）；**ComfyUI-MelBandRoFormer**（音轨分离）；**[ComfyUI-Frame-Interpolation](https://github.com/Fannovel16/ComfyUI-Frame-Interpolation)**，作者 Fannovel16（FILM）；**comfyui-inpaint-cropandstitch**（Flux.2 局部重绘）；以及 **[GAP LTX 2.3 Motion](https://github.com/GeekatplayStudio/LTX-2-3-LipSync)**，GeekatplayStudio 出品（口型同步/分镜/长音频）。
- **[ComfyUI-Flux2Klein-Enhancer](https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer)**，作者 capitan01R，面向 FLUX.2 Klein 的免训练多参考身份迁移节点套件。注意：PolyForm Noncommercial 许可证（商用需单独授权）。
- **[Smart Image Crop and Stitch](https://github.com/HallettVisual/ComfyUI-Smart-Image-Crop-and-Stitch)**，作者 HallettVisual，面向高分辨率重绘与细节编辑的自动尺寸裁剪/拼接节点对（Apache-2.0）。

v2.5.0 还借助了更多人的工作。同时感谢：

- **[Anima ControlNet-LLLite](https://huggingface.co/kohya-ss/Anima-LLLite)**，作者 [kohya-ss](https://huggingface.co/kohya-ss)，为 Anima 基础模型带来深度、线稿、姿态、涂鸦和蒙版编辑的控制与重绘补丁（由 Comfy-Org 为 ComfyUI 重新打包）。注意：非商用许可证，继承自 Anima 基础权重。
- **[krea2_style_reference](https://huggingface.co/ostris/krea2_turbo_style_reference)** 和 **[ComfyUI-Krea2-Ostris-Edit](https://github.com/ostris/ComfyUI-Krea2-Ostris-Edit)**，作者 [ostris](https://github.com/ostris)，Krea 2 Turbo 图像风格参考 LoRA 及本工具包收录的指令编辑节点；还有 [reverentelusarca](https://huggingface.co/reverentelusarca) 的 **krea2-detail-enhancer-edit-lora**。
- **[JoyAI-Image](https://github.com/jd-opensource/JoyAI-Image)**，JD（jd-opensource）出品，现已原生支持于 ComfyUI 核心的指令图像编辑模型（Apache-2.0）。

完整的逐组件许可信息见 [ATTRIBUTION.md](ATTRIBUTION.md)。如果其中有任何地方错误归属了你的作品，请提 issue，我们会修正。

## 参与贡献

请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。它说明了本工具包接受什么、不接受什么以及为什么，还有任何知识条目必须达到的标准。大型 PR 之前先提 issue 是受欢迎的，通常也更快。

## 许可证

Apache-2.0，见 [LICENSE](LICENSE) 和 [NOTICE](NOTICE)。v3.1.0 及之前的版本为 MIT，该授权继续有效。第三方组件保留各自的许可证。

<div align="center">

Made by **[AI VFX NEWS](https://aivfxnews.com/)**

</div>
