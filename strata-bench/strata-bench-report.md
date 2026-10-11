# Strata 本机服务诊断报告

> 诊断时间：2026-10-10（周六）  
> 主机：wangbin-x99（Ubuntu 24.04, Kernel 7.0.0-34-generic, 48GB RAM）  
> 诊断范围：LLM 服务状态、日志、硬件异常排查

---

## 1. 当前服务状态

| 项目 | 状态 |
|------|------|
| Strata 服务进程 | **已停止** |
| GPU 0（RTX 2080 Ti） | 空闲，32°C, P8, 171MB VRAM |
| GPU 1（RTX 2080 Ti） | 空闲，34°C, P22W, 90MB VRAM |
| 端口 8080 监听 | **无**（服务已停） |
| 其他 LLM 进程 | 无 |

### 最后一次运行时间段
- 启动日志时间：约 **20:13**
- 日志最后写入时间：**23:17**
- 运行时长约 3 小时

---

## 2. 硬件状态

### GPU（nvidia-smi 580.178.04 / CUDA 13.0）

```
GPU 0: 32°C | P8 | 24W/200W | 171MB/22528MB | 0% 占用
GPU 1: 34°C | P22W | 22W/200W |  90MB/22528MB | 0% 占用
```

### dmesg 检查
- 无 GPU 错误、无 OOM killer 记录、无内存错误

### 内存（已知硬件缺陷）
- 根据历史记忆：memtester 曾检测到低位 0x4a1123800 区域的比特翻转缺陷
- **当前状态未重新检测**，与本次服务无关

---

## 3. Strata 服务配置

### 模型
- **Qwen3.8-Flash-Next-GSQ-RCO-IQ2_XS**（IQ2_XS 量化）
- 模型文件：`Strata-data/models/IQ2_XS/`（2 个 GGUF 文件，约 78GB）

### 推理参数
```json
--pack                        Strata-data/packs/iq2_xs
--expert-profile              data/expert-profile.bin
--expert-cache                auto
--prefill                     auto
--spec                        4
--mtp                         Strata-data/mtp/rt
--max-context                 131072
--kv                          int8
--resident-experts
--pcie-frac                   1.00
--spec-min-p                  0.70
```

### 配置要点
- **Expert cache**：自动管理，RAM 驻留约 1.26 GiB
- **PCIe 分数 1.00**：CPU/GPU 间专家切换带宽全开
- **Speculative decoding**：spec=4, spec-min-p=0.70
- **KV 量化**：int8，节省 VRAM
- **上下文上限**：131072 tokens

---

## 4. 运行性能数据

### 生成速度（各上下文长度）

| 上下文长度 | 生成 token 数 | 速度 (tok/s) | 耗时 |
|-----------|-------------|-------------|------|
| ~21K | 51 | 74.7 | 20s |
| ~136 | 164 | 66.6 | 3s |
| 10K | 128 | 61.7 | 19s |
| 20K | 128 | 62.3 | 2s |
| 30K | 128 | 61.4 | 15s |
| 50K | 128 | 59.1-60.0 | 27s |
| 100K | 128 | 58.3-58.8 | 41s |
| 130K | 128 | 54.8 | 32s |

### 缓存命中率
- **解码专家缓存命中率：100%**（全部请求）
- PCIe 旁路读取：< 0.5%（正常）
- 文件 tier 读取：按需从磁盘加载（主存约 570K+ blob reads）

### 预填充吞吐
- 短上下文（~21K）：1116 tok/s
- 中等上下文（~50K）：1349 tok/s
- 大上下文（~130K）：1079 tok/s

---

## 5. 日志异常分析

### ✅ 正常项
1. **服务启动正常**：层分裂自动分配（GPU0+GPU1），专家缓存预热完成
2. **服务关闭正常**：Ctrl+C 正常退出，无 crash 信号
3. **无硬件错误**：dmesg 和 journalctl 均无 GPU/OOM/内存错误
4. **缓存命中率稳定**：始终 100%

### ⚠️ 需要关注的问题

#### 问题 1：推理预算耗尽（反复出现）
```
the reply reached max tokens while still thinking, so it has no answer: 
a thinking budget (reasoning_budget_tokens, in the request or in strata-<model>.json 
for every request) leaves room to answer
```

**原因**：推理预算（thinking budget）设为 128 tokens，模型将全部 token 用于"思考"，没有剩余 token 生成回复内容。这不是 bug，而是配置问题。

**解决建议**：
- 在 `strata-iq2_xs.json` 中调整 `reasoning_budget_tokens`（当前隐含值约 128）
- 或者每次请求时指定一个更小的 `reasoning_budget_tokens`，留出足够 token 给回复
- 例如：`"reasoning_budget_tokens": 64`（留 64 tokens 给回复）

#### 问题 2：服务手动停止
服务最后正常停止，无异常退出原因。可能是：
- 用户手动 Ctrl+C
- 脚本超时退出
- 无持续负载导致长期空闲

### 📋 无严重异常
- 无 OOM killer
- 无 GPU 错误/ECC 错误
- 无服务崩溃/crash
- 无通信中断/连接重置错误
- 磁盘 I/O 正常（major faults 极少，0-1 次/请求）

---

## 6. 服务配置详情

### 进程启动配置 (`strata-iq2_xs.json`)
```json
{
  "exe": "/home/wangbin/qwen3.8flash/strata/engine/strata",
  "model_name": "qwen3.8-flash-next-iq2_xs",
  "gpu": [0, 1],
  "layer_split": "auto",
  "port": 8080,
  "log": "/home/wangbin/qwen3.8flash/strata/strata-iq2_xs.log",
  ...
}
```

### 启动日志关键信息
```
layer split across GPUs [0, 1] (auto)
filling the GPU's expert cache (12499 experts, 16.51 GiB of VRAM) ...
ready: http://127.0.0.1:8080/v1  (context 131072 tokens)
WARNING: no API key - anyone on your network can use this model.
```

### 启动耗时
- 专家缓存预热：约 50-60 秒（正常）
- 服务就绪：从启动到 ready 约 60-80 秒

---

## 7. 结论

| 维度 | 状态 |
|------|------|
| 服务健康度 | **健康**（已停止，但运行期间无异常） |
| GPU 状态 | **正常**（温度、功耗、VRAM 均正常） |
| 模型推理性能 | **正常**（60-75 tok/s，缓存命中率 100%） |
| 硬件安全性 | **正常**（无错误日志） |
| 配置合理性 | **需调整**（推理预算导致无回复内容） |

### 建议
1. **调整 `reasoning_budget_tokens`**：当前推理预算占满全部生成 token，模型只思考不回复
2. **添加 API Key**：日志警告当前网络可访问服务，建议配置 `api_key`
3. **定期检测内存**：内存缺陷在历史中记录过，建议定期 memtester 验证
4. **服务管理**：如需长期运行，建议使用 systemd 或 nohup 确保服务恢复

---

*报告生成：2026-10-10 | 诊断工具：ps, nvidia-smi, journalctl, dmesg, 日志分析*
