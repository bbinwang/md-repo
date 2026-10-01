> 原文：https://github.com/duckyshell/ComfyUI-MiniMaxH3-Prompt-Writer/blob/8292bb40b41c1e20271bbee9ed1a4d87b6281029/guides/VIDEO_PROMPT_WRITING_GUIDE_base_en.md （ComfyUI-MiniMaxH3-Prompt-Writer 内置副本，与 MiniMax 官方 [VIDEO_PROMPT_WRITING_GUIDE_base_en.md](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md) 内容一致，中文翻译）

# 视频提示词写作指南（T2VA / I2VA / FL2VA / L2VA）

## 1. 任务概述

- **T2VA**（文生视频音频）：从文本构建完整的视听时间线。
- **I2VA**（首帧图生视频音频）：T2VA 主体 + 首帧对齐指令 [instruction] + 从首帧向前发展的视觉路径。
- **FL2VA**（首尾帧生视频音频）：T2VA 主体 + 首尾帧对齐指令 + 从首帧连续过渡到尾帧的路径。
- **L2VA**（尾帧图生视频音频）：T2VA 主体 + 尾帧对齐指令 + 从一个合理的前置状态收敛到尾帧的路径。

## 2. 最终提示词结构

### 2.1 第一部分：对齐指令

**T2VA** 没有图像对齐指令，直接以三个核心字段开头。

**I2VA** 始终使用：

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```

**FL2VA** 始终使用：

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.
```

**L2VA** 始终使用：

```text
How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.
```

其中 `N` 是实际最后一个分镜 [Shot] 的序号，`S.SS` 是有效视频时长，保留两位小数。该指令必须是最终提示词的第一行，其后空一行再接核心字段。

### 2.2 第二部分：三个核心字段

```text
integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```

- **integrated_multimodal_description**（综合多模态描述）：沿时间线描述画面、动作、分镜、说话人、对白、歌唱以及剧情内声音 [diegetic audio]。
- **overall_soundscape**（整体声景）：概括整个视频中的环境音、物理动作声以及人声非语言声。
- **non_diegetic_music**（非剧情音乐）：描述角色听不到、只有观众能听到的背景音乐。

## 3. 如何把关键帧融入多模态描述

### 3.1 I2VA：从图像出发，向前发展

`<Picture 1>` 是视频 0.00 秒处的实际首帧，属于 `[Shot 1]`。描述应先确立图像中的风格、主体、构图和场景锚点，再描述下一个动作。人物身份、服装、颜色、关键道具和空间关系应保持一致。

推荐结构：**首帧锚定 → 动作起始 → 连续发展 → 结果或反应**。

### 3.2 FL2VA：描述首尾帧之间的路径

图 1 是开头，图 2 是结尾。重点描述主体如何移动、姿态如何变化、道具如何被操作、构图如何演变，以及场景或光线如何过渡。

FL2VA 通常倾向使用单一分镜，以便模型能从首帧到尾帧连续插值。只有在明确指定时才使用多个分镜。尾帧必须由视频末尾的最后一个 `[Shot N]` 到达。

推荐结构：**首帧状态 → 可观察的中间变化 → 差异逐步收窄 → 尾帧状态**。

### 3.3 L2VA：推断开头，结尾落在图像上

`<Picture 1>` 是视频的尾帧，属于最后一个 `[Shot N]`；它天然不属于 Shot 1。根据用户意图和尾帧推断一个合理的前置状态，然后描述人物、道具、镜头和场景如何逐步逼近参考图像。

推荐结构：**合理的前置状态 → 明确的动作与过渡路径 → 最后一个分镜中逐步收敛 → 落在尾帧上**。

## 4. 三个共享核心字段的写法

### 4.1 沿时间线展开多模态描述

`integrated_multimodal_description` 是改写后提示词的主体。每个细节都应对应可见或可听的内容：视觉风格、初始构图、主体外观与位置、场景与关键道具、动作与反应、镜头切换、口头语言以及同步的剧情内声音。

在 `[Shot 1]` 开头，声明整体风格和初始构图。常见风格包括 `Cinematic`（电影感）、`live-action`（真人实拍）、`2D-animated`（二维动画）、`3D CG`（三维 CG）、`claymation`（黏土动画）、`watercolor`（水彩）和 `vintage film`（复古胶片）。关键帧任务应从参考图推导风格；T2VA 则从用户文本中选择。

```text
[Shot 1] Live-action, cinematic, a medium-wide shot frames...
```

### 4.2 分镜与切换

