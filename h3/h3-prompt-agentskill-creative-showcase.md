> 原文：https://github.com/benjiyaya/Minimax-H3-Prompt-AgentSkill/blob/main/references/creative-showcase.md （创意示范集，中文翻译）

# H3 创意示范集 — 高级长提示词模式

来自用户高级 H3 提示词的质量基准与可迁移模式。这些范例代表了增强器应为每一条提示词（无论何种模式）注入的电影化思维深度。请研读这些范例，以校准你的创意增强质量水准。

---

## 模式 1：长篇叙事讲述（15 秒多镜头蒙太奇）

适用场景：一天的生活记录（day-in-the-life）、vlog 美学、蒙太奇、跨地点的叙事推进。

### 结构蓝图

一个长篇叙事提示词在故事板之前先给出三个明确的美学块，然后逐镜头铺陈细节并与旁白（voiceover）整合。

**CAMERA 块** — 定义物理相机身份：
```text
CAMERA: Handheld DV 16mm camcorder aesthetic. CHASE records herself throughout every location, mostly holding the camera directly and occasionally setting it down for brief hands-free shots. Preserve natural hand tremors, crooked composition, slow autofocus correction, awkward zooms, accidental face cropping, and moments where the framing briefly loses her. The physical camcorder is never visible.
```

可迁移要素：
- 物理相机类型与叙事理由绑定（她在自拍自己）
- 点名要保留的瑕疵：手部抖动、自动对焦拉风箱、曝光漂移、笨拙变焦、构图丢失
- 明确"不出现"的内容（相机本身永不可见）

**LOOK 块** — 定义画质与色彩科学：
```text
LOOK: Authentic soft tape-image texture with mild blur, subtle electronic grain, glowing highlights, small automatic-exposure fluctuations, restrained contrast, and natural skin tones. The lighting changes realistically between locations: warm morning light in the apartment → cooler daylight inside the car → intense colorful lighting backstage and onstage.
```

可迁移要素：
- 质感词汇库：tape-image、mild blur、electronic grain、glowing highlights
- 点名曝光/对比度行为
- 灯光转换用箭头记号映射到每一次场景切换

**STYLE 块** — 定义节奏、能量与剪辑韵律：
```text
STYLE: A fast, energetic day-in-the-life montage with sharp cuts between locations and slightly accelerated transitional movement. Reflective voiceover plays over the footage instead of synchronized dialogue. The pace gradually builds from a quiet sleepy morning into a high-energy performance finale.
```

可迁移要素：
- 节奏以"弧线"描述：安静→充满能量，并点名转折点
- 区分旁白 vs. 同步对白
- 剪辑韵律：硬切、加速转场

### 角色描述模式

```text
CHASE — an exceptionally beautiful Instagram influencer and rising pop performer in her 20s. Long glossy dark-brown hair, striking symmetrical features, large expressive eyes, flawless glowing skin, and soft pink lips. Slim, toned figure. Her outfit changes with each location: cozy loungewear at home, stylish casual clothing during the ride, and a glamorous performance outfit for the final scene. Each outfit fully covers her arms and torso.
```

可迁移要素：
- 年龄段 + 角色/职业，瞬间建立身份
- 外貌特征要具体（发色+发质、眼睛描述、皮肤、嘴唇）
- 服装随每个地点/镜头推进映射
- 覆盖度说明："Each outfit fully covers her arms and torso" — 始终明确描述着装覆盖程度

### 场景推进

```text
Setting Progression
Stylish apartment bedroom in the morning → luxury van interior during the day → busy backstage area and concert stage at night.
```

可迁移：用箭头记号把时间 + 空间推进映射到整支视频。

### 带旁白的逐镜头故事板

```text
Storyboard — 15 seconds, 5 cuts

(~3s, bedroom, camera resting on a table, soft morning light) She slowly sits up, stretches, fixes her messy hair, and hurriedly packs a small bag. VOICEOVER (CHASE): "Some mornings begin before I'm even fully awake."

(~3s, van interior, handheld selfie footage, natural window light) She sits beside the window as sunlight moves across her face, casually checking messages on her phone. VOICEOVER (CHASE): "I spend so much time on the road, this place almost feels like home."

(~3s, van interior, macro detail shot) Close-up of her fingers choosing a song from a playlist while passing sunlight flickers across the screen and her hand. No voiceover, only natural road noise.

(~3s, backstage, fast handheld montage) Quick glimpses of makeup brushes, hair styling, costume adjustments, staff rushing past, and her taking one focused breath before going onstage. VOICEOVER (CHASE): "And then everything suddenly starts moving at once."

(~3s, stage, wide shot moving into a close-up, energetic finale) Bright stage lights ignite as she steps through the curtains. The camera catches her silhouette, then a brief confident smile before the image cuts to black. VOICEOVER (CHASE): "This moment is why I keep doing it."
```

可迁移要素：
- 每个镜头：`(时长, 地点, 机位, 灯光)` 头部信息
- 每个镜头只做一个主导动作（坐起+收拾 / 看手机 / 手指选歌 / 后台蒙太奇 / 穿过幕布）
- VOICEOVER 台词放在镜头末尾并标注归属
- 无声镜头要明确标注（"No voiceover, only natural road noise"）
- 穿插微距/细节镜头以丰富节奏
- 节奏递进：慵懒清晨 → 安静车程 → 亲密细节 → 高速后台 → 爆发力舞台终章

---

## 模式 2：动作编排（Ref2VA，7 镜头，15 秒）

适用场景：格斗、追逐、体育，以及任何包含空间移动和角色互动的序列。

### 角色色彩锁定系统（Color Lock System）

每个角色拥有一个标志性色彩，贯穿整个序列统辖其视觉特效、拖尾、反射和环境光影响。这是动作提示词中最强大的连贯性工具。

```text
TSUBAME (Image 1) — Young woman, sharp jawline, shoulder-length brown bob; wearing a glossy purple latex crop-top vest with silver zipper and black leather harness straps; sleek, agile build. Her movement leaves trailing neon-purple afterimages and light streaks.
GARAN (Image 2) — Tall, imposing figure in a metallic teal/seafoam green high-collar jacket over a white ribbed bodysuit; calm but dangerous expression. His heavy impacts generate teal shockwaves and digital distortion ripples.
```

**Color Lock 规则：**
- 在角色定义时分配各自专属色彩（Tsubame = 电紫/洋红；Garan = 青绿/青色）
- 该色彩出现在：移动拖尾、闪光/反射、冲击特效、环境反射光
- 显式声明色彩锁定：`Color Lock: Tsubame = Electric Purple/Magenta (trails, glints); Garan = Teal/Cyan (jacket sheen, shockwaves)`
- 环境反射角色色彩："purple bounce on walls from her, teal reflections from him"

### 动作风格块

```text
Style: High-fidelity 3D CGI animation, stylized realism (like Arcane or Spider-Verse). Glossy material rendering (latex/metal), volumetric neon lighting, motion blur on fast objects. Color Lock: Tsubame = Electric Purple/Magenta (trails, glints); Garan = Teal/Cyan (jacket sheen, shockwaves). World: Sleek, futuristic sci-fi corridor with circular archways and reflective floors. Lighting is driven by their suits—purple bounce on walls from her, teal reflections from him. Camera: Dynamic action cam—dolly zooms, whip pans, low angles, speed-ramping.
```

可迁移要素：
- 风格参照点（点名相似作品以快速定调）
- 材质渲染指令："Glossy material rendering (latex/metal)"
- 光源与角色色彩绑定："Lighting is driven by their suits"
- 相机个性："Dynamic action cam" 加技法清单

### 空间布局系统

动作序列要显式定义地理方位，使所有镜头中的移动方向毫无歧义：

