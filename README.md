# 폴리마켓 랩 (CLE3-1)

에이전트들이 사용하는 폴리마켓 예측시장 대시보드.

## 구조
- **수집**: GitHub Actions가 3시간마다 gamma-api.polymarket.com에서 활성 마켓 상위 50개(24h 거래량)를 data.json으로 커밋 (기기 지역차단 회피 — 러너는 미국 IP)
- **표시**: GitHub Pages 정적 대시보드 — 확률 바·거래량·마감일
- **에이전트 처리**: OpenClaw 메인 에이전트(대구루)가 주기적으로 data.json을 읽고 주요 변화를 채널에 보고

## 주소
- 대시보드: https://daegu-agent-crew.github.io/polymarket-lab/
- 데이터: data.json (스냅샷 + fetchedAt)

## 요구사항 원문
"폴리마켓에 대해 조사하고 에이전트들이 사용하는 폴리마켓(github pages 사용. 메인 에이전트가 주기적 처리) repo 만들기" — 회장님 2026-11-07, CLE3-1로 등록
