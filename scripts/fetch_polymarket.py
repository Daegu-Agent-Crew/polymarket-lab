#!/usr/bin/env python3
"""Polymarket gamma API fetcher v3 — GitHub Actions 러너에서 실행.
엔드포인트 2종 시도 + 원시 응답 진단 로그.
"""
import json, os, time, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) polymarket-lab/1.0", "Accept": "application/json"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def fnum(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0

def first_price(m):
    op = m.get("outcomePrices")
    if isinstance(op, str):
        first = op.strip().strip('[]').split(",")[0].strip().strip('"')
        return fnum(first) * 100
    if isinstance(op, list) and op:
        return fnum(op[0]) * 100
    return None

def row(m):
    prob = first_price(m)
    return {
        "question": m.get("question") or m.get("title") or "?",
        "slug": m.get("slug"),
        "url": "https://polymarket.com/market/" + str(m.get("slug") or ""),
        "prob": round(prob, 1) if prob is not None else None,
        "vol24h": round(fnum(m.get("volume24hr"))),
        "volTotal": round(fnum(m.get("volumeNum") or m.get("volume"))),
        "liquidity": round(fnum(m.get("liquidityNum") or m.get("liquidity"))),
        "endDate": m.get("endDate"),
        "category": (m.get("category") or "").strip(),
    }

def main():
    sources = [
        "https://gamma-api.polymarket.com/markets?limit=50&closed=false&order=volume24hr&ascending=false",
        "https://gamma-api.polymarket.com/events?limit=30&closed=false&order=volume24hr&ascending=false",
    ]
    rows = []
    for url in sources:
        try:
            data = get(url)
            print("[diag]", url.split("polymarket.com")[1], "→ type", type(data).__name__, "len", len(data) if isinstance(data, list) else "?")
            if isinstance(data, list) and data:
                print("[diag] keys:", sorted(list(data[0].keys()))[:12])
                print("[diag] raw first:", json.dumps(data[0], ensure_ascii=False)[:300])
            items = data if isinstance(data, list) else data.get("data", [])
            for m in items:
                if isinstance(m, dict) and (m.get("question") or m.get("title")):
                    rows.append(row(m))
            if rows:
                break
        except Exception as e:
            print("[diag] failed:", url, repr(e))
    out = {"fetchedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "source": "gamma-api.polymarket.com", "count": len(rows), "markets": rows}
    path = os.path.join(os.path.dirname(__file__), "..", "data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("wrote", len(rows), "markets")

if __name__ == "__main__":
    main()
