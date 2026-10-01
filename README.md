# md-repo

文章转 Markdown 归档仓库：把有价值的博客/文章/官方文档翻译为中文 Markdown 并存档。

## 目录

### h3/ — MiniMax H3（开源全模态视频生成模型）

- [MiniMax H3 模型卡](./h3/minimax-h3-modelcard.md) — [原文](https://huggingface.co/MiniMaxAI/MiniMax-H3)：系统概览、模型架构（H3-Context-IR / H3-Base / H3-Regenerate-2K）、本地部署与 2K 工作流
- [视频提示词写作指南·基础任务](./h3/video-prompt-writing-guide-base.md) — [原文](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md)：T2VA / I2VA / FL2VA / L2VA 提示词结构、镜头运动、对话与声音写法
- [视频提示词写作指南·全参考模式](./h3/video-prompt-writing-guide-ref.md) — [原文](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md)：六段式改写输出格式、参考标签与保留性分析
- [ComfyUI MiniMax H3 视频生成指南](./h3/comfyui-minimax-h3-tutorial.md) — [原文](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)：工作流索引、分辨率设置、Sage Attention 加速
- [MiniMax H3 Day-0 Support in ComfyUI](./h3/minimax-h3-day-0-support-in-comfyui.md) — [原文](https://blog.comfy.org/p/minimax-h3-day-0-support-in-comfyui)：ComfyUI 官方博客，本地推理优化（显存降 66%，RTX 3060 可跑）
- [ComfyUI-Agent-Kit](./h3/comfyui-agent-kit.md) — [原文](https://github.com/SlavaSexton/ComfyUI-Agent-Kit)：让 Claude Code/Codex/Gemini CLI/Qwen Code 驱动本地 ComfyUI 的多智能体工具包（README 翻译）
- [ComfyUI-Agent-Kit 内置 minimax-h3 技能](./h3/comfyui-agent-kit-minimax-h3-skill.md) — [原文](https://github.com/SlavaSexton/ComfyUI-Agent-Kit/blob/main/shared/minimax-h3/SKILL.md)：H3 三字段提示词格式、`<d>` 对话标记、量化与加速阶梯、排障表
- [Minimax-H3-Prompt-AgentSkill](./h3/h3-prompt-agentskill.md) — [原文](https://github.com/benjiyaya/Minimax-H3-Prompt-AgentSkill)：Hermes Agent 技能，粗创意+素材 → H3 生产级提示词（README 翻译）；配套译文：[SKILL.md](./h3/h3-prompt-agentskill-SKILL.md) · [基础多镜头格式](./h3/h3-prompt-agentskill-base-multishot-format.md) · [Ref2VA 六段式格式](./h3/h3-prompt-agentskill-ref2va-format.md) · [创意示范集](./h3/h3-prompt-agentskill-creative-showcase.md)

### comfyui/ — ComfyUI 相关

- [视频提示词写作指南·全参考模式（ComfyUI_Fill-Nodes 副本）](./comfyui/video-prompt-writing-guide-ref.md) — [原文](https://github.com/filliptm/ComfyUI_Fill-Nodes/blob/a32f9b6a5a55528731d9e6c38a2fd2ce89cb2819/nodes/audio/prompt_guides/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md)：与 MiniMax 官方指南内容一致（MD5 校验相同），六段式改写输出格式

## 说明

- 每篇文章一个 `.md` 文件，按主题建子目录，文件名与原文 slug 一致
- 正文为中文翻译，示例提示词/代码块/标记词保留英文原文
- 文件头部附原文链接
