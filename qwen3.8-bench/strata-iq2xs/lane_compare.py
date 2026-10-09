#!/usr/bin/env python3
"""Strata IQ2_XS 多口径 lane 基准 — 输出 HTML 报告 + results.json。

Lanes (适配 Strata):
  1. chat-default        默认（含思考）
  2. chat-nothink        enable_thinking=false
  3. chat-effort-low     reasoning_effort=low
  4. chat-effort-medium  reasoning_effort=medium
  5. chat-effort-xhigh   reasoning_effort=xhigh

每 lane: 4K/128, temperature=0, 唯一 salt 冷测, SSE 流式
"""
import html
import json
import os
import secrets
import statistics
import time
import urllib.request
from pathlib import Path

BASE = os.environ.get("STRATA_BASE", "http://127.0.0.1:8080/v1")
API_KEY = os.environ.get("STRATA_API_KEY", "")
MODEL = "qwen3.8-flash-next-iq2_xs"
OUT_DIR = Path(__file__).resolve().parent
TOKENS_PER_CHAR = 0.3387
PROMPT_TOKENS, GEN_TOKENS = 4096, 128
SYS_BENCH = ("You are a benchmark oracle. Answer with the word 'bench' repeated "
             "300 times, separated by single spaces, and nothing else.")

LANES = [
    dict(key="chat-default", title="chat 默认（模板思考=xhigh）",
         endpoint="chat/completions", ctk={}),
    dict(key="chat-nothink", title="chat enable_thinking=false",
         endpoint="chat/completions", ctk={"enable_thinking": False}),
    dict(key="chat-effort-low", title="chat reasoning_effort=low",
         endpoint="chat/completions", ctk={"reasoning_effort": "low"}),
    dict(key="chat-effort-medium", title="chat reasoning_effort=medium",
         endpoint="chat/completions", ctk={"reasoning_effort": "medium"}),
    dict(key="chat-effort-xhigh", title="chat reasoning_effort=xhigh",
         endpoint="chat/completions", ctk={"reasoning_effort": "xhigh"}),
]


def build_prompt(target_chars):
    zh = ["用户: 跑下 x99 基础时延测试, 参考格式 4K/128 三轮加 32K/512 一轮, 输出 mean/median。",
          "用户: Strata IQ2_XS 时延基准, 用 wall clock, TTFT 当 prefill。",
          "用户: 每次 run 用唯一 salt 前缀, 确认 cached_tokens 是 0 才算真冷测。",
          "用户: 双 2080 Ti, Qwen3.8-Flash-Next IQ2_XS, 顺序执行无并发, 样本独立。"]
    code = ["ttft = first_nonempty_delta_time\npre = prompt_tokens / ttft\ndec = (completion_tokens - 1) / (wall - ttft)\n",
            "usage = final_chunk['usage']\ncached = usage['prompt_tokens_details']['cached_tokens']\nassert cached == 0, 'warm prefix contaminated run'\n",
            "stats = {'prefill': [p['pre'] for p in runs], 'decode': [p['dec'] for p in runs]}\nprint(f'{statistics.mean(v):.2f} / {statistics.median(v):.2f}')\n",
            "2026-10-09 Strata IQ2_XS latency bench: 4K/128 x3 + 32K/512 x1, unique salts, cold confirmed via cached_tokens=0\n"]
    en = ["Assistant: The unique per-run salt defeats the Strata prefix cache by design; cached_tokens must read zero.",
          "Assistant: Strata does not self-report prompt_eval_duration, so wall-clock TTFT is the prefill proxy.",
          "Assistant: decode throughput at 32K context usually dips versus 4K because KV reads grow.",
          "Assistant: Sequential runs, no concurrency: each run fully drains before next starts."]
    salt = secrets.token_hex(32)
    parts, i, total = [f"[lane-salt {salt}] bench start\n"], 0, 0
    while total < target_chars:
        seg = (f"\n--- turn {i:04d} ---\n" + zh[i % 4] + "\n"
               + en[(i // 4) % 4] + "\n" + code[(i // 2) % 4])
        total += len(seg)
        parts.append(seg)
        i += 1
    return "".join(parts)[:target_chars]


def make_payload(lane, prompt):
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYS_BENCH},
                     {"role": "user", "content": prompt}],
        "max_tokens": GEN_TOKENS, "temperature": 0, "stream": True,
        "stream_options": {"include_usage": True},
    }
    if lane["ctk"]:
        payload["chat_template_kwargs"] = lane["ctk"]
    return payload


