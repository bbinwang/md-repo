# qwen3.8-bench — x99 vLLM decode 吞吐口径基准

目标环境：192.168.2.108（双 RTX 2080Ti TP2，vLLM-2080Ti-Definitive v0.2.2-post3）
模型：`Qwen3.8-27B-NVFP4` + DFlash2 投机解码（`num_speculative_tokens=7`，greedy draft）

## 背景：为什么同一个模型有 180 和 80 两种 decode tok/s

排查结论（2026-10-06/07 实测）：

- **计时公式不是差异来源**。把两个脚本的公式套在同一条流上，结果差 <1%。
- **引擎步频恒定** ≈ 44–47 ms/步，所有 lane 一致。
- **差异 100% 来自投机解码每步接受的 token 数**：

```
decode tok/s ≈ tok/步 ÷ 步频
            ≈ (接受率 × (k+1)) ÷ 43.5ms        # k=7 → 上限 8 tok/步 ≈ 184 tok/s
```

chat 模板默认思考模式（resolved `xhigh`），模型把生成预算花在思考文本上，
draft 猜不中 → 接受率 ~30-40% → ~70-90 tok/s。关思考或锁死输出 token →
接受率 100% → ~181 tok/s（引擎上限口径，与 launcher 启动自测 181.78 重合）。

## 文件说明

| 文件 | 说明 |
|---|---|
| `README.md` | 本文档 |
| `lane_compare.py` | 6-lane 口径基准脚本，输出 `report.html` + `results.json` |
| `x99_latency.py` | x99 日常基准脚本（146 上的原版 + 新增 `--no-think` 参数） |
| `report.html` | 最近一轮 6-lane 报告（总览表 + 结论 + 各 lane 明细） |
| `results.json` | 最近一轮原始数据（含每步接受直方图 `per_step_accepted`） |

## 基准口径对照

### x99_latency.py（日常口径）

```
TTFT          = 首个非空 delta (role/content/reasoning) 到达时刻
prefill tok/s = prompt_tokens / TTFT
decode  tok/s = (completion_tokens - 1) / (wall - TTFT)
```

- `/v1/chat/completions` 流式，固定 SYS_BENCH + CJK/EN/code 合成 4K prompt
- 每 run 唯一 salt 前缀，`cached_tokens == 0` 才算冷测（PASS 判定项）
- token 数取服务端 `usage`，不本地重切

### launcher 启动自测口径（仓库 `launcher.sh` → `tools/profile_request.py`）

```
prefill tok/s = prompt_tokens / TTFT
decode  tok/s = (completion_tokens − 首批tokens) / (首token→末token 墙钟)
```

- `/v1/completions` + `allowed_token_ids` 锁死单一 token + `temperature=0` + `ignore_eos`
- 接受率强制 100%（稳态），测前有 warmup → 结果即引擎步频上限
- 结果存 `run-logs/start-manager.state` 的 `LAST_PERF_*`

两者分母窗口几乎等价（x99 的 wall 多含流尾 [DONE]，影响 <1%），可直接对比的前提是
**思考模式一致**。

## lane_compare.py 代码说明

每个 lane = 一种"接口 × 思考参数"组合，统一 4K/128、temperature=0、唯一 salt 冷 cache：

| lane key | 接口 | 思考参数 | 对应口径 |
|---|---|---|---|
| `chat-default` | chat | 模板默认（=xhigh） | x99 脚本原行为 |
| `chat-nothink` | chat | `enable_thinking=false` | x99 `--no-think` |
| `chat-effort-low` | chat | `reasoning_effort=low` | 三档思考强度之一 |
| `chat-effort-medium` | chat | `reasoning_effort=medium` | 三档思考强度之二 |
| `chat-effort-xhigh` | chat | `reasoning_effort=xhigh` | 三档思考强度之三（=默认） |
| `completions-forced` | completions | `allowed_token_ids` 锁单 token | launcher 自测口径 |

关键实现（单文件、纯标准库）：

- `build_prompt()`：与 x99_latency.py 同款合成文本（`TOKENS_PER_CHAR=0.3387` 校准密度），
  每 run 注入唯一 salt 保证 prefix cache miss。
- `run_lane()`：逐 chunk 解析 SSE 流，记录 TTFT / 首→末 token 窗口 / 每 chunk token 数；
  捕获服务端 per-request 指标（需服务端 `--per-request-spec-decode-metrics detailed`），
  结构为 `chunk.metrics.speculative_decoding.{draft_acceptance_rate, mean_acceptance_length,
  num_spec_steps, per_step_accepted, ...}`。
- 同一条流上同时计算两种口径公式（`decode_x99` / `decode_launcher`），用于证明等价。
- `render_report()`：生成 HTML——总览对比表、动态结论要点、每 lane 明细
  （参数 JSON、完整输入/输出文本，reasoning 与 content 分开、计时与指标）。
- 产物：`report.html`（人读）+ `results.json`（机器可读，含 `per_step_accepted` 直方图）。

### 用法

```bash
python3 lane_compare.py                          # 默认打 http://192.168.2.108:8000/v1
X99_BASE=http://<host>:8000/v1 python3 lane_compare.py
python3 lane_compare.py --base http://127.0.0.1:8000/v1 --sleep 3

python3 x99_latency.py --no-think                # 引擎上限口径（可与 launcher LAST_PERF_* 对标）
python3 x99_latency.py                           # 原口径（思考模式）
```

`x99_latency.py --no-think`：payload 加 `chat_template_kwargs={"enable_thinking": false}`，
透传到全部 run（4K/128 ×3 + 32K/512 ×1）。默认不带参数 = 原行为。

## 实测数据（2026-10-07，4K/128，本机对 108）

| lane | 接受率 | tok/步 | 步频 ms | decode x99口径 | decode launcher口径 | 输出特征 |
|---|---|---|---|---|---|---|
| chat-default | 42.4% | 3.88 | 45.0 | **88.1** | 88.1 | 全是思考文本 |
| chat-nothink | 100% | 8.00 | 46.7 | **181.4** | 181.4 | bench 复读 |
| chat-effort-low | 61.3% | 5.33 | 45.6 | **121.0** | 121.1 | 思考（简短） |
| chat-effort-medium | 60.0% | 5.12 | 45.5 | **116.4** | 116.4 | 思考 |
| chat-effort-xhigh | 32.9% | 3.20 | 44.8 | **72.7** | 72.8 | 思考（较长） |
| completions-forced | 84.2%* | 6.74 | 46.1 | **153.1** | 153.2 | 强制单 token |

\* 冷启动前 3 步 0 接受（rejection sampler JIT warmup），稳态 7/7=100%；
launcher 官方自测因先跑 warmup 记 181.78（4K/128）/ 172.76（32K/512），
与本环境 `--no-think` 实测 181.48 / 172.47 差 0.2%。

对照 `x99_latency.py` 默认口径历史值：4K/128 decode ≈ 70-90（思考模式波动，
取决于当轮接受率），32K/512 ≈ 74。

## 结论与使用建议

1. **对比口径前先对齐思考模式**：`--no-think` 出来的是引擎上限（~181），
   思考模式出来的是"带 reasoning 的真实体感"（~70-120，随 effort 档位变化）。
2. launcher 自测数字（`LAST_PERF_DECODE_MEAN`）是**上限口径**，不代表真实生成速度。
3. 日常回归建议固定 `--no-think`（波动小、可对标 launcher）；
   评估真实体验用默认思考口径。
4. 思考强度档位对速度影响显著：xhigh ≈ 73 < medium ≈ 116 < low ≈ 121 << 关思考 181 tok/s。
