> 原文：https://github.com/filliptm/ComfyUI_Fill-Nodes/blob/a32f9b6a5a55528731d9e6c38a2fd2ce89cb2819/nodes/audio/prompt_guides/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md （ComfyUI_Fill-Nodes 内置副本，与 MiniMax 官方 [VIDEO_PROMPT_WRITING_GUIDE_ref_en.md](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md) 内容一致，中文翻译）

# 全参考模式（Full-Reference）改写输出格式指南

本指南说明全参考模式下改写输出的组织结构与撰写方式。

所有六个改写部分均以英文撰写。仅以下内容保留原语言：`<d>` 内的对白与歌词，以及画面中可见的文字。

**描述细致度：** `detailed_description` 应尽可能详尽、明确。对于每个镜头，须清楚交代当前构图、主体外观与位置、环境与光照、动作与状态变化、镜头运动、当前声音，以及参考内容实际出现或生效的位置。避免将描述压缩为剧情梗概或参考关系清单。

> 镜头、镜头运动、说话人、对白与普通声音的基础格式与 Video Prompt Writing Guide（T2VA / I2VA / FL2VA / L2VA）共享。本指南聚焦全参考模式特有的参考标签、分析部分及格式差异。

## 1. 整体结构

一份完整的改写输出按以下顺序包含六个部分：

| 部分 | 用途 |
| --- | --- |
| `subject_definitions` | 定义被参考的内容及其参考标签 |
| `summary` | 概括任务类型、目标视频及主要参考关系 |
| `retention_analysis` | 描述被参考内容如何被保留、迁移或复用 |
| `detailed_description` | 按播放顺序描述画面、动作、镜头、声音与对白 |
| `overall_soundscape` | 概括环境氛围与物理声音 |
| `non_diegetic_music` | 描述仅观众可闻的背景音乐 |

## 2. 参考标签与定义（`subject_definitions`）

全参考改写使用四类标签来标识被参考内容的来源与角色：

| 标签 | 含义 |
| --- | --- |
| `<Subject N>` | 从参考素材中抽象出来、可在目标视频中复用或修改的可见内容 |
| `<Picture N>` | 用作具体目标帧或分镜规划锚点的参考图片 |
| `<Video N>` | 提供剪辑源、续接起点或整段时间结构的参考视频 |
| `<Audio N>` | 被复制或参考的音频信号 |

> 一旦某内容被赋予参考标签，该标签在 `subject_definitions`、`summary`、`retention_analysis`、`detailed_description` 及音频部分中含义保持一致。

`subject_definitions` 定义后续需要单独跟踪的每一项被参考内容，例如人物、环境、源视频结构或音频轨道。每项单独一行，说明其标签所指、参考角色及需要遵循的主要特征；在需要明确出处时点名对应的源素材。如果 `<Picture N>` 或 `<Video N>` 仅用于指明另一被参考项的来源、后续不会被单独分析或使用，则在该项定义中引用即可，无需另起一行。`retention_analysis` 记录每个被参考项出现的位置，以及它是被完整保留、部分保留、迁移还是复用。

### 2.1 `<Subject N>`

`<Subject N>` 用于可复用的可见内容，包括：

- 人物、动物或物体
- 场景、背景或环境
- 服装、道具、界面或视觉特效
- 风格、动作、表情或姿态

它代表将在目标视频中实际使用的内容单元，而非源文件本身。一个主体可由多个参考素材共同定义，一个参考素材也可提供多个主体。

```text
<Subject 1> is the young woman in <Picture 1>, with long dark hair, a blue cardigan, and a thin silver necklace.
```

当同一主体来自多个素材时，合并来源并说明各素材提供了什么：

```text
<Subject 1> is the woman whose appearance comes from <Picture 1> and whose walking motion comes from <Video 1>.
```

### 2.2 `<Picture N>`

当参考图片本身充当某镜头的首帧、关键帧、尾帧、被剪辑的关键帧或构图锚点时，使用独立的 `<Picture N>`：

```text
<Picture 2> is the first frame of [Shot 1], showing a woman seated beside a café window.
```

如果图片仅用于定义角色、场景、服装或风格，则不要创建独立的 picture 条目，而是在对应的 `<Subject N>` 定义中引用该图片来源。