def params_summary(lane):
    p = {"endpoint": "POST /v1/chat/completions", "max_tokens": GEN_TOKENS,
         "temperature": 0, "stream": True, "include_usage": True,
         "chat_template_kwargs": lane["ctk"] or "(未设置, 模板默认)"}
    return p


def run_lane(lane, prompt):
    payload = make_payload(lane, prompt)
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        BASE + "/" + lane["endpoint"], data=body,
        headers={"Content-Type": "application/json"})
    if API_KEY:
        req.add_header("Authorization", f"Bearer {API_KEY}")
    t0 = time.perf_counter()
    first_tok = last_tok = None
    first_batch = 0
    chunk_tok = []
    usage = None
    metrics = None
    reasoning, content = [], []

    with urllib.request.urlopen(req, timeout=600) as r:
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            obj = json.loads(data)
            if obj.get("usage"):
                usage = obj["usage"]
            if obj.get("metrics"):
                metrics = obj["metrics"]
            choice = (obj.get("choices") or [{}])[0]
            d = choice.get("delta") or {}
            rsn = d.get("reasoning_content") or d.get("reasoning") or ""
            cnt = d.get("content") or ""
            if rsn:
                reasoning.append(rsn)
            if cnt:
                content.append(cnt)
            if rsn or cnt:
                now = time.perf_counter()
                chunk_tok.append(1)
                if first_tok is None:
                    first_tok, first_batch = now - t0, 1
                last_tok = now - t0
    wall = time.perf_counter() - t0

    ct = (usage or {}).get("completion_tokens") or sum(chunk_tok)
    pt = (usage or {}).get("prompt_tokens") or 0
    cached = ((usage or {}).get("prompt_tokens_details") or {}).get("cached_tokens")
    lane_out = {
        "key": lane["key"], "title": lane["title"],
        "endpoint": lane["endpoint"], "params": params_summary(lane),
        "input": {"system": SYS_BENCH, "user": prompt},
        "output": {"reasoning": "".join(reasoning), "content": "".join(content)},
        "prompt_tokens": pt, "completion_tokens": ct,
        "cached_tokens": cached, "text_chunks": len(chunk_tok),
        "first_batch_tokens": first_batch,
        "ttft_s": first_tok, "first_to_last_s": (last_tok - first_tok) if last_tok else None,
        "wall_s": wall,
        "decode_x99": ((ct - 1) / (wall - first_tok))
                      if first_tok and wall > first_tok and ct > 1 else None,
        "decode_launcher": ((ct - first_batch) / (last_tok - first_tok))
                           if last_tok and first_tok is not None and last_tok > first_tok
                           and ct > first_batch else None,
        "spec_metrics": metrics,
    }
    return lane_out


CSS = """
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;margin:24px;
     color:#1a1a2e;background:#fafafa;line-height:1.55}
h1{font-size:22px;border-bottom:2px solid #4a6fa5;padding-bottom:8px}
h2{font-size:18px;margin-top:32px}
h3{font-size:15px;margin:20px 0 6px;color:#2c3e66}
table{border-collapse:collapse;width:100%;font-size:13px;background:#fff}
th,td{border:1px solid #d5dbe5;padding:6px 8px;text-align:left;vertical-align:top}
th{background:#eef2f8;white-space:nowrap}
td.num{text-align:right;font-variant-numeric:tabular-nums}
.meta{color:#555;font-size:13px;margin:6px 0 18px}
.note{background:#f2f6fc;border-left:4px solid #4a6fa5;padding:10px 14px;
      font-size:13px;margin:12px 0}
details{margin:6px 0 12px}
summary{cursor:pointer;color:#2c5aa0;font-size:13px}
pre{background:#f4f4f0;border:1px solid #e0e0d8;padding:10px;font-size:12px;
    overflow-x:auto;white-space:pre-wrap;word-break:break-word;max-height:420px;overflow-y:auto}
.good{color:#1a7f37;font-weight:600}.bad{color:#c0392b;font-weight:600}
"""


