---
name: h3-video-prompt-enhancer
description: "Use when making MiniMax H3 video prompts from media + ideas."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [video, prompt-engineering, minimax-h3, comfyui, text-to-video, image-to-video, creative]
    related_skills: [comfyui]
---

> 原文：https://github.com/benjiyaya/Minimax-H3-Prompt-AgentSkill/blob/main/SKILL.md （技能主文件 SKILL.md，中文翻译）

# H3 Video Prompt Enhancer

## 概述

把用户的粗略视频创意 + 附加素材转化为生产级的 MiniMax H3 视频生成提示词。本技能处理两种 H3 生成模式：

- **Ref2VA** —— 当用户提供参考素材（角色设定图、风格图、参考视频、声音样本）时使用。输出 6 段式结构化提示词。完整规范请加载 `references/ref2va-format.md`。
- **Base MultiShot**（T2VA / I2VA / FL2VA / L2VA）—— 用于文生视频或以图片为锚点的生成。输出带时间戳的多镜头提示词。完整规范请加载 `references/base-multishot-format.md`。

本技能的独特价值：它不只是做到格式合规 —— 在映射到精确的 H3 输出格式之前，还会用专业级的电影化细节（镜头美学、视觉质感、灯光设计、节奏弧线、空间编排、连续性追踪）对创意进行**创造性增强**。质量基准与高级长篇提示词的模式示例请加载 `references/creative-showcase.md`。

## 适用时机

**在以下情况触发：**
- 用户附加了 1 个或多个图片/视频/音频文件，并描述了想创建的视频
- 用户说 "make a video prompt" / "enhance this for H3" / "write a Ref2VA prompt" / "img2vid" / "txt2vid"
- 用户提供视频概念，希望将其结构化为 MiniMax H3 生成格式
- 用户提到 H3、MiniMax、Ref2VA、ComfyUI 视频生成
- 用户粘贴创意简报（CAMERA/LOOK/STYLE 格式），希望转换为 H3 格式

**以下情况不要使用：**
- 非 H3 视频模型（Sora、Runway、Kling 等）—— 输出格式是 H3 专用的
- 纯图片生成提示词
- 不涉及新生成内容的视频剪辑任务

## 第 0 步：判断模式

根据用户附加的素材和表述来判断 H3 模式：

| 用户提供 | 模式 | 格式参考 |
|---|---|---|
| 参考图片/视频/音频（角色设定图、风格参考、声音片段） | **Ref2VA** | `references/ref2va-format.md` |
| 无素材 —— 只有一个文字创意 | **T2VA**（文生视频） | `references/base-multishot-format.md` |
| 1 张图作为首帧 | **I2VA**（图生视频） | `references/base-multishot-format.md` |
| 2 张图（首帧 + 尾帧） | **FL2VA**（首尾帧生视频） | `references/base-multishot-format.md` |
| 仅 1 张图作为尾帧 | **L2VA**（尾帧生视频） | `references/base-multishot-format.md` |

**关键区别：** 图片用作*首/尾帧锚点* = I2VA/FL2VA/L2VA。图片用作*角色/风格参考*（而非帧位置）= Ref2VA。有歧义时询问用户："这张图是帧锚点（视频的首帧或尾帧），还是参考（角色/风格/场景）？"

## 第 1 步：收集参数

在增强之前确认以下参数（缺失时询问，但创意足够清晰时可继续）：

- **duration_s**：4–15 秒（整数）。未指定时默认为 8。
- **aspect ratio**：16:9、9:16、1:1、4:3、21:9。默认为 16:9。
- **shot count**：由规划器决定，或尊重用户明确给出的数量。预算：4–6 秒 → 1–2 个镜头；7–10 秒 → 2–3 个镜头；11–15 秒 → 3–5 个镜头。
- **asset inventory**：每个附加文件是什么、扮演什么角色。按模态编号决定标签：Image k → `<Picture k>` 或 `<Subject N>`；Video k → `<Video k>`；Audio k → `<Audio k>`。

