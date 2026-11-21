---
type: architecture
title: 5대 Agent Skills 및 DeepAgents Architect 아키텍처
description: Progressive Disclosure 기반 5대 MIT Agent Skills와 CompositeBackend·HumanInTheLoopMiddleware가 결합된 DeepAgents Build-Time Architect를 설명합니다.
tags:
  - architecture
  - agent-skills
  - deepagents
  - hitl
  - compliance
verified:
  - by: openwiki/0.7.2
    at: 2026-11-21T17:30:29.653Z
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
generated: { by: "antigravity", at: "2026-11-21T17:30:29.653Z" }
---

# 5대 Agent Skills 및 DeepAgents Architect 아키텍처

`zerostreet-skills`는 고객 에이전트 온보딩 단계(Build-Time)에 필요한 5종의 MIT 라이선스 Agent Skills와 이를 Progressive Disclosure 방식으로 적재하는 DeepAgents 기반 아키텍트(`create_zerostreet_architect_agent`)를 제공합니다.

## 1. Progressive Disclosure 5대 Agent Skills (`skills/`)

모든 스킬은 Anthropic Agent Skills 명세(`SKILL.md` YAML Frontmatter)를 따르며, 특정 종목 매수·매도 추천이나 목표 주가 생성을 금지하고 기술적 서술 분석(Descriptive Analytics)과 엔지니어링 스캐폴딩만 수행합니다.

| 스킬 디렉터리 (`name`) | 역할 요약 | 주요 적용 대상 |
| :--- | :--- | :--- |
| `sovereign-system-architect` | 하이브리드 레이어(Data/Hot-Path/Research) 조립 및 HITL 스캐폴딩 | [SKILL.md](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/skills/sovereign-system-architect/SKILL.md#L1-L23) |
| `portfolio-risk-audit` | `RunTrace` 사후 요인 귀인, HHI 집중도, 3σ 분포 이탈 감사 | [SKILL.md](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/skills/portfolio-risk-audit/SKILL.md#L1-L26) |
| `pre-trade-risk-gate` | 결정론적 킬스위치·회전율 한도·노셔널·HITL 승인 게이트 설계 | [SKILL.md](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/skills/pre-trade-risk-gate/SKILL.md#L1-L25) |
| `macro-crisis-sim` | 2020 COVID·2022 금리 쇼크·2024 엔캐리 스트레스 리플레이 | [SKILL.md](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/skills/macro-crisis-sim/SKILL.md#L1-L25) |
| `rebalance-math-solver` | 단체(Simplex) 비중 투영, 델타 수량 계산, 이차 회전율 페널티 수식 | [SKILL.md](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/skills/rebalance-math-solver/SKILL.md#L1-L26) |

## 2. 스킬 레지스트리 및 규제 무결성 검증 (`skill_registry.py`)

[skill_registry.py](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/src/zerostreet_skills/skill_registry.py#L1-L128)는 Progressive Disclosure 2단계 로딩과 컴플라이언스 검사를 수행합니다.

* **Level 1 탐색 (`discover_skills`)**: `skills/` 하위 디렉터리의 `SKILL.md` Frontmatter만 파싱하여 `SkillCatalogEntry`(이름·설명·라이선스·허용 툴) 목록을 반환합니다.
* **Level 2 본문 적재 (`load_skill_markdown`)**: 경로 탈출(`/`, `\`, `..`)을 차단한 뒤 요청된 단일 스킬의 `SKILL.md` 전체 본문을 로드합니다.
* **규제/무결성 검사 (`validate_skills_compliance`)**: 5대 필수 스킬 존재 여부, 이름(64자 이하)·설명(1024자 이하) 규격, `license == "MIT"`, 그리고 `.pt`/`.pth`/`.safetensors`/`.onnx`/`.ckpt` 가중치 바이너리 0건을 검증합니다.

## 3. DeepAgents Build-Time Architect (`architect_agent.py`)

`create_zerostreet_architect_agent()`([architect_agent.py](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/src/zerostreet_skills/architect_agent.py#L1-L188))는 `deepagents==0.7.41`의 미들웨어 스택을 조합하여 안전한 온보딩 에이전트를 구성합니다.

```
create_zerostreet_architect_agent(model, workspace_dir, skills_dir)
 ├── CompositeBackend
 │    ├── default "/"        ──▶ FilesystemBackend(workspace_dir, virtual_mode=True)
 │    └── route "/skills/"   ──▶ FilesystemBackend(skills_dir, virtual_mode=True)
 ├── SkillsMiddleware(sources=["/skills/"])
 ├── SubAgent("risk-audit-reviewer") + extra_subagents (e.g. AlphaGraph CompiledSubAgent)
 └── HumanInTheLoopMiddleware(interrupt_on={"submit_foundry_compile_job": True}) + InMemorySaver
```

* **비추론(None) 모델 차단**: `model=None` 사용 시 폐기 경고가 발생하는 최신 DeepAgents 규격에 맞춰 명시적 `model` 전달을 강제합니다.
* **HITL 유료 작업 일시 중지**: Foundry GPU 컴파일(`submit_foundry_compile_job`) 호출 직전에 그래프 실행을 일시 중지(`__interrupt__`)하며, 사용자가 `Command(resume={"decisions": [{"type": "approve"}]})`로 승인한 경우에만 `AlphaSmithFoundryClient.compile_policy()`를 실행합니다.

## 관련 문서

<!-- openwiki: broken internal link [/openwiki/workflows/foundry-mcp-scaffolding.md] link "/openwiki/workflows/foundry-mcp-scaffolding.md" is root-absolute, which no real consumer resolves against the repository root (not a coding agent reading the page, not GitHub's Markdown renderer, not a local viewer); use a path relative to this file instead. Fix the href or restore the target, then delete this comment. -->
* [Foundry MCP 서버 및 Sovereign 스캐폴딩 워크플로우](/openwiki/workflows/foundry-mcp-scaffolding.md)
<!-- openwiki: broken internal link [/openwiki/quickstart.md] link "/openwiki/quickstart.md" is root-absolute, which no real consumer resolves against the repository root (not a coding agent reading the page, not GitHub's Markdown renderer, not a local viewer); use a path relative to this file instead. Fix the href or restore the target, then delete this comment. -->
* [zerostreet-skills 빠른 시작 및 아키텍처 맵](/openwiki/quickstart.md)