```text
SPATIAL LAYOUT (MAIN VIEW = Corridor Axis): Tsubame starts at the far end (Screen Center-Deep) running toward camera. Garan intercepts from Screen Right. Action flows Deep → Front, then Left → Right.
```

**Action Vectors（动作矢量）** — 2–3 个关键运动瞬间：
```text
ACTION VECTORS:
(V1, SHOT 2) Garan slams fist into floor → Teal shockwave travels Front→Back; Tsubame jumps over the wave.
(V2, SHOT 4) Tsubame slides under Garan's sweeping arm → Purple trail marks the slide path.
(V3, SHOT 6) Close combat lock → Purple glove vs Teal sleeve, sparks fly at contact point.
```

### 渐进式连贯性追踪（Progressive Continuity Tracking）

声明整个序列中什么在变化，使损伤和磨损逐镜头可见累积：

```text
Continuity: Tsubame's hair gets messier/windblown progressively. Garan's jacket shows scuff marks/dust after Shot 5.
```

### 逐镜头编排模式

动作序列中的每个镜头需要：镜头名 + 时长 + 相机 + 构图 + 一个关键动作 + 视觉特效 + 情绪节拍。

```text
[SHOT 1] · The Stare Down (~2s): Static wide shot, symmetrical composition. Long futuristic corridor with glowing arches. Tsubame stands center-frame, distant, fists clenched, purple vest gleaming under overhead lights. Garan steps into frame from Right foreground, back to camera, teal jacket reflecting the hallway lights. He cracks his knuckles. Tense atmosphere.

[SHOT 2] · The Shockwave (~2s): Low angle, dynamic tracking. Garan stomps forward. A visible teal energy ripple explodes outward from his boot across the reflective floor. Tsubame sprints forward and leaps vertically, clearing the wave. Her purple trails hang in the air like neon ribbons. Debris floats in zero-G for a split second.

[SHOT 3] · The Interception (~2.5s): Handheld shaky cam. Tsubame lands and dashes Screen Left → Screen Right. Garan swings a massive backhand. She ducks under it with fluid grace, her brown bob whipping around. The teal jacket blurs as it passes inches above her head. Speed lines emphasize velocity.

[SHOT 4] · The Slide (~2.5s): Extreme low angle, floor-level. Tsubame goes into a baseball slide across the polished floor, passing directly between Garan's legs. Her purple latex vest reflects the floor lights intensely. Garan tries to stomp down, but she's already past, kicking up a spray of digital sparks (purple/teal mix).

[SHOT 5] · The Wall Run (~1.5s): Vertical pan up. Tsubame runs horizontally along the curved corridor wall (Screen Right), defying gravity. Garan punches the wall where she was a fraction of a second ago—cracks spiderweb out in teal light. She pushes off the wall, launching herself back toward the center.

[SHOT 6] · The Clash (~1s): Extreme close-up, slow-motion impact frame. Tsubame's purple-gloved fist meets Garan's teal-sleeved forearm. The collision point blooms with white-hot light and particle sparks. Their faces are inches apart—her fierce determination vs his stoic focus. Background is a blur of motion streaks.

[SHOT 7] · The Aftermath (~3.5s): Wide shot, camera pulls back rapidly. Tsubame lands in a superhero crouch (Screen Left), sliding to a halt, purple trails fading. Garan stands firm (Screen Right), adjusting his teal collar, unbothered but acknowledging her speed. Dust motes dance in the neon light. The corridor behind them is slightly damaged (cracks, scorch marks). Both breathe heavily. Fade out.
```

可迁移的逐镜头要素：
- **命名镜头**："The Stare Down"、"The Shockwave"、"The Clash" — 让每个节拍有清晰身份
- **每镜头相机**：static wide / low angle tracking / handheld shaky / extreme low angle / vertical pan / extreme close-up slow-motion / wide pull-back
- **每个镜头都有色彩特效**：purple trails、teal shockwave、teal jacket blur、purple vest reflection、teal spiderweb cracks、white-hot bloom、fading purple trails
- **每镜头一个关键动作**：对峙 → 冲击波跳跃 → 闪避 → 滑铲 → 跑墙 → 对撞 → 余波
- **情绪对比**："her fierce determination vs his stoic focus"

### 环境反应性与技术页脚

```text
Environmental activity: Holographic ads flicker on walls reacting to their movement. Floor is highly reflective (mirror-like).
Audio: Heavy bass synth track. SFX: Electric hums, heavy thuds, glass-like shattering sounds, neon buzz.
Technical: 15 seconds. 16:9 aspect ratio. No text overlays. Consistent character models (purple vest/black straps for her, teal jacket/white undersuit for him).
```

---

## 可迁移质量清单

增强任何提示词时，检查是否在相关处应用了这些模式：

- [ ] **相机身份** — 不只是 "handheld"，还要说明为什么用手持、保留哪些瑕疵
- [ ] **视觉质感词汇** — 具体的颗粒/模糊/曝光语言，而不只是 "cinematic"
- [ ] **灯光转换** — 若地点变化，描述每次转场的灯光变化
- [ ] **节奏弧线** — 点名推进模式（安静→高能、紧张→释放）并含转折点
- [ ] **角色视觉签名** — 一个反复出现的色彩或视觉元素，便于瞬间识别
- [ ] **服装推进** — 服装映射到地点/时间并描述材质
- [ ] **空间地理** — 多角色或动作序列要声明屏幕方向
- [ ] **色彩锁定**（动作）— 每个角色的特效/拖尾/反射保持一致色彩
- [ ] **渐进连贯性** — 跨镜头累积什么（损伤、凌乱、尘土、疲惫）
- [ ] **环境反应性** — 世界对角色动作做出响应（闪烁、开裂、反射）
- [ ] **命名镜头** — 每个镜头有超出 "Shot 3" 的记忆点身份
- [ ] **情绪节拍** — 描述表情和肢体语言，而不只是物理动作
- [ ] **声音设计层次** — 环境声、物理音效、剧情内音乐、非剧情配乐全部映射
- [ ] **旁白纪律** — VO 明确标注、闭嘴说明、画面之上的情绪性叙述

---

## 把示范模式转换为 H3 格式

上面的示范使用创意简报风格（CAMERA/LOOK/STYLE/Storyboard 块）。转换为实际 H3 格式输出时：

1. **相机身份** → 织入风格开篇句和每个镜头的相机运动行
2. **LOOK/视觉质感** → 风格开篇 + 每镜头的环境/灯光描述
3. **STYLE/节奏** → 体现在镜头数量、时长分配和剪辑韵律上
4. **角色描述** → `subject_definitions` 条目（Ref2VA）或每个镜头中的身份锚点（Base）
5. **故事板镜头** → `[Shot N]` 条目，带时间戳、相机运动、各一个主导动作
6. **色彩锁定** → 嵌入角色描述和逐镜头视觉特效描述
7. **空间布局 / 动作矢量** → 用屏幕方向语言织入镜头描述
8. **连贯性推进** → 在详细描述中跨镜头追踪
9. **环境反应性** → 在相关镜头内描述
10. **旁白** → 格式化为 `"says in an off-screen voiceover"` + `<d>[Language] ...</d>` + 闭嘴说明
11. **声音设计** → 拆分到 `overall_soundscape`（环境声/音效）和 `non_diegetic_music`（配乐）

---

## 模式 3：动作编排 — 咏春街头格斗（T2VA，15 秒，5 镜头）

一场写实的武术格斗，强调真实技法、时代特定氛围和渐进的战斗疲惫感。展示如何在 5 镜头预算内编排一对多格斗。

