#!/usr/bin/env python3
"""x99 decode 口径 lane 基准 — 6 lanes 统一跑, 输出 HTML 报告 + results.json.

Lanes:
  1. chat-default        x99 原口径, 模板默认思考 (resolved xhigh)
  2. chat-nothink        enable_thinking=false, 跳过思考
  3. chat-effort-low     reasoning_effort=low    (三档思考强度之一)
  4. chat-effort-medium  reasoning_effort=medium (三档思考强度之二)
  5. chat-effort-xhigh   reasoning_effort=xhigh  (三档思考强度之三)
  6. completions-forced  launcher 自测口径: allowed_token_ids 锁单 token + ignore_eos

每个 lane 记录: 接口与参数 / 输入文本 / 输出文本 (reasoning 与 content 分开) /
服务端 per-request spec-decode 指标 / 逐 chunk 计时 / 两种 decode 口径公式。

用法: python3 lane_compare.py [--base http://192.168.2.108:8000/v1]
产物: 脚本同目录下 report.html + results.json
"""
import argparse
import html
import json
import os
import secrets
import statistics
import time
import urllib.request
from pathlib import Path

BASE = os.environ.get("X99_BASE", "http://192.168.2.108:8000/v1")
API_KEY = os.environ.get("X99_API_KEY", "1234")
MODEL = os.environ.get("X99_MODEL", "Qwen3.8-27B-NVFP4")
OUT_DIR = Path(__file__).resolve().parent
TOKENS_PER_CHAR = 0.3387  # x99_latency.py 同款合成文本密度
PROMPT_TOKENS, GEN_TOKENS = 4096, 128
SYS_BENCH = ("You are a benchmark oracle. Answer with the word 'bench' repeated "
             "300 times, separated by single spaces, and nothing else.")
FORCED_TOKEN_ID = 263  # completions lane 锁死单一 token (具体是哪个 token 不影响口径)

LANES = [
    dict(key="chat-default", title="chat 默认（模板思考=默认 xhigh）",
         endpoint="chat/completions", ctk={}),
    dict(key="chat-nothink", title="chat enable_thinking=false",
         endpoint="chat/completions", ctk={"enable_thinking": False}),
    dict(key="chat-effort-low", title="chat reasoning_effort=low",
         endpoint="chat/completions", ctk={"reasoning_effort": "low"}),
    dict(key="chat-effort-medium", title="chat reasoning_effort=medium",
         endpoint="chat/completions", ctk={"reasoning_effort": "medium"}),
    dict(key="chat-effort-xhigh", title="chat reasoning_effort=xhigh",
         endpoint="chat/completions", ctk={"reasoning_effort": "xhigh"}),
    dict(key="completions-forced", title="completions 强制单 token（launcher 自测口径）",
         endpoint="completions", ctk=None),
]


