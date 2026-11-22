---
type: quickstart
title: zerostreet-skills Quickstart & Business Overview / zerostreet-skills 빠른 시작 및 비즈니스 개요
description: Introduces the top-of-funnel B2A growth role, 5 MIT Agent Skills, Foundry MCP setup, and DeepAgents Architect for zerostreet-skills. ZeroStreet MIT Agent Skills, Foundry MCP 서버, DeepAgents Architect의 비즈니스 역할 및 설정 맵을 안내합니다.
tags:
  - quickstart
  - zerostreet-skills
  - mcp
  - deepagents
  - business-context
verified:
  - by: openwiki/0.7.2
    at: 2026-11-22T03:46:58.038Z
sources:
  - id: openwiki-source-d271781df50b232396052753
    resource: repo://claude_desktop_config.example.json
  - id: openwiki-source-05ccef8d4cf1698187f20464
    resource: repo://pyproject.toml
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
  - id: openwiki-source-8fed81e51001634cf0ad976d
    resource: repo://src/zerostreet_skills/__init__.py
generated: { by: "antigravity", at: "2026-11-22T03:46:58.038Z" }
---

# zerostreet-skills Quickstart & Business Overview / 빠른 시작 및 비즈니스 개요

`zerostreet-skills` (`0.1.0`, MIT) is the open-source Layer 0.5 B2A onboarding package for **ZeroStreet (`주식회사 제로스트리트`)**, providing **5 Agent Skills (`skills/`)**, the **Foundry MCP server (`zerostreet-foundry-mcp`)**, and the **DeepAgents Build-Time Architect Agent** ([`__init__.py`](../src/zerostreet_skills/__init__.py)).

`zerostreet-skills` (`0.1.0`)는 `주식회사 제로스트리트` B2A 스택의 오픈소스(MIT) 온보딩 패키지로, **5대 Agent Skills**, **Foundry MCP 서버**, 및 **DeepAgents Build-Time Architect**를 제공합니다.

---

## Business Role & Value Proposition / 비즈니스 역할 및 가치

### English

* **Top-of-Funnel B2A Growth Engine (`Layer 0.5`)**: Installs directly into coding agents (Claude Code, Codex, Antigravity, OpenClaw), converting the user's own assistant into a ZeroStreet system integrator.
* **Natural Conversion Funnel to AlphaSmith Foundry**: Guided by 5 progressive-disclosure skills and 6 MCP tools, customer agents validate risk rules, simulate macro crises, generate `alphagraph` runtime scaffolds, and pause for human approval before calling paid `AlphaSmith` GPU compilation.
* **Compliance & 0-Byte Weights**: Contains **0 bytes** of vendor policy weights and restricts every playbook to Descriptive Analytics and engineering scaffolding without stock/trade recommendations ([`README.md`](../README.md)).

### 한국어

* **B2A 최상단 유입(Top-of-Funnel) 성장 엔진**: Claude Code·Codex·Antigravity·OpenClaw 등 코딩 에이전트에 즉시 장착되어, 고객 에이전트가 스스로 ZeroStreet 아키텍처 설계 및 통합 엔지니어 역할을 수행하도록 합니다.
* **AlphaSmith 유료 파운드리 전환 퍼널**: 5대 스킬과 MCP 툴을 통해 리스크 규칙·위기 리플레이·런타임 스캐폴드를 자동 생성한 뒤 HITL 승인을 거쳐 유료 `AlphaSmith` GPU 컴파일로 연결합니다.
* **규제·가중치 0바이트 원칙**: 회사 자체 학습 가중치 0바이트를 유지하며 종목 매수/매도 추천 없이 서술적 분석과 코드 스캐폴딩만 제공합니다.

---

## 1. Package Components & MCP Client Setup / 패키지 구성 및 MCP 연동

| Component / 구성 요소 | Role / 역할 | Path / 경로 |
| :--- | :--- | :--- |
| `pyproject.toml` | `mcp[cli]`, `deepagents`, `zerostreet-schema` deps & `zerostreet-foundry-mcp` CLI / 의존성·스크립트 정의 | [pyproject.toml](../pyproject.toml) |
| `claude_desktop_config.example.json` | Sample MCP client config using `uv` and env vars / Claude Desktop 연동 템플릿 | [claude_desktop_config.example.json](../claude_desktop_config.example.json) |
| `skill_registry.py` | 5 `SKILL.md` progressive disclosure loader & audit / 5대 스킬 로딩·규제 검증 | [skill_registry.py](../src/zerostreet_skills/skill_registry.py) |
| `foundry_mcp.py` | `MCPServer` 6 tools & `AlphaSmithFoundryClient` / MCP 6종 툴 및 클라이언트 | [foundry_mcp.py](../src/zerostreet_skills/foundry_mcp.py) |
| `architect_agent.py` | `CompositeBackend` (`/skills/`) + `HumanInTheLoopMiddleware` / 아키텍트 빌더 | [architect_agent.py](../src/zerostreet_skills/architect_agent.py) |

See [`claude_desktop_config.example.json`](../claude_desktop_config.example.json) to register `uv --directory /path/to/zerostreet-skills run zerostreet-foundry-mcp` with `ALPHASMITH_BASE_URL` and `ZEROSTREET_API_KEY`.

---

## 2. Local Verification / 로컬 개발 및 검증 실행

```bash
uv sync --dev
uv run ruff check .
uv run pytest -q
```

---

## 3. OpenWiki Documentation Routing Map / OpenWiki 문서 라우팅 맵

* [Agent Skills & DeepAgents Architect Architecture / 5대 스킬 및 Architect 아키텍처](./architecture/skills-and-architect-agent.md) — 5 `SKILL.md` files, `validate_skills_compliance`, `CompositeBackend`, and `interrupt_on`
* [Foundry MCP Server & Sovereign Scaffolding Workflow / Foundry MCP 및 스캐폴딩 워크플로우](./workflows/foundry-mcp-scaffolding.md) — 6 `MCPServer` tools, `AlphaSmithFoundryClient`, schema validation, and scaffolding
