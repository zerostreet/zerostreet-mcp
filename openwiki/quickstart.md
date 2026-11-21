---
type: quickstart
title: zerostreet-skills 빠른 시작 및 아키텍처 맵
description: ZeroStreet MIT Agent Skills, Foundry MCP 서버, DeepAgents Build-Time Architect 설정 및 문서 맵을 안내합니다.
tags:
  - quickstart
  - zerostreet-skills
  - mcp
  - deepagents
verified:
  - by: openwiki/0.7.2
    at: 2026-11-21T17:30:29.653Z
sources:
  - id: openwiki-source-d271781df50b232396052753
    resource: repo://claude_desktop_config.example.json
  - id: openwiki-source-05ccef8d4cf1698187f20464
    resource: repo://pyproject.toml
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
  - id: openwiki-source-8fed81e51001634cf0ad976d
    resource: repo://src/zerostreet_skills/__init__.py
generated: { by: "antigravity", at: "2026-11-21T17:30:29.653Z" }
---

# zerostreet-skills 빠른 시작 및 아키텍처 맵

`zerostreet-skills` (`0.1.0`)는 `주식회사 제로스트리트` B2A 스택의 오픈소스(MIT) 온보딩 패키지로, **5대 Agent Skills (`skills/`)**, **Foundry MCP 서버 (`zerostreet-foundry-mcp`)**, 및 **DeepAgents Build-Time Architect Agent**를 제공합니다 ([__init__.py](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/src/zerostreet_skills/__init__.py#L1-L38)).

## 1. 컴플라이언스 및 라이선스 원칙

* **MIT 오픈소스 & 가중치 0바이트**: 회사가 자체 학습한 정책 체크포인트(`.pt`, `.safetensors` 등)를 일절 포함하지 않으며, 고객 전용 가중치는 `AlphaSmith` Serverless RL Foundry를 통해 고객 목적함수 기반으로만 생성됩니다 ([README.md](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/README.md#L1-L29)).
* **비투자자문 원칙**: 모든 스킬과 에이전트 프롬프트는 특정 종목 매수·매도 추천 및 목표 주가 제시를 금지하고, Descriptive Analytics(사후 귀인·위기 스트레스 수치·가드레일 검증)와 소프트웨어 스캐폴딩만 담당합니다.

## 2. 패키지 구성 및 MCP 클라이언트 연동

| 구성 파일 / 모듈 | 역할 | 경로 |
| :--- | :--- | :--- |
| `pyproject.toml` | `mcp[cli]`, `deepagents`, `zerostreet-schema` 의존성 및 `zerostreet-foundry-mcp` 스크립트 정의 | [pyproject.toml](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/pyproject.toml#L1-L48) |
| `claude_desktop_config.example.json` | Claude Desktop 등 MCP 클라이언트용 `zerostreet-foundry` 연결 템플릿 | [claude_desktop_config.example.json](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/claude_desktop_config.example.json#L1-L17) |
| `skill_registry.py` | 5종 `SKILL.md` Progressive Disclosure 로딩 및 컴플라이언스 검증 | [skill_registry.py](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/src/zerostreet_skills/skill_registry.py#L1-L128) |
| `foundry_mcp.py` | `mcp.server.mcpserver.MCPServer` 기반 6개 툴 및 `AlphaSmithFoundryClient` | [foundry_mcp.py](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/src/zerostreet_skills/foundry_mcp.py#L1-L239) |
| `architect_agent.py` | `CompositeBackend` (`/skills/` 라우트) + `HumanInTheLoopMiddleware` 기반 Architect | [architect_agent.py](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/src/zerostreet_skills/architect_agent.py#L1-L188) |

`claude_desktop_config.example.json`을 참고해 `uv --directory /path/to/zerostreet-skills run zerostreet-foundry-mcp` 명령과 `ALPHASMITH_BASE_URL`, `ZEROSTREET_API_KEY` 환경변수를 등록할 수 있습니다.

## 3. 로컬 개발 및 검증 실행

```bash
uv sync --dev
uv run ruff check .
uv run pytest -q
```

## 4. OpenWiki 문서 라우팅 맵

<!-- openwiki: broken internal link [/openwiki/architecture/skills-and-architect-agent.md] link "/openwiki/architecture/skills-and-architect-agent.md" is root-absolute, which no real consumer resolves against the repository root (not a coding agent reading the page, not GitHub's Markdown renderer, not a local viewer); use a path relative to this file instead. Fix the href or restore the target, then delete this comment. -->
* [5대 Agent Skills 및 DeepAgents Architect 아키텍처](/openwiki/architecture/skills-and-architect-agent.md) — `SKILL.md` 5종, `validate_skills_compliance`, `CompositeBackend` 및 `interrupt_on` 설계
<!-- openwiki: broken internal link [/openwiki/workflows/foundry-mcp-scaffolding.md] link "/openwiki/workflows/foundry-mcp-scaffolding.md" is root-absolute, which no real consumer resolves against the repository root (not a coding agent reading the page, not GitHub's Markdown renderer, not a local viewer); use a path relative to this file instead. Fix the href or restore the target, then delete this comment. -->
* [Foundry MCP 서버 및 Sovereign 스캐폴딩 워크플로우](/openwiki/workflows/foundry-mcp-scaffolding.md) — `MCPServer` 6개 툴, `AlphaSmithFoundryClient`, 정책 스키마 검증 및 스캐폴드 흐름
