---
pipeline_tag: image-text-to-video
license: other
license_name: minimax-h3-community-license-agreement
license_link: LICENSE
library_name: minimax-h3
tags:
  - text-to-video
  - image-to-video
  - image-text-to-video
  - video-to-video
  - text-to-audio-video
  - image-to-audio-video
  - image-text-to-audio-video
  - video-to-audio-video
  - audio-to-audio-video
  - audio-video-generation
  - multimodal
  - synchronized-audio-video
  - reference-to-audio-video
  - diffusers
---

> 原文：https://huggingface.co/MiniMaxAI/MiniMax-H3 （模型卡 README，中文翻译）

<div align="center">
  <img width="100%" src="assets/minimax-h3.png" alt="MiniMax">
</div>

<p align="center">
  <a href="https://hailuoai.video" target="_blank"><img src="https://img.shields.io/badge/Hailuo%20AI-FF6C37?logo=minimax&logoColor=white" alt="Hailuo AI"></a>
  <a href="https://platform.minimax.io/docs/guides/text-generation" target="_blank"><img src="https://img.shields.io/badge/API-FF6C37?logo=minimax&logoColor=white" alt="API"></a>
  <a href="https://www.minimax.io" target="_blank"><img src="https://img.shields.io/badge/MiniMax%20Website-FF6C37?logo=minimax&logoColor=white" alt="MiniMax Website"></a>
  <a href="https://github.com/MiniMax-AI/MiniMax-H3" target="_blank"><img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white" alt="GitHub"></a>
  <a href="https://huggingface.co/MiniMaxAI/MiniMax-H3" target="_blank"><img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=black" alt="Hugging Face"></a>
  <br>
  <a href="https://modelscope.cn/organization/minimax" target="_blank" rel="noopener noreferrer"><img alt="ModelScope MiniMax AI" src="https://img.shields.io/badge/ModelScope-MiniMax%20AI-white?labelColor=%23EF3D5D"></a>
  <a href="https://platform.minimaxi.com/docs/faq/contact-us" target="_blank"><img src="https://img.shields.io/badge/WeChat-07C160?logo=wechat&logoColor=white" alt="WeChat"></a>
  <a href="https://discord.com/invite/dbMxutw7tP" target="_blank"><img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE"><img src="https://img.shields.io/badge/LICENSE-4CAF50?logo=creativecommons&logoColor=white" alt="LICENSE"></a>
</p>


# MiniMax H3

## News
官方提供的提升提示词写作水平的技能（skills）：[skills on github](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills)