## 第 2 步：创造性增强

这是核心增值环节。拿用户的创意，在七个维度上加以丰富。目标：产出具有专业分镜脚本深度和电影智慧的提示词。每种模式的完整示例请查阅 `references/creative-showcase.md`。

### 增强维度

**1. 镜头身份（Camera Identity）** —— 赋予与场景基调匹配的独特镜头美学：
- 物理类型：手持、三脚架、无人机、斯坦尼康、移动轨道、监控摄像头、行车记录仪、POV、环绕镜头
- 保留的瑕疵（风格适当时）：手部抖动、自动对焦拉风箱、曝光波动、镜头光晕、运动模糊、生硬变焦
- 格式/美学暗示：16mm 胶片、DV 磁带、干净数字、变形宽银幕、复古摄像机、广播电视

**2. 视觉质感（Visual Texture / LOOK）** —— 定义画质与色彩科学：
- 颗粒/噪点：胶片颗粒、电子噪点、干净数字、VHS 扫描纹、轻微模糊
- 色彩基调：暖/冷、高饱和/低饱和、高/低对比度、自然肤色
- 灯光设计：自然光、棚拍、霓虹、黄金时刻、混合光源、实景实用光源
- 灯光过渡：如果镜头之间场景变化，描述光线如何切换

**3. 节奏弧线（Pacing Arc）** —— 规划整个时长内的能量推进：
- 铺垫模式：安静→有活力、紧张→释放、缓慢铺垫→爆发峰值→沉淀、稳定节奏
- 剪辑节奏：向高潮加速剪辑、缓慢沉思的停留、踩着音乐节拍剪辑
- 让节奏弧线匹配创意简报的情感意图

**4. 角色细节（Character Detail）** —— 用具体性充实每个出镜人物：
- 外貌：年龄段、体型、发色/发型、肤色、独特特征（疤痕、雀斑、异色瞳）
- 服装：带颜色、材质、质感、配饰的具体衣物 —— 注明跨场景或跨时间的变化
- 视觉签名：一个反复出现的颜色或视觉元素，让角色在每个镜头中都能被一眼认出（例如 "electric purple energy trails"、"glossy teal jacket reflections"、"always wears a red scarf"）
- 覆盖度提示：完整描述着装 —— 除非用户明确要求，避免暗示暴露服装

**5. 空间地理（Spatial Geography）** —— 针对动作序列或多场景视频：
- 屏幕方向：谁从哪里进入、运动矢量（Left→Right、Deep→Front、前景↔背景）
- 关键动作时刻：定义整个序列的 2–3 个关键运动节拍
- 环境布局：空间里有什么、如何打光、反射表面、纵深

**6. 连续性推进（Continuity Progression）** —— 追踪镜头之间的变化，让视频显得连贯：
- 物理状态：损伤累积、头发变乱、衣服变湿/撕裂/沾灰
- 环境：道具移动、灯光闪烁、天气变化、碎片散落
- 情绪：表情和肢体语言随时间线自然演变

**7. 声音设计规划（Sound Design Plan）** —— 规划完整的音频图景：
- 环境音：房间底噪、环境氛围、背景人声、车流、风声
- 物理动作声：脚步、撞击、布料摩擦、门轴吱呀、液体倾倒
- 非剧情配乐：配器、速度、节奏、动态变化（写入 `non_diegetic_music` 字段）
- 剧情内音乐：有可见声源的音乐 —— 收音机、音箱、现场演奏（写入镜头描述）
- 对白 vs 旁白：清楚标注哪些是镜头前说出的、哪些是画外旁白

### 单镜头质量标准

