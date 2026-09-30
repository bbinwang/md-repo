> 原文：https://docs.comfy.org/tutorials/video/minimax/minimax-h3 （ComfyUI MiniMax H3 视频生成指南，中文翻译）

# ComfyUI MiniMax H3 视频生成指南

如何在 ComfyUI 中使用开放权重的 MiniMax H3：文生视频、图生视频与参考生视频工作流，支持原生立体声音频、提示词撰写技巧以及 Sage Attention 加速。

[MiniMax H3](https://www.minimax.io/blog/minimax-h3) 是 MiniMax 的通用全模态生成模型，现已开放权重。它在单一上下文中联合理解文本、图像、视频与音频，并生成带**原生立体声音频**的视频：语音、音效与音乐在同一次前向推理中一起建模，而非事后叠加。输出最高 2K 分辨率、24fps、约 15 秒。
ComfyUI 原生支持 MiniMax H3。文档分为五个页面：

- **总览**（本页）：模型能力、工作流索引、输出分辨率与加速方案

- **[原生工作流](/tutorials/video/minimax/minimax-h3-native)**：文生视频、图生视频、参考生视频，以及原生节点进阶技巧

- **[多帧参考（Multiframe Reference）](/tutorials/video/minimax/minimax-h3-multiframe)**：在输出时间线的特定位置锚定参考帧

- **[Fun ControlNet Union](/tutorials/video/minimax/minimax-h3-fun-controlnet)**：用控制视频驱动 H3，或使用遮罩进行视频局部重绘

- **[提示词指南](/tutorials/video/minimax/minimax-h3-prompt-guide)**：MiniMax 官方提示词撰写指南、通用技巧与提示词嵌入

H3 的开放权重让你可以在本地运行该模型。本地生成输出的商业使用需要 [MiniMax 商业许可](https://comfy.org/minimax/license)，可通过 Comfy（唯一官方经销渠道）获取。在 Comfy Cloud 上生成的内容已包含商业权利。

## 主要特性

- **原生立体声音频**：对白、音效与音乐随视频一起生成，同步打包在一个 MP4 中

- **多模态上下文**：文本、图像、视频与音频参考可在一次生成中组合使用

- **参考驱动生成**：从参考素材中锁定角色身份、风格、动作、镜头运动或声音

- **指令遵循**：用自然语言描述参考与目标镜头之间的关系

- **精准文字渲染**：拼写出的文字与品牌元素渲染清晰

- **开放权重**：在 ComfyUI 中本地运行，完全掌控每个参数

## 快速上手

ComfyUI 已支持开放权重的 MiniMax H3。开始步骤：

- 将 ComfyUI 更新到 0.30.0 或更高版本

- 进入 **Template Library** > **Video** > 选择任一 MiniMax H3 工作流

- 按弹窗提示下载模型并运行工作流

模型文件托管在 Hugging Face 的 [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3) 仓库中。

## 工作流索引

模板库目前内置五个示例工作流。它们只是示例模板，并非完整清单：通过原生 MiniMax H3 节点，模型还支持更多生成模式，你可以用这些节点搭建更多工作流。

## 文生视频（T2V）

从文本提示词生成带原生立体声音频的视频

## 图生视频（I2V）

从输入图像生成视频，可选首帧/尾帧控制

## 参考生视频（R2V）

从参考图像、视频与音频中锁定角色、风格、动作、镜头运动或声音

## 多帧参考（Multiframe Reference）

通过链式连接的 Add Guide 节点，在输出时间线的特定位置锚定参考帧

## Fun ControlNet Union

用 Canny、Depth、HED、MLSD 或 Pose 控制视频驱动 H3，或使用遮罩进行视频局部重绘

底层节点模式：通过 `MiniMaxH3ImageToVideo` 节点实现首/尾帧图生视频（fl2va），通过 `MiniMaxH3ReferenceToVideo` 节点实现基于图像、视频与音频的参考驱动生成（ref2va）。
提示词撰写资源（MiniMax 官方指南、通用技巧与提示词嵌入）请见[提示词指南](/tutorials/video/minimax/minimax-h3-prompt-guide)。

## 设置输出分辨率

每个工作流都使用 **Resolution Selector** 节点控制整体输出尺寸。该节点根据三个设置计算 `width` 与 `height`，其输出直接连接到 MiniMax H3 节点的 `width` 与 `height` 输入：

- **Aspect ratio（宽高比）**：选择预设，如 `16:9 (Widescreen)`、`9:16 (Portrait Widescreen)` 或 `1:1 (Square)`

- **Megapixels（百万像素）**：输出的目标总像素数。值越大画面越大；值越小运行越快

- **Multiple（倍数）**：计算出的分辨率会舍入到该数字的最接近倍数。保持为 `32` 以匹配 H3 的分辨率网格

模板自带一个快速预览尺寸。若要在 16:9 下输出全画质，可将 Resolution Selector 的 Megapixels 设为 `0.98` 以获得 H3 的原生画幅（短边 768px，16:9 下为 1344x768），或直接在 MiniMax H3 节点的 `width` 与 `height` 输入中填写 `1344 x 768`（其默认值）。跳过 `1.0` 百万像素这一档：它会得到 1376x768，超出模型 768x1344 的像素面积上限。

## 使用 Sage Attention 加速生成

示例工作流使用标准 attention 实现。通过 [Sage Attention](https://github.com/woct0rdho/SageAttention) 大致可以将生成速度翻倍，且质量损失极小。Sage Attention 是可选依赖，需要自行安装：

- 安装 `sageattention` Python 包。从 [SageAttention releases](https://github.com/woct0rdho/SageAttention/releases) 页面下载与你的 PyTorch 和 CUDA 版本匹配的 wheel，然后用 `pip install <wheel-file>` 安装。

- 安装 [KJNodes 自定义节点](https://github.com/kijai/ComfyUI-KJNodes)，它提供 `Patch Sage Attention KJ` 节点。可使用 ComfyUI Manager，或将仓库克隆到 `ComfyUI/custom_nodes/` 后重启 ComfyUI。

- 在工作流中添加 `Patch Sage Attention KJ` 节点，并将其连接在 `UNETLoader` 与 `BasicGuider` 节点之间：其 `model` 输入接收来自 `UNETLoader` 的模型，其 `model` 输出接入 `BasicGuider` 的 `model` 输入。将 `sage_attention` 设为 `auto`。

- 照常运行工作流。只有 guider 需要该补丁；scheduler 只生成 sigmas，保持原样即可。

注意事项：

- Sage Attention 要求 float16 或 bfloat16 张量。MiniMax H3 部分层以其他 dtype 运行，因此你可能在控制台看到 "Input tensors must be in dtype of torch.float16 or torch.bfloat16, using pytorch attention instead" 消息。这是预期现象；受影响的层会回退到标准 attention，生成仍可正常完成。

- 另一种方式是不添加节点，而是通过 `--use-sage-attention` 启动参数在全局启用 Sage Attention。
