# Changelog

All notable changes to **`zerostreet-mcp`** (formerly `zerostreet-skills`) are documented in this file.
The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

이 프로젝트의 주요 변경 이력은 Keep a Changelog 1.1.0 및 SemVer 2.0.0 규격을 따릅니다.

---

## [Unreleased]

### Changed
- Renamed repository, package (`zerostreet_mcp`), and primary CLI entrypoint (`zerostreet-mcp`) from `zerostreet-skills` to put the `FastMCP` (`fastmcp>=4.0`) server upfront while retaining built-in Agent Skills (`skills/`) and DeepAgents Architect (`architect_agent.py`).
- 저장소·패키지(`zerostreet_mcp`)·기본 CLI 엔트리포인트(`zerostreet-mcp`) 이름을 `zerostreet-skills`에서 `zerostreet-mcp`로 변경하여 `FastMCP`(`fastmcp>=4.0`) 서버 역할을 전면에 내세우고 내장 에이전트 스킬·아키텍트를 통합 제공합니다.

## [0.1.0] - 2026-11-22

### Added
- Initial MIT open-source release of **zerostreet-skills**: 5 Build-Time `SKILL.md` skills (`sovereign-system-architect`, `portfolio-risk-audit`, `pre-trade-risk-gate`, `macro-crisis-sim`, `rebalance-math-solver`), FastMCP Foundry server (`zerostreet-foundry-mcp`), DeepAgents Build-Time Architect scaffold, and bilingual OpenWiki documentation.
- **zerostreet-skills** 초기 오픈소스 릴리스: Build-Time 코딩 에이전트 스킬 5종, FastMCP 서버(`zerostreet-foundry-mcp`) 및 Architect 에이전트 스캐폴드를 포함합니다.
