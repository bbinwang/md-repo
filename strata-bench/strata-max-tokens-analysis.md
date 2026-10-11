# Strata 最大输出 Token 深度分析

> 分析时间：2026-10-10  
> 数据来源：`startup.log`（启动测试日志） + 源码分析

---

## 核心结论

**最大输出 token 数 = `max_context - prompt_tokens - 8`（CTX_SLACK）**

当前配置：
- `max_context = 131072`  tokens（从 `--max-context 131072`）
- 空提示（5 tokens prompt）→ 最大输出 ≈ **131059 tokens**
- 实际限制来自 `reasoning_budget_tokens` 或请求时的 `max_tokens` 参数

---

## 日志数据完整统计

### 完成原因分布

| 输出 Token 数 | 请求次数 | 完成原因 | 说明 |
|-------------|---------|---------|------|
| 5 | 3 | length | 模型只用 5 token 就结束了（可能是 ping/check） |
| 51 | 1 | stop | 短提示正常完成 |
| **128** | **26** | length | 大多数请求的输出被截断在 128 |
| 164 | 1 | stop | 短提示正常完成 |

### 两种 thinking 上限

```
thinking: 64 of max 128 tokens       → 有 reasoning_budget_tokens=128 限制
thinking: 8 of max 130928 tokens     → 无限制（max_context 减去提示长度）
```

---

## 源码分析：为什么 thinking 只有 128？

### 1. `reasoning_budget_tokens` 配置

**配置文件中没有设置**：
```json
// strata-iq2_xs.json
"reasoning_budget_tokens": null   // 未设置，默认 None
```

**但**：`runconfig.py` 定义该配置项可编辑：
```python
("reasoning_budget_tokens", "int>=0", 
 "Cap the thinking of every request at this many tokens (0 or empty: no cap)")
```

**可能的来源**：
- **模型共享设置（shared settings）**：Strata 的 Web UI "Settings" 视图允许全局设置 `reasoning_budget_tokens`，这会通过 `set_shared()` 应用到所有请求
- **请求参数**：客户端发送 `reasoning_budget_tokens: 128`

### 2. max_tokens / max_new 的默认值

源码关键逻辑（`server.py:prepare()`）：
```python
room = ctx - CTX_SLACK - len(ids)    # ctx=131072, CTX_SLACK=8
if max_new is None or max_new <= 0:
    max_new = room                    # 上下文剩余空间 = 最大可能输出
```

**所以不设置 max_tokens 时，理论上可以输出最多 ~131064 tokens**。

### 3. reasoning_budget 的截断逻辑

源码（`server.py:run()`）：
```python
budget = self.reasoning_budget(sampling) if thinking else None

# 当 budget 不为 None 时：
if budget and parser.state == "reasoning":
    thought += 1
    if thought >= budget and not parser.buf and not detok.pending():
        wrap = True    # 达到推理预算 → 关闭思考，开始回复
        break
```

当 `budget=128` 时，模型最多思考 128 tokens，然后关闭思考标签开始回复。

### 4. "length" finish 的原因

```
done: 128 tokens in 15s (length)
```

这里的 `length` 不是 **输出** token 被截断，而是 **总 token（思考+回复）** 用完了：

1. 模型用了 128 tokens 做"思考"
2. 关闭思考标签，开始写回复
3. 但 **max_tokens（或默认的 room）也设成了 128**，或者回复没来得及写就被 length 截断

实际上，日志中的 `done: 128 tokens` 指的是 **生成的总 token 数 = 思考 token + 回复 token**，全部被截断在 128。

---

## 最后一次成功完成的任务

```
[strata] done: 164 tokens in 3 s (67.1 tok/s) (stop)
```

- 这是**正常完成**的请求（finish_reason=stop）
- 提示很短，总生成 token = 164（可能思考 + 回复的总和）
- 无推理预算限制（`thinking: 8 of max 130928`）

---

## 配置建议

### 当前问题分析

`reasoning_budget_tokens=128` 的存在导致：
1. 模型花 128 tokens 做思考
2. 关闭思考后，回复部分也被截断（总输出 = 128）
3. **结果：回复为空或极短**

### 推荐修复

**方案一：减小推理预算，留出回复空间**
```json
{
  "reasoning_budget_tokens": 64
}
```
→ 思考最多 64 tokens，剩余 64 tokens 用于回复（假设 max_tokens=128）

**方案二：增大 max_tokens 并设置合理推理预算**
```json
{
  "reasoning_budget_tokens": 128,
  "max_tokens": 4096
}
```
→ 思考 128 tokens + 回复最多 4096 个

**方案三：完全关闭推理预算限制（不建议，太慢）**
```json
{
  "reasoning_budget_tokens": 0
}
```
→ 模型可以无限制思考，可能超时或 token 耗尽

### 如何在 Web UI 修改

1. 打开 `http://127.0.0.1:8080/`
2. 进入 Settings → 找到 `reasoning_budget_tokens`
3. 修改为 `64` 或更小
4. 或通过 API：`POST /settings` → `{"reasoning_budget_tokens": 64}`

---

## 服务测试验证（建议执行）

启动服务后，测试不同配置下的最大输出：

```bash
# 测试 1：无限制（理论上最大输出 = context - prompt - 8）
curl -s -X POST http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-flash-next-iq2_xs",
    "messages": [{"role": "user", "content": "输出 500 个重复的 token: a a a a a..."}],
    "max_tokens": 1000,
    "reasoning_effort": "none"
  }' | python -m json.tool

# 测试 2：有推理预算限制
curl -s -X POST http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-flash-next-iq2_xs",
    "messages": [{"role": "user", "content": "输出 500 个重复的 token: a a a a a..."}],
    "max_tokens": 4096,
    "reasoning_budget_tokens": 64,
    "reasoning_effort": "high"
  }' | python -m json.tool
```

---

## 总结

| 项目 | 值 |
|------|-----|
| **上下文上限** | 131,072 tokens |
| **理论最大输出** | ~131,064 tokens（空提示时） |
| **当前生效的推理预算** | 128 tokens（来源未知，可能是 shared settings） |
| **实际输出上限** | ~128 tokens（被推理预算截断） |
| **正常完成的最大输出** | 164 tokens（最后一个短测试） |
| **需要修改的配置** | `reasoning_budget_tokens` 或请求级 `reasoning_budget_tokens` |
