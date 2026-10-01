# Parlor vs PersonalJarvis:家用语音助手选型对比

> 调研日期:2026-10-01
> 背景:寻找一个可二次开发的底座,改造成家用对话助手(类似豆包能力):实时对话、可打断、自定义声色、QA 总结问答(给孩子用),并支持本地 agent 写代码(自用)。
> 本机环境:Apple M4 Pro / 48 GB RAM / arm64 / macOS 26.3

## TL;DR

- **选定 PersonalJarvis 作为底座**:需求清单 6 项中 4 项(声色、总结、持久记忆、agent 写码)命中其已有架构;三层模型设计天然匹配"孩子聊天 + 自用编码"双场景;产品化程度高(安装器/权限/密钥管理)。
- **Parlor 作为实时对话体验的参考实现**:借鉴其 smart-turn、说话中预填 prompt cache、逐句流式 TTS 等技巧。
- 意外收获:本机已有 CosyVoice 项目,可接入 PersonalJarvis 的 TTS provider 架构,实现中文/儿童声色。

---

## 一、项目概览

### Parlor(fikrikarim/parlor)

完全端侧(on-device)、实时、多模态(语音 + 视觉)的 AI 对话助手,对标 OpenAI GPT-Live。

- **诞生背景**:作者此前自托管免费语音 AI(Bule AI)帮数百名月活用户练习英语口语;GPT-Live 发布后决定升级,硬约束是 100% 本地运行。
- **架构**:浏览器(麦克风 + 摄像头)→ WebSocket(音频 PCM + JPEG 帧)→ FastAPI 服务端
  - smart-turn-v3(~20ms)判断"是否说完"
  - Gemma 4 E4B(llama.cpp QAT q4_0)边听边看,流式回复
  - Kokoro TTS 逐句合成
  - 可选后台 reasoner(OpenAI 兼容端点 + 联网搜索)
- **特色模式**:
  - Live translation mode:同声传译,"Translate everything I say into English" 直到 "stop translating"
  - Just-listen mode:静默速记,只转写不回复
  - Barge-in:说话可打断 AI,服务端 abort 生成
- **性能**(M3 Pro,e2b 模型):短问带摄像头 ~0.8s 首响;长问 ~1.5s

### PersonalJarvis(PersonalJarvis/PersonalJarvis)

语音驱动的个人 AI 生态系统 / meta-orchestrator。定位:"普通语音助手只会说,Personal Jarvis 直接把事干了"。

- **三层模型,自动交接**:
  1. **Realtime 模型** — 承载对话,<1s 应答
  2. **Brain/工具模型** — 需要工具时句子中途交接(读 wiki、改配置、打电话、操作屏幕)
  3. **编码 agent 工人** — 耗时任务在隔离 worktree 跑,产出前过 critic 审查(Claude Code / Codex CLI / Gemini CLI)
- **核心能力**:computer use(接管鼠标键盘)、MCP 连接、Knowledge Wiki 持久记忆、Artifacts 报告、Twilio 真实外呼、任意应用听写
- **全链路可本地**:自托管 Realtime 服务器(~12GB 显存,实验性)、Ollama brain、Whisper large-v3 / Nemotron 3.5 STT、Piper / Kokoro / Qwen3-TTS TTS;仅 Twilio 和编码 agent 例外
- **发布形态**:pip 包 `personal-jarvis`、一键安装器(Win/macOS/Linux)、homebrew tap、scoop bucket、桌面 App

---

## 二、规模与热度对比

| | **Parlor** | **PersonalJarvis** |
|---|---|---|
| ⭐ Stars | **2,070** / 271 forks | 78 / 34 forks |
| 创建时间 | 2026-04 | 2026-05-31 |
| 最近提交(快照) | 2026-08-03 | **2026-08-28**(更活跃) |
| 一方代码量 | **~6,500 行**(4.7K Python + 1.7K JS) | **~70 万行**(53 万 Python + 18 万 TS/JS) |
| 测试 | 14 个测试文件 + 10 个 benchmark 脚本 | **1,959 个测试文件 / ~46 万行** |
| 产品化 | 研究预览版,自认 "rough edges" | pip 包、安装器、打包渠道、权限管理、产品文档、网站、Discord |
| 代码风格 | 精品小作坊,一人可通读 | 重工程(AI 辅助生成为主,单文件最大 1.7 万行) |