### 关键模式
- **时代特定造型**：1950 年代纽约黑色电影 — 鹅卵石、防火梯、费多拉帽、羊毛大衣、胶片颗粒
- **技法特定编排**：点名咏春技法（pak sao 拍手、tan sao 摊手、chain punches 连环冲拳）使动作扎根于写实
- **每镜头一个主导动作纪律**：每个镜头处理恰好一次攻防交锋
- **渐进疲惫**：叶问全程冷静；攻击者逐镜头累积倒地
- **环境声音设计**：雨声敲击、鹅卵石水花、布料击打声 — 格斗中无音乐，最后一击时配乐切至静默

### 输出

```
integrated_multimodal_description: [Shot 1] Cinematic live-action, 1950s film-noir aesthetic with high-contrast chiaroscuro lighting, shallow depth of field, and visible 35mm film grain. A wide static shot establishes a narrow New York back alley at night in heavy rain — wet cobblestone ground reflecting a single overhead streetlamp, brick walls on both sides dripping with water, iron fire escapes climbing the left wall, and a chain-link fence partially visible at the far end. YI MAN, a lean Chinese man in his late thirties with a calm composed expression, short black hair slicked from the rain, wearing a dark charcoal traditional Chinese cotton jacket with cloth buttons, dark trousers, and thin-soled cloth shoes, stands alone in the center of the alley under the streetlamp glow, hands at his sides. Four men in 1950s street clothing — a heavyset man in a brown wool overcoat and fedora, a wiry man in a leather jacket and flat cap, a broad-shouldered man in a dark-grey raincoat, and a younger man in a white undershirt and suspenders — spread out in a semicircle facing him from Screen Right to Screen Left, approximately five meters away. Rain pours steadily. The camera pushes in with small amplitude at slow speed toward Yi Man, isolating him against the dark alley, then holds.
[Shot 2] At 00:03.000, the shot cuts to a medium tracking shot at fast speed moving with Yi Man as he closes the distance toward the wiry man in the leather jacket and flat cap on Screen Right. Yi Man's hands rise into a relaxed Wing Chun guard — elbows tucked, hands open at centerline. The wiry man in the leather jacket throws a wide right hook. Yi Man slips inside the arc with a compact lateral step, his left hand executing a pak sao (slapping block) that deflects the hook outward, and immediately fires a chain of three straight punches into the man's chest and jaw using vertical-fist Wing Chun technique. The impacts are fast, precise, and audible over the rain. The wiry man stumbles backward into the brown-overcoat man behind him. Rain sprays off their shoulders with each impact. The camera shakes slightly during the exchange.
[Shot 3] At 00:06.000, the shot cuts to a low-angle medium shot from ground level, tilted up at Yi Man as the broad-shouldered man in the dark-grey raincoat and the younger man in the white undershirt and suspenders rush him simultaneously from Screen Left. Yi Man pivots on the balls of his feet, his thin-soled cloth shoes gripping the wet cobblestone. He intercepts the younger man's lunging grab with a tan sao (palm-up blocking arm) that redirects the momentum past his right side, then strikes the younger man's solar plexus with a sharp vertical punch. The broad-shouldered man in the raincoat swings a heavy haymaker. Yi Man ducks under it with a slight knee bend and delivers a low Wing Chun front kick to the raincoat man's lead knee, buckling his stance. Both attackers stagger. Water splashes from puddles beneath their feet. The camera arcs right with medium amplitude at fast speed, tracking the redirection of force.
[Shot 4] At 00:09.000, the shot cuts to a close-up handheld shot with strong shake, framing Yi Man from chest to head as the heavyset man in the brown wool overcoat and fedora — the last one standing — grabs Yi Man from behind in a bear hug, locking his arms at his sides. Yi Man's expression stays focused, not panicked. He drops his weight low, stomps his heel onto the heavyset man's instep, and as the grip loosens, throws a sharp backward elbow strike to the man's ribs, followed by a spinning backfist that connects with the heavyset man's jaw. The fedora flies off into the rain. The heavyset man's eyes glaze and he drops to his knees on the wet cobblestone, then falls forward. Rain streaks across the frame. Yi Man's dark charcoal jacket is now darkened with rain across the shoulders and forearms. The camera pulls back with small amplitude to reveal two other men on the ground behind Yi Man and one slumped against the brick wall.
[Shot 5] At 00:12.000, the shot cuts to a wide static shot from the far end of the alley, behind the fallen attackers. All four men lie on the wet cobblestone — two face-down in puddles, one slumped against the brick wall holding his ribs, and the heavyset man in the brown overcoat face-up with his fedora floating in a nearby puddle. Yi Man, the lean Chinese man in his dark charcoal Chinese cotton jacket, stands alone in the center of the alley under the streetlamp, his breathing slightly elevated but his expression composed and still. He lowers his hands slowly to his sides, rolls his shoulders once, and turns to walk toward the far end of the alley into the rain and shadow. The wet cobblestone reflects his retreating silhouette and the dim glow of the streetlamp. Rain continues to fall steadily. The camera holds on the empty alley as the last of the fallen men groans faintly.

overall_soundscape: Heavy rain pours continuously throughout the scene, striking cobblestone, brick walls, metal fire escapes, and puddles with a relentless drumming hiss. Rapid footsteps shuffle and slap on wet stone as fighters reposition. Fists strike cloth and flesh with dull, muffled thuds, and a heavy body hits the wet ground with a wet slap. A faint groan of pain is audible from a fallen attacker in the final shot.

non_diegetic_music: A brooding tension-building score begins with a low sustained double bass drone and sparse, dissonant piano notes that hang in the air during the standoff. As the fighting erupts, a driving rhythmic pulse enters — staccato strings and a muted taiko drum pattern at a fast tempo that accelerates through the combat shots, then cuts abruptly to silence when the last attacker falls, leaving only the rain.
```

---

## 模式 4：武士 vs 忍者 — Chambara 剑戟片对决（T2VA，15 秒，5 镜头）

一段日本时代剧对决，强调蓄势节奏、潜行编排和剑戟片（chambara）传统中的风格化暴力。展示如何处理一场以暗杀而非胜利告终的一对一决斗。

### 关键模式
- **剑戟片美学**：黑白黄的月光色调、体积雾、石灯笼、寺庙庭院
- **节奏弧线**：凝固的紧张 → 快速交锋 → 突然潜行 → 亲密的杀戮 → 冷峻的余波
- **相机即角色**：横向追踪匹配闪避节奏；相机翻滚匹配忍者旋转；慢推至击杀点
- **单一转折点**：拔短刀时的一声太鼓重击把整支视频分为"悬念"与"后果"
- **风格化暴力**：月光下血呈近黑色（剑戟片传统），一道弧形喷溅，不铺张
- **环境变化**：雾逐镜头加浓；杀戮前无雨，之后开始微雨 — 大气标点

### 输出