当图片作为分镜或镜头规划参考时，说明它对应哪些镜头以及提供了哪些规划信息：

```text
<Picture 3> is a storyboard reference for [Shot 1] and [Shot 2], defining their viewpoint, subject placement, and shot order.
```

### 2.3 `<Video N>`

`<Video N>` 专用于整视频级的关系，例如：

- 剪辑一条原视频
- 从原视频结尾处续接
- 参考原视频的镜头运动、剪辑、节奏或时间结构

```text
<Video 1> is the source video for the target video edit.
```

如果参考视频中的人物、物体、场景、动作或特效作为可见内容被复用，它们仍归入 `<Subject N>`。`<Video N>` 标识素材或结构来源，不能替代主体标签。

### 2.4 `<Audio N>`

`<Audio N>` 表示独立的音频素材，或参考视频中启用的同步音轨。常见用途包括：

- 复制音频信号的全部或部分
- 参考背景音乐风格
- 参考说话人的音色与演绎方式
- 使用原音频中的对白、歌词或音效
- 参考节拍、节奏或音频连续性

当 `<Audio N>` 明确对应目标说话人时，在定义中复用该说话人的全局 ID：说话人对应已定义主体时写作 `<Subject N> (Sx)`，否则使用稳定的嗓音描述后接 `(Sx)`。该 ID 来自目标视频的全局说话人顺序，不在音频定义中独立分配或重新编号。说话人编号规则见第 5.4 节：

```text
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).
```

当一个音频素材承担多种角色时，用一句自然的语句描述这些角色，不要拆出额外的子条目。

### 2.5 来自同一参考视频的画面轨与音频轨

`<Video N>` 与 `<Audio N>` 独立编号。每个编号仅表示标签在其自身类别中的顺序，不编码两类之间的配对关系。因此同一参考视频可能对应 `<Video 1>` 与 `<Audio 2>`；编号不同并不妨碍它们来自同一源素材。

普通参考视频不会仅因文件含有声音就产生 `<Audio N>`。

`<Audio N>` 的定义主要说明音频的角色，不必点名其来源的 `<Video N>`。仅在需要消除出处歧义时说明共同来源，例如：

```text
<Video 1> is the source video for the target video edit.
<Audio 2> is the synchronized audio track of <Video 1> and is reused in the target video.
```

## 3. `summary`

本部分用一段简短的英文概括目标视频及其参考关系，以方括号的任务类型前缀开头：

```text
[reference generation] ...
[video editing + reference generation + audio reuse] ...
```

根据每个参考素材在目标视频中实际扮演的角色选择任务类型：

| 任务类型 | 使用场景 |
| --- | --- |
| `keyframe completion` | 图片充当目标视频的首帧、关键帧、尾帧、被剪辑的关键帧或其他具体帧锚点 |
| `reference generation` | 图片、视频或音频素材为角色、场景、风格、动作、镜头运动、分镜等提供生成引导，但既不充当具体帧，也不是被剪辑或续接的源视频 |
| `video editing` | 直接修改既有源视频；编辑图片或在静帧关键帧之间生成不属于此类型 |
| `video continuation` | 新内容从既有源视频续接、延展、恢复或转场 |
| `audio reuse` | 同一音频信号被全部或部分复用 |
| `audio reference` | 音频信号未被直接复制；仅参考其音乐风格、音色、对白或歌词内容、音效质感、节拍或连续性 |

当任务满足多种关系时，用 ` + ` 组合任务类型，且不重复同一类型。例如，从源视频续接同时用一张图片作尾帧，写作 `[video continuation + keyframe completion]`。剪辑源视频并保留其原音频，可写作 `[video editing + audio reuse]`。

仅仅存在视频或音频不会自动产生对应的任务类型。如果参考视频仅提供镜头运动、剪辑或节奏，通常属于 `reference generation`。只有该视频被直接剪辑或续接时才使用 `video editing` 或 `video continuation`。

剪辑源视频时，若其原音频仍然可闻，也应使用 `audio reuse`。续接源视频但未直接复制音频信号时，若新音频仅延续原音轨的可闻特征，使用 `audio reference`。

