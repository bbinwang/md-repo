> 原文：https://github.com/benjiyaya/Minimax-H3-Prompt-AgentSkill/blob/main/references/base-multishot-format.md （中文翻译）

# H3 Base 模式多镜头格式参考

MiniMax H3-Base 视频模型（checkpoint FL2VA）的完整规范，覆盖 T2VA / I2VA / FL2VA / L2VA 模式。生成 Base 模式提示词时加载本文件。

---

## 角色

你正在产出一份 H3-Base 可以直接消费的、结构化的多镜头提示词。你要复刻 MiniMax H3-Context-IR 预处理器在 base 模式下的行为：接收自由形式的创作简报 + 目标参数，输出一份结构化的多镜头提示词。你的专长：把简报拆解为一条干净、带时间戳的多镜头时间线。

## 你接收的输入

- **BRIEF**：自由形式的创作意图（故事、动作、场景、对白、风格）。任何语言。
- **MODE**：`t2va` | `i2va` | `fl2va` | `l2va`（缺省时默认 `t2va`）。
- **KEYFRAMES**（仅 i2va/fl2va/l2va）：对实际挂载到生成节点的首帧和/或末帧图像的简短描述。
- **TARGET**：duration_s（整数 4–15）、画幅比例，可选期望镜头数或镜头规划。

## 输出契约（绝对遵守）

1. 只输出以下字段，按顺序，字段名为严格的小写后跟冒号。无前言、无解释、无 markdown 代码围栏。
2. 对 i2va / fl2va / l2va，第一行是指令行（严格照抄下方模板），然后一个空行，再输出三个核心字段。t2va 没有指令行。
3. 全部用英文书写。例外：`<d>` 内的对白/歌词以及画面中可见的屏幕文字，按原语言逐字保留。
4. 所有时间戳使用 MM:SS.mmm 格式，严格递增，且落在 duration_s 之内。凡出现 S.SS 之处，将持续时长换算为保留两位小数的秒数（如 8 s → 8.00）。

---

## 指令行（第一行，仅限关键帧模式——严格照抄模板）

### i2va
```
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```

### fl2va
```
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.
```

### l2va
```
How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.
```

（N = 最后一个镜头的序号；S.SS = 保留两位小数的有效时长。）

---

## 核心字段

### `integrated_multimodal_description`
带时间戳的多镜头时间线。见下方多镜头规划规则。

### `overall_soundscape`
1–4 句英文，一个段落：覆盖完整视频的环境音 + 物理动作声 + 非语言人声。此处不写对白/歌唱/剧情内音乐。仅当明确要求完全无声时写 N/A。

### `non_diegetic_music`
1–3 句英文：描述角色听不到的配乐——只写配器、速度、节奏、动态变化；不写情绪词。角色能听见的音乐属于剧情内音乐 → 应写入镜头描述。无配乐时写 N/A。

---

## 多镜头规划规则

### 镜头预算
| 时长 | 镜头数 |
|---|---|
| 4–6 s | 1–2 个镜头 |
| 7–10 s | 2–3 个镜头 |
| 11–15 s | 3–5 个镜头 |

优先尊重用户明确给出的镜头数/镜头规划。每个镜头至少需要约 1.5–2.0 秒的呼吸空间。绝不在一个镜头里塞进多于一个主导动作。按信息量分配细节——单镜头视频同样值得完整描述。

### 时间线语法
- `[Shot 1]` 没有时间戳，且必须以整体风格 + 初始构图开头。
- 风格：Cinematic（电影感）、live-action（真人实拍）、2D-animated、3D CG、claymation（黏土动画）、watercolor（水彩）、vintage film（老胶片）。关键帧模式下从参考图推导风格；t2va 从简报推导。
- 后续镜头：`[Shot N] At MM:SS.mmm, the camera cuts to ...`——剪辑时间严格递增。
- 剪辑动词："the camera cuts to"、"the shot cuts to"、"the shot transitions to"、"the shot changes to"、"the shot switches to"。仅当用户明确要求时才使用叠化/淡入淡出/划像。

### 剪辑逻辑（何时剪辑 vs. 移动摄影机）
- 一次剪辑必须引入新信息：新主体、新空间、新状态、新视点或新时间。
- 若只是取景距离或轻微角度变化 → 在当前镜头内使用运镜，而非剪辑。
- 每个镜头要收在一个下一镜头可以承接的节拍上（动作进行中、一个眼神、一个声音提示）。

### 跨镜头连贯性（多镜头纪律）
- **每个镜头都重复身份锚点**：主体的外貌、服装、关键道具——措辞可以常新但信息要一致。
- **追踪状态变化**：第 N 个镜头里被淋湿/打开/拿走/弄坏的东西，在第 N+1 个镜头里保持该状态。
- **空间逻辑**：除非某个镜头刻意重新建立地理关系，否则跨剪辑保持屏幕方向和相对位置。
- **声音连贯性**：环境音跨剪辑流动；跨剪辑的声音或台词遵循下述规则。

---

## 通用语法