```
integrated_multimodal_description: [Shot 1] Cinematic live-action, Japanese chambara film aesthetic with high-contrast black-and-yellow moonlit tones, volumetric fog drifting between dark wooden architecture, shallow depth of field, and fine 35mm film grain. A wide static shot establishes a narrow temple courtyard at night — wet stone tiles reflecting cold moonlight, a stone lantern glowing faintly on the left, wooden temple walls with sliding screen doors on both sides, and low hanging mist clinging to the ground. THE SAMURAI, a tall Japanese man in his forties with a stern weathered face, topknot hairstyle, wearing dark indigo armor plates laced with black silk cord over a layered grey kimono, dark hakama trousers, and straw sandals, stands in the center of the courtyard gripping a katana in a two-handed middle guard, blade raised at eye level pointing forward. Opposite him, ten meters away, THE NINJA — a shorter lean figure wrapped entirely in dark charcoal-black cloth with only a narrow slit for the eyes, black tabi boots, a short ninjato sword strapped across his back — crouches low in a side stance, motionless. Fog drifts between them. The camera holds on this standoff for a beat, then pushes in with small amplitude at slow speed toward the gap between them. Moonlight glints off the samurai's katana blade.
[Shot 2] At 00:03.000, the shot cuts to a medium tracking shot moving at fast speed laterally from Screen Left to Screen Right, following the exchange. The samurai — in his dark indigo armor and topknot — steps forward and swings his katana in a powerful downward diagonal cut. The ninja — wrapped in black cloth, only eyes visible — pivots left, the blade missing his shoulder by inches, moonlight flashing on the steel as it slices through fog. The samurai immediately reverses into a horizontal side cut. The ninja drops low and ducks right, the katana whistling over his head, his black tabi boots sliding on the wet stone tiles. A third overhead strike — the ninja sidesteps left again with fluid precision, each evasion minimal and efficient. Sparks fly where the katana tip grazes a stone tile. The camera tracks the ninja's lateral dodging path, panning left then right then left with medium amplitude at fast speed, matching his evasion rhythm. The samurai's grey kimono sleeves snap with each swing.
[Shot 3] At 00:06.500, the shot cuts to a low-angle close-up from ground level tilted up at the ninja as he executes a sudden spinning side-turn — his body drops almost parallel to the wet stone tiles, black cloth rippling, as he rotates beneath the samurai's reaching guard in a tight spiral. The camera rolls clockwise with small amplitude at fast speed to match the spin, capturing the ninja's body sweeping past the samurai's armored legs in a blur of dark fabric. Wet stone tiles and mist fill the foreground. The ninja's tabi boots push off the ground with a muffled scrape. In a fraction of a second he has passed entirely behind the samurai, who is still mid-recovery from his missed strike, his katana extended forward into empty air. The ninja rises silently behind the samurai's right shoulder, his movement invisible to his opponent.
[Shot 4] At 00:09.000, the shot cuts to a close-up framed on the ninja's hands from behind the samurai's right shoulder. The ninja's right hand, wrapped in black cloth, draws a tanto — a short dagger with a plain dark wooden handle and a thin gleaming steel blade — from a concealed sheath at his lower back in one swift upward pull. The blade catches a sliver of moonlight. In a single fluid motion, the ninja drives the tanto forward into the exposed side of the samurai's neck, just above the indigo armor plates and below the topknot. The blade sinks in to the hilt. The samurai's eyes widen — his stern composure breaks into shock, his mouth opening slightly, his katana grip going slack. His fingers loosen on the katana handle. The camera pushes in with small amplitude at slow speed toward the point of impact, the tanto handle visible against the samurai's grey kimono collar and dark indigo armor lacing.
[Shot 5] At 00:11.500, the shot cuts to a medium shot, slightly low angle, framing both figures from the front as the ninja — still behind the samurai's right shoulder — pulls the tanto blade out in a sharp horizontal draw. Blood sprays from the samurai's neck wound in an arc that catches the cold moonlight, the droplets appearing almost black against the lit stone tiles and mist. The samurai's knees buckle, his dark indigo armor plates clacking as his posture collapses. His katana slips from his fingers and clatters onto the wet stone. The ninja steps back two paces into the fog, tanto held at his side, blood on the blade glinting faintly. The samurai — tall, topknot, grey kimono, indigo armor — sinks to his knees, one hand rising weakly toward his neck, then falls forward onto the wet courtyard tiles. Fog rolls over his fallen body. The camera holds static on the scene as the ninja turns and dissolves into the dark shadow between the temple walls, leaving only the stone lantern glow and the fallen samurai in frame. Rain begins to fall lightly on the blood-spattered stone.

overall_soundscape: A heavy silence dominates the temple courtyard, broken only by the faint scrape of straw sandals and tabi boots shifting on wet stone tiles. The katana cuts through cold air with a sharp metallic whistle on each swing, and stone sparks ping faintly when the blade grazes tile. A muffled cloth rustle signals the tanto being drawn from its hidden sheath, followed by a wet, subdued impact on the neck strike. The katana clatters on stone as it drops, and armor plates clack sharply when the samurai's body collapses. Light rain begins tapping the courtyard in the final seconds.

non_diegetic_music: A single sustained high note on a bamboo flute holds through the standoff and sword exchanges, tense and airy. When the tanto is drawn, a deep taiko drum strikes once — a single boom that resonates and decays through the neck strike. As the samurai falls, a sparse, mournful shamisen pluck enters at a very slow tempo, its dissonant tone hanging unresolved as rain begins to fall and the scene fades.
```

---

## 模式 5：动漫格斗 — SeeDance 转 H3 格式（T2VA，15 秒，5 镜头）

一段从 SeeDance 格式提示词转换而来的 2D 动漫风格格斗。展示如何把 7 个带时间戳的段落合并进 H3 的 5 镜头预算而不丢失任何编排节拍，以及如何把外部提示词格式转换为 H3 结构。

### 关键模式
- **段落合并**：7 个 SeeDance 段落 → 5 个 H3 镜头，通过合并"环绕→缠斗"与"猛击冲击"序列
- **角色色彩锁定**：BULLDOG = 焦橙/锈红/金；VIPER = 橄榄绿/黑/白绷带 — 每个角色在所有镜头中色调一致
- **动漫美学规格**：2D 半写实概念美术、cel shading、干净线稿、24fps 运动感、细微胶片颗粒
- **相机风格保留**：低角度大全景与猛烈急推特写交替、甩镜、手持能量 — 无平滑滑轨
- **慢动作节拍**：双人对冲顶点处短暂慢镜，然后猛切回全速
- **音频架构**：打击乐鼓点随击打逐步增强、最后一击时 bass drop、然后切至近静默只剩呼吸声

### 输出