分镜脚本中的每个镜头必须明确：
- **构图**：景别（远景、中景、近景、特写、微距），角度（平视、低角度、高角度、俯拍、荷兰角）
- **镜头运动**：用自然英语写 类型 + 幅度 + 速度（例如 "The camera pushes in with small amplitude at slow speed"）
- **主体动作**：每个镜头恰好一个主导动作 —— 绝不塞进多个动作
- **环境/灯光**：能看到什么、如何打光、一天中的时间线索
- **声音提示**：这个具体时刻能听到什么
- **参考标签**（仅 Ref2VA）：被参考内容在哪里出现或生效

## 第 3 步：格式化与输出

加载对应的格式参考文件，产出最终 H3 提示词。

**Ref2VA** → 加载 `references/ref2va-format.md`。严格按顺序输出 6 个段落：
1. `subject_definitions:` —— 每个被追踪条目一行
2. `summary:` —— 任务类型前缀 + 一段话
3. `retention_analysis:` —— 每个标签的保真度标记
4. `detailed_description:` —— 350–500 词，以风格开头，随后是 `[Shot N]` 时间线
5. `overall_soundscape:` —— 1–4 句
6. `non_diegetic_music:` —— 1–3 句或 N/A

**Base MultiShot** → 加载 `references/base-multishot-format.md`。输出：
1. 指令行（仅 I2VA/FL2VA/L2VA —— 使用参考文件中的精确模板）
2. `integrated_multimodal_description:` —— 带时间戳的多镜头时间线
3. `overall_soundscape:` —— 1–4 句
4. `non_diegetic_music:` —— 1–3 句或 N/A

### 关键格式规则（两种模式通用）

- 只输出指定字段 —— 不加前言、解释、markdown 围栏、评论
- 全部用英文书写。例外：`<d>` 标签内的对白/歌词以及可见的屏幕文字保持原语言、原样保留
- 时间戳：`[Shot 1]` 没有时间戳，以风格 + 初始构图开头。后续镜头：`[Shot N] At MM:SS.mmm, the camera cuts to ...`，时间在时长内严格递增
- 一次剪辑必须带来新信息（主体、空间、状态、视点、时间）。如果只有距离/角度变化，用镜头运动代替剪辑
- 镜头运动 = 运动类型 + 幅度 + 速度，写成自然英语动作，而不是堆叠标签
- 对白格式：身份识别短语 + 说话人 ID + 语气表演放在 `<d>` 外；`<d>` 内只有语言标签 + 原话：`<d>[English] Wait for us!</d>`
- 用户对白原样保留 —— 绝不翻译、改写或转述
- 旁白：用精确短语 "says in an off-screen voiceover" + 紧接着说明 "while his/her lips remain completely closed"
- 屏幕文字（招牌、霓虹、字幕）：英文双引号，原样保留，不翻译
- 避免具名第三方 IP、真实名人、商标角色 —— 用泛化描述

### 镜头运动词汇表

类型：Zoom In/Out、Push In/Pull Out、Pan L/R、Truck L/R、Tilt Up/Down、Pedestal Up/Down、Arc Shot、Tracking Shot、Static Shot、Shake Slightly/Strongly、POV、Roll CW/CCW。
幅度："with small amplitude" / "with large amplitude"（中等时省略）。
速度："at slow speed" / "at fast speed"（正常时省略）。

## 第 4 步：呈现给用户

生成 H3 提示词后：
1. 把完整提示词放在代码块中呈现，便于直接复制
2. 说明检测到的是哪种模式及原因
3. 标记所做的一切假设（例如 "Assumed 8s duration and 16:9 — adjust if needed"）
4. 主动提出可以细化具体方面：镜头美学、节奏、角色细节、镜头数量、声音设计

## 来自 Showcase 的创意模式

用户维护着代表质量基准的高级长篇提示词示例。完整示例请加载 `references/creative-showcase.md`。关键可迁移模式：

**长篇叙事**（蒙太奇、一天纪实、剧情）：
- 在分镜之前用显式的 CAMERA/LOOK/STYLE 区块定义美学
- 服装与场景随时间推进，附带灯光过渡
- 旁白在非同步画面之上承载情感叙事
- 节奏从安静开场铺垫到高能结尾
- 每镜头分镜脚本，含时间、动作和 VO 台词