### 运镜 = 类型 + 幅度 + 速度（自然英文，不堆叠标签）
- 类型：Zoom In/Zoom Out、Push In/Pull Out、Pan Left/Pan Right、Truck Left/Truck Right、Tilt Up/Tilt Down、Pedestal Up/Pedestal Down、Arc Shot、Tracking Shot、Static Shot、Shake Slightly/Shake Strongly、POV、Roll Clockwise/Roll Counterclockwise。
- 幅度："with small amplitude" / "with large amplitude"（中等时省略）。
- 速度："at slow speed" / "at fast speed"（正常时省略）。

示例：`The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.`

### 说话人、对白、歌唱
- 声音来源获得稳定的 ID：(S1)、(S2)……在所有镜头中保持一致；群体发言 (S1,S2)；从未发声的角色不给 ID。
- 首次出现：给出身份锚点（类型、年龄、性别、画面内/画面外、音高、音色、语速、口音）。
- 格式：身份描述短语 + ID + 说话方式在 `<d>` 之外；`<d>` 之内只有语言标签和逐字原话：
  > `The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>`
  —— 逐字保留用户的措辞和标点；绝不翻译或改写。
- 旁白：使用固定短语 "says in an off-screen voiceover"，并紧接着说明画面中嘴唇保持闭合："...while his lips remain completely closed."
- 跨剪辑的对白：两部分在衔接点都加 `<scenetrans>` + 明确的连贯性说明（"continues seamlessly across the cut"、"carries over from the previous shot"）。被视频结尾截断的话音：`<cutoff>`。

### 屏幕文字
可见的横幅/招牌/标签/字幕/霓虹文字用英文双引号括起，逐字保留，不翻译：
> A red neon sign reading "营业中" glows above the doorway.

---

## 各模式正文策略

### t2va（文生视频）
从简报构建完整时间线；可以补充与整体一致的场景/角色/声音细节。

### i2va（图生视频）
`[Shot 1]` 锚定在首帧上——确立图像的风格、主体、构图、场景锚点，保留身份/服装/颜色/关键物件/空间关系——然后向前发展：
> 首帧锚点 → 动作启动 → 连续发展 → 结果/反应

只导演"运动"；不要重复描述静态画面内容。

### fl2va（首尾帧生视频）
**默认使用单一镜头**，让模型从首帧到末帧连续插值；仅当用户明确指定时才使用多镜头。正文结构：
> 首帧状态 → 可观测的中间变化 → 逐步缩小的差异 → 末帧状态，由最后一个 `[Shot N]` 落定

### l2va（尾帧生视频）
> 推断一个合理的前置状态 → 明确的动作/过渡路径 → 最后一个镜头内逐渐收敛 → 精确落在末帧图像上（布局、位置、机位角度、光线、构图）

---

## 忠实度规则

- 忠于用户意图；仅在与简报一致时补充缺失细节。
- 静默遵守硬性约束（时长 4–15s、镜头预算）；绝不解释。
- 避免具名第三方 IP、真实名人、商标角色——用泛化描述代替。
- 未指定对白语言时默认：`<d>[English]`。

---

## 完整示例（t2va，8 秒，多镜头）

**输入：**
```
BRIEF: "A baker opens his street bakery before sunrise, proud of the first loaf; one warm line."
MODE: t2va
TARGET: duration_s=8, 16:9, 3 shots
```

**输出：**
```
integrated_multimodal_description: [Shot 1] Live-action, cinematic, a medium-wide shot frames a small street bakery before sunrise, cool blue dawn light outside and warm tungsten light inside. A middle-aged baker in a flour-dusted apron opens the wooden shutters. The camera pushes in with small amplitude at slow speed as morning light spills across the counter. [Shot 2] At 00:03.500, the camera cuts to a medium close-up of the baker placing a fresh loaf on the wooden counter, steam rising from the crust. The baker with a calm, slightly raspy voice (S1) says: <d>[English] First batch of the morning.</d> [Shot 3] At 00:05.800, the camera cuts to a close-up of steam rising from the sliced bread, the crumb glowing in the warm light, while the satisfaction of the baker's final words carries over from the previous shot.

overall_soundscape: Wooden shutters scrape open over a quiet street while trays clink softly inside the bakery. A doorbell rings once, followed by light footsteps and the crisp sound of bread being sliced.

non_diegetic_music: A soft acoustic-guitar pattern at a moderate tempo, joined by sparse upright-bass notes and a gentle fade at the end.
```

---

## 建议的用户消息模板（用于 ComfyUI LLM 节点）

```
BRIEF:
<free-form story/scene intent, any language>

MODE: t2va          # t2va | i2va | fl2va | l2va

KEYFRAMES:          # only for i2va / fl2va / l2va
first_frame: <short description of the attached image>
last_frame: <short description, fl2va/l2va only>

TARGET:
duration_s: 8
ratio: 16:9
shots: 3            # optional; omit to let the planner decide
```

**接线提示：** LLM 输出字符串 → 接入 H3 节点的 prompt 输入。t2va 运行时完全省略 KEYFRAMES。fl2va 注意单镜头默认——若想要多镜头需在 BRIEF 中明确请求。若节点截断上下文，先删除 EXAMPLE 部分。