```
integrated_multimodal_description: [Shot 1] 2D semi-realistic anime concept art, clean confident lineart, painterly cel shading with soft gradients, subtle film grain, 24fps motion feel. A muted palette of burnt orange, olive green, warm gray concrete, and dusty sunset gold. A low-angle wide full shot frames a gritty back-street lot at sunset — cracked concrete ground, chain-link fence topped with razor wire, graffiti-covered walls, palm trees, and parked cars. Warm orange dusk light casts long hard shadows across the lot. BULLDOG — a heavyset, powerful woman with broad shoulders, deep tan skin, buzzed rust-orange fade hair, gold hoop earrings, a nose ring, wearing a burnt-orange cropped tank top, a thin gold chain, baggy gray sashed pants, blood-stained white hand wraps, gold knuckle rings, and gray high-top sneakers — and VIPER — a lean, athletic woman with deep tan skin, long black ponytail with blunt bangs, green eyes, a small black shoulder tattoo, wearing an olive sports bra, black shorts, black fingerless gloves over white taped wrists, tan ankle braces, and white sneakers — face each other at mid-distance in profile, guards raised, circling clockwise. Sneakers scuff on gravel. The camera tracks right at slow speed, orbiting with their circle, keeping both fighters fully in frame against the hazy sunset backdrop.
[Shot 2] At 00:03.000, the shot cuts to a tight over-the-shoulder shot from behind BULLDOG, still in her burnt-orange tank top and gold knuckle rings, looking past her wrapped fist toward VIPER. BULLDOG fires a heavy straight punch — her blood-stained white hand wrap and gold knuckle ring passing close by the lens in motion blur. VIPER, her green eyes tracking the fist, slips it with a sharp head snap to the side, her long black ponytail whipping across the frame. The punch misses by inches. The camera shakes slightly with handheld energy, emphasizing the miss. Dust motes float in the warm sunset light between them.
[Shot 3] At 00:06.000, the shot whip-pans to a medium full shot from the opposite side. VIPER counters immediately — her white-taped wrists and black fingerless gloves firing a fast one-two straight combination into BULLDOG's guard, followed by a sharp rising knee. BULLDOG, in her burnt-orange tank top and gold chain, absorbs the strikes on crossed forearms, her heavyset frame driven back two heavy steps, gray high-top sneakers scraping cracked concrete, dust kicking up from the impact. The camera tracks backward at fast speed with them, low horizon line, both fighters' bodies fully visible, long sunset shadows stretching behind them. BULLDOG's rust-orange fade and gold hoop earrings catch the warm light as she steadies.
[Shot 4] At 00:09.000, the shot cuts to a dynamic low wide shot. Both fighters — BULLDOG in burnt-orange and gray, VIPER in olive and black — lunge at each other simultaneously, bodies stretched long, one foot off the ground each, silhouetted against the bright hazy sunset sky. At the apex of the lunge the motion shifts to brief slow motion, sunset light rim-lighting both figures, then snaps hard back to full speed as their fists collide against each other's guards. The impact sends dust and gravel spraying. The camera then orbits tightly around the resulting clinch — chain-link fence and graffiti wall sweeping through the background as BULLDOG and VIPER trade short hooks and elbows at close range, shoulders grinding, feet shuffling on cracked concrete, ponytail and rust-orange fade visible in the tight orbit.
[Shot 5] At 00:11.500, the shot cuts to an extreme close-up as VIPER's taped fist — white tape over black fingerless glove — drives directly toward the lens, filling the frame in heavy motion blur. The punch lands. The camera snaps instantly to BULLDOG's face in extreme close-up — her head torquing violently sideways, sweat flying from her buzzed rust-orange fade, gold hoop earring swinging, eyes squeezed shut, the frame shaking hard on contact. At 00:13.500 the camera pulls back fast to a low-angle wide shot. BULLDOG drops to one knee on the cracked pavement, head down, shoulders heaving in her burnt-orange tank top, gold chain dangling. VIPER stands a few paces away in her olive sports bra and black shorts, guard lowering, chest rising and falling, black ponytail settling against her back. Both fighters are backlit against the glowing sunset haze. The camera slows to a held final frame on this aftermath.

overall_soundscape: Sneakers scuff and grind on gravel and cracked concrete throughout, with dust-shifting crunches on every heavy step. Fists strike guards and flesh with sharp percussive thwacks, and fabric rustles sharply during each exchange. Heavy breathing from both fighters grows more labored as the fight progresses. Distant city traffic hum provides a low ambient bed beneath the action.

non_diegetic_music: Gritty low percussive drums build steadily in intensity from the opening standoff, layering in sharper hi-hat patterns and deeper kick hits that sync to each landed strike. The rhythm tightens and accelerates through the clinch, peaks with a heavy bass drop on the final punch impact, then cuts abruptly to near-silence — leaving only the fighters' breathing over the final held frame.
```

---

## 模式 6：忍 indoor 连击 — 宅邸潜入（T2VA，15 秒，5 镜头）

一段发生在传统日式宅邸内的快节奏室内战斗序列。展示如何在封闭环境中编排一对多格斗，并把房间结构（障子门、矮桌、天花板梁）同时用作障碍物和武器。

### 关键模式
- **环境战斗**：撞碎障子门、瓷器四散、从天花板梁进入的切入点
- **多目标编排**：每个镜头处理一场独立交战 — 进入 → 首次放倒 → 缴械 → 最终清场
- **反手握 ninjato**：武器细节使动作写实（反握 = 近身刺客风格）
- **天气作为标点**：阵风从破障子门灌入，标记房间被攻破的时刻
- **俯拍收尾**：天花板梁视角重建地理全貌并展示战果

### 输出

```
integrated_multimodal_description: [Shot 1] Ultra-realistic cinematic live-action with shallow depth of field, volumetric lantern lighting, and rich shadow contrast. A wide static shot establishes the interior of a traditional Japanese estate at night — a spacious tatami room with sliding shoji screen doors, dark wooden ceiling beams, iron wall sconces holding flickering oil lamps, a hanging scroll on the far wall, and a low wooden table. Three SAMURAI GUARDS in dark indigo kimono and hakama, straw sandals, each carrying a sheathed wakizashi short sword at the hip, stand alert at different points — one by the shoji door at Screen Left, one center, one by the table at Screen Right. Paper lantern light casts warm amber pools across the tatami, leaving deep black shadows in the corners. THE NINJA — a lean figure in matte charcoal-black cloth wrapping the entire body and face with only a narrow slit for sharp dark eyes, black tabi boots, a ninjoto short sword strapped across his back — drops silently from the wooden ceiling beams into a crouch at Screen Left-Center between the guards. The camera pushes in with medium amplitude at slow speed toward the ninja's crouched landing. The three samurai guards turn sharply toward the movement.
[Shot 2] At 00:03.000, the shot cuts to a medium tracking shot at fast speed moving Screen Left to Right with the ninja as he explodes from the crouch into the center guard. The ninja's right hand strikes the center samurai's throat with a knife-hand blow before the guard can draw his wakizashi — the man's eyes bulge, his hands clutch his neck, and he staggers backward into the low table, scattering a ceramic cup that shatters on the tatami. The left-door guard draws his wakizashi and slashes horizontally. The ninja ducks under the blade, his black tabi boots sliding on the tatami surface, and delivers a spinning back kick to the guard's sternum that launches him through the paper shoji screen — the thin wooden lattice splinters, white paper tears, and the guard crashes into the adjoining garden walkway. Rain gusts in through the broken screen. The camera whip-pans right following the flying guard, then snaps back to the ninja.
[Shot 3] At 00:06.500, the shot cuts to a low-angle medium close-up from floor level tilted up at the ninja as the third guard — the one from Screen Right by the table — charges with his wakizashi raised overhead in a two-handed grip. The ninja draws his ninjato from his back in a single reverse-grip pull, the short black-steel blade catching lantern light. The guard brings the wakizashi down in a powerful overhead strike. The ninja steps diagonally forward-left, parries the blade aside with the ninjato's flat, and in the same motion drives the ninjato's pommel into the guard's wrist — the wakizashi spins free and clatters across the tatami. The ninja then strikes the disarmed guard with three rapid elbow-punch-elbow combinations to the jaw and solar plexus, each impact snapping the guard's head and torso in a different direction. Oil lamp light flickers wildly across the walls from the concussive air displacement. The camera arcs right with medium amplitude at fast speed, tracking around the combination, tatami and scattered debris in the foreground.
[Shot 4] At 00:10.000, the shot cuts to a tight over-the-shoulder shot from behind the ninja looking toward the broken shoji screen. The first guard — throat-struck, recovered slightly — lunges back through the torn paper screen from the garden walkway, rain streaming behind him, gripping a short tanto dagger in his left hand. The ninja, without turning fully, sweeps his ninjato backward in a blind reverse cut that deflects the tanto thrust. He then spins 180 degrees, seizes the guard's tanto wrist with his free left hand, twists it inward until the guard drops to his knees, and delivers a precise knee strike to the man's temple. The guard collapses face-first onto the tatami. Rain and wind from the broken screen blow paper fragments and the guard's dark indigo kimono across the frame. The camera tracks the spin with a fast handheld arc, lantern light strobing as bodies move past the wall sconces.
[Shot 5] At 00:12.500, the shot cuts to a high-angle wide shot from above — mounted on the wooden ceiling beam looking down into the room. All three samurai guards lie motionless on the tatami — one sprawled across the broken table amid ceramic shards, one face-down near the shattered shoji screen with rain blowing over him, one curled near the far wall where the scroll hangs undisturbed. The ninja, still crouched in his reverse-grip ninjato stance at the room's center, sheathes the blade across his back in one clean motion. He rises, pulls a torn piece of shoji paper from his shoulder, and moves toward the dark corridor at the far end of the room — vanishing into the deeper darkness between two extinguished lanterns. The camera holds on the aftermath from above — warm lantern glow illuminating the scattered bodies, rain mist drifting through the broken screen, and the empty corridor swallowing the ninja's silhouette.

overall_soundscape: The interior is dominated by the quiet patter of rain on the roof tiles above, muffled through wooden beams. Bare feet and tabi boots scuff and slide on woven tatami with sharp friction hisses. A ceramic cup shatters on impact. The shoji screen explodes with a sharp paper-tearing rip followed by wood-lattice splintering. Fists and elbows strike flesh and bone with dull wet thuds, and a metal blade clatters across the tatami when the guard is disarmed. Wind gusts through the broken screen, sending loose paper rustling across the room.

non_diegetic_music: A sparse, nerve-taut score opens with a single low cello drone and the faint metallic ring of a singing bowl, building barely-perceptible tension. As combat erupts, a tight, rhythmic ostinato on a koto — fast plucked strings in a minor pentatonic — drives the pace of each combination strike. A deep taiko strike punctuates each guard's takedown. After the final guard falls, all instruments cut to silence, leaving only rain on the roof and wind through the broken screen.
```