**动作编排**（战斗、追逐、体育）：
- 每角色色彩锁定 —— 每个角色的特效/轨迹/反射都有签名色
- 显式的空间布局与屏幕方向（Deep→Front、Left→Right）
- 动作矢量 —— 定义每个镜头的关键运动时刻
- 渐进连续性 —— 损伤累积、头发被风吹乱、出现灰尘/裂纹
- 严格执行镜头数量 —— 说出数量并坚持
- 环境响应性 —— 全息图闪烁、地面反射、墙壁因动作而开裂

## 常见陷阱

1. **把 Ref2VA 参考图当作帧锚点。** 角色设定图或风格参考是 `<Subject>`，不是 `<Picture>`。只有当图片确实是具体的帧位置（首帧、关键帧、尾帧）时才单独使用 `<Picture N>`。拿不准时，把图片引用写进相关的 `<Subject N>` 行内。

2. **在一个镜头里塞多个动作。** 每个镜头一个主导动作 —— 这是 H3 的硬性约束。如果简报描述了顺序动作，用剪辑拆分到多个镜头。

3. **遗漏镜头运动。** 每个镜头都需要显式的镜头运动规范 —— 相机不动也要写 "Static Shot"。省略会让模型瞎猜。

4. **跨镜头角色身份不一致。** 在每个镜头中重复身份锚点（发型、服装、关键道具），措辞新鲜但保持一致。如果第 3 镜头发乱了，第 4 镜头也要保持乱。

5. **镜头数量与时长不匹配。** 尊重预算：4–6 秒 → 1–2 个镜头；7–10 秒 → 2–3 个镜头；11–15 秒 → 3–5 个镜头。不要给 5 秒视频规划 5 个镜头。

6. **混用剧情内与非剧情音乐。** 角色能听到的音乐（收音机、现场演奏、手机外放）写进镜头描述。角色听不到的背景配乐写进 `non_diegetic_music`。同一段音乐绝不两处都写。

7. **（Ref2VA）编造参考标签。** 绝不创建超出 `subject_definitions` 定义的标签。`<Subject 3>` 在它出现的每个段落中含义相同。不同模态的不同索引独立编号。

8. **翻译或改写对白。** 在 `<d>` 标签内保留用户原话 —— 包括标点、犹豫语气和语言。用户用其他语言写的，绝不翻译成英文。

9. **跳过风格开场。** `detailed_description`（Ref2VA）或 `integrated_multimodal_description`（Base）必须在 `[Shot 1]` 之前以 1–2 句整体风格描述开场。不要直接跳进第一个镜头。

10. **时间戳混乱。** `[Shot 1]` 从不带时间戳。之后每个镜头都需要 `At MM:SS.mmm` 且时间严格递增。把时长正确转换为秒（8s → 指令行中的 8.00）。

## 验证清单

- [ ] 根据附加素材和用户意图正确检测模式
- [ ] 七个增强维度全部应用（镜头、质感、节奏、角色、空间、连续性、声音）
- [ ] 输出只包含必需的 H3 字段 —— 无前言、无 markdown 围栏、无多余评论
- [ ] 时间戳严格递增且落在 duration_s 之内
- [ ] 每个镜头恰好一个主导动作
- [ ] 每个镜头都指定了镜头运动（类型 + 幅度 + 速度）
- [ ] 跨所有镜头角色身份一致（每个镜头重复锚点）
- [ ] 对白以 `<d>[Language] ...</d>` 格式原样保留
- [ ] `[Shot 1]` 之前有风格开场
- [ ] （仅 Ref2VA）参考标签使用一致，且未超出 subject_definitions 编造
- [ ] 时长（4–15 秒）和宽高比已指定，或已假设并标记
- [ ] 无具名 IP、名人或商标角色名
- [ ] 剧情内音乐在镜头描述中，非剧情配乐在 `non_diegetic_music` 中
