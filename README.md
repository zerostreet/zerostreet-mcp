# zerostreet-skills (`MIT`, Layer 0.5)

**`zerostreet-skills`**는 ZeroStreet (`주식회사 제로스트리트`)의 B2A(Business-to-Agent) 고객 에이전트 온보딩 및 아키텍처 조립을 위한 **오픈소스 MIT Agent Skills 5종**, **Foundry MCP 서버 (`zerostreet-foundry-mcp`)**, 및 **DeepAgents Build-Time Architect Agent**를 제공합니다.

## 구성 요소

1. **5대 Agent Skills (`skills/`)** — Progressive Disclosure 규격(`SKILL.md`):
   - `sovereign-system-architect`: AlphaGraph·HyperAlpha-VLA·AlphaSmith Foundry 아키텍처 설계 및 스캐폴딩
   - `portfolio-risk-audit`: RunTrace 사후 귀인 및 기술적 리스크 감사 (Descriptive Analytics Only)
   - `pre-trade-risk-gate`: 주문 전 킬스위치·슬리피지·체결 게이트 규칙 설계
   - `macro-crisis-sim`: 2020 COVID / 2022 금리 쇼크 / 2024 엔캐리 위기 스트레스 리플레이
   - `rebalance-math-solver`: 델타(Δ) 제약 최적화 및 다기간 회전율 수학 모델링
2. **Foundry MCP Server (`zerostreet_skills.foundry_mcp`)**:
   - Claude Code / Codex / Antigravity / OpenClaw 등 외부 에이전트가 AlphaSmith Foundry 컴파일 및 위기 평가 엔드포인트에 연결하도록 툴 스키마를 제공합니다.
3. **DeepAgents Architect (`zerostreet_skills.architect_agent`)**:
   - `create_deep_agent` + `SkillsMiddleware` + `CompositeBackend` (`/skills/` 읽기 전용 마운트) + `interrupt_on={"submit_foundry_compile_job": True}` HITL 승인을 결합한 Build-Time 에이전트를 제공합니다.

## 컴플라이언스 원칙

- **투자자문·추천 원천 배제**: 모든 `SKILL.md` 및 프롬프트는 특정 종목 매수·매도 추천이나 목표 주가 생성을 금지하고, 기술적 위험 감사·수치 분석(Descriptive Analytics) 및 소프트웨어 엔지니어링 스캐폴딩만 수행합니다.
- **가중치 0바이트 원칙**: 본 MIT 저장소에는 회사가 자체 학습한 정책 가중치 파일(`.pt`)이 포함되지 않습니다.

## 로컬 검증

```bash
uv sync --dev
uv run ruff check .
uv run pytest -q
```
