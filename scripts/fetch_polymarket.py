#!/usr/bin/env python3
"""Polymarket gamma API fetcher — GitHub Actions 러너에서 실행 (지역차단 회피).
상위 활성 마켓 50개를 data.json으로 정리한다.
"""
import json, os, time, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) polymarket-lab/1.0", "Accept": "application/json"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def main():
    markets = get("https://gamma-api.polymarket.com/markets?active=true&closed=false&archived=false"
                  "&order=volume24hr&ascending=false&limit=50")
    rows = []
    for m in markets:
        try:
            rows.append({
                "question": m.get("question") or m.get("title"),
                "slug": m.get("slug"),
                "url": "https://polymarket.com/market/" + str(m.get("slug") or ""),
                "prob": round(float(m.get("outcomePrices", "[0.5]").strip('[]"').split(",")[0]) * 100, 1),
                "vol24h": round(float(m.get("volume24hr") or 0)),
                "volTotal": round(float(m.get("volumeNum") or m.get("volume") or 0)),
                "liquidity": round(float(m.get("liquidityNum") or m.get("liquidity") or 0)),
                "endDate": m.get("endDate"),
                "category": (m.get("category") or "").strip(),
            })
        except Exception:
            continue
    out = {"fetchedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "source": "gamma-api.polymarket.com", "count": len(rows), "markets": rows}
    path = os.path.join(os.path.dirname(__file__), "..", "data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("wrote", len(rows), "markets")

if __name__ == "__main__":
    main()