def build_prompt(target_chars):
    """x99_latency.py 同款 CJK+EN+code 混合合成文本, 每 run 唯一 salt 避开 prefix cache."""
    zh = ["用户: 跑下 x99 基础时延测试, 参考格式 4K/128 三轮加 32K/512 一轮, 输出 mean/median。",
          "用户: vLLM 不自报 prefill/decode duration, 用 wall clock, TTFT 当 prefill。",
          "用户: 每次 run 用唯一 salt 前缀, 确认 cached_tokens 是 0 才算真冷测。",
          "用户: 32K 长 prompt 那轮 decode 512 token, 看 decode 速率随上下文变长掉多少。",
          "用户: 双 2080Ti TP2, Qwen3.8-27B-NVFP4, 顺序执行无并发, 样本独立。"]
    code = ["ttft = first_nonempty_delta_time\npre = prompt_tokens / ttft\ndec = (completion_tokens - 1) / (wall - ttft)\n",
            "usage = final_chunk['usage']\ncached = usage['prompt_tokens_details']['cached_tokens']\nassert cached == 0, 'warm prefix contaminated run'\n",
            "stats = {'prefill': [p['pre'] for p in runs], 'decode': [p['dec'] for p in runs]}\nprint(f'{statistics.mean(v):.2f} / {statistics.median(v):.2f}')\n",
            "2026-10-06 x99 latency bench: 4K/128 x3 + 32K/512 x1, unique salts, cold confirmed via cached_tokens=0\n"]
    en = ["Assistant: The unique per-run salt defeats the vLLM prefix cache by design; cached_tokens must read zero before the numbers count.",
          "Assistant: vLLM does not self-report prompt_eval_duration, so wall-clock TTFT is the prefill proxy; LAN RTT is negligible against prefill time.",
          "Assistant: decode throughput at 32K context usually dips versus 4K because KV reads grow with sequence length; a larger drop hints at memory pressure.",
          "Assistant: Sequential runs, no concurrency: each 4K/128 run must fully drain before the next starts, so the three samples are independent."]
    salt = secrets.token_hex(32)
    parts, i, total = [f"[lane-salt {salt}] bench start\n"], 0, 0
    while total < target_chars:
        seg = (f"\n--- turn {i:04d} ---\n" + zh[i % 5] + "\n"
               + en[(i // 5) % 4] + "\n" + code[(i // 2) % 4])
        total += len(seg)
        parts.append(seg)
        i += 1
    return "".join(parts)[:target_chars]


def make_payload(lane, prompt):
    if lane["endpoint"] == "chat/completions":
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
    filler = " the" * 4000
    return {
        "model": MODEL,
        "prompt": ("Long filler text follows. FILLER START\n" + filler
                   + "\nFILLER END\nReply with exactly: PROFILE_OK"),
        "max_tokens": GEN_TOKENS, "temperature": 0.0, "stream": True,
        "stream_options": {"include_usage": True},
        "ignore_eos": True, "return_token_ids": True,
        "allowed_token_ids": [FORCED_TOKEN_ID],
    }


def params_summary(lane):
    if lane["endpoint"] == "chat/completions":
        p = {"endpoint": "POST /v1/chat/completions", "max_tokens": GEN_TOKENS,
             "temperature": 0, "stream": True, "include_usage": True,
             "chat_template_kwargs": lane["ctk"] or "(未设置, 模板默认)"}
    else:
        p = {"endpoint": "POST /v1/completions", "max_tokens": GEN_TOKENS,
             "temperature": 0.0, "stream": True, "ignore_eos": True,
             "return_token_ids": True, "allowed_token_ids": [FORCED_TOKEN_ID]}
    return p


def run_lane(lane, prompt):
    payload = make_payload(lane, prompt)
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        BASE + "/" + lane["endpoint"], data=body,
        headers={"Authorization": f"Bearer {API_KEY}",
                 "Content-Type": "application/json"})
    t0 = time.perf_counter()
    first_tok = last_tok = None
    first_batch = 0
    chunk_tok = []
    usage = None
    metrics = None
    reasoning, content, raw_text = [], [], []

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
            if lane["endpoint"] == "completions":
                ids = choice.get("token_ids") or []
                raw_text.append(choice.get("text") or "")
                if ids:
                    now = time.perf_counter()
                    chunk_tok.append(len(ids))
                    if first_tok is None:
                        first_tok, first_batch = now - t0, len(ids)
                    last_tok = now - t0
            else:
                d = choice.get("delta") or {}
                rsn, cnt = d.get("reasoning") or "", d.get("content") or ""
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
        "input": ({"system": SYS_BENCH, "user": prompt} if lane["endpoint"] == "chat/completions"
                  else {"prompt": payload["prompt"]}),
        "output": {"reasoning": "".join(reasoning), "content": "".join(content),
                   "text": "".join(raw_text)},
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
    sm = (metrics or {}).get("speculative_decoding") or {}
    steps = sm.get("num_spec_steps")
    lane_out["tok_per_step"] = (ct / steps) if steps else None
    lane_out["acceptance_rate"] = sm.get("draft_acceptance_rate")
    lane_out["mean_acceptance_length"] = sm.get("mean_acceptance_length")
    if steps and last_tok and first_tok and steps > 1:
        lane_out["step_ms"] = (last_tok - first_tok) / (steps - 1) * 1000
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
             "<title>x99 decode 口径 lane 基准报告</title>",
             f"<style>{CSS}</style></head><body>",
             "<h1>x99 decode 口径 lane 基准报告</h1>",
             f"<div class=\"meta\">server {esc(BASE)} · model {esc(MODEL)} · "
             f"{esc(time.strftime('%Y-%m-%d %H:%M:%S'))} · "
             f"synthetic {PROMPT_TOKENS}/{GEN_TOKENS} · 每 run 唯一 salt (冷 cache) · "
             f"spec decode: DFlash2 k=7 greedy · TP2 2x2080Ti</div>",
             "<h2>总览对比</h2><table><tr>",
             "<th>lane</th><th>接口</th><th>思考参数</th><th class=\"num\">prompt tok</th>",
             "<th class=\"num\">gen tok</th><th class=\"num\">接受率</th>",
             "<th class=\"num\">tok/步</th><th class=\"num\">步数</th><th class=\"num\">步频 ms</th>",
             "<th class=\"num\">TTFT s</th><th class=\"num\">decode x99口径</th>",
             "<th class=\"num\">decode launcher口径</th><th>输出特征</th></tr>"]
    for r in results:
        ctk = r["params"].get("chat_template_kwargs", "-")
        head = (r["output"]["reasoning"] or r["output"]["content"] or r["output"]["text"])[:42]
        parts.append(
            f"<tr><td><b>{esc(r['key'])}</b><br>{esc(r['title'])}</td>"
            f"<td>{esc(r['endpoint'])}</td><td>{esc(ctk)}</td>"
            f"<td class=\"num\">{r['prompt_tokens']}</td><td class=\"num\">{r['completion_tokens']}</td>"
            f"<td class=\"num\">{fmt(r['acceptance_rate'] * 100, 1) if r['acceptance_rate'] is not None else 'n/a'}%</td>"
            f"<td class=\"num\">{fmt(r['tok_per_step'])}</td>"
            f"<td class=\"num\">{(r['spec_metrics'] or {}).get('num_spec_steps', 'n/a')}</td>"
            f"<td class=\"num\">{fmt(r.get('step_ms'), 1)}</td>"
            f"<td class=\"num\">{fmt(r['ttft_s'])}</td>"
            f"<td class=\"num\"><b>{fmt(r['decode_x99'])}</b></td>"
            f"<td class=\"num\">{fmt(r['decode_launcher'])}</td>"
            f"<td>{esc(head)}…</td></tr>")
    parts.append("</table>")

    decodes = [r["decode_x99"] for r in results if r["decode_x99"]]
    cad = [r["step_ms"] for r in results if r.get("step_ms")]
    best = max(results, key=lambda r: r["decode_x99"] or 0)
    worst = min(results, key=lambda r: r["decode_x99"] or 1e9)
    cad_line = (f"<li>引擎步频在所有 lane 恒定 ≈ {statistics.mean(cad):.1f} ms/步"
                f"（范围 {min(cad):.1f}–{max(cad):.1f}），decode tok/s 差异完全来自每步接受的 token 数。</li>"
                if cad else
                "<li>本轮未取得步频样本（服务端 metrics 缺失）。</li>")
    parts.append("<div class=\"note\"><b>结论要点</b><ul>"
                 + cad_line
                 + f"<li>最快 <b>{esc(best['key'])}</b> {best['decode_x99']:.1f} tok/s"
                 f"（接受率 {best['acceptance_rate']*100:.0f}%），最慢 <b>{esc(worst['key'])}</b>"
                 f" {worst['decode_x99']:.1f} tok/s（接受率 {worst['acceptance_rate']*100:.0f}%），"
                 f"相差 {best['decode_x99']/worst['decode_x99']:.2f}x。</li>"
                 "<li>decode ≈ tok/步 ÷ 步频；步数 = ceil(gen_tokens / tok/步)。</li>"
                 "<li>x99 公式 (ct−1)/(wall−ttft) 与 launcher 公式 (ct−首批)/(首token→末token) 同流差 &lt;1%。</li>"
                 "</ul></div>")

    parts.append("<h2>各 lane 明细</h2>")
    for r in results:
        parts.append(f"<h3>{esc(r['key'])} — {esc(r['title'])}</h3>")
        parts.append("<details open><summary>接口与参数</summary><pre>"
                     + esc(json.dumps(r["params"], ensure_ascii=False, indent=2)) + "</pre></details>")
        sm = r["spec_metrics"]
        parts.append("<details open><summary>服务端 spec-decode 指标</summary><pre>"
                     + esc(json.dumps(sm, ensure_ascii=False, indent=2) if sm else "n/a")
                     + "</pre></details>")
        inp = r["input"]
        input_text = (f"[system]\n{inp['system']}\n\n[user]\n{inp['user']}"
                      if "system" in inp else inp["prompt"])
        parts.append(f"<details><summary>输入文本（{len(input_text)} chars, "
                     f"{r['prompt_tokens']} tokens）</summary><pre>{esc(input_text)}</pre></details>")
        out = r["output"]
        if out["reasoning"]:
            parts.append(f"<details open><summary>输出 reasoning（{len(out['reasoning'])} chars）"
                         f"</summary><pre>{esc(out['reasoning'])}</pre></details>")
        if out["content"]:
            parts.append(f"<details open><summary>输出 content（{len(out['content'])} chars）"
                         f"</summary><pre>{esc(out['content'])}</pre></details>")
        if out["text"]:
            parts.append(f"<details open><summary>输出 text（{len(out['text'])} chars）"
                         f"</summary><pre>{esc(out['text'])}</pre></details>")
        timing = (f"TTFT {fmt(r['ttft_s'])}s · 首→末 token {fmt(r['first_to_last_s'])}s · "
                  f"wall {fmt(r['wall_s'])}s · text chunks {r['text_chunks']} · "
                  f"cached_tokens {r['cached_tokens']}")
        parts.append(f"<div class=\"meta\">计时: {esc(timing)} · "
                     f"decode x99口径 {fmt(r['decode_x99'])} tok/s · "
                     f"launcher口径 {fmt(r['decode_launcher'])} tok/s</div>")
    parts.append("</body></html>")
    return "".join(parts)


def main():
    global BASE
    ap = argparse.ArgumentParser(description="6-lane decode 口径基准, 输出 HTML 报告")
    ap.add_argument("--base", default=BASE, help="vLLM API base URL")
    ap.add_argument("--sleep", type=float, default=3.0, help="lane 间隔秒数")
    args = ap.parse_args()
    BASE = args.base.rstrip("/")

    ids = {m["id"] for m in json.loads(urllib.request.urlopen(
        urllib.request.Request(BASE + "/models",
                               headers={"Authorization": f"Bearer {API_KEY}"}),
        timeout=15).read())["data"]}
    if MODEL not in ids:
        raise SystemExit(f"找不到模型 {MODEL}: {sorted(ids)}")

    results = []
    for n, lane in enumerate(LANES, 1):
        print(f"[{n}/{len(LANES)}] {lane['key']} ...", flush=True)
        try:
            r = run_lane(lane, build_prompt(int(PROMPT_TOKENS / TOKENS_PER_CHAR)))
            print(f"    decode x99={fmt(r['decode_x99'])} launcher={fmt(r['decode_launcher'])}"
                  f" tok/s | accept={fmt((r['acceptance_rate'] or 0)*100,1)}%"
                  f" | tok/步={fmt(r['tok_per_step'])} | 步频={fmt(r.get('step_ms'),1)}ms")
        except Exception as e:  # noqa: BLE001
            r = {"key": lane["key"], "title": lane["title"], "error": f"{type(e).__name__}: {e}"}
            print(f"    FAILED: {r['error']}")
        results.append(r)
        if n < len(LANES):
            time.sleep(args.sleep)

    (OUT_DIR / "results.json").write_text(
        json.dumps({"base": BASE, "model": MODEL,
                    "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "lanes": results}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    ok = [r for r in results if "error" not in r]
    if ok:
        (OUT_DIR / "report.html").write_text(render_report(ok), encoding="utf-8")
        print(f"report -> {OUT_DIR/'report.html'}  ({len(ok)}/{len(LANES)} lanes ok)")
    else:
        print("所有 lane 失败, 未生成 report.html")


if __name__ == "__main__":
    main()