summary 使用先前定义的 `<Subject N>`、`<Picture N>`、`<Video N>`、`<Audio N>` 标签描述主要主体、镜头流程及各参考素材的角色。本部分不得引入新的参考标签。

对于视频剪辑任务，summary 在任务类型前缀之后以下列语句开头：

```text
The target video is an edited version of <Video 1>.
```

## 4. `retention_analysis`

本部分描述每项被参考内容在目标视频中如何被保留、迁移、复制或参考。每个参考标签一行，并保持 `subject_definitions` 中确立的含义。

### 4.1 可见内容

`<Subject N>`、`<Picture N>`、`<Video N>` 使用以下关系标记。这些标记在输出格式中是固定的英文取值：

| 关系标记 | 含义 |
| --- | --- |
| `fully_preserved` | 被参考内容被定义的角色被完整保留 |
| `partially_preserved` | 被参考内容仍在使用，但部分定义特征被更改或仅部分保留 |
| `attribute_transfer` | 被参考特征被迁移到另一个可辨识的目标主体 |
| `weak_reference` | 仅保留风格、类别、构图或氛围上的大致相似 |

主体条目：

```text
<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - ...
```

图片条目：

```text
<Picture 2> ([Shot 1] first frame): fully_preserved - ...
```

视频结构条目：

```text
<Video 1> (cut and pacing structure): weak_reference - ...
```

### 4.2 音频

`<Audio N>` 使用以下关系标记：

| 关系标记 | 含义 |
| --- | --- |
| `fully_copy` | 完整源音频充当目标视频的完整最终音轨 |
| `partially_copy` | 仅复制部分时间线或选定音频层，或复制后添加、移除、替换了其他声音 |
| `reference` | 信号未被直接复制；仅参考其音色、节奏、音乐风格、对白内容或声音质感 |
| `weak_reference` | 仅保留类别或氛围上的大致相似 |

```text
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track.
```

```text
<Audio 2>: reference - the target speaker follows <Audio 2>'s voice timbre and measured delivery without copying the original signal.
```

每个关系标记只能在 `subject_definitions` 中为该标签已定义的参考角色范围内选择。不要把目标视频中新增的动作、背景或剧情事件视为参考保真度的损失。

## 5. `detailed_description`

这是全参考改写的主体部分。它按目标视频播放顺序逐镜头描述画面、动作、声音与对白，并在适用的位置插入参考标签。

### 5.1 基础格式

基础格式遵循 Video Prompt Writing Guide（T2VA / I2VA / FL2VA / L2VA）：

- 正文以英文撰写。对白、歌词与可见文字保留原语言。
- `[Shot 1]` 标记开场镜头，无时间戳。后续镜头使用 `[Shot N] At MM:SS.mmm, ...` 标记切镜时间。
- 镜头运动以自然英文写在当前镜头之内，需要表达时包含运动类型、幅度与速度。
- 为有声来源分配稳定的 `(S1)`、`(S2)` 等后续 ID。对白与歌词写作 `<d>[Language] ...</d>`。
- 对白跨越剪辑、语音被视频结尾截断、跨镜头连续音频分别使用 `<scenetrans>`、`<cutoff>` 及相应的连续性描述。

关于镜头词汇、群组发言、旁白、跨剪辑对白与可见文字的完整规则与示例，参见 Video Prompt Writing Guide（T2VA / I2VA / FL2VA / L2VA）。

### 5.2 全参考模式差异

| 维度 | T2VA | 全参考模式 |
| --- | --- | --- |
| 主字段 | `integrated_multimodal_description` | `detailed_description` |
| 风格开篇 | 写在 `[Shot 1]` 之后 | 在 `[Shot 1]` 之前用一两句英文确立 |
| 参考信息 | 不使用全参考标签 | 在 `<Subject N>`、`<Picture N>`、`<Video N>`、`<Audio N>` 首次出现处及其角色生效处插入 |
| 音频关系 | 描述目标视频自身的声音 | 在对应镜头或音频阶段引用 `<Audio N>` 并说明信号是被复制还是被参考 |

开篇示例：

```text
The target video is in a cinematic, literary music-video style with soft lighting and a slightly desaturated color palette.
[Shot 1] The scene opens in a crowded urban street...
[Shot 2] At 00:09.000, the shot cuts to an extreme close-up...
```