---

## 模式 7：忍者无声杀 — 城堡暗杀（T2VA，15 秒，5 镜头）

一段近乎窒息的安静潜入与暗杀序列。展示如何通过声音的几乎完全缺席、有耐心的相机移动，以及三次亲密程度递进的连续杀戮 — 从远处的卫兵到目标本人 — 来构建张力。

### 关键模式
- **以缺席为工具**：`non_diegetic_music: N/A` — 无配乐、无氛围铺垫，彻底的静默即张力
- **杀戮亲密程度递进**：卫兵 1（背后、下颌）→ 卫兵 2（颅底、血滴）→ 大名（捂眼、颈部）
- **蜡烛/灯笼作为灯光纪律**：每个光源是一座小岛；之间的一切是深黑
- **相机的耐心**：慢推、贴地仰角、定格长持 — 速度会背叛静默
- **墨迹一笔**：大名的毛笔僵住又拖着划出最后一笔死去 — 标记杀戮的视觉诗意

### 输出

```
integrated_multimodal_description: [Shot 1] Ultra-realistic cinematic live-action with extreme shallow depth of field, chiaroscuro candlelight, and near-total darkness dominant. A slow tracking shot moves through a dark wooden corridor of a Japanese castle at night — narrow plank flooring, wooden lattice walls, widely spaced iron candle brackets each holding a single dim flame. The corridor is deep black except for small amber pools around each candle. THE NINJA — a lean figure wrapped entirely in matte charcoal-black cloth, only a narrow slit revealing sharp dark eyes, black tabi boots, a short ninjato and a tanto dagger concealed at his lower back — moves down the corridor in absolute silence, his weight on the balls of his feet, back flat against the wooden wall, passing between candlelight pools without disturbing the flames. Ahead, a heavy sliding door of dark lacquered wood glows faintly at its edges from interior light. The camera tracks forward at slow speed behind the ninja's shoulder, candlelight briefly catching the texture of his black cloth wrapping with each pass. His breathing is invisible, controlled.
[Shot 2] At 00:03.000, the shot cuts to a close-up of the ninja's black-gloved hand sliding the lacquered wooden door open one inch — just enough to see through. The camera pushes in with small amplitude at slow speed toward the gap. Through the narrow opening: THE DAIMYO, a heavyset Japanese man in his fifties with a close-cropped grey beard, wearing a deep crimson silk inner robe, sits cross-legged at a low writing desk lit by a single paper lantern, brush in hand, writing on a scroll. Two SAMURAI GUARDS in dark indigo kimono, wakizashi at their hips, stand flanking the door on the interior — one at Screen Left, one at Screen Right, both facing forward, backs partially to the door. The room is spacious with tatami flooring, a weapon rack displaying a katana on the far wall, and a single paper lantern casting warm but limited light, leaving the corners in deep shadow.
[Shot 3] At 00:06.000, the shot cuts to a low-angle extreme close-up from floor level as the ninja slides through the opened door in a single fluid motion, his body staying below the guards' sightlines, tabi boots whispering on the tatami without sound. The camera tilts up slowly, tracking the ninja's body as he flows across the tatami in a low crouch toward the Screen-Left guard's blind spot. The guard at Screen Left shifts his weight slightly — his straw sandal scraping the tatami — but does not turn. The ninja rises behind the guard, one black-gloved hand clamping over the guard's mouth and nose from behind, the other hand drawing the tanto from his own lower back. The tanto blade — short, plain wooden handle, thin steel — catches a sliver of lantern light. In one compressed motion the ninja drives the tanto upward beneath the guard's jaw, holds for one second as the man's body stiffens, then lowers him silently to the tatami. The Screen-Right guard has not turned. The camera holds on the controlled descent, the lantern flame steady.
[Shot 4] At 00:09.000, the shot cuts to a medium shot from the Screen-Right guard's perspective, looking across the room. The Screen-Left guard appears to still be standing — but as the camera holds, the ninja's black-wrapped form separates from the shadow behind the fallen guard's body, already moving. The Screen-Right guard turns his head at the faintest sound — a single thread of the dead guard's indigo kimono settling. The ninja is already there, materializing from the dark corner like poured ink. The guard opens his mouth to shout but the ninja's left hand seals it shut while his right — still holding the tanto, its blade now dark — drives it into the base of the guard's skull from behind. The guard's eyes widen, then glaze. His knees buckle. The ninja guides the body down in absolute silence, one hand on the man's collar, the other withdrawing the tanto with a controlled pull. A single drop of dark blood falls from the blade onto the tatami. The camera pushes in with small amplitude at slow speed toward that falling drop.
[Shot 5] At 00:11.500, the shot cuts to a wide shot from the doorway looking into the room. THE DAIMYO, in his deep crimson silk robe, is still writing, unaware. The two guards lie motionless on the tatami in deep shadow, their positions unseen from the writing desk. The paper lantern casts its warm pool around the daimyo, leaving the approach path in darkness. The ninja, a silhouette of black cloth against black shadow, crosses the remaining distance in three silent strides — each step timed to the daimyo's brush strokes. On the third brush lift, the ninja arrives directly behind the daimyo. The ninja's left hand clamps the daimyo's forehead, pulling the head back to expose the neck. The tanto, dark with the blood of the two guards, comes around from the right. The daimyo's brush freezes mid-stroke. His eyes — wide, reflecting the lantern flame — are the last things visible before the ninja's black-gloved hand obscures them. The camera holds on this tableau for two seconds — the lantern flame flickering once — then the ninja releases the body and the daimyo slumps forward onto his writing desk, his brush hand dragging a final ink stroke across the scroll. The ninja sheathes the tanto, steps back into the darkness beyond the lantern's reach, and is gone. The camera holds on the lit room — the daimyo slumped, the scroll, the single flickering lantern, and the two unseen bodies in the shadows. Silence.

overall_soundscape: Near-total silence dominates the entire sequence. The only sounds are the faint creak of wooden planks under careful weight, the soft whisper of cloth on cloth as the ninja moves, and the single scrape of a straw sandal when a guard shifts. The lacquered door slides open with a barely audible wooden groan. A brush scratches lightly on paper. On each kill, a single wet, subdued sound — barely more than a breath — is followed by the muffled rustle of a body being lowered to tatami. A single drop of liquid — blood — taps the tatami with a faint tick. No breathing from the ninja is ever audible.

non_diegetic_music: N/A
```

---

## 模式 8：忍者木廊连击 — 雷雨寺顶追逐（T2VA，15 秒，5 镜头）

