#!/usr/bin/env python3
"""x99 基础时延测试 — vLLM (2080Ti-Definitive) prefill/decode 吞吐基准。

仿 omlx_latency.py 结构, 适配 vLLM:
  vLLM 不向 usage 自报 prompt_eval_duration / generation_duration,
  故时延用 wall clock (本机 Mac → 192.168.2.108:8000, LAN RTT ~1ms, 相对
  prefill/decode 耗时可忽略):
      TTFT        = 首个非空 delta (role/content/reasoning) 到达时刻
      prefill tok/s = prompt_tokens / TTFT   (TTFT 含首 token 生成, 大 prompt 下可忽略)
      decode  tok/s = (completion_tokens - 1) / (wall - TTFT)
  冷测确认: usage.prompt_tokens_details.cached_tokens == 0
      (每 run 唯一随机 salt 前缀 → vLLM prefix cache 必 miss, 同 omlx 原则)

方案 (固定参考格式, 不即兴变体):
  Reference lane: synthetic 4K/128, 3 sequential runs
  Long lane:      32K/512, 1 run
  顺序执行 (无并发), 样本独立。

用法: python3 x99_latency.py [--no-think]   (需 x99 vLLM 在 192.168.2.108:8000 运行)
      --no-think: payload 加 chat_template_kwargs={"enable_thinking": false},
      跳过思考直接作答。双 2080Ti + DFlash2 下 decode 从 ~70-90 (思考文本,
      draft 接受率 ~30%) 回到引擎上限 ~180 tok/s (接受率 100%), 与 launcher
      启动自测口径 (LAST_PERF_DECODE_MEAN) 直接可比。
判定: 4 个 run 全部 200 + cached_tokens=0 + 实际 prompt tokens 偏离目标 ≤10%
      → PASS, 否则 FAIL (exit 1)。
"""
import argparse
import json
import os
import secrets
import statistics
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("X99_BASE", "http://192.168.2.108:8000/v1")
API_KEY = os.environ.get("X99_API_KEY", "1234")
MODEL = os.environ.get("X99_MODEL", "Qwen3.8-27B-NVFP4")
TOKENS_PER_CHAR = 0.3387  # 本脚本合成文本实测密度 (2026-10-06 校准, CJK+code+EN 混合)
QUICK_PROMPT_TOKENS, QUICK_GEN, QUICK_RUNS = 4096, 128, 3
LONG_PROMPT_TOKENS, LONG_GEN = 32768, 512
SYS_BENCH = ("You are a benchmark oracle. Answer with the word 'bench' repeated "
             "300 times, separated by single spaces, and nothing else.")


def stream_chat(model, prompt, max_tokens, timeout=600, chat_template_kwargs=None):
    """stream + include_usage; 返回 (usage, finish_reason, wall_s, ttft_s)."""
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYS_BENCH},
                     {"role": "user", "content": prompt}],
        "max_tokens": max_tokens, "temperature": 0, "stream": True,
        "stream_options": {"include_usage": True},
    }
    if chat_template_kwargs:
        payload["chat_template_kwargs"] = chat_template_kwargs
    body = json.dumps(payload).encode()
    req = urllib.request.Request(BASE + "/chat/completions", data=body,
                                 headers={"Authorization": f"Bearer {API_KEY}",
                                          "Content-Type": "application/json"})
    t0 = time.perf_counter()
    t_first, usage, finish = None, None, None
    with urllib.request.urlopen(req, timeout=timeout) as r:
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if payload == "[DONE]":
                break
            chunk = json.loads(payload)
            for ch in chunk.get("choices") or []:
                d = ch.get("delta") or {}
                # 首个非空 delta (role/content/reasoning) 即 TTFT
                if t_first is None and any(d.get(k) for k in ("role", "content", "reasoning")):
                    t_first = time.perf_counter() - t0
                if ch.get("finish_reason"):
                    finish = ch["finish_reason"]
            if chunk.get("usage"):
                usage = chunk["usage"]
    return usage, finish, time.perf_counter() - t0, t_first


