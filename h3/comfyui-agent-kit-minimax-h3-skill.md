> 原文：https://github.com/SlavaSexton/ComfyUI-Agent-Kit/blob/main/shared/minimax-h3/SKILL.md （ComfyUI-Agent-Kit 内置 minimax-h3 技能，中文翻译）

---
name: minimax-h3
description: Use when writing or debugging prompts for MiniMax H3 (Hailuo 3) video-with-audio generation, running the open weights locally in ComfyUI, choosing a quant or an acceleration LoRA for the VRAM you have, wiring reference-to-video with images, video or audio, or when a generated clip produces gibberish speech, drifts off a reference identity, garbles audio after a latent upscale, or refuses to run on a build that looks current.
---

# MiniMax H3（Hailuo 3）

H3 可以**同时生成视频与同步的立体声音频**，输入可以是文本、图像、参考视频、参考音频，或任意组合。无论你调用托管 API 还是本地运行开源权重，都是同一个模型家族，但两条路径的接线方式完全不同，而且只有一条是免费的。

**两条路径，不要混淆。**
- **托管 API**：partner 节点 `MinimaxHailuo03TextToVideoNode` / `...FirstLastFrameNode` / `...ReferenceNode`，分类为 `partner/video/MiniMax`。2K 输出，按秒计费，没有本地权重。
- **本地开源权重**：核心节点 `MiniMaxH3ImageToVideo` 与 `MiniMaxH3ReferenceToVideo`，来自 `comfy_extras/nodes_minimax_h3.py`。768p，免费，下文全部讲的是这条路径。

**谁管什么，让你只开一个文件而不是三个。** 本文件管提示词格式与运行规则。旁边的 `reference.md` 管权重、量化规格、加速包及其接线。Kit 中 `MODELS.md` 的 MiniMax 条目管节点级图（每个节点和插槽）以及许可证。三者冲突时以节点代码为准，出现的偏差值得当作 bug 上报。

## 提示词格式不是自由散文

H3-Base 消费的是一个托管提示词精炼器（**H3-Context-IR**）的输出，而它**不**在开源发布中。所以本地要自己按精炼器的输出形状来写。根据 MiniMax 官方的 `VIDEO_PROMPT_WRITING_GUIDE_base_en.md`，格式是一行可选的指令、一个空行，然后三个字段：

```
integrated_multimodal_description: [Shot 1] ... [Shot 2] At 00:04.500, ...

overall_soundscape: ...

non_diegetic_music: ...
```

- `integrated_multimodal_description` 沿时间线承载画面、动作、镜头、说话人、对白和剧情内声音。`overall_soundscape` 概括环境氛围与物理动作的声音。`non_diegetic_music` 是角色听不到的配乐。
- **图像模式需要一个固定的首行。** I2V：`For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.`。首尾帧模式使用同时点名两张图片及其各自落点秒数（保留两位小数）的对齐句。

### 一个完整提示词，从头到尾

不见完整示例，上面的说明都无法落地。这是一个官方格式的 5 秒文生视频简报：

```
integrated_multimodal_description: [Shot 1] Cinematic medium-wide shot, Push In slowly. A bicycle mechanic in
a navy work coat lowers a metal shutter in a narrow workshop at dusk; warm tungsten light spills across
scattered tools and rain-dark pavement outside. He pauses, looks toward the street. At 00:03.200 he switches
off the bench lamp and the frame drops to ambient blue. The mechanic (weathered voice, mid-fifties, speaks
English only) says quietly: <d>[English] That's enough for today.</d>

overall_soundscape: Steady rain on a metal awning, the rolling clatter of the shutter, one soft click of the
lamp switch, distant tyres on wet asphalt. No music from within the scene.

non_diegetic_music: Sparse solo piano, slow, minor key, entering after the shutter closes and fading to
silence on the lamp click.
```

对于**图生视频**，同样的块前面加上那个固定行和一个空行：

```
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] ...
```

注意真正干活的是什么：一个摄影机和声音都能跟得上的物理动作、一个来自固定词表的摄影机运动、用 `<d>` 包裹以保证台词逐字精确的对白，以及两个音频字段保持分离，使剧情内声音和配乐互不打架。

## 对白："语音是胡话" 的最常见原因

说话人有稳定 ID：`(S1)`、`(S2)`、合说的 `(S1,S2)`。**台词放进带语言标签的 `<d>` 里**，而谁在说、怎么说这些信息都放在外面。台词逐字照抄，不要改写或翻译：

```
The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>
```

没有 `<d>`，模型就不会被告知确切的词句，只能即兴编发音。画外音需要确切短语 `says in an off-screen voiceover`，并声明嘴唇保持闭合。台词跨剪辑点时用 `<scenetrans>`，语音被结尾截断时用 `<cutoff>`。屏幕文字用双引号包裹、逐字照抄。

## 摄影机是受控词表

运动类型 + 幅度 + 速度；默认的中等幅度、正常速度直接省略不写：`Zoom In/Out`、`Push In/Pull Out`、`Pan Left/Right`、`Truck Left/Right`、`Tilt Up/Down`、`Pedestal Up/Down`、`Arc Shot`、`Tracking Shot`。