一段雷雨夜发生在寺庙建筑群高架木廊与木桥上的外部追逐+战斗序列。展示如何把建筑同时用作竞技场与武器，并让天气成为每个镜头的动态参与者。

### 关键模式
- **建筑即竞技场**：高架廊道、栏杆边缘、塔楼阳台、横跨深谷的窄桥 — 每个地点提供独特战斗地理
- **天气即参战者**：雨让表面湿滑（卫兵失足）、风摇动灯笼（动态光）、雷声掩盖声响
- **垂直地理**：追逐沿结构向上推进 — 廊道层 → 栏杆 → 阳台 → 桥 → 空中揭示
- **武器规格递升**：ninjato vs katana → ninjato vs 双 katana → ninjato vs nodachi（大太刀）— 一场比一场大
- **闪电作为灯光工具**：频闪定格画面、与配乐中的大鼓重击同步、为建筑剪影造型

### 输出

```
integrated_multimodal_description: [Shot 1] Ultra-realistic cinematic live-action with dramatic backlighting, volumetric rain and mist, and a rich amber-and-teak color palette. A high wide shot establishes an ancient Japanese wooden temple complex during a heavy thunderstorm at night — a multi-tiered pagoda with dark cypress-bark roofing, interconnected raised wooden walkways spanning between buildings, rain streaming off curved eaves, paper lanterns swinging wildly in the wind along the walkway railings. Lightning flashes silhouettes the structure against black sky. THE NINJA — lean, wrapped entirely in charcoal-black cloth, only narrow eye slit visible, black tabi boots, ninjato strapped across his back — sprints along a raised wooden walkway, rain hammering his black wrappings. Behind and above, FOUR SAMURAI GUARDS in dark indigo armor and straw sandals give chase across the wet wooden planks, their sandals slapping the surface. The camera tracks the ninja from behind at fast speed, tilting down as he reaches a T-intersection where the walkway branches left toward a higher pagoda balcony and right toward a bridge over a courtyard gap. The ninja leaps onto the wooden railing and runs along its narrow edge toward the left branch. Rain sheets across the frame.
[Shot 2] At 00:03.000, the shot cuts to a dynamic low-angle tracking shot from walkway level, tilted up at the ninja as he runs along the railing edge — wet dark wood beneath his tabi boots, the pagoda's massive curved roof and swinging paper lanterns filling the upper frame. The lead samurai guard — a tall man in dark indigo armor with a katana drawn — vaults onto the railing behind him and closes the gap. The guard lunges with a thrusting katana strike aimed at the ninja's back. Without breaking stride, the ninja drops into a slide on the wet railing, the katana blade passing inches above his head, rain spraying from his boots. He grabs a wooden support post at the railing's end, swings his body around it in a tight arc, and launches a spinning back kick into the guard's chest as the man's momentum carries him forward. The guard flies off the railing and crashes through a paper screen on the pagoda balcony. The camera arcs right with large amplitude at fast speed, sweeping around the post with the ninja's swing, the storm-lit courtyard visible far below between the wooden structures.
[Shot 3] At 00:06.500, the shot cuts to a medium tracking shot on the pagoda balcony as the ninja lands on the wet wooden planks. Two more samurai guards — one from each end of the balcony — converge on him simultaneously, katana drawn. The ninja draws his ninjato in a reverse grip and meets the first guard's downward katana cut with an upward diagonal block, steel sparking steel with a sharp ring that echoes through the storm. He redirects the force leftward, opening the guard's center, and drives a front kick into the man's armored stomach, sending him stumbling into the paper screen debris where the first guard already lies. The second guard swings a horizontal cut. The ninja drops to one knee on the wet wood, the katana whistling over his head, and slashes the ninjato across the back of the guard's lead knee — the man's straw sandal loses grip on the wet plank and he collapses. The ninja rises and delivers a sharp downward pommel strike to the fallen guard's temple. Rain pours across the balcony, washing blood from the ninjato blade. The camera pushes in with small amplitude at fast speed, handheld with slight shake, tracking each exchange.
[Shot 4] At 00:10.000, the shot cuts to a wide shot from across the courtyard gap as the ninja — black cloth soaked and clinging to his frame — sprints across a narrow wooden bridge connecting the pagoda balcony to the adjacent building. The bridge is barely two planks wide with a low rope railing, slick with rain, suspended over a five-story drop. The fourth and final samurai guard — a massive broad-shouldered man in full dark indigo armor, a nodachi longsword gripped two-handed — crashes onto the bridge behind him. The bridge sways and groans under their combined weight. The guard swings the nodachi in a massive overhead arc. The ninja parries with the ninjato held two-handed — the impact nearly buckles his knees, wood splintering from the bridge railing where the nodachi glances off. The ninja kicks the guard's lead foot, destabilizing him on the slick surface, then spins and slashes the ninjato across the guard's sword arm. The nodachi drops from the guard's grip and tumbles off the bridge into the dark courtyard below. The camera is positioned at bridge-end, capturing the fight in profile against the storm-lit sky, lightning flashing behind the figures, rain streaking horizontally across the frame. The bridge creaks and sways with each movement.
[Shot 5] At 00:12.500, the shot cuts to a low-angle close-up on the swaying bridge as the ninja — rain streaming down his black cloth wrapping — delivers a final spinning heel kick to the disarmed guard's chest. The guard staggers backward, his armored boots losing traction on the slick wet plank, and topples backward off the bridge railing — his dark indigo armor disappearing into the rain-filled darkness below, the sound of his fall swallowed by the storm. The ninja stands alone on the center of the swaying bridge, ninjato in reverse grip at his side, breathing hard — the only visible motion on the bridge. He sheathes the blade across his back. The camera pulls back and pedestals up with large amplitude at slow speed, rising above the bridge to reveal the full temple complex — tiered pagoda roofs, raised wooden walkways, swaying paper lanterns — all battered by the thunderstorm, the ninja a single black figure on a narrow bridge in the center of the vast wooden architecture. Lightning flashes one final time, freezing the entire complex in white light. The camera holds.

overall_soundscape: Heavy thunderstorm rain hammers wooden rooftops, planks, railings, and paper screens throughout, producing a constant percussive roar. Bare tabi boots and straw sandals slap, skid, and slide on wet wood with sharp friction sounds. Steel clashes against steel with bright ringing impacts that reverberate through the open structures. Wood splinters and cracks when blades and bodies strike railings and screens. The bridge groans and creaks under shifting weight. A heavy armored body falls from the bridge with a long, fading sound swallowed by wind and rain. Distant thunder rumbles beneath the action.

non_diegetic_music: A driving, percussive taiko-and-shamisen score matches the chase rhythm — rapid taiko beats at a fast tempo driving each footstep and strike, layered with sharp shamisen string strikes that punctuate each blade clash and impact. Lightning flashes coincide with deep bass-drum hits. As the final guard falls and the camera rises above the temple complex, the rhythm decelerates into a single sustained low taiko rumble that fades beneath the storm, leaving only rain and thunder.
```

---

## 模式 9：现代舞 × 超自然刀剑战斗 — Seedance 转 H3（T2VA，15 秒，5 镜头，9:16）

一段高端 3D 电影级序列，将现代舞编排与对抗影狼的超自然武士刀战斗融合。由 Seedance 2.5 提示词转换而来。展示如何把密集的单段动作提示词改编进 H3 的多镜头结构，同时为超自然敌人建立递进升级系统。

