---
type: architecture
title: Agent Skills & DeepAgents Architect Architecture / 5대 Agent Skills 및 DeepAgents Architect 아키텍처
description: Explains the 5 progressive-disclosure MIT Agent Skills and DeepAgents Build-Time Architect wired with CompositeBackend and HumanInTheLoopMiddleware. Progressive Disclosure 기반 5대 MIT Agent Skills와 CompositeBackend·HumanInTheLoopMiddleware가 결합된 DeepAgents Architect를 설명합니다.
tags:
  - architecture
  - agent-skills
  - deepagents
  - hitl
  - compliance
verified:
  - by: openwiki/0.7.2
    at: 2026-11-22T03:46:58.038Z
sources:
  - id: openwiki-source-69edce1fc0862963647404f2
    resource: repo://skills/macro-crisis-sim/SKILL.md
  - id: openwiki-source-29750a025e5f4ef35c5314e1
    resource: repo://skills/portfolio-risk-audit/SKILL.md
  - id: openwiki-source-54b2773684bf7488d264f77d
    resource: repo://skills/pre-trade-risk-gate/SKILL.md
  - id: openwiki-source-7597f47b57afc6ecf4f181f3
    resource: repo://skills/rebalance-math-solver/SKILL.md
  - id: openwiki-source-579263068899c572607fd0b3
    resource: repo://skills/sovereign-system-architect/SKILL.md
  - id: openwiki-source-dfccdc09722b6de4c2f7435d
    resource: repo://src/zerostreet_skills/architect_agent.py
  - id: openwiki-source-848edfd4b5c24ded30e2a7cc
    resource: repo://src/zerostreet_skills/skill_registry.py
generated: { by: "antigravity", at: "2026-11-22T03:46:58.038Z" }
---

# Agent Skills & DeepAgents Architect Architecture / 5대 Agent Skills 및 DeepAgents Architect 아키텍처

`zerostreet-skills` packages 5 MIT-licensed Agent Skills for build-time onboarding together with `create_zerostreet_architect_agent`, a DeepAgents runtime that loads them via progressive disclosure and gates paid cloud calls behind human approval.

`zerostreet-skills`는 고객 에이전트 온보딩 단계(Build-Time)에 필요한 5종의 MIT 라이선스 Agent Skills와 이를 Progressive Disclosure 방식으로 적재하는 DeepAgents 기반 아키텍트(`create_zerostreet_architect_agent`)를 제공합니다.

---

## 1. Progressive Disclosure 5 Agent Skills (`skills/`) / 5대 Agent Skills

Every skill follows the Anthropic Agent Skills specification (`SKILL.md` YAML frontmatter), strictly forbids buy/sell recommendations or price targets, and restricts output to Descriptive Analytics and engineering scaffolding.

모든 스킬은 `SKILL.md` YAML Frontmatter 명세를 따르며, 특정 종목 매수·매도 추천이나 목표 주가 생성을 금지하고 기술적 서술 분석(Descriptive Analytics)과 엔지니어링 스캐폴딩만 수행합니다.

| Skill (`name`) | Role Summary / 역할 요약 | File / 경로 |
| :--- | :--- | :--- |
| `sovereign-system-architect` | Hybrid layer assembly (Data/Hot-Path/Research) & HITL scaffolding / 하이브리드 아키텍처 조립 | [SKILL.md](../../skills/sovereign-system-architect/SKILL.md) |
| `portfolio-risk-audit` | Ex-post `RunTrace` attribution, HHI concentration, and 3σ drift audits / 사후 요인 귀인 및 분포 이탈 감사 | [SKILL.md](../../skills/portfolio-risk-audit/SKILL.md) |
| `pre-trade-risk-gate` | Deterministic kill-switch, turnover cap, notional, and HITL gate design / 결정론적 사전 리스크 게이트 | [SKILL.md](../../skills/pre-trade-risk-gate/SKILL.md) |
| `macro-crisis-sim` | 2020 COVID, 2022 Rate Shock, and 2024 Yen Carry stress replay / 3대 역사적 위기 리플레이 | [SKILL.md](../../skills/macro-crisis-sim/SKILL.md) |
| `rebalance-math-solver` | Simplex projection, share deltas, and quadratic turnover penalties / 리밸런싱 수학 모델링 | [SKILL.md](../../skills/rebalance-math-solver/SKILL.md) |