第一个分镜不加时间戳。后续分镜使用递增的分镜编号，且每个分镜以一个严格递增、落在视频时长内的切换时间开头：

```text
[Shot 2] At 00:03.500, the camera cuts to...
```

普通切换使用 `the camera cuts to`、`the shot cuts to`、`the shot transitions to`、`the shot changes to` 或 `the shot switches to`。仅当用户明确要求时，才可使用叠化 [cross-dissolve]、淡入淡出 [fade] 或划像 [wipe]。每次切换都应引入关于主体、空间、状态、视点或时间的新信息。如果只需改变景别或轻微角度，优先使用镜头运动。

### 4.3 镜头运动：运动类型 + 幅度 + 速度

一个完整的镜头运动表达包含三个维度：**运动类型 [motion type]** 定义镜头如何移动，**幅度 [amplitude]** 定义构图变化的范围，**速度 [speed]** 定义变化的节奏。仅在有意义时才写幅度和速度；中等幅度和正常速度通常省略。

| 维度 | 可用表达 | 说明 |
|-|-|-|
| 运动类型 | `Zoom In / Zoom Out` | 机身不动，焦距变化 |
| 运动类型 | `Push In / Pull Out` | 镜头前移 / 后移 |
| 运动类型 | `Pan Left / Pan Right` | 镜头原位水平摇转 |
| 运动类型 | `Truck Left / Truck Right` | 镜头水平平移 |
| 运动类型 | `Tilt Up / Tilt Down` | 镜头原位垂直摇转 |
| 运动类型 | `Pedestal Up / Pedestal Down` | 整机上升 / 下降 |
| 运动类型 | `Arc Shot` | 镜头绕主体弧线运动 |
| 运动类型 | `Tracking Shot` | 镜头跟随移动的主体 |
| 运动类型 | `Static Shot` | 机位与镜头保持静止 |
| 运动类型 | `Shake Slightly / Shake Strongly` | 轻微 / 强烈镜头晃动 |
| 运动类型 | `POV` | 主观视点 |
| 运动类型 | `Roll Clockwise / Roll Counterclockwise` | 镜头绕光轴顺时针 / 逆时针旋转 |
| 幅度 | `with small amplitude` | 小范围变化 |
| 幅度 | `with large amplitude` | 大范围变化 |
| 速度 | `at slow speed` | 缓慢运动 |
| 速度 | `at fast speed` | 快速运动 |

镜头运动应写成镜头内自然的英文动作，而不是堆叠成句末的独立标签：

```text
The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.
The camera pans right with large amplitude at fast speed, revealing the open doorway.
The camera holds a static shot as the runner exits the frame.
```

### 4.4 说话人、对白与歌唱

说话、唱歌或发出画外人声的主体使用稳定的编号 ID，如 `(S1)`、`(S2)`。当多个已编号的说话人一起说话或唱歌时，使用复合 ID，如 `(S1,S2)`。同一说话人在各分镜中保持同一 ID；从不发声的角色不分配说话人 ID。

说话人首次出现时，应从画面和声音上下文提供足够信息以建立稳定身份，例如角色类型、年龄、性别、是否出镜、音高、音色、语速或口音。说话人的身份描述、ID、动作和语气放在 `<d>` 之外；`<d>` 内只包含语言标签和用户实际提供的口头内容。逐字保留原始的每一个词和标点，不翻译、不改写。

```text
The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>
The two children (S1,S2) shout together, <d>[English] Wait for us!</d>
```

旁白 [voiceover] 使用固定短语 `says in an off-screen voiceover`。每个旁白 `<d>` 块之后应立即声明对应的画面中角色嘴唇保持闭合：

```text
The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d> while his lips remain completely closed.
```

同一句对白或歌词跨越切换点时，在两部分的连接处使用 `<scenetrans>`，并明确说明声音跨切换延续。当语音被视频结尾截断时使用 `<cutoff>`。连续性可用 `continues seamlessly across the cut`、`continues uninterrupted into the next shot`、`carries over from the previous shot` 或 `remains audible across the transition` 表达。

### 4.5 画面内文字

画面中实际可见的横幅、招牌、标签、字幕或霓虹文字，放入英文双引号中。逐字保留原文与标点，不做翻译。

```text
A red neon sign reading "营业中" glows above the doorway.
```

### 4.6 overall_soundscape

用一段连续的 1–4 句英文概括整个视频中的环境音、物理动作声和人声非语言声，例如风、雨、车流、脚步、布料摩擦、撞击、呼吸、笑声或喘息。对白、歌唱和剧情内音乐已属于多模态描述，不应在此重复。仅当用户明确要求全片完全无声时才使用 `N/A`。