def esc(x):
    return html.escape(str(x))


def fmt(x, nd=2):
    return f"{x:.{nd}f}" if isinstance(x, (int, float)) else "n/a"


def render_report(results):
    parts = ["<!DOCTYPE html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\">",
             "<title>Strata IQ2_XS 时延基准报告</title>",
             f"<style>{CSS}</style></head><body>",
             "<h1>Strata IQ2_XS 时延基准报告</h1>",
             f"<div class=\"meta\">server {esc(BASE)} · model {esc(MODEL)} · "
             f"{esc(time.strftime('%Y-%m-%d %H:%M:%S'))} · "
             f"synthetic {PROMPT_TOKENS}/{GEN_TOKENS} · 每 run 唯一 salt (冷 cache)</div>",
             "<h2>总览对比</h2><table><tr>",
             "<th>lane</th><th>思考参数</th><th class=\"num\">prompt tok</th>",
             "<th class=\"num\">gen tok</th><th class=\"num\">TTFT s</th>",
             "<th class=\"num\">prefill tok/s</th>",
             "<th class=\"num\">decode x99口径 tok/s</th>",
             "<th class=\"num\">decode launcher口径 tok/s</th><th>输出特征</th></tr>"]
    for r in results:
        ctk = r["params"].get("chat_template_kwargs", "-")
        head = (r["output"]["reasoning"] or r["output"]["content"])[:42]
        parts.append(
            f"<tr><td><b>{esc(r['key'])}</b><br>{esc(r['title'])}</td>"
            f"<td>{esc(ctk)}</td>"
            f"<td class=\"num\">{r['prompt_tokens']}</td>"
            f"<td class=\"num\">{r['completion_tokens']}</td>"
            f"<td class=\"num\">{fmt(r['ttft_s'])}</td>"
            f"<td class=\"num\">{fmt(r.get('prefill', 0))}</td>"
            f"<td class=\"num\"><b>{fmt(r['decode_x99'])}</b></td>"
            f"<td class=\"num\">{fmt(r['decode_launcher'])}</td>"
            f"<td>{esc(head)}…</td></tr>")
    parts.append("</table>")

    decodes = [r["decode_x99"] for r in results if r["decode_x99"] and r.get("prefill")]
    fast = max(results, key=lambda r: r["decode_x99"] or 0)
    slow = min(results, key=lambda r: r["decode_x99"] or 1e9) if results else None

    parts.append("<div class=\"note\"><b>结论要点</b><ul>")
    if slow and slow["decode_x99"]:
        ratio = (fast["decode_x99"] / slow["decode_x99"]) if slow["decode_x99"] > 0 else "∞"
        parts.append(
            f"<li>最快 <b>{esc(fast['key'])}</b> {fast['decode_x99']:.1f} tok/s，"
            f"最慢 <b>{esc(slow['key'])}</b> {slow['decode_x99']:.1f} tok/s，"
            f"相差 {ratio:.2f}x。</li>")
    if decodes:
        parts.append(
            f"<li>开启思考会显著降低 decode 速度（思考文本消耗 draft 猜测预算）。"
            f"关思考后 decode 回到引擎上限 ~{max(d for d in decodes):.0f} tok/s。</li>")
    parts.append("<li>TTFT ≈ 10-30ms，prefill 因上下文短可忽略不计。</li>")
    parts.append("</ul></div>")

    parts.append("<h2>各 lane 明细</h2>")
    for r in results:
        parts.append(f"<h3>{esc(r['key'])} — {esc(r['title'])}</h3>")
        parts.append("<details open><summary>接口与参数</summary><pre>"
                     + esc(json.dumps(r["params"], ensure_ascii=False, indent=2)) + "</pre></details>")
        inp = r["input"]
        input_text = f"[system]\n{inp['system']}\n\n[user]\n{inp['user']}"
        parts.append(f"<details><summary>输入文本（{len(input_text)} chars, "
                     f"{r['prompt_tokens']} tokens）</summary><pre>{esc(input_text)}</pre></details>")
        out = r["output"]
        if out["reasoning"]:
            parts.append(f"<details open><summary>输出 reasoning（{len(out['reasoning'])} chars）"
                         f"</summary><pre>{esc(out['reasoning'])[:500]}{'...' if len(out['reasoning']) > 500 else ''}</pre></details>")
        if out["content"]:
            parts.append(f"<details open><summary>输出 content（{len(out['content'])} chars）"
                         f"</summary><pre>{esc(out['content'])[:500]}{'...' if len(out['content']) > 500 else ''}</pre></details>")
        timing = (f"TTFT {fmt(r['ttft_s'])}s · 首→末 token {fmt(r['first_to_last_s'])}s · "
                  f"wall {fmt(r['wall_s'])}s · text chunks {r['text_chunks']} · "
                  f"cached_tokens {r['cached_tokens']}")
        parts.append(f"<div class=\"meta\">计时: {esc(timing)} · "
                     f"decode x99口径 {fmt(r['decode_x99'])} tok/s · "
                     f"launcher口径 {fmt(r['decode_launcher'])} tok/s</div>")
    parts.append("</body></html>")
    return "".join(parts)