def build_prompt(target_chars, tag):
    salt = secrets.token_hex(32)  # 每 run 唯一 → prefix cache 必 miss
    zh = [
        "用户: 跑下 x99 基础时延测试, 参考格式 4K/128 三轮加 32K/512 一轮, 输出 mean/median。",
        "用户: vLLM 不自报 prefill/decode duration, 用 wall clock, TTFT 当 prefill。",
        "用户: 每次 run 用唯一 salt 前缀, 确认 cached_tokens 是 0 才算真冷测。",
        "用户: 32K 长 prompt 那轮 decode 512 token, 看 decode 速率随上下文变长掉多少。",
        "用户: 双 2080Ti TP2, Qwen3.8-27B-NVFP4, 顺序执行无并发, 样本独立。",
    ]
    code = [
        "ttft = first_nonempty_delta_time\npre = prompt_tokens / ttft\ndec = (completion_tokens - 1) / (wall - ttft)\n",
        "usage = final_chunk['usage']\ncached = usage['prompt_tokens_details']['cached_tokens']\nassert cached == 0, 'warm prefix contaminated run'\n",
        "stats = {'prefill': [p['pre'] for p in runs], 'decode': [p['dec'] for p in runs]}\nprint(f'{statistics.mean(v):.2f} / {statistics.median(v):.2f}')\n",
        "2026-10-06 x99 latency bench: 4K/128 x3 + 32K/512 x1, unique salts, cold confirmed via cached_tokens=0\n",
    ]
    en = [
        "Assistant: The unique per-run salt defeats the vLLM prefix cache by design; cached_tokens must read zero before the numbers count.",
        "Assistant: vLLM does not self-report prompt_eval_duration, so wall-clock TTFT is the prefill proxy; LAN RTT is negligible against prefill time.",
        "Assistant: decode throughput at 32K context usually dips versus 4K because KV reads grow with sequence length; a larger drop hints at memory pressure.",
        "Assistant: Sequential runs, no concurrency: each 4K/128 run must fully drain before the next starts, so the three samples are independent.",
    ]
    parts, i, total = [f"[lat-salt-{tag} {salt}] bench start\n"], 0, 0
    while total < target_chars:
        seg = (f"\n--- turn {i:04d} ---\n" + zh[i % 5] + "\n"
               + en[(i // 5) % 4] + "\n" + code[(i // 2) % 4])
        total += len(seg)
        parts.append(seg)
        i += 1
    return "".join(parts)[:target_chars]


def run_once(model, prompt_tokens, gen_tokens, timeout=600, chat_template_kwargs=None):
    chars = int(prompt_tokens / TOKENS_PER_CHAR)
    prompt = build_prompt(chars, f"{prompt_tokens}tok")
    t0 = time.time()
    status, err, res = None, None, None
    try:
        usage, finish, wall, ttft = stream_chat(model, prompt, gen_tokens, timeout,
                                                chat_template_kwargs)
        res = (usage, finish, wall, ttft)
        status = "ok"
    except urllib.error.HTTPError as e:
        status, err = f"HTTP {e.code}", e.read().decode()[:300]
    except Exception as e:  # noqa: BLE001
        status, err = f"{type(e).__name__}", str(e)[:300]
    elapsed = time.time() - t0
    time.sleep(2)
    return {"status": status, "err": err, "res": res, "elapsed": elapsed,
            "prompt_chars": chars}


def rates_of(usage, finish, wall, ttft):
    pt = usage.get("prompt_tokens") or 0
    ct = usage.get("completion_tokens") or 0
    cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens", 0)
    pre = pt / ttft if ttft and ttft > 0 else None
    dec = (ct - 1) / (wall - ttft) if (wall and ttft and wall > ttft and ct > 1) else None
    return {"prompt_tokens": pt, "completion_tokens": ct, "cached_tokens": cached,
            "finish": finish, "wall": wall, "ttft": ttft,
            "prefill": pre, "decode": dec}


def f6(x):
    return f"{x:.6f}" if x is not None else "n/a"


def main():
    parser = argparse.ArgumentParser(description="x99 基础时延测试 (vLLM prefill/decode 吞吐基准)")
    parser.add_argument("--no-think", action="store_true",
                        help="payload 加 chat_template_kwargs={'enable_thinking': false}, "
                             "跳过思考作答; decode 回到引擎上限口径, 与 launcher 自测可比")
    args = parser.parse_args()
    chat_template_kwargs = {"enable_thinking": False} if args.no_think else None

    req = urllib.request.Request(BASE + "/models",
                                 headers={"Authorization": f"Bearer {API_KEY}"})
    with urllib.request.urlopen(req, timeout=15) as r:
        ids = {m["id"] for m in json.loads(r.read())["data"]}
    if MODEL not in ids:
        print(f"FAIL: 找不到模型 {MODEL}: {sorted(ids)}")
        sys.exit(1)

    print(f"x99 latency bench  model={MODEL}  @ {BASE}")
    print(f"thinking={'disabled (--no-think)' if args.no_think else 'default (model chat template)'}")
    print(f"date={time.strftime('%Y-%m-%d %H:%M:%S')}  (wall-clock timing, vLLM no self-report)")

    # ---- Reference lane: synthetic 4K/128, 3 sequential runs ----
    print(f"Reference lane: synthetic {QUICK_PROMPT_TOKENS // 1024}K/{QUICK_GEN}, "
          f"{QUICK_RUNS} sequential runs (prefix cache enabled, unique benchmark prefixes)")
    samples = []
    for i in range(QUICK_RUNS):
        r = run_once(MODEL, QUICK_PROMPT_TOKENS, QUICK_GEN,
                     chat_template_kwargs=chat_template_kwargs)
        if r["status"] == "ok":
            m = rates_of(*r["res"])
            samples.append((r, m))
            drift = (m["prompt_tokens"] - QUICK_PROMPT_TOKENS) / QUICK_PROMPT_TOKENS
            flag = "" if abs(drift) <= 0.1 else f"  [WARN 实际 tokens 偏离目标 {drift:+.0%}]"
            print(f"  {i + 1}. prefill {f6(m['prefill'])} tok/s | decode {f6(m['decode'])} tok/s{flag}")
        else:
            print(f"  {i + 1}. FAILED: {r['status']} {r['err']}")
        time.sleep(3)

    pres = [m["prefill"] for _, m in samples if m["prefill"] is not None]
    decs = [m["decode"] for _, m in samples if m["decode"] is not None]
    print("Aggregate:")
    if pres:
        print(f"  Prefill mean/median: {statistics.mean(pres):.2f} / "
              f"{statistics.median(pres):.2f} tok/s")
    else:
        print("  Prefill mean/median: n/a")
    if decs:
        print(f"  Decode mean/median: {statistics.mean(decs):.2f} / "
              f"{statistics.median(decs):.2f} tok/s")
    else:
        print("  Decode mean/median: n/a")

    # ---- Long lane: 32K/512 ----
    print(f"Long {LONG_PROMPT_TOKENS // 1024}K/{LONG_GEN}:")
    long_r = run_once(MODEL, LONG_PROMPT_TOKENS, LONG_GEN,
                      chat_template_kwargs=chat_template_kwargs)
    long_m = None
    if long_r["status"] == "ok":
        long_m = rates_of(*long_r["res"])
        ldrift = (long_m["prompt_tokens"] - LONG_PROMPT_TOKENS) / LONG_PROMPT_TOKENS
        flag = "" if abs(ldrift) <= 0.1 else f"  [WARN 实际 tokens 偏离目标 {ldrift:+.0%}]"
        print(f"  prefill {f6(long_m['prefill'])} / decode {f6(long_m['decode'])} tok/s{flag}")
    else:
        print(f"  FAILED: {long_r['status']} {long_r['err']}")

    # ---- details / cold confirmation ----
    print("Details:")
    for i, (r, m) in enumerate(samples):
        cold = m["cached_tokens"] == 0
        print(f"  quick{i + 1}: prompt={m['prompt_tokens']} gen={m['completion_tokens']} "
              f"cached={m['cached_tokens']} finish={m['finish']} "
              f"ttft={m['ttft']:.2f}s wall={m['wall']:.2f}s "
              f"cold={'OK' if cold else 'WARN: cache reuse detected'}")
    if long_m is not None:
        cold = long_m["cached_tokens"] == 0
        print(f"  long:   prompt={long_m['prompt_tokens']} gen={long_m['completion_tokens']} "
              f"cached={long_m['cached_tokens']} finish={long_m['finish']} "
              f"ttft={long_m['ttft']:.2f}s wall={long_m['wall']:.2f}s "
              f"cold={'OK' if cold else 'WARN: cache reuse detected'}")
    elif long_r["status"] != "ok":
        print(f"  long:   FAILED {long_r['status']} {long_r['err']}")

    drifts = [abs(m["prompt_tokens"] - QUICK_PROMPT_TOKENS) / QUICK_PROMPT_TOKENS
              for _, m in samples]
    if long_m is not None:
        drifts.append(abs(long_m["prompt_tokens"] - LONG_PROMPT_TOKENS) / LONG_PROMPT_TOKENS)
    drift_ok = all(d <= 0.10 for d in drifts)
    all_ok = (len(samples) == QUICK_RUNS
              and drift_ok
              and all(m["cached_tokens"] == 0 for _, m in samples)
              and long_r["status"] == "ok"
              and long_m is not None
              and long_m["cached_tokens"] == 0)
    print("=" * 56)
    print(f"PASS: {QUICK_RUNS}x {QUICK_PROMPT_TOKENS // 1024}K/{QUICK_GEN} + "
          f"{LONG_PROMPT_TOKENS // 1024}K/{LONG_GEN} 全冷基准完成" if all_ok
          else "FAIL: 有 run 失败 / 检测到缓存复用 / token 数偏离目标 >10%, 见 Details")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