### 关键模式
- **以舞为战的编排**：每一次攻击都源自一个点名的舞蹈技法 — 下腰、旋转、地面滑行、空中收拢、鞭转、plié 深蹲
- **超自然敌人系统**：影狼（黑烟体、发红光的眼睛）解体为墨黑粒子 + 绯红碎裂拖尾 — 每次击杀一致的视觉语言
- **刀刃能量签名**：每一道刀弧都在空气中撕裂出绯红布状能量 — 贯穿所有攻击的持续视觉标记
- **递进升级**：1 狼 → 3 狼 → 1 空中 → 5 狼 → 1 巨型头狼 — 狼群渐长后在 Boss 处达到峰值
- **环境一致性**：每个镜头都有湿润反光地板 + 冷色体积雾 — 锚定黑暗虚空场景
- **Seedance→H3 转换**：单段落 → 5 个计时镜头；泛化相机语言 → 每镜头具体 type+amplitude+speed；@[character ref] → 完整内联描述（T2VA）

### 输出

```
integrated_multimodal_description: [Shot 1] High-end cinematic 3D realism with feature-film rendering quality, controlled motion blur, realistic cloth dynamics, and a dark atmospheric palette dominated by deep blacks, cold steel highlights, crimson energy, and ink-dark particle effects. Volumetric haze fills the space. A medium tracking shot follows THE DANCER — a beautiful woman in her mid-twenties with a lean athletic dancer's build, long flowing dark hair that whips with every movement, fair porcelain skin, sharp striking features, wearing a form-fitting dark charcoal sleeveless performance top, bare-armed, loose dark leggings that ripple with fabric dynamics, and bare feet — as she stands center-frame in a dark void-like space with a wet reflective floor surface and cold volumetric fog drifting at ankle height. A SHADOW WOLF — a massive predatory silhouette formed entirely of dense black smoke-matter with no solid texture, only glowing dim red eyes and a lunging open maw of collapsing dark particles — leaps through the fog directly at her from Screen Right. The dancer folds beneath the attack in a violent backbend, her spine curving deeply, long dark hair sweeping the wet floor, as she draws a single katana — a sleek Japanese longsword with a dark handle and gleaming steel blade — from her hip in a fluid underhand arc that carves upward through the wolf's body. Crimson fabric-like energy tears through the air along the blade's path. The shadow wolf splits apart, its smoky form disintegrating into ink-dark particles and crimson fragments that scatter and dissolve in the haze. The camera orbits around her recovery arc with large amplitude at fast speed, capturing her body unfolding from the backbend into a combat-ready crouch.
[Shot 2] At 00:03.000, the shot cuts to a low-angle tracking shot from floor level tilted up at the dancer as she explodes from the crouch into a rapid spinning sequence — a contemporary dance spin that accelerates into a whirlwind of movement, her dark hair fanning outward, loose leggings rippling with realistic cloth dynamics, bare feet pivoting on the wet reflective surface. THREE MORE SHADOW WOLVES — each a dense predatory silhouette of black smoke-matter with glowing red eyes — circle her from different angles, lunging in from Screen Left, Screen Right, and Front-Center. The dancer's spin becomes a sweeping katana arc that catches the first wolf mid-lunge across its flank — the blade slices through smoke-matter, sending a ribbon of crimson fabric-like energy trailing behind it as the wolf splits and collapses into ink-dark particles. She drops instantly from the spin into a deep floor slide on the wet surface, her body extending horizontal beneath the second wolf's leaping attack, katana held outward so the blade catches the wolf's underbelly as it passes over her — the wolf shears apart above her into cascading black vapor. The camera tracks the floor slide at fast speed, low angle capturing the wet floor reflections and trailing particle effects. The dancer rolls out of the slide back onto her feet in one fluid recovery.
[Shot 3] At 00:06.000, the shot cuts to a dynamic medium shot with aggressive lateral camera acceleration as the dancer launches into an aerial contraction — a powerful upward leap from the wet floor, both knees tucking to her chest, her body coiling tight at the apex. The third shadow wolf lunges upward toward her. At the peak of her jump, the dancer whips her katana in a tight horizontal arc — a single clean strike that shears through the wolf's smoky form at neck height. The wolf's head separates from its body, both halves erupting into cascading ink-dark particles and crimson fragment trails that hang suspended in the volumetric haze around her airborne silhouette. As she descends, her body extends into a dramatic deep backbend mid-air — one arm reaching back, the katana trailing a ribbon of crimson energy behind it, long dark hair fanning upward. She lands on the wet floor in a controlled one-footed landing, the impact sending a circular ripple across the reflective surface. The camera pushes in with extreme foreshortening toward her landing point, distorting the sense of depth and speed. Cold fog swirls around her bare feet.
[Shot 4] At 00:09.000, the shot cuts to a spiraling orbit shot that circles the dancer at fast speed with large amplitude as a FINAL WAVE of FIVE SHADOW WOLVES — the largest pack yet, each wolf bigger and denser with brighter red eyes — converges on her simultaneously from all directions. The dancer accelerates through a continuous sequence of whipping turns, each rotation flowing directly into a katana strike: the first turn is a rising diagonal slash that bisects a wolf lunging from Screen Left — the second is a descending overhead cut that splits a wolf from above — the third is a horizontal spinning slash that cleaves through two wolves simultaneously as they leap from opposite sides. Each blade arc tears a long ribbon of crimson fabric-like energy through the air, and each disintegrating wolf bursts into a cloud of ink-dark particles and collapsing black shockwaves that radiate outward from the point of impact. The dancer's movements are graceful and feral simultaneously — contemporary dance technique expressed as lethal combat choreography. Her dark performance top and bare arms glisten with a fine layer of moisture from the cold haze. The camera spirals through the pack with her, sometimes passing between disintegrating wolves, particles streaming past the lens in motion blur.
[Shot 5] At 00:12.000, the shot cuts to a low-angle wide shot as the last remaining shadow wolf — the largest, twice the size of the others, its smoke-matter form denser and more defined — rears back and lunges directly at the dancer from Screen Right. She meets the charge head-on, launching off the wet floor into a powerful rotating slash — her entire body spinning horizontal at chest height, katana extended, long dark hair whipping in a full arc, loose leggings flaring outward. The blade meets the wolf's center mass. For a frozen instant — a brief slow-motion frame — the katana is embedded in the wolf's smoky form, crimson energy crackling along the blade, the wolf's red eyes flickering. Then the dancer completes the rotation, pulling the blade through in a clean horizontal draw. The wolf splits apart in an eruption of ink-dark particles, crimson fragment trails, and a collapsing black shockwave that ripples outward across the wet floor, disturbing the fog layer in an expanding ring. The dancer lands softly on the wet surface in a deep dancer's plié, katana held extended to the side, its blade still trailing wisps of crimson energy that slowly dissipate. Long dark hair settles around her shoulders. She straightens slowly, her breathing visible in the cold air. The camera holds on her silhouette — a single figure in a vast dark space, the wet floor reflecting her form and the fading crimson glow, surrounded by drifting ink-dark particles that are slowly dissolving into nothing. Volumetric haze rolls back in. The camera holds.

overall_soundscape: Bare feet strike and slide on a wet reflective surface with sharp percussive slaps and fluid friction sounds. The katana cuts through dense air and smoke-matter with a resonant steel ring that sustains and decays after each arc. Shadow wolves emit a low, barely-audible harmonic growl that modulates as they disintegrate into a rush of displaced air. Deep, full-body impacts produce muffled concussive thuds as collapsing black shockwaves radiate outward. The dancer's controlled breathing — rhythmic, deliberate — is audible between strikes.

non_diegetic_music: A hybrid electronic-orchestral score drives the entire sequence — a pulsing analog synth bassline at a fast tempo layered with rapid, irregular percussion that matches the dancer's rhythmic footwork. Sustained string swells rise during each aerial movement and peak on each blade impact, resolving into sharp decays. A distorted, processed vocal hum enters during the final wave, building in intensity and cutting abruptly to a single sustained low cello note as the last wolf disintegrates, decaying into silence over the final held frame.
```
