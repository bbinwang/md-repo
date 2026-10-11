#!/usr/bin/env python3
"""
Strata performance benchmark
Target: Strata Qwen3.8-Flash-Next IQ2_XS (2×2080 Ti)
Contexts: 1w, 2w, 3w, 5w, 10w, 13w tokens
Output: 128 tokens (fixed)
Metrics: PP (prefill tokens/s), TG (generation tokens/s), decode time
"""

import urllib.request
import json
import time
import sys
import os

BASE_URL = "http://127.0.0.1:8080/v1/chat/completions"
MODEL = "qwen3.8-flash-next-iq2_xs"
OUTPUT_TOKENS = 128

# Test context lengths (tokens)
TEST_CONTEXTS = [10000, 20000, 30000, 50000, 100000, 130000]


def generate_prefix(num_tokens: int) -> str:
    """Generate prefix of approximately num_tokens tokens using repeated Chinese char."""
    return "中" * num_tokens


def test_context(context_len: int):
    """Run one benchmark iteration and return results dict."""
    prefix = generate_prefix(context_len)
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prefix}],
        "max_tokens": OUTPUT_TOKENS,
        "temperature": 0.0,
        "stream": False,
    }
    data = json.dumps(payload).encode("utf-8")

    print(f"\n{'='*60}")
    print(f"Test: {context_len:,} tokens (payload {len(data):,} bytes)")
    print(f"{'='*60}")

    start = time.time()
    try:
        req = urllib.request.Request(
            BASE_URL,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer dummy",
            },
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=600)
        result = json.loads(resp.read())
        elapsed = time.time() - start

        usage = result.get("usage", {})
        timings = result.get("timings", {})

        pt = usage.get("prompt_tokens", 0)
        ct = usage.get("completion_tokens", 0)
        pms = timings.get("prompt_ms", 0)
        dms = timings.get("predicted_ms", 0)
        cache_n = timings.get("cache_n", 0)
        finish_reason = result.get("choices", [{}])[0].get("finish_reason", "")

        pp = pt / (pms / 1000) if pms > 0 else 0
        tg = ct / (dms / 1000) if dms > 0 else 0

        print(f"  ✅ PP: {pp:.1f} tok/s  |  TG: {tg:.1f} tok/s  |  Decode: {dms/1000:.2f}s")
        print(f"  Prompt: {pms/1000:.2f}s  |  Tokens: {pt:,} prompt + {ct} gen")
        print(f"  Cache hit: {cache_n} slots reused")

        if finish_reason == "length":
            print(f"  ⚠️  Output truncated (max_tokens={OUTPUT_TOKENS})")

        return {
            "ctx": context_len,
            "pt": pt,
            "ct": ct,
            "pp": round(pp, 1),
            "tg": round(tg, 1),
            "pms": pms,
            "dms": dms,
            "total": round(elapsed, 1),
            "cache": cache_n,
        }

    except Exception as e:
        elapsed = time.time() - start
        print(f"  ❌ {type(e).__name__} after {elapsed:.1f}s: {str(e)[:100]}")
        return None


def main():
    """Run all benchmark tests."""
    results = []

    for length in TEST_CONTEXTS:
        print(f"\n>>> Starting test for {length:,} tokens...")
        result = test_context(length)
        if result is None:
            print(f"\n❌ Test failed at {length:,} tokens. STOPPING.")
            break
        results.append(result)

    # Print summary table
    print("\n" + "=" * 70)
    print("SUMMARY: PP (Prefill) and TG (Token Generation)")
    print("=" * 70)
    print(
        f"{'Context':>10} {'PP (tok/s)':>10} {'TG (tok/s)':>10} "
        f"{'Decode(s)':>9} {'Total(s)':>9} {'Cache':>7}"
    )
    for r in results:
        print(
            f"{r['ctx']:>10,} {r['pp']:>10.1f} {r['tg']:>10.1f} "
            f"{r['dms']/1000:>9.2f} {r['total']:>9.1f} {r['cache']:>7}"
        )

    # Save results to JSON for later use
    results_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "bench-results.json"
    )
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {results_file}")


if __name__ == "__main__":
    main()
