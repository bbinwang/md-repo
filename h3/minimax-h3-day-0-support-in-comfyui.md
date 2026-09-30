# MiniMax H3 Day-0 Support in ComfyUI: Open Weights, Native Audio, and 2K Video

> 原文：[ComfyUI Blog — MiniMax H3 Day-0 Support in ComfyUI](https://blog.comfy.org/p/minimax-h3-day-0-support-in-comfyui) · Comfy Org

MiniMax H3 今日发布开放权重，并已于当天早晨在 ComfyUI 中获得原生支持——第 0 天（Day-0）支持。

这是一个下一代开放权重视频模型。输入文本、图像、视频或音频，它就能生成带真实立体声的视频，最高 2K 分辨率、单条最长 15 秒。这是 MiniMax 的第三代视频模型（继 Hailuo 01 和 Hailuo 02 之后），也是该公司首个开放权重的视频模型。

[在 Comfy Cloud 上试用](https://links.comfy.org/4pTj4QV)

## 模型亮点

- **文生视频（Text-to-video）**——仅靠提示词。

- **图生视频（Image-to-video）**——让静态图像动起来。

- **首尾帧控制（First-and-last-frame）**——控制开头帧、结尾帧或两者，其余由模型补全。

- **参考生成视频（Reference-to-video）**——提供参考图像、视频或音频，将主体、运动或声音贯穿整条视频。

输出可达 2K、最长 15 秒。音频与视频在同一个生成过程中同步产出，原生立体声，而非后期合成。

### 多模态上下文理解

这是 MiniMax 最先宣传的能力，也是把五个独立任务合并为一个模型的关键。真实工作很少只用单一模态：H3 同时接收图像、音频和视频，并根据提示词中描述的它们之间的关系进行理解。只需描述输入素材与你想要的镜头之间的关系，模型会自己完成跨模态处理。

### 原生立体声音频

音频是模型自身的属性，不是后处理。所有音频输出均为原生立体声。

### 编辑与运动迁移

运动迁移（motion transfer）对节点工作流最关键：参考视频提供运动——运镜、表演、剪辑节奏——而主体和风格来自其他素材。结合原位编辑（in-place editing），可以不断迭代同一个镜头。

## 示例提示词

### 示例 1：漫画风超级英雄

```
Bold comic-book ink style, heavy linework, red and blue-black palette, night city. Use <Picture 2> and <Picture 1> as reference frames and <Audio 1> exactly as it is.
CUT 1: top-down view of the little boy superhero on the rooftop — red cape fluttering in the wind, hands planted on his hips, freckles and a cocky grin as he looks straight up into the camera. The camera slowly descends toward him as he delivers his line — as he speaks, comic-book graphic overlay text word by word in sync with his voice: "GET READY TO" - "MEET" — "YOUR" — "MAKER" — huge jagged comic lettering, white with heavy black outlines and red drop shadows, tilted at scrappy angles, until the three words hang stacked in the air above him between his face and the lens.
TRANSITION: a violent WHIP PAN off the rooftop that SMEARS the floating words away with it, motion-streaked —
CUT 2: low hero angle on the colossal black mech-kaiju towering over the skyline as it rears back and unleashes a GIANT terrifying ROAR — jaws wide with fangs, red eyes and chest-core flaring blinding bright, blue lightning arcing off its head, the roar's shockwave rippling dust and rattling windows down the buildings, comic-style speed-lines and ink splatter bursting from the impact of the sound. It leans INTO the camera as the roar peaks. Hold on the roar.
```

### 示例 2：透明电竞鼠标产品片

```
Editorial tech product film. The transparent gaming mouse from <Picture 1> in its original scene: a pitch-black studio void with a dark, subtle reflective surface, lit by dramatic duotone vibrant blue and warm neon orange rim lighting, deep soft shadow falloff into pure black. Monochromatic dark palette with electric blue and amber accents. Material motif: glowing internal metallic micro-components and glossy acrylic refractions. The environment is constant throughout.
SHOT 1: The scene opens exactly on image 1, the mouse resting confidently on the dark surface; the blue and orange lights slowly pulse brighter, refracting deeply through the transparent acrylic shell as the camera executes a slow, deliberate push-in to reveal the intricate circuitry.
SHOT 2: Cut to an extreme macro profile of the ridged scroll wheel and layered internal micro-components; the camera glides slowly along the side as a sharp beam of warm orange light sweeps across the metallic textures, contrasting perfectly against the deep blue ambient glow.
SHOT 3: Cut to a low-angle beauty shot: the mouse levitates weightlessly a few centimeters above the dark reflective surface, rotating in a slow, precise orbit; the duotone lighting flares gently along the glassy transparent edges before fading slowly into a sleek silhouette.
Audio: deep pulsing sub-bass room tone, sharp tactile mechanical clicks, a sweeping glassy whoosh on cuts, and a rising electronic swell that resolves to near-silence on the final fade.
```

### 示例 3：金缮面具时尚大片

```
High-fashion editorial film, luxurious slow motion throughout, soft gradient studio sky. 
MUSIC & SFX: a cinematic score fusing deep taiko drums, shimmering koto plucks and modern sub-bass drives the film

SHOT 1: beside her, the mask hangs BROKEN — shattered into the floating shard formation of <Picture 2>, every kintsugi piece suspended and slowly rotating in place, the gold seams between them dim and waiting. She turns her eyes to it.
SHOT 2: THE ASSEMBLY, with enormous energy — the gold seams IGNITE, arcs of molten light leaping shard to shard like welding fire, and the pieces snap together one by one, accelerating from slow to rapid-fire, each snap flaring gold, molten droplets spinning off, the surrounding liquid ribbons shuddering with shockwave ripples — until the final shard slams home and the whole mask fuses, its kintsugi veins blazing.
SHOT 3: the golden dragon of <Picture 3> SWOOPS through the frame in one huge serpentine fly-through — red glass antlers first, its coils wrapping the space around her and the mask, scales throwing golden light, its wake dragging the crimson liquid into a spiral behind it.
SHOT 4: in the dragon's wake the mask magnetically RIPS across the air onto her face — a fast, hard, perfectly straight pull — seating with a deep flare as every gold crack lights, and glowing kintsugi veins spread from the mask's edge down her neck and across the sunset jacket, embroidery igniting thread by thread.
SHOT 5: she descends and lands softly ON the dark liquid wave, snapping into a poised warrior stance and holding it like a lookbook frame — the dragon coiled behind her shoulder, both liquids spiraling upward around her into a double helix. Held editorial poster frame as the camera settles.
Use <Picture 1>, <Picture 2>, <Picture 3> as reference images. 
```

### 示例 4：鱼眼汽水广告

```
Vibrant fisheye product commercial, hyper-saturated summer light, the woman from <Picture 1> in a yellow raincoat crouched by a jungle waterfall holding a rainbow-gradient soda can toward the lens, condensation dripping.
MUSIC: an upbeat tropical house track drives the entire film — punchy kick drum, bright steel-drum plucks, warm bass groove.

CUT 1 : the fisheye hero frame — as she looks into the lens, GIANT BOLD TYPOGRAPHY stamps across the background behind her, one word per beat: "STAY" then "HYDRATED" — massive clean white block letters spanning the whole scene, curving with the fisheye distortion, sitting behind her but in front of the waterfall. She reaches her opposite hand towards the can and hooks a finger under the tab.
TRANSITION: extreme close-up of the tab — it OPENS with a crisp CLICK-hiss, and exactly on the click the fisheye lens iris shutters closed to black, like a camera blinking.
CUT 2: the iris reopens on a new POV — the can EXTREMELY distorted in the foreground, huge and warped by the fisheye, she smiles and dumps the liquid out of the can onto the floor, droplets scattering weightlessly, sunlight refracting rainbow through the stream, the waterfall soft behind her.
TRANSITION: she lowers the can and one fat droplet falls toward the lens, filling the frame —
CUT 3: through the droplet into the final wide: the rainbow can floating upright and serene in the turquoise waterfall pool, label facing camera, bobbing gently in the mist, the waterfall thundering softly behind — and "STAY COMFY" shimmering as a reflection on the water's surface beside it. Hold the product hero frame.
Crisp, joyful, premium product-ad energy. Fisheye distortion in every shot.
```

## 为 ComfyUI 本地推理深度优化

让 H3 在消费级硬件上流畅运行需要大量机器学习工程。团队发现模型的调制权重（约占参数总量 40%）可以被剪枝，并用功能等价的查找表（lookup table）替代，在不损失输出质量的前提下大幅缩小显存占用。

在此基础上，权重自带精确高效的 int8 convrot 量化，自定义算子（custom kernels）进一步降低了推理时的峰值显存。

最终总显存占用**降低 66%：从全精度 123.6 GB 降到最小模型变体的 42.5 GB**。配合动态 VRAM 卸载（dynamic VRAM offloading），让这个下一代 2K 视频模型可以在 RTX 3060 这类显卡上本地运行。

## 快速上手

- 更新 ComfyUI 到最新版 **0.30.0**，或使用 [Comfy Cloud](https://links.comfy.org/4pTj4QV)

- 下载以下工作流，或在模板库中找到它们：

[下载 MiniMax H3 I2V 工作流](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_i2v.json)

[下载 MiniMax H3 R2V 工作流](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_r2v.json)

[下载 MiniMax H3 T2V 工作流](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_t2v.json)

- 按工作流内的说明下载模型，保存到正确的模型目录。

- 编写提示词，接入任意帧或参考输入，运行。

模型权重：🤗 [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3)

一如既往，享受创作吧！
