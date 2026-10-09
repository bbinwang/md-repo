# Strata IQ2_XS 时延基准报告

**测试时间**: 2026-10-09 19:09 CST · **服务器**: http://127.0.0.1:8080/v1 · **模型**: qwen3.8-flash-next-iq2_xs

---

## 1. 硬件与模型信息

| 项目 | 规格 |
|------|------|
| CPU | Intel E5-2680 v4 @ 2.40GHz (14C/28T) |
| GPU | 2× NVIDIA GeForce RTX 2080 Ti (22.5GB VRAM each) |
| 内存 | 48GB DDR4 ECC |
| 系统 | Ubuntu 24.04, kernel 7.0.0-34-generic |
| 模型 | Qwen3.8-Flash-Next (IQ2_XS 量化) |
| 引擎 | Strata 0.1.x (split-layer, auto GPU split) |

---

## 2. 基础时延测试 (4K/128 × 3 + 32K/512 × 1)

**口径**: prefill = prompt_tokens / TTFT · decode = (completion_tokens - 1) / (wall - TTFT) · 冷测确认: cached_tokens == 0

| 测试 | Prompt tok | Gen tok | TTFT (s) | Wall (s) | Prefill tok/s | Decode tok/s | Cold |
|------|------------|---------|----------|----------|---------------|--------------|------|
| quick1 | 4,340 | 128 | 0.0058 | 7.28 | 753K | 85.8 | ✓ |
| quick2 | 4,340 | 128 | 0.0057 | 7.14 | 761K | 91.1 | ✓ |
| quick3 | 4,343 | 128 | 0.0057 | 7.53 | 759K | 71.3 | ✓ |
| **Avg / Median** | — | — | — | — | **757K** | **82.7 / 85.8** | — |
| long32K | 34,207 | 512 | 0.0252 | 31.83 | 1,359K | 77.3 | ✓ |

**基准要点**:
- 4K/128 冷测中，decode 吞吐 **85.8 tok/s** (median)，prefill **757K tok/s**
- 32K/512 长上下文 decode 降至 **77.3 tok/s**（-6.5%），KV cache 读取效率尚可
- TTFT ≈ 5.8ms（实测 5-7ms），表示首个 token 到达时间

---

## 3. 多口径 Lane 对比 (4K/128)

所有 lane 使用相同合成 prompt, temperature=0, 唯一 salt 冷测

| Lane | 思考模式 | Prompt tok | Gen tok | TTFT (s) | Decode x99 | Decode launcher | Reasoning | Content |
|------|----------|------------|---------|----------|------------|-----------------|-----------|---------|
| **chat-default** | 模板默认 (xhigh) | 4,456 | 128 | 5.82 | **79.8** | 79.8 | 487 chars | 0 chars |
| **chat-nothink** | enable_thinking=false | 4,420 | 128 | 5.76 | **105.5** | 105.5 | 0 chars | 767 chars |
| chat-effort-low | reasoning_effort=low | 4,447 | 128 | 5.79 | **99.1** | 99.2 | 207 chars | 485 chars |
| chat-effort-medium | reasoning_effort=medium | 4,418 | 128 | 5.74 | **97.1** | 97.2 | 281 chars | 353 chars |
| chat-effort-xhigh | reasoning_effort=xhigh | 4,457 | 128 | 5.80 | **80.4** | 80.4 | 496 chars | 0 chars |

---

## 4. 关键发现

### 4.1 思考模式对速度影响

| 模式 | Decode tok/s | vs nothink | 影响 |
|------|-------------|------------|------|
| chat-nothink (关闭) | **105.5** | 基准 | 最快 |
| chat-effort-low | 99.1 | -6.1% | 轻微 |
| chat-effort-medium | 97.1 | -8.0% | 中等 |
| chat-default | 79.8 | -24.4% | ⚠ 显著 |
| chat-effort-xhigh | 80.4 | -23.8% | ⚠ 显著 |

**结论**: Strata 默认推理模式会输出长 reasoning（~487 chars），占用了大量生成预算。关闭思考可提速 **32%**。

### 4.2 上下文长度影响

| 配置 | Decode tok/s | 变化 |
|------|-------------|------|
| 4K / 128 (avg) | 82.7 | 基准 |
| 32K / 512 | 77.3 | -6.5% |

32K 上下文 decode 降速约 6.5%，IQ2_XS 量化 KV cache 读取效率良好。

### 4.3 Strata 参数兼容性

| 参数 | 支持状态 | 说明 |
|------|----------|------|
| stream | ✓ | SSE 流式输出正常 |
| stream_options.include_usage | ✓ | 返回 usage 统计 |
| temperature=0 | ✓ | 确定性输出 |
| max_tokens | ✓ | 限制生成长度 |
| reasoning_content | ⚠ | Strata 推理字段名是 `reasoning_content` 而非 `reasoning` |
| enable_thinking | ⚠ | chat-nothink 有效，但 chat-default 仍输出 reasoning |
| reasoning_effort | ⚠ | 对速度有显著影响 |

---

## 5. 快速参考

| 场景 | 推荐配置 | 预期速度 |
|------|----------|----------|
| 最佳速度 | chat-nothink + temperature=0 | ~105 tok/s |
| 需要思考过程 | chat-effort-low | ~99 tok/s |
| 默认（含思考） | chat-default | ~80 tok/s |
| 长上下文推理 | 32K context | ~77 tok/s |

---

*报告基于 Strata IQ2_XS 模型在双 2080 Ti 硬件上的实测数据*