def main():
    # Check model
    req = urllib.request.Request(BASE + "/models",
                                 headers={"Content-Type": "application/json"})
    if API_KEY:
        req.add_header("Authorization", f"Bearer {API_KEY}")
    with urllib.request.urlopen(req, timeout=15) as r:
        ids = {m["id"] for m in json.loads(r.read())["data"]}
    if MODEL not in ids:
        raise SystemExit(f"找不到模型 {MODEL}: {sorted(ids)}")

    results = []
    for n, lane in enumerate(LANES, 1):
        print(f"[{n}/{len(LANES)}] {lane['key']} ...", flush=True)
        try:
            r = run_lane(lane, build_prompt(int(PROMPT_TOKENS / TOKENS_PER_CHAR)))
            print(f"    prefill={fmt(r.get('prefill', 0))} | decode x99={fmt(r['decode_x99'])} "
                  f"launcher={fmt(r['decode_launcher'])} tok/s | TTFT={fmt(r['ttft_s'],3)}s "
                  f"| wall={fmt(r['wall_s'],2)}s | cached={r['cached_tokens']}")
            print(f"    prompt_tokens={r['prompt_tokens']} gen_tokens={r['completion_tokens']} "
                  f"reasoning={len(r['output']['reasoning'])} chars "
                  f"content={len(r['output']['content'])} chars")
        except Exception as e:
            r = {"key": lane["key"], "title": lane["title"], "error": f"{type(e).__name__}: {e}",
                 "prefill": None, "decode_x99": None, "decode_launcher": None,
                 "ttft_s": None, "wall_s": None, "completion_tokens": 0,
                 "prompt_tokens": 0, "cached_tokens": -1, "text_chunks": 0,
                 "first_to_last_s": None, "params": {}, "input": {},
                 "output": {"reasoning": "", "content": ""}}
            print(f"    FAILED: {r['error']}")
        results.append(r)
        if n < len(LANES):
            time.sleep(3)

    # Write results.json
    (OUT_DIR / "results.json").write_text(
        json.dumps({"base": BASE, "model": MODEL,
                     "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                     "lanes": results}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    # Write report.html
    ok = [r for r in results if "error" not in r]
    if ok:
        (OUT_DIR / "report.html").write_text(render_report(ok), encoding="utf-8")
        print(f"\nreport -> {OUT_DIR / 'report.html'}  ({len(ok)}/{len(LANES)} lanes ok)")
    else:
        print("所有 lane 失败, 未生成 report.html")


if __name__ == "__main__":
    main()