**反直觉事实**:parlor star 高 26 倍,但代码只有 PersonalJarvis 的 1%。

## 三、采集能力对比(代码级验证)

| | Parlor | PersonalJarvis |
|---|---|---|
| 麦克风 | ✅ 浏览器 getUserMedia audio + AudioWorklet PCM | ✅ 双路:桌面 `mic_listener.py`(PortAudio 16kHz)+ Web `realtimeAudio.ts` |
| 摄像头实时采集 | ✅ 640×480 前置,canvas 缩 320px / JPEG 0.7,WebSocket 推流,Gemma 4 实时"看" | ❌ 仅 entitlement 预留,无实际采集代码(getUserMedia 只请求 audio) |
| 屏幕采集 | ❌ | ✅ Screen Recording → Computer Use / 屏幕视觉 |

### Parlor 摄像头的作用

1. **视觉问答**:每轮话语附一帧画面,系统提示 "Mention what you see on their camera if relevant";可举物问名、指文本问读法
2. **英语学习场景延伸**:看图说话 / 情景对话
3. **低延迟拼图**:一开口就发帧,趁说话预填 llama.cpp prompt cache(带画面问题首 token 快 ~75%)
4. **逐模式开关**(`wants_camera`):conversation ✅ / translate ❌(译员不掺画面) / listen ❌(只转写)
5. **架构是测量出来的**:`camerabench.py` 对比"每轮附帧 vs 按需工具调用",实测结论 keep 每轮附帧
6. **隐私**:帧仅本地处理,浏览器可随时关,拒绝授权自动退化纯语音

## 四、需求映射(家用对话助手场景)

| 需求 | Parlor | PersonalJarvis |
|---|---|---|
| 实时对话 | ✅ ~0.8s 首响,级联管线调优极佳 | ✅ Realtime 协议(云端)或自托管(48GB 可跑,实验性) |
| 打断 barge-in | ✅ 服务端 abort,实测打磨 | ✅ interrupt intent 分类 + VAD 边界处理 |
| **自定义声色** | ⚠️ 仅 Kokoro,声色有限,per-mode 固定 | ✅ **多 TTS provider**(Piper/Kokoro/Qwen3-TTS/Cartesia),对话中动态切换 |
| QA 总结问答 | ⚠️ 仅可选 background reasoner | ✅ Knowledge Wiki + Artifacts + mission 审查 |
| 给孩子用 | 需自制儿童模式/内容过滤 | 需自制,但 provider 架构换儿童声色更容易 |
| **本地 agent 写代码** | ❌ | ✅ **核心能力**:驱动编码 CLI,隔离 worktree + critic |

## 五、选型结论与路线

### 以 PersonalJarvis 为底座

1. **架构命中率高**:声色、总结、记忆、agent 写码均为已有能力;往 parlor 加 agent 编排 = 从零建架构,往 PJ 调对话体验 = 调参换 provider
2. **双场景天然分层**:孩子用 realtime 层(轻快、儿童声色),自用 tool 层 + coding agent 层,一套系统两种人格
3. **产品完成度**:安装器、权限管理、密钥管理、家长可控开关——家庭场景刚需
4. **中文声色路线**:本机 CosyVoice 可接入 PJ 的 TTS provider 插件架构(Kokoro 中文声色弱)
5. **硬件富余**:M4 Pro 48GB 可跑全本地链路(~12GB realtime + Ollama brain + Whisper/Nemotron)

### Parlor 作为参考实现

借鉴其打磨过的实时对话技巧:smart-turn 完整性判断、说话中预填 prompt cache、逐句流式 TTS、服务端 barge-in abort。

### 风险提示

- PJ 代码量 ~70 万行(AI 生成为主),深度定制前需先摸清 `conductor` / `jarvis/realtime` / `jarvis/speech` 三模块脉络
- PJ 自托管 realtime 标注 experimental,barge-in 实际体验需上机验证
- 儿童内容过滤/家长控制两个项目都没有,需自建

---

## 附:本地项目路径

- Parlor:`~/projects/parlor`(含中文架构文档 `docs/wangbin/`)
- PersonalJarvis:`~/projects/PersonalJarvis`
- CosyVoice:`~/projects/CosyVoice`、`~/projects/cuda_cosyvoice`(可作中文 TTS provider)