## Online API
通过 API 直接使用 MiniMax\-H3。
- 国际版：[platform\.minimax\.io](https://platform.minimax.io/docs/api-reference/video-generation-v2-create) \| 中国版：[platform\.minimaxi\.com](https://platform.minimaxi.com/docs/api-reference/video-generation-v2-create)

## Online App
通过 App 直接使用 MiniMax\-H3。
- WebApp 国际版：[hailuoai\.video](https://hailuoai.video/tools/minimax-h3) \| 中国版：[hailuoai\.com](https://hailuoai.com/)
- 桌面端 国际版：[hub\.minimax\.io](https://hub.minimax.io/) \| 中国版：[hub\.minimaxi\.com](https://hub.minimaxi.com/)

## 系统概览
MiniMax H3 是一个通用全模态（omni-modal）生成系统。它支持对由文本、图像、视频和音频组成的多模态上下文进行统一理解，并可生成分辨率最高 2K、时长最长 15 秒、带原生立体声音频的视频。得益于面向任务泛化的系统设计，H3 在预训练阶段就具备广泛的多模态上下文理解与生成能力，从而能够出色地遵循复杂的多模态指令。

H3 支持以下输入与输出规格：

| 类别 | 规格 |
|---|---|
| 输出时长 | 4–15 秒 |
| 输出宽高比 | 支持多种宽高比，包括但不限于 21:9、16:9、4:3、1:1、3:4、9:16 |
| 输出分辨率 | 支持多种分辨率。默认短边为 768 像素。使用 H3-Regenerate-2K 可实现 2K \| 生成 |
| 输出帧率 | 24 FPS |
| 输出音频 | 32 kHz 立体声 |
| 支持的对话语言 | 稳定支持 11 种语言：阿拉伯语、中文、英语、法语、德语、意大利语、日语、韩语、葡萄牙语、俄语、西班牙语；其他语言也有不同程度的支持 |

### 模型变体与输入规格

| 模型变体 | 输入模式 | 规格 |
|---|---|---|
| H3-Base-FL2VA | 首尾帧模式 | 支持输入零张、一张或两张图像。 <br><br>- 无图像输入：文生视频模式 <br>- 一张图像输入：首帧生视频或尾帧生视频 <br>- 两张图像输入：首尾帧生视频 |
| H3-Base-Ref2VA | 全参考（omni-reference）模式 | 支持多模态参考输入： <br><br>- **图像：** ≤ 9 张 <br>- **视频：** ≤ 3 段；每段须为 2–15 秒；总时长 ≤ 15 秒 <br>- **音频：** ≤ 3 段；每段须为 2–15 秒；总时长 ≤ 15 秒 <br>- **混合输入：** 所有输入类型的文件总数最多 12 个 |

![Image](assets/overview.png)

完整的 H3 系统由以下三个模块组成：
- H3-Context-IR：随着输入日益复杂，我们构建了一个专用系统来深入理解并精炼输入的多模态指令，然后将其转换为 H3 能够直接理解的形式——上下文中间表示（Context Intermediate Representation）——用于生成。**H3-Context-IR 对最终输出质量至关重要，因此我们强烈建议将其接入你的生成流水线，或者按照「提示词指南（Prompting Guidance）」构建你自己的上下文处理系统。**
- H3-Base：基于 H3-Context-IR 的输出生成音频和视频，产出 768p 分辨率的结果。
- H3-Regenerate-2K：将 768p 结果连同原始上下文一起回灌给 H3，以 2K 分辨率重新生成输出。该过程既利用了 H3 强大的生成能力，也利用了原始上下文中蕴含的丰富信息，从而能够产出细节更准确、视觉保真度更高的高分辨率输出。

## 模型架构

### H3\-Context\-IR

H3\-Context\-IR 是一个面向自由格式多模态输入的托管式预处理与编排系统。

它能够解读文本、图像、音频和参考视频之间的关系，以及这些素材与预期生成输出之间的关系。其内部工作流包括指令解析、跨模态关联、时序理解与复杂逻辑推理。

H3\-Context\-IR 将其对上下文的理解序列化为 H3\-Base 可接受的结构化表示。在不偏离用户原始意图的前提下，它也会在适当之处补充缺失或欠明确的语义细节。

由于 H3\-Context\-IR 依赖多阶段工作流以及多个托管模型和服务，它未包含在本次开源发布中。我们提供了可复现官方工作流行为的 API，同时提供详细教程，开发者可以按照 **Prompting Guidance（提示词指南）** 构建自己的预处理系统。

详细使用说明见 **Recommended Workflow — Full 2K Workflow（推荐工作流 — 完整 2K 工作流）**。

**安全护栏**

用户提交的文本、图像和视频以及增强后的提示词都会经过自动审核。涉嫌违法、色情或侵犯第三方权利的内容可能被拦截。我们采用业界标准的过滤措施，但无法完全消除误判和漏判。这些护栏不影响被许可方在 MiniMax H3 Community License 下的义务，尤其是与合法使用和使用限制相关的义务。

### H3\-Base

![Image](assets/full-arch.png)

#### 架构概览

- H3\-Base 使用各模态对应的编码器或 VAE 对不同模态进行编码，并将编码后的表示组织成统一的打包多模态序列。在整段序列送入 H3\-Omni\-Transformer 之前，使用 RoPE 捕获 token 之间必要的空间与时间关系。

- 具体而言，文本由 H3\-Encoder 编码；视觉输入由 H3\-Encoder 和 H3\-VisualVAE 共同编码；音频仅由 H3\-AudioVAE 编码。

- H3\-Omni\-Transformer 联合预测视频与音频 latent，随后分别解码为视频和立体声音频。

- 为降低长多模态序列的计算开销，H3 原生支持稀疏注意力（sparse-attention）训练与推理。首发开源版本仅提供全注意力（full attention）推理。我们的稀疏注意力实现将在后续更新中发布。

#### H3\-Encoder

- H3\-Encoder 使用 Qwen3\-VL\-32B 的完整预训练权重，并将第 50 层的隐藏状态提供给 H3\-Omni\-Transformer。

- 我们在 tokenizer 配置中添加了若干特殊 token，如 `<d>`。使用 H3 时，必须使用 H3 仓库中提供的 tokenizer 及相关配置文件。

#### H3\-VAE

H3 使用相互独立的视觉与音频 latent 来表示各自的模态。

##### H3\-VisualVAE

- H3\-VisualVAE 是一个时间因果（temporally causal）视频自编码器，空间压缩倍率为 16×，时间压缩倍率为 4×，具有 24 个 latent 通道，记为 f16t4d24。我们应用了多种 latent 空间优化技术，以同时提升重建质量和 latent 的可学习性。

- 在送入 H3\-Omni\-Transformer 之前，视觉 latent 会沿 `(time, height, width)` 维度以 `1 × 2 × 2` 的 patch 大小进一步 patchify。因此，进入 Transformer 的视觉 token 的有效空间下采样倍率为 32×，时间下采样倍率保持 4×。

- H3\-VisualVAE 的 latent 空间针对重建质量和生成模型的学习的难易程度均做了优化。在训练完其编码器后，我们额外训练了一个基于 ViT 的解码器，以降低解码开销并进一步提升重建质量。

##### H3\-AudioVAE

- H3-AudioVAE 对左右声道使用相同的编码器和解码器，但独立处理每个声道，随后将解码后的声道重新合并，从而实现立体声音频的输入与输出。
- 对每个声道，H3-AudioVAE 将 32 kHz 音频压缩为时间率为 40 Hz 的 latent token 序列。
- 受 VA-VAE 启发，我们优化了 latent 空间，在保持音频重建质量的同时让生成模型更容易学习。

#### H3\-Omni\-Transformer

- 为了可扩展性与泛化性，我们采用了相对简洁的 Transformer block 设计。H3\-Omni\-Transformer 是一个 33B 参数的稠密单流 Transformer，其中约 13B 参数位于 AdaLN 相关分支。由于 AdaLN 调制的输出可以预计算并缓存，在仅推理部署中无需加载这些参数。我们发布了完整的模型权重，以支持包括微调在内的后续开发。

- 注意力层和 FFN 层均不包含模态专属结构。模态专属参数仅限于输入/输出层和 AdaLN 分支。其中，模态专属 AdaLN 以较低的额外训练与推理开销提升了生成质量。

- 模型使用三维多模态旋转位置编码（Multimodal Rotary Position Embeddings，MM\-RoPE）来表示时间维和两个空间维 `(t, h, w)` 上的位置关系。

- 在训练的最后阶段，我们引入了原生稀疏注意力以降低长序列的计算开销。稀疏注意力实现未包含在首发开源版本中，将在后续更新中单独发布。

    

### H3-Regenerate-2K

- 对于 H3 的 2K 分辨率输出，我们没有采用传统的专用超分辨率模块，而是让 H3 基础模型以 in-context（上下文内）的方式对其自身的低分辨率结果进行再生成。

- 这一方式有两大优势：(1) 再生成过程可以最大程度复用 H3 基础模型的生成能力；(2) in-context 形式在产出高分辨率输出时可以复用原始多模态上下文，从而恢复出传统超分方法只能「猜测」的信息，例如小字文本和细节。

- In-context 再生成也是任务泛化的一个例证。

- **由于系统复杂度较高，该模块尚未开源，待就绪后我们将发布。** 我们提供了用于验证官方结果的 API，见下文 "Full 2K Workflow"。



## 推荐工作流

为帮助社区正确部署 MiniMax H3，我们提供两种验证方法。

完整的 H3 系统由 H3\-Context\-IR、H3\-Base 和 H3\-Regenerate\-2K 三个模块组成。「Full 2K Workflow」提供了一个面向 2K 输出的端到端验证流水线，将开放平台 API 与本地部署的 H3\-Base 相结合。「Local Deployment of H3-Base」一节提供了仅使用本地部署的 H3\-Base 验证 768p 输出的方法。

此外，「Prompting Guidance」一节提供了详细教程，帮助社区开发自己的提示词系统。

### H3-Base 本地部署

MiniMax H3 以两个任务专用的 checkpoint 发布。每个 checkpoint 包含一个专用的 Omni Transformer 模型，以及所需的 processor、tokenizer、文本编码器、Visual VAE 和独立的 Audio VAE 组件。

|Checkpoint|支持的任务|输入条件|输出|精度|
|---|---|---|---|---|
|MiniMax\-H3 Base FL2VA|文生音视频 \(`t2va`\)、首/尾帧生音视频 \(`fl2va`\)|文本；可选首帧、尾帧或两者|视频和音频|BF16|
|MiniMax\-H3 Base Ref2VA|参考生音视频 \(`ref2va`\)|文本，附参考图像、视频和/或音频|视频和音频|BF16|

发布的 checkpoint 是经过 CFG 蒸馏的 Omni Transformer 模型权重。

每个 checkpoint 以自包含的 Hugging Face 风格仓库形式分发，包含以下组件：

```text
<TASK>/
├── model_index.json
├── processor/
├── tokenizer/
├── text_encoder/
├── transformer/
├── visual_vae/
└── audio_vae/
```

下载模型。仓库同时托管原始 checkpoint（`FL2VA/`、`Ref2VA/`）与 diffusers 格式，因此请按你的框架所需范围进行下载：

`model_index.json` 是仓库级公开入口。各任务族的 diffusers 索引仍分别位于 `FL2VA/model_index.json` 和 `Ref2VA/model_index.json`。

```bash
# Original checkpoint, both task families (SGLang, vLLM):
hf download MiniMaxAI/MiniMax-H3 --include "model_index.json" "FL2VA/*" "Ref2VA/*" --local-dir MiniMax-H3

# Or a single task family:
hf download MiniMaxAI/MiniMax-H3 --include "model_index.json" "FL2VA/*" --local-dir MiniMax-H3
```

diffusers 用户无需手动下载：`ModularPipeline.from_pretrained("MiniMaxAI/MiniMax-H3")` 会自动拉取所需组件。加载方法详见 [diffusers 文档](https://huggingface.co/docs/diffusers/main/en/api/pipelines/minimax_h3)。

我们推荐使用以下推理框架来服务该模型：

- [SGLang](https://docs.sglang.io/) \- 见 [cookbook](https://docs.sglang.io/cookbook/diffusion/MiniMax/MiniMax-H3) 

- [vLLM](https://github.com/vllm-project/vllm) \- 见 [vllm recipes](https://recipes.vllm.ai/MiniMaxAI/MiniMax-H3)

- [diffusers](https://github.com/huggingface/diffusers) \- 见 [diffusers docs](https://huggingface.co/docs/diffusers/main/en/api/pipelines/minimax_h3)

- [ComfyUI](https://github.com/Comfy-Org/ComfyUI) \- 见 [Comfy 教程](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)；使用 [R2V 模板](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_r2v.json) / [T2V 模板](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_t2v.json)

#### Sglang 部署

这里以 sglang 作为部署示例。更多部署配置见 [MiniMax\-H3 部署指南](https://docs.sglang.io/cookbook/diffusion/MiniMax/MiniMax-H3#3-serve-minimax-h3)。

FL2VA：

```bash
sglang serve \
  --model-path MiniMaxAI/MiniMax-H3 \
  --num-gpus 4 \
  --ulysses-degree 4 \
  --performance-mode speed \
  --host 0.0.0.0 \
  --port 30010 \
  --model-variant fl2va
```

Ref2VA：

```bash
sglang serve \
  --model-path MiniMaxAI/MiniMax-H3 \
  --num-gpus 4 \
  --ulysses-degree 4 \
  --performance-mode speed \
  --host 0.0.0.0 \
  --port 30011 \
  --model-variant ref2va
```

#### 可复现的 768p 案例

以下 T2VA、FL2VA、Ref2VA 三个用例演示了如何复现 MiniMax\-H3 的视频\-音频生成。

| 用例 | 请求 | 结果 |
|---|---|---|
| T2VA | [查看脚本](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/reproducible-768p-t2va-request.sh) | [t2va.mp4](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/t2va.mp4) |
| FL2VA | [查看脚本](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/reproducible-768p-fl2va-request.sh) | [fl2va.mp4](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/fl2va.mp4) |
| Ref2VA | [查看脚本](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/reproducible-768p-ref2va-request.sh) | [ref2va.mp4](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/ref2va.mp4) |

### 完整 2K 工作流（Full 2K\-Workflow）

本节说明如何将本地部署的 SGLang 服务与官方 **H3\-Context\-IR** 和 **H3\-Regenerate\-2K** API 相结合，以复现 MiniMax API 直接生成的 2K 视频质量。

开始之前，请先配置 SGLang 端点和你的 MiniMax API 凭据：

```bash
# URL of your SGLang deployment
SGLANG_DEPLOYMENT_URL="<sglang-deployment-url>"

# MiniMax API endpoint (choose one)
# CN
MINIMAX_API_BASE="https://api.minimaxi.com"
# Global
# MINIMAX_API_BASE="https://api.minimax.io"

# API token obtained from the MiniMax platform
TOKEN="<token>"
```

MiniMax 平台：

API 文档：
- Create H3-2K: use /video-generation-v2-create [EN-docs](https://platform.minimax.io/docs/api-reference/video-generation-v2-create), [CN-docs](https://platform.minimaxi.com/docs/api-reference/video-generation-v2-create)
- H3-Context-IR：use /video-generation-v2-h3-context-ir [EN-docs](https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir), [CN-docs](https://platform.minimaxi.com/docs/api-reference/video-generation-v2-h3-context-ir)
- H3-Regenerate-2K：use /video-generation-v2-regeneration [EN-docs](https://platform.minimax.io/docs/api-reference/video-generation-v2-regeneration), [CN-docs](https://platform.minimaxi.com/docs/api-reference/video-generation-v2-regeneration)


下述示例将本地 H3\-Base 输出文件编码为 Base64 Data URL。生产环境中，建议将视频上传到可公开访问的 URL，并将该 URL 作为 `base_video` 传入。

对以下每个案例，我们都提供了通过开放平台 API 直接生成的 2K 与 768p 参考输出，便于验证结果。

#### case\-T2VA

- 类型：文生视频
- 时长：10 秒
- 宽高比：16:9

<table>
  <thead>
    <tr><th>stage</th><th>request</th><th>result</th></tr>
  </thead>
  <tbody>
    <tr><td>H3-Context-IR</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-t2va-h3-context-ir.sh">View script</a></td><td><pre><code class="language-json">{
  &quot;task&quot;: {
    &quot;id&quot;: &quot;&lt;task_id&gt;&quot;,
    &quot;model&quot;: &quot;MiniMax-H3&quot;,
    &quot;status&quot;: &quot;succeeded&quot;,
    &quot;created_at&quot;: &quot;&lt;created_at&gt;&quot;,
    &quot;updated_at&quot;: &quot;&lt;updated_at&gt;&quot;,
    &quot;content&quot;: {
      &quot;prompt&quot;: &quot;integrated_multimodal_description: [Shot 1] Cinematic, medium wide shot, pushing in slowly. In the cavernous, dimly lit bridge of a starship, sleek metallic consoles with glowing amber displays flank a massive, curved observation window. A female captain, in her late 40s with an athletic build and short silver-streaked black hair, stands in the center midground. She wears a structured, high-collared dark navy military tunic with silver chest insignias. Her back is to the camera, silhouetted against the cool, ambient starlight pouring through the thick glass. She stands perfectly still with her hands clasped tightly behind her back. Outside the window, a massive armada of jagged, dark grey dreadnoughts hovers in tight formation against a deep purple space nebula. The fleet&#39;s massive rear thrusters begin to glow with an intense, escalating bright blue light. [Shot 2] At 00:04.500, the camera cuts to a close-up of the captain&#39;s face and shakes strongly. The brilliant blue-white light from the fleet&#39;s gathering energy reflects vividly in her dark eyes. Suddenly, a blinding white flash floods through the window, completely washing out the background as the fleet jumps to hyperspace. The sheer spatial force violently jolts the bridge, causing the captain from Shot 1 to stagger slightly forward, her shoulders tensing as she visibly braces herself against the physical tremors. As the intense white light fades abruptly, leaving only the dim, empty expanse of the purple nebula reflected on her starkly lit skin, her jaw clenches, and she slowly closes her eyes in the newly emptied space.\noverall_soundscape: A low, resonant hum of the ship&#39;s ambient life support systems serves as the baseline, soon drowned out by an audible, escalating, high-pitched electronic whine as the fleet outside charges its hyperdrives. A massive, deafening, bass-heavy boom and sharp crackle erupts during the blinding flash, accompanied by the loud metall... [truncated]
    },
    &quot;duration&quot;: 10,
    &quot;usage&quot;: {
      &quot;total_tokens&quot;: 8565,
      &quot;prompt_tokens&quot;: 5650,
      &quot;completion_tokens&quot;: 2915
    },
    &quot;ratio&quot;: &quot;16:9&quot;,
    &quot;task_type&quot;: &quot;h3_context_ir&quot;,
    &quot;modality&quot;: &quot;text&quot;
  }
}</code></pre></td></tr>
    <tr><td>H3-Base</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-t2va-h3-base.sh">View script</a></td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/t2va.mp4">t2va.mp4</a></td></tr>
    <tr><td>H3-Regenerate-2K</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-t2va-h3-regenerate-2k.sh">View script</a></td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/t2va_2k.mp4">t2va_2k.mp4</a></td></tr>
    <tr><td>Reference 2K result by directly calling Open Platform API</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-t2va-reference-2k-result-by-directly-calling-open-platform-api.sh">View script</a></td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/h3_direct_2k.mp4">h3_direct_2k.mp4</a></td></tr>
    <tr><td>Reference 768P result by directly calling Open Platform API</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-t2va-reference-768p-result-by-directly-calling-open-platform-api.sh">View script</a></td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/h3_direct_768p.mp4">h3_direct_768p.mp4</a><br></td></tr>
  </tbody>
</table>

#### case\-I2VA

- 类型：首帧图生视频
- 时长：8 秒
- 宽高比：自适应

<table>
  <thead>
    <tr><th>stage</th><th>request</th><th>result</th></tr>
  </thead>
  <tbody>
    <tr><td>H3-Context-IR</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-i2va-h3-context-ir.sh">View script</a></td><td><pre><code class="language-json">{
  &quot;task&quot;: {
    &quot;id&quot;: &quot;&lt;task_id&gt;&quot;,
    &quot;model&quot;: &quot;MiniMax-H3&quot;,
    &quot;status&quot;: &quot;succeeded&quot;,
    &quot;created_at&quot;: &quot;&lt;created_at&gt;&quot;,
    &quot;updated_at&quot;: &quot;&lt;updated_at&gt;&quot;,
    &quot;content&quot;: {
      &quot;prompt&quot;: &quot;For the target video, at 0.00 seconds into the target video, &lt;Picture 1&gt; (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] This is a live-action, cinematic shot with a shallow depth of field. The camera holds a perfectly static shot throughout the entire eight-second duration, capturing a cozy family gathering in a traditional Japanese dining room. The scene opens with a large, intricately patterned blue and white ceramic bowl of ramen in the immediate foreground, rendered in crisp, sharp focus. The bowl sits on a smooth, polished long wooden table. Inside the bowl, a rich, oily golden-brown broth surrounds yellow wavy noodles, topped with two thick, round slices of chashu pork featuring visible fat marbling and a distinct spiral meat pattern. A generous mound of freshly chopped, bright green scallions rests in the center, and a crisp, dark green rectangular sheet of nori seaweed is tucked into the right edge. To the left of the bowl, a pair of light brown wooden chopsticks rests horizontally on a small, dark rectangular chopstick rest, near a small cylindrical ceramic teacup with blue painted patterns. On the right side of the table, a spherical paper lantern with a ribbed bamboo frame sits on a black wooden base. In the background, a large family of seven is gathered around the table, initially appearing as a soft, blurred presence. Behind them, traditional Japanese sliding shoji screens with wooden lattice frames are open, revealing a bright outdoor scene with lush green trees. Early in the clip, the thick, white steam rising from the hot ramen broth immediately intensifies, billowing upwards in thick, swirling clouds that dance continuously above the bowl. As the clip progresses into the middle seconds, the camera maintains its static position while the focus begins a deliberate, smooth shift deeper into the room. The foreground ramen bowl, its vibrant ingredients, and the rising steam gradu... [truncated]
    },
    &quot;duration&quot;: 8,
    &quot;usage&quot;: {
      &quot;total_tokens&quot;: 22822,
      &quot;prompt_tokens&quot;: 12800,
      &quot;completion_tokens&quot;: 10022
    },
    &quot;ratio&quot;: &quot;16:9&quot;,
    &quot;task_type&quot;: &quot;h3_context_ir&quot;,
    &quot;modality&quot;: &quot;text&quot;
  }
}</code></pre></td></tr>
    <tr><td>H3-Base</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-i2va-h3-base.sh">View script</a></td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/i2va.mp4">i2va.mp4</a></td></tr>
    <tr><td>H3-Regenerate-2K</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-i2va-h3-regenerate-2k.sh">View script</a></td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/i2va_2k.mp4">i2va_2k.mp4</a><br></td></tr>
    <tr><td>Reference 2K result by directly calling Open Platform API</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-i2va-reference-2k-result-by-directly-calling-open-platform-api.sh">View script</a></td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/i2va_direct_2k.mp4">i2va_direct_2k.mp4</a></td></tr>
    <tr><td>Reference 768P result by directly calling Open Platform API</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-i2va-reference-768p-result-by-directly-calling-open-platform-api.sh">View script</a></td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/i2va_direct_768p.mp4">i2va_direct_768p.mp4</a></td></tr>
  </tbody>
</table>

#### case\-Ref2VA

- 类型：多模态参考生视频（视频 + 音频）
- 时长：5 秒
- 宽高比：自适应

<table>
  <thead>
    <tr><th>stage</th><th>request</th><th>result</th></tr>
  </thead>
  <tbody>
    <tr><td>H3-Context-IR</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-ref2va-h3-context-ir.sh">View script</a></td><td><pre><code class="language-json">{
  &quot;task&quot;: {
    &quot;id&quot;: &quot;&lt;task_id&gt;&quot;,
    &quot;model&quot;: &quot;MiniMax-H3&quot;,
    &quot;status&quot;: &quot;succeeded&quot;,
    &quot;created_at&quot;: &quot;&lt;created_at&gt;&quot;,
    &quot;updated_at&quot;: &quot;&lt;updated_at&gt;&quot;,
    &quot;content&quot;: {
      &quot;prompt&quot;: &quot;subject_definitions:\n&lt;Subject 1&gt; is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt, and silver rings, holding a small black lamb in his arms in &lt;Video 1&gt;.\n&lt;Video 1&gt; is the source video for the editing task.\n&lt;Audio 1&gt; is the synchronized audio track of &lt;Video 1&gt;, providing the background music.\n&lt;Audio 2&gt; is the voice timbre reference for &lt;Subject 1&gt;&#39;s voice, containing a spoken male voiceover.\n\nsummary:\n[video editing + audio reference + audio reuse] The target video is an edited version of &lt;Video 1&gt;. &lt;Subject 1&gt;, wearing a bright pink suit and holding a black lamb, stands in a grassy field with other white lambs in the background. The edit animates &lt;Subject 1&gt;&#39;s face to speak the user-provided dialogue. &lt;Audio 1&gt; is partially reused as the continuous background music, while the target references the calm male voice timbre of &lt;Audio 2&gt; for &lt;Subject 1&gt;&#39;s spoken lines.\n\nretention_analysis:\n&lt;Subject 1&gt; (appears in [Shot 1]): fully_preserved - the man retains his identity, wavy blonde hair, pink suit, white shirt, accessories, and the black lamb he holds, with his mouth newly animated to speak.\n&lt;Video 1&gt; (source video editing): fully_preserved - the original camera framing, warm golden hour lighting, grassy hill setting, and background white lambs are maintained while the central character is edited.\n&lt;Audio 1&gt;: partially_copy - the atmospheric background music from &lt;Audio 1&gt; is reused in the target video, mixed beneath the newly added spoken dialogue.\n&lt;Audio 2&gt;: reference - the target audio references the male voice timbre from &lt;Audio 2&gt; to generate &lt;Subject 1&gt;&#39;s spoken dialogue.\n\ndetailed_description:\nThe target video is in realistic photographic style.\n[Shot 1] The shot begins from the source &lt;Video 1&gt;... [truncated]
    },
    &quot;duration&quot;: 5,
    &quot;usage&quot;: {
      &quot;total_tokens&quot;: 39299,
      &quot;prompt_tokens&quot;: 33323,
      &quot;completion_tokens&quot;: 5976
    },
    &quot;ratio&quot;: &quot;16:9&quot;,
    &quot;task_type&quot;: &quot;h3_context_ir&quot;,
    &quot;modality&quot;: &quot;text&quot;
  }
}</code></pre></td></tr>
    <tr><td>H3-Base</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-ref2va-h3-base.sh">View script</a></td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/r2va.mp4">r2va.mp4</a><br></td></tr>
    <tr><td>Reference 2K result by directly calling Open Platform API</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-ref2va-reference-2k-result-by-directly-calling-open-platform-api.sh">View script</a></td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/r2va_2k.mp4">r2va_2k.mp4</a></td></tr>
    <tr><td>H3 API 2K in Open Platform for reference</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-ref2va-h3-api-2k-in-open-platform-for-reference.sh">View script</a></td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/r2va_direct_2k.mp4">r2va_direct_2k.mp4</a><br></td></tr>
    <tr><td>Reference 768P result by directly calling Open Platform API</td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/scripts/readme/full-2k-ref2va-reference-768p-result-by-directly-calling-open-platform-api.sh">View script</a></td><td><a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/assets/r2va_direct_768p.mp4">r2va_direct_768p.mp4</a><br></td></tr>
  </tbody>
</table>

### 提示词指南（Prompting Guidance）

[VIDEO\_PROMPT\_WRITING\_GUIDE\_base\_en\.md](docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md)

[VIDEO\_PROMPT\_WRITING\_GUIDE\_ref\_en\.md](docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md)

skills to improve prompt: https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills

## License

- MiniMax H3 依据 [MiniMax H3 Community License Agreement](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE) 发布。
- [License 问答](docs/QA-about-License.md)
- [申请表（仅限美国/欧盟/英国/韩国）](https://platform.minimax.io/h3-license)

## 联系我们

联系我们：[model@minimax.io](mailto:model@minimax.io)。