---

## 2. Skill Registry & Compliance Audit (`skill_registry.py`) / 스킬 레지스트리 및 규제 검증

[`skill_registry.py`](../../src/zerostreet_skills/skill_registry.py) enforces progressive 2-stage loading and automated compliance checks:

[`skill_registry.py`](../../src/zerostreet_skills/skill_registry.py)는 2단계 점진적 로딩과 자동 컴플라이언스 검증을 수행합니다.

* **Level 1 Discovery (`discover_skills`) / 1단계 메타데이터 탐색**: Parses `SKILL.md` YAML frontmatter only and returns sorted `SkillCatalogEntry` objects. (Frontmatter만 읽어 정렬된 메타데이터 목록을 반환합니다.)
* **Level 2 Full Load (`load_skill_markdown`) / 2단계 본문 적재**: Blocks path traversal (`/`, `\`, `..`) before returning a skill's complete `SKILL.md` instructions. (경로 탈출 문자를 차단한 뒤 전체 본문을 반환합니다.)
* **Compliance Validation (`validate_skills_compliance`) / 규제·무결성 검사**: Verifies presence of all 5 expected skills, name (`<= 64`) and description (`<= 1024`) length caps, `license == "MIT"`, and zero weight binaries (`.pt`, `.pth`, `.safetensors`, `.onnx`, `.ckpt`). (5대 필수 스킬, 길이 제한, MIT 라이선스 및 바이너리 가중치 0건을 검증합니다.)

---

## 3. DeepAgents Build-Time Architect (`architect_agent.py`) / DeepAgents Architect 구조

`create_zerostreet_architect_agent()` ([`architect_agent.py`](../../src/zerostreet_skills/architect_agent.py)) composes `deepagents==0.7.41` middleware cleanly for customer onboarding:

`create_zerostreet_architect_agent()`는 `deepagents==0.7.41` 미들웨어 스택을 조합하여 안전한 온보딩 에이전트를 구성합니다.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart TB
    ARCH["create_zerostreet_architect_agent(model, workspace_dir, skills_dir)"]
    ARCH --> CB["CompositeBackend"]
    CB --> WS["default / -> FilesystemBackend(workspace_dir)"]
    CB --> SK["route /skills/ -> FilesystemBackend(skills_dir)"]
    ARCH --> SM["SkillsMiddleware(sources=['/skills/'])"]
    ARCH --> SUB["SubAgent(risk-audit-reviewer) + extra_subagents"]
    ARCH --> HITL["HumanInTheLoopMiddleware(interrupt_on=submit_foundry_compile_job) + InMemorySaver"]
```

* **Explicit Model Enforcement / 명시적 모델 필수**: Rejects `model=None` in alignment with `deepagents>=0.7` model deprecation warnings. (`model=None`을 거부하여 명시적 모델 주입을 강제합니다.)
* **HITL Paid Compilation Gate / 유료 컴파일 일시 중지**: Pauses execution (`__interrupt__`) right before `submit_foundry_compile_job`, running `AlphaSmithFoundryClient.compile_policy()` only after receiving `Command(resume={"decisions": [{"type": "approve"}]})`. (유료 GPU 컴파일 직전에 그래프를 멈추고 사용자 명시 승인 시에만 실행합니다.)

## Related Documentation / 관련 문서

* [Foundry MCP Server & Sovereign Scaffolding Workflow / Foundry MCP 서버 워크플로우](../workflows/foundry-mcp-scaffolding.md)
* [zerostreet-skills Quickstart & Business Overview / 빠른 시작 및 비즈니스 개요](../quickstart.md)
