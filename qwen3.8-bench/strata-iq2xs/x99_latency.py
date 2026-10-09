#!/usr/bin/env python3
"""Strata IQ2_XS 基础时延测试 — prefill/decode 吞吐基准。

适配 Strata 服务 (http://127.0.0.1:8080/v1)，模型 qwen3.8-flash-next-iq2_xs。
口径与 x99_latency.py 一致：
    TTFT        = 首个非空 delta (role/content/reasoning) 到达时刻
    prefill tok/s = prompt_tokens / TTFT
    decode  tok/s = (completion_tokens - 1) / (wall - TTFT)
冷测确认: usage.prompt_tokens_details.cached_tokens == 0
每 run 唯一随机 salt 前缀 → prefix cache 必 miss
"""
import json
import os
import secrets
import statistics
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("STRATA_BASE", "http://127.0.0.1:8080/v1")
API_KEY = os.environ.get("STRATA_API_KEY", "")
MODEL = "qwen3.8-flash-next-iq2_xs"
TOKENS_PER_CHAR = 0.3387  # 与 x99_latency.py 同款校准
QUICK_PROMPT_TOKENS, QUICK_GEN, QUICK_RUNS = 4096, 128, 3
LONG_PROMPT_TOKENS, LONG_GEN = 32768, 512
SYS_BENCH = ("You are a benchmark oracle. Answer with the word 'bench' repeated "
             "300 times, separated by single spaces, and nothing else.")


def stream_chat(model, prompt, max_tokens, timeout=600):
    """stream + include_usage; 返回 (usage, finish_reason, wall_s, ttft_s)."""
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYS_BENCH},
                     {"role": "user", "content": prompt}],
        "max_tokens": max_tokens, "temperature": 0, "stream": True,
        "stream_options": {"include_usage": True},
    }
    body = json.dumps(payload).encode()
    req = urllib.request.Request(BASE + "/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"}
                                 if API_KEY else {"Content-Type": "application/json"})
    if API_KEY:
        req.add_header("Authorization", f"Bearer {API_KEY}")
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
                if t_first is None and any(d.get(k) for k in ("role", "content", "reasoning", "reasoning_content")):
                    t_first = time.perf_counter() - t0
                if ch.get("finish_reason"):
                    finish = ch["finish_reason"]
            if chunk.get("usage"):
                usage = chunk["usage"]
    return usage, finish, time.perf_counter() - t0, t_first


def build_prompt(target_chars, tag):
    salt = secrets.token_hex(32)
    zh = [
        "用户: 跑下 x99 基础时延测试, 参考格式 4K/128 三轮加 32K/512 一轮, 输出 mean/median。",
        "用户: Strata IQ2_XS 时延基准, 用 wall clock, TTFT 当 prefill。",
        "用户: 每次 run 用唯一 salt 前缀, 确认 cached_tokens 是 0 才算真冷测。",
        "用户: 双 2080 Ti, Qwen3.8-Flash-Next IQ2_XS, 顺序执行无并发, 样本独立。",
    ]
    code = [
        "ttft = first_nonempty_delta_time\npre = prompt_tokens / ttft\ndec = (completion_tokens - 1) / (wall - ttft)\n",
        "usage = final_chunk['usage']\ncached = usage['prompt_tokens_details']['cached_tokens']\nassert cached == 0, 'warm prefix contaminated run'\n",
        "stats = {'prefill': [p['pre'] for p in runs], 'decode': [p['dec'] for p in runs]}\nprint(f'{statistics.mean(v):.2f} / {statistics.median(v):.2f}')\n",
        "2026-10-09 Strata IQ2_XS latency bench: 4K/128 x3 + 32K/512 x1, unique salts, cold confirmed via cached_tokens=0\n",
    ]
    en = [
        "Assistant: The unique per-run salt defeats the Strata prefix cache by design; cached_tokens must read zero before the numbers count.",
        "Assistant: Strata does not self-report prompt_eval_duration, so wall-clock TTFT is the prefill proxy; LAN RTT is negligible.",
        "Assistant: decode throughput at 32K context usually dips versus 4K because KV reads grow with sequence length.",
        "Assistant: Sequential runs, no concurrency: each 4K/128 run must fully drain before the next starts.",
    ]
    parts, i, total = [f"[lat-salt-{tag} {salt}] bench start\n"], 0, 0
    while total < target_chars:
        seg = (f"\n--- turn {i:04d} ---\n" + zh[i % 4] + "\n"
               + en[(i // 4) % 4] + "\n" + code[(i // 2) % 4])
        total += len(seg)
        parts.append(seg)
        i += 1
    return "".join(parts)[:target_chars]


def run_once(model, prompt_tokens, gen_tokens, timeout=600):
    chars = int(prompt_tokens / TOKENS_PER_CHAR)
    prompt = build_prompt(chars, f"{prompt_tokens}tok")
    t0 = time.time()
    status, err, res = None, None, None
    try:
        usage, finish, wall, ttft = stream_chat(model, prompt, gen_tokens, timeout)
        res = (usage, finish, wall, ttft)
        status = "ok"
    except urllib.error.HTTPError as e:
        status, err = f"HTTP {e.code}", e.read().decode()[:300]
    except Exception as e:
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
    # Check model availability
    req = urllib.request.Request(BASE + "/models",
                                 headers={"Content-Type": "application/json"})
    if API_KEY:
        req.add_header("Authorization", f"Bearer {API_KEY}")
    with urllib.request.urlopen(req, timeout=15) as r:
        ids = {m["id"] for m in json.loads(r.read())["data"]}
    if MODEL not in ids:
        print(f"FAIL: 找不到模型 {MODEL}: {sorted(ids)}")
        sys.exit(1)

    print(f"Strata IQ2_XS latency bench  model={MODEL}  @ {BASE}")
    print(f"date={time.strftime('%Y-%m-%d %H:%M:%S')}  (wall-clock timing)")
    print(f"hardware: 2x RTX 2080 Ti (22.5GB VRAM), 48GB RAM, E5-2680 v4")
    print()

    # ---- Reference lane: 4K/128, 3 sequential runs ----
    print(f"Reference lane: 4K/128, {QUICK_RUNS} sequential runs (cold cache)")
    samples = []
    for i in range(QUICK_RUNS):
        r = run_once(MODEL, QUICK_PROMPT_TOKENS, QUICK_GEN)
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
    print("\nAggregate:")
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
    print(f"\nLong 32K/512:")
    long_r = run_once(MODEL, LONG_PROMPT_TOKENS, LONG_GEN)
    long_m = None
    if long_r["status"] == "ok":
        long_m = rates_of(*long_r["res"])
        ldrift = (long_m["prompt_tokens"] - LONG_PROMPT_TOKENS) / LONG_PROMPT_TOKENS
        flag = "" if abs(ldrift) <= 0.1 else f"  [WARN 实际 tokens 偏离目标 {ldrift:+.0%}]"
        print(f"  prefill {f6(long_m['prefill'])} / decode {f6(long_m['decode'])} tok/s{flag}")
    else:
        print(f"  FAILED: {long_r['status']} {long_r['err']}")

    # ---- details / cold confirmation ----
    print("\nDetails:")
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
    print("\n" + "=" * 56)
    if all_ok:
        print(f"PASS: 3x 4K/128 + 1x 32K/512 全冷基准完成")
    else:
        print("FAIL: 有 run 失败 / 检测到缓存复用 / token 数偏离目标 >10%, 见 Details")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