对于生成任务，`detailed_description` 通常为 350–500 个英文单词。对白密集的内容优先完整呈现语音时间线，而不是机械凑词数。视频剪辑类描述随源视频复杂度伸缩，不必遵循生成任务的字数范围。单一镜头不自动意味着描述更短；应根据各镜头的信息量分配细节。

### 5.3 在镜头中使用参考标签

在重要 `<Subject N>` 首次清晰出现时，结合镜头中实际可见的内容描述其被参考的特征、画面中的位置及当前动作。后续镜头继续使用同一标签，无需重新定义标签含义。

具体帧锚点使用自然表述：

```text
the shot begins from <Picture 1>
the shot's keyframe corresponds to <Picture 2>
the shot ends on <Picture 3>
```

剪辑或续接原视频时，在其来源状态、结构或续接关系适用的位置自然地引用 `<Video N>`。在音频关系生效的镜头或语义阶段引用 `<Audio N>`。

### 5.4 说话人、音频来源与对白

基础的说话人 ID 与 `<d>` 格式遵循 T2VA。当被参考的主体实际开口说话时，同时保留视觉参考标签与说话人 ID：

```text
<Subject 2> (S1) turns toward the woman and says, <d>[English] Last summer, I went to my grandfather's house. He talked about you.</d>
```

`<Subject N>` 标识被参考的主体，`(Sx)` 标识实际说话人。主体开口时写作 `<Subject N> (Sx)`。同一主体画外发声时保持相同形式并标注 `off-screen`。说话人不对应任何已定义主体时，使用稳定的嗓音描述后接 `(Sx)`。

当语音内容只是被直接复用的 BGM 或完整音轨中的提示，而没有具体人物、角色、旁白者或其他独立发声来源实际发出时，以 `<Audio N>` 作为可闻来源，不要凭空增加 `(Sx)`。若有具体人物、角色、旁白者或其他独立发声来源发出该声音，则为该来源分配并复用 `(Sx)`：

```text
When <Audio 1> reaches the phrase <d>[English] I'm lonely lonely lonely lonely lonely I'm lonely</d>, <Subject 1> performs the corresponding hand gesture without becoming a separate speaker source.
```

当参考音频中的对白、旁白或歌词被直接复用，或输入提示明确要求重新演绎时，在 `<d>` 内保留精确的原文与原语言。听不清的部分写 `[unclear]`，不要猜测或改写。标点规范化为表达句子所需的基础书写符号，如 `,`、`.`、`?`、`!`；删除重复波浪号、emoji、项目符号以及重复或装饰性标点。完整的陈述、疑问与感叹句在 `</d>` 之前分别以 `.`、`?` 或 `!` 结尾。

当仅参考音色、节奏、情绪或演绎方式时，不要把参考音频中的原始对白带入目标视频。

`(Sx)` 按目标视频中实际发声事件的顺序一次性分配。在 `detailed_description` 中每次实际发声事件都复用对应 ID；在 `subject_definitions` 中绑定到目标说话人的 `<Audio N>` 定义也复用同一 `(Sx)`，但绝不独立分配新 ID。不要在 `retention_analysis` 中写 `(Sx)`。仅存在于被直接复用的 BGM 或完整音轨中的语音提示使用 `<Audio N>`；由具体人物、角色、旁白者或其他独立发声来源实际发出的声音使用 `(Sx)`。

## 6. `overall_soundscape` 与 `non_diegetic_music`

这两类声音的定义遵循 Video Prompt Writing Guide（T2VA / I2VA / FL2VA / L2VA）。

`overall_soundscape` 概括全片的环境氛围与物理声音。对白、歌唱及与特定镜头同步的声音事件保留在 `detailed_description` 中：

```text
overall_soundscape: Quiet indoor room tone and a low ventilation hum continue throughout the video.
```

`non_diegetic_music` 描述角色听不到、仅观众可闻的背景音乐。存在音乐时，说明其配器、速度与动态发展：

```text
non_diegetic_music: A restrained solo-piano score at a slow tempo, with sustained low cello underneath and no swell.
```

使用参考音频时，仅在与可闻层匹配的部分说明其复制或参考关系：环境与音效属于 `overall_soundscape`，仅观众可闻的配乐属于 `non_diegetic_music`。若同一音频同时提供两类内容，则在各部分分别描述对应关系：