## 参考到视频：给每个文件贴上任务标签

`<Subject N>` 是真正干活的那个，因为它负责绑定素材来源："`<Subject 1>` is the woman whose appearance comes from `<Picture 1>` and whose walking motion comes from `<Video 1>`."（`<Subject 1>` 是外观来自 `<Picture 1>`、走路动作来自 `<Video 1>` 的那位女性。）此外 `<Picture N>` 是构图或画面锚点，`<Video N>` 是剪辑或时序来源，`<Audio N>` 是被复制的信号。

**参考到视频有它自己的输出契约，是六个小节，不是上面的三个字段。** MiniMax 发布了**两份**提示词指南，直到 2026-08-09 本技能只认识第一份。`VIDEO_PROMPT_WRITING_GUIDE_base_en.md` 管 T2VA / I2VA / FL2VA / L2VA，给出本文件开头的那三个字段。`VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` 管全参考模式，开头写道："A complete rewrite output consists of six sections in the following order"（一次完整的改写输出由以下顺序的六个小节组成）：

```
subject_definitions: <Subject 1> is ... whose appearance comes from <Picture 1> ...
summary: ...
retention_analysis: ...
detailed_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: ...
```

`subject_definitions` 声明各参考素材及其标签；`summary` 陈述任务类型、目标视频与参考素材的主要关系；`retention_analysis` 说明每份参考素材如何被保留、迁移或复用；`detailed_description` 按播放顺序承载画面、动作、镜头、声音与对白；最后两个字段与基础模式含义相同。顺序是固定的，且字段名是 **`retention_analysis`**，不是 `retention`。注意这是同一个字符串里的六个命名散文小节，不是 JSON 数组——不管第三方节点的文档怎么说。以上通过阅读 `MiniMaxAI/MiniMax-H3` 上的指南（23 553 字节，2026-08-09）确认；核心节点本身对此不做任何校验，`comfy_extras/nodes_minimax_h3.py` 只接受一个普通多行字符串，所以写错了不会有任何提示——除了结果本身。

官方卡片给出的上限：**9 张图片、3 段视频、3 段音频、共 12 个文件**，每段 2 到 15 秒、合计 15 秒，并且**音频永远不能是唯一参考**。本地 `MiniMaxH3ReferenceToVideo` 节点有**四组** Autogrow 输入族达到这些上限：`ref_images`（最多 9）、`ref_videos`（3）、**`ref_video_audios`（3，同编号参考视频的原声轨）**和 `ref_audios`（3，独立音频）。模板只显示三个图片插槽并不意味着那就是上限。

## 可以照着写的十个生产任务

Krea 2026-08-05 的指南把 H3 提示词定位成制片文书，每条片子一个任务：导演单镜头简报 · 定时三拍预告 · 首尾帧过渡段落 · 网红身份与声线锁定 · 参考动作表演 · 原生音频产品揭示 · 含必现文字与负面词的品牌标题揭示 · 保护区帧内物体替换 · UI 演示 · 全参考导演简报。先选任务，再决定哪个控制必须保住：摄影机、时序、身份、动作来源，还是那个声音事件。

注意他们的示例用 `[0-3s]` 节拍风格，这是可读的速记法，并非 MiniMax 自己的 `[Shot N]` 加 `At 00:04.500` 惯例。两者都能用；本地环境下官方形式是更稳的默认选择。

## 会咬人的运行事实

- **帧数落在网格上。** `length` 必须满足**除以 17 余 5**（124 帧 ≈ 5 秒，73 ≈ 3 秒，362 ≈ 15 秒）。节点称之为 "17k+5 grid"，训练范围约 124 到 362 帧。
- **原生分辨率约 1 MP**，模板默认 **1344 x 768**、24 fps。更高只会消耗时间和显存，不会带来更多真实细节；官方 2K 路线是一次托管端的重生成，未开源。
- **时长：** 训练并测试过的是 5 到 15 秒。更长也能跑，但属于未训练区域。
- **速度：** 开源发布只有**全量注意力**；稀疏注意力承诺稍后提供。这就是它慢的原因，也是下面社区加速方案重要的原因。
- **许可证：** 权重开放但不是开源，且地域条款异常严格。见 `MODELS.md`。

## 出错时怎么查

| 症状 | 最可能的原因 |
|---|---|
| 语音听起来流利但全是胡话 | 台词没有放进 `<d>[Language] ... </d>` 里 |
| 人脸在片中漂移 | 没有 `<Subject N>` 绑定身份来源，或放大后参考素材尺度不对 |
| latent 放大后音频变糊 | `audio_denoise` 留在默认值 1.0（推断原因，未实测）；音频收敛晚，所以第一遍应多跑一些去噪调度 |
| 人群里动画做错了脸 | 参考尺寸设成了 `match`，而身份需要 `max` |
| 加速节点拒绝加载 | 构建版本低于加速包要求；打过的 tag 不代表够新 |
| 输出长度与要求不符 | `length` 掉出了 17k+5 网格 |
