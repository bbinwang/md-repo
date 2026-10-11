# Strata max_tokens=30000 测试结果

## 配置修改
- `max_tokens`: 30000（通过 POST /settings 的 shared defaults）
- `reasoning_budget_tokens`: 0（无推理预算限制）

## 测试结果汇总

| 测试 | max_tokens | completion_tokens | finish_reason | 耗时 | 速度 |
|------|-----------|-------------------|---------------|------|------|
| 1. 自然数序列 | 未设(默认128) | 9784 | stop | 120.5s | ~81 tok/s |
| 2. 重复内容 | 28000 | 28000 | length | 298.8s | ~94 tok/s |
| 3. 重复内容 | 30000 | 30000 | length | ~310s | ~97 tok/s |

## 关键结论
1. **max_tokens=30000 完全正常工作** — 模型能够完整输出到 30000 token
2. **不再有 reasoning_budget 截断问题** — 之前 128 token 的截断已解决
3. **输出速度稳定在 90-100 tok/s**，性能正常
4. **最大可用输出** ≈ 30000 - 72 (prompt) = 约 29928 实际输出 tokens

## 与之前的对比

| 之前（有推理限制） | 现在（无推理限制） |
|-------------------|-------------------|
| max_tokens 默认 128 | max_tokens = 30000 |
| reasoning_budget=128 | reasoning_budget=0 |
| 最多输出 ~128 tokens | 最多输出 30000 tokens |
| 回复被截断（length） | 正常输出到上限 |