```text
overall_soundscape: Steady rain taps against the café windows while low room ambience continues underneath. The entrance bell rings once, followed by wet footsteps and the soft scrape of a chair.
```

### 4.7 non_diegetic_music

用 1–3 句英文描述角色听不到、只有观众能听到的背景音乐。聚焦配器、速度、节奏和动态变化；不要使用抽象的情绪词，也不要解释配乐的情感功能。角色能听到的歌唱、乐器、广播、电视或手机音乐属于剧情内事件，应写进多模态描述。没有非剧情音乐时使用 `N/A`。

```text
non_diegetic_music: Sparse piano notes at a slow tempo, joined by sustained low strings that gradually increase in volume before fading out.
```

## 5. 案例

### 案例 1：T2VA

没有参考图时，直接从文本构建完整时间线。可以添加与用户意图保持一致的场景、人物、动作和声音细节。

```text
integrated_multimodal_description: [Shot 1] Live-action, cinematic, a medium-wide shot frames a baker opening the shutters of a small street bakery before sunrise. The camera pushes in with small amplitude at slow speed as the middle-aged baker with a calm, slightly raspy voice (S1) places a fresh loaf on the wooden counter and says: <d>[English] First batch of the morning.</d> [Shot 2] At 00:05.000, the camera cuts to a close-up of steam rising from the sliced bread while the baker's final words carry over from the previous shot.

overall_soundscape: Wooden shutters scrape open over a quiet street as trays clink softly inside the bakery. The doorbell rings once, followed by light footsteps and the crisp sound of bread being sliced.

non_diegetic_music: A soft acoustic-guitar pattern at a moderate tempo, joined by sparse upright-bass notes and a gentle fade at the end.
```

### 案例 2：I2VA

先写首帧对齐指令，再以图 1 中的主体、构图和场景作为 Shot 1 的起点，然后描述场景如何继续发展。

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, the young woman shown in <Picture 1> remains beside the rain-covered train window, preserving her appearance, clothing, seat position, and the carriage layout. The camera trucks right with small amplitude at slow speed as she lifts her gaze from the folded letter toward the passing city lights. Her reflection moves across the glass while the quiet, breathy young woman (S1) says: <d>[English] I get off at the next station.</d> She folds the letter along its existing crease.

overall_soundscape: The train wheels produce a steady metallic rhythm beneath a low ventilation hum. Rain ticks against the window while paper rustles softly in her hands.

non_diegetic_music: Sustained cello notes at a slow tempo with widely spaced piano tones, gradually decreasing in volume.
```

### 案例 3：FL2VA

两张图分别锚定开头和结尾。主体部分不应重复两段静态图像描述，而应提供连接二者的运动路径。以下示例为 8 秒单一分镜。

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 8.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, a rain-soaked cyclist begins in the position and framing established by Picture 1, holding a closed black umbrella beside a silver bicycle. The camera pulls out with small amplitude at slow speed as she releases the bicycle handle, raises the umbrella above her shoulder, and presses the runner upward until the canopy opens. Water rolls from the expanding fabric while she steps beneath it, rotates the handle into the final angle, and settles into the pose, spacing, and composition established by Picture 2 at the end of the shot.

overall_soundscape: Rain falls steadily on the pavement, followed by the metallic click of the umbrella runner and the soft snap of the canopy opening. Water drips from the bicycle frame as distant traffic passes.

non_diegetic_music: N/A
```

### 案例 4：L2VA

图像只锚定最终时刻。先建立一个兼容的前置状态，再让动作、道具状态和构图在最后一个分镜中逐步落在图 1 上。以下示例为 6 秒单一分镜。

```text
How the reference pictures align with the target video — <Picture 1> (from [Shot 1]) aligns with the 6.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, a close shot begins with an intact drinking glass near the edge of a dark wooden table, while the same hand and sleeve visible in <Picture 1> approach from the right. The camera pushes in with small amplitude at slow speed as the fingertips strike the rim. The glass tips, falls, and hits the floor with a sharp impact; cracks spread through it as fragments slide outward. Toward the end, the moving pieces lose momentum and settle into the exact broken arrangement, hand position, camera angle, lighting, and final composition established by <Picture 1>.

overall_soundscape: Fingertips tap the glass before it scrapes across the tabletop, falls, and breaks with a sharp crash. Small fragments scatter and gradually stop sliding across the floor.

non_diegetic_music: A low electronic pulse at a slow tempo, ending immediately after the glass breaks.
```