```text
overall_soundscape: The copied ambience layer from <Audio 1> continues throughout the target video.
non_diegetic_music: <Audio 2> is directly reused as the complete audience-only score.
```

完整对白与歌词只能写在 `detailed_description` 的 `<d>` 内；不要在这两部分中重复。

## 7. 完整示例

<details>
<summary>展开完整示例</summary>

```text
subject_definitions:
<Subject 1> is the coffee-shop environment in <Picture 1>, featuring an exposed brick wall, an orange tufted sofa with patterned pillows, a neon sign, and a wooden coffee table.
<Subject 2> is the fluffy white Samoyed in <Picture 2>, <Picture 3>, and <Picture 4>, with thick white fur, pointed ears, a dark nose, and a curved tail.
<Subject 3> is the young blonde woman in <Video 1>, with long blonde hair and a light-pink button-down shirt with rolled-up sleeves.
<Subject 4> is the young man in <Video 2>, with short wavy brown hair and a dark-grey hoodie with drawstrings.
<Audio 1> is the voice-timbre reference for <Subject 3> (S1), containing a spoken English vocal layer.

summary:
[reference generation + audio reference] The target video shows <Subject 3> eating a cookie in <Subject 1>. <Subject 4> enters with <Subject 2>, which lunges toward the cookie. The three-shot exchange uses <Audio 1> as the voice-timbre reference for <Subject 3> and ends with a canned audience laugh.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the exposed brick wall, orange tufted sofa, patterned pillows, neon sign, and wooden coffee table are retained.
<Subject 2> (appears in [Shot 1], [Shot 2]): fully_preserved - the Samoyed's thick white fur, pointed ears, dark nose, and curved tail are retained.
<Subject 3> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the blonde woman's identity, long hair, and light-pink shirt are retained.
<Subject 4> (appears in [Shot 1], [Shot 2]): fully_preserved - the young man's short wavy brown hair and dark-grey hoodie are retained.
<Audio 1>: reference - its vocal timbre guides the dialogue delivery of <Subject 3> without copying the original signal.

detailed_description:
The target video uses a realistic multi-camera sitcom style with warm indoor lighting.
[Shot 1] A medium shot establishes <Subject 1>, the coffee shop with its exposed brick wall, orange tufted sofa, patterned pillows, neon sign, and wooden coffee table. <Subject 3> (S1), the young woman with long blonde hair and a light-pink button-down shirt with rolled-up sleeves, sits on the sofa holding a chocolate-chip cookie. From the left, <Subject 4>, the young man with short wavy brown hair and a dark-grey hoodie with drawstrings, enters holding the leash of <Subject 2>, the thick-furred white Samoyed with pointed ears, a dark nose, and a curved tail. The dog lunges toward the cookie and pulls the leash taut. <Subject 3> (S1) jerks her hand back and, using the clear youthful voice timbre referenced from <Audio 1>, exclaims with light annoyance, <d>[English] Hey! Watch your dog!</d> She closes her lips and guards the cookie while <Subject 4> pulls the dog back.
[Shot 2] At 00:03.000, the shot cuts to a close-up of <Subject 4> (S2), the young man in the dark-grey hoodie from Shot 1, sitting beside <Subject 3> on the sofa and holding <Subject 2> securely in his arms. <Subject 4> (S2) says in a casual young male voice with a playful tone and an easy conversational pace, <d>[English] He just likes cookies more than me.</d> He closes his mouth into an apologetic smile and strokes the dog's thick white fur.
[Shot 3] At 00:05.000, the shot cuts to a close-up of <Subject 3> (S1), the blonde woman in the light-pink shirt from Shot 1. Her annoyance softens as she looks toward the Samoyed. <Subject 3> (S1) replies in the same clear youthful voice referenced from <Audio 1> with an amused cadence, <d>[English] Well, he has good taste at least.</d> She smiles and raises the cookie in a small toast-like gesture. A classic canned audience laugh begins immediately after the line and continues through the final frame.

overall_soundscape:
Soft indoor coffee-shop room tone continues throughout the scene.

non_diegetic_music:
N/A
```

</details>
