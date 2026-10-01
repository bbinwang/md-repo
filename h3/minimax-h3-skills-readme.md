> 原文：https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills （MiniMax-H3 官方 Skills 目录 README，中文翻译）

> 译注：仓库内 8 个风格技能已自带中文版（`SKILL.cn.md`），可直接阅读原文件。

# MiniMax H3 Skills

本目录包含 [MiniMax H3](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/README.md) 随附的技能：**1 个提示词编写技能**和 **8 个特定风格的视频生成技能**。每个技能位于独立文件夹中，包含可安装的 `SKILL.md`（风格技能还附带中文版 `SKILL.cn.md`）及其所需的参考资料。

## 状态

这些技能仍在积极维护和持续演进中。8 个风格技能同时提供双语 `SKILL.md`/`SKILL.cn.md`；`h3-prompt-writing` 目前仅有英文版。

## 安装

使用 [skills CLI](https://github.com/vercel-labs/skills) 安装技能：

```bash
# 列出本仓库中所有可用技能
npx skills add https://github.com/MiniMax-AI/MiniMax-H3 --list

# 安装全部技能
npx skills add https://github.com/MiniMax-AI/MiniMax-H3 --skill '*'

# 安装单个技能
npx skills add https://github.com/MiniMax-AI/MiniMax-H3 --skill h3-prompt-writing
```

## 技能列表

### h3-prompt-writing

[SKILL.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing/SKILL.md)

为全部五种生成模式（T2VA、I2VA、FL2VA、L2VA、Ref2VA）编写结构化的 MiniMax H3 视频生成提示词。该技能将多模态请求改写为 H3 的提示词结构——`integrated_multimodal_description`、`overall_soundscape` 和 `non_diegetic_music`——对齐关键帧，并为图片、视频和音频定义引用标签。它在 [`references/`](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing/references/) 下附带两份提示词指南：

- [`base-en.txt`](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing/references/base-en.txt) —— 基础文本/关键帧模式
- [`ref-en.txt`](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing/references/ref-en.txt) —— 全参考（Ref2VA）模式

### minimalist-product-ad-generator

<p align="center">
  <img src="https://github.com/MiniMax-AI/MiniMax-H3/raw/main/assets/minimalist-product-ad-generator.gif" alt="minimalist-product-ad-generator" width="240">
</p>

将产品图片和广告需求转化为简洁、极简风格的产品广告短片，适用于电商推广和产品发布。该技能会确认格式和产品变体、提炼卖点、撰写简洁的英文广告文案、规划卡点排版和分镜，并生成具有精致镜头语言的高端产品影片。不适用于 KOC 真人出镜口播广告、通用剪辑或复杂的屏幕演示。

[SKILL.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/minimalist-product-ad-generator/SKILL.md) · [SKILL.cn.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/minimalist-product-ad-generator/SKILL.cn.md)

### 3d-animation-short-generator

<p align="center">
  <img src="https://github.com/MiniMax-AI/MiniMax-H3/raw/main/assets/3d-animation-short-generator.gif" alt="3d-animation-short-generator" width="240">
</p>

从一个故事创意出发，通过有序的制作流程创作完整的风格化 3D 动画短片：项目简报、故事大纲、角色和环境卡片、标准化镜头规划、文字或可选的铅笔分镜、视频模型选择、单镜头生成、组装、BGM 匹配和最终审校。专为端到端的叙事动画打造，可强力控制角色一致性、场景连续性、节奏、镜头、表演和音频。不适用于单张图片、简单剪辑、写实真人实拍或单个独立片段。

[SKILL.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/3d-animation-short-generator/SKILL.md) · [SKILL.cn.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/3d-animation-short-generator/SKILL.cn.md)

### papercraft-stop-motion-explainer

<p align="center">
  <img src="https://github.com/MiniMax-AI/MiniMax-H3/raw/main/assets/papercraft-stop-motion-explainer.gif" alt="papercraft-stop-motion-explainer" width="240">
</p>

通过触感十足的手工纸艺视觉来讲解科学、教育或通识内容。该技能会提取学习目标和视觉隐喻、提出创意方向、设计纸质角色、分层立体场景和道具、创建预览概念以及图片和视频提示词，并规划分镜、镜头运动、转场和音效，全程配有分阶段确认和审校清单。它输出可直接投入制作的纸艺定格动画讲解包，也可只输出选定的资产，如静态提示词、图片序列提示词、短视频提示词或分镜。最适合剪纸、立体书、分层立体场景和微缩定格讲解类内容。

[SKILL.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/papercraft-stop-motion-explainer/SKILL.md) · [SKILL.cn.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/papercraft-stop-motion-explainer/SKILL.cn.md)

### brand-promo-video-generator

<p align="center">
  <img src="https://github.com/MiniMax-AI/MiniMax-H3/raw/main/assets/brand-promo-video-generator.gif" alt="brand-promo-video-generator" width="240">
</p>

面向为品牌、产品、网站、应用、店铺或个人项目制作宣传内容的营销人员和创作者。该技能会整理品牌信息和素材来源、选定叙事方向、规划精确的节拍和镜头、生成所需的图片、视频、旁白或音乐，并完成组装和交付前审校。它输出一支突出产品能力、使用场景和行动号召的宣传短片。最适合产品发布、网站展示和社交推广；不适用于在未获授权素材的情况下模仿真实品牌标识，或虚构产品功效。

[SKILL.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/brand-promo-video-generator/SKILL.md) · [SKILL.cn.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/brand-promo-video-generator/SKILL.cn.md)

### music-video-subtitle-generator

<p align="center">
  <img src="https://github.com/MiniMax-AI/MiniMax-H3/raw/main/assets/music-video-subtitle-generator.gif" alt="music-video-subtitle-generator" width="240">
</p>

面向制作 AI 音乐视频或带歌词排版的情感短片的音乐人、视频创作者和社交媒体剪辑师。该技能会分析节拍和人声时机、分离角色/场景/文字参考、设计随节拍律动的空间排版、将长作品拆解为相互衔接的镜头、审校提示词，并为 H3 或其他视频工具路由生成。它输出 MV 概念、镜头提示词、歌词文字方案和拼接指导。最适合风格化 MV 和字幕驱动的音乐视觉作品。

[SKILL.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/music-video-subtitle-generator/SKILL.md) · [SKILL.cn.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/music-video-subtitle-generator/SKILL.cn.md)

### co-op-game-intro-generator

<p align="center">
  <img src="https://github.com/MiniMax-AI/MiniMax-H3/raw/main/assets/co-op-game-intro-generator.gif" alt="co-op-game-intro-generator" width="240">
</p>

创作双人合作游戏的菜单或开场动画。该技能会锁定身份特征，在固定的菜单框架上（配色、按钮、图标和排版相互协调）生成一张待确认的概念图，然后基于确认结果为最终视频重构角色、UI 文案和事件时机指令。它输出一部包含两个角色、玩家卡片和菜单交互动画的合作游戏开场片。最适合游戏概念展示、角色主导的菜单和社交内容。

[SKILL.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/co-op-game-intro-generator/SKILL.md) · [SKILL.cn.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/co-op-game-intro-generator/SKILL.cn.md)

### paper-collage-explainer-generator

<p align="center">
  <img src="https://github.com/MiniMax-AI/MiniMax-H3/raw/main/assets/paper-collage-explainer-generator.gif" alt="paper-collage-explainer-generator" width="240">
</p>

为旁白、知识点、观点或抽象主题赋予触感十足的纸拼贴视觉语言。该技能会提取含义、提出视觉隐喻、准备制作方案和分镜、生成经确认的半调拼贴静态图，然后创建带纸张运动和触感音效的定格动画片段，最后可选进行成片组装。默认保留拼贴音效，除非另行要求，否则不添加 BGM、旁白或字幕。最适合讲解类内容、观点表达、故事视觉和社交 B-roll 素材。

[SKILL.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/paper-collage-explainer-generator/SKILL.md) · [SKILL.cn.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/paper-collage-explainer-generator/SKILL.cn.md)

### handdrawn-live-video-generator

<p align="center">
  <img src="https://github.com/MiniMax-AI/MiniMax-H3/raw/main/assets/handdrawn-live-video-generator.gif" alt="handdrawn-live-video-generator" width="240">
</p>

创作将粗糙的发光手绘动画与实拍空间相融合的超现实短片。该技能会明确物理接触点、设计连续的形态变化、逃脱路线和延迟的手持追逐运动，然后用用户的语言撰写一个可复用的 15 秒 16:9 视频提示词。确认后会推荐使用 MiniMax H3 生成，并检查接触真实感、镜头延迟、粗糙发光笔触质感和非恐怖基调。最适合单场景创意短片，不适用于精致 CG、恐怖惊吓、毛绒角色或多场景剪辑。

[SKILL.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/handdrawn-live-video-generator/SKILL.md) · [SKILL.cn.md](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/handdrawn-live-video-generator/SKILL.cn.md)

## 参与贡献

这些技能仍在持续改进中，欢迎社区贡献。如果你优化了现有技能或添加了新技能，请提交 PR——贡献或优化技能可获得 API 额度奖励。
