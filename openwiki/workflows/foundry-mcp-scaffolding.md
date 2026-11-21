---
type: workflow
title: Foundry MCP 서버 및 Sovereign 스캐폴딩 워크플로우
description: mcp 2.x MCPServer 기반 6개 Foundry·스킬 툴과 AlphaSmithFoundryClient, 정책 스키마 검증 및 로컬 런타임 스캐폴드 워크플로우를 설명합니다.
tags:
  - workflows
  - mcp
  - foundry
  - scaffolding
  - zerostreet-schema
verified:
  - by: openwiki/0.7.2
    at: 2026-11-21T17:30:29.653Z
sources:
  - id: openwiki-source-f6d7762b242723b33719f7bc
    resource: repo://src/zerostreet_skills/foundry_mcp.py
  - id: openwiki-source-660754668846d949ebc10551
    resource: repo://tests/test_skills_and_mcp.py
generated: { by: "antigravity", at: "2026-11-21T17:30:29.653Z" }
---

# Foundry MCP 서버 및 Sovereign 스캐폴딩 워크플로우

`zerostreet_skills.foundry_mcp`는 외부 코딩 에이전트(Claude Desktop/Code, Codex, Antigravity 등)가 `stdio` MCP 프로토콜을 통해 ZeroStreet 5대 스킬을 조회하고, `AlphaSmith` 컨트롤 플레인에서 사용자 전용 Policy Head를 컴파일하거나 로컬 `AlphaGraph` 런타임 설정을 조립할 수 있도록 돕습니다 ([foundry_mcp.py](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/src/zerostreet_skills/foundry_mcp.py#L1-L239)).

## 1. `mcp>=2.0` `MCPServer` 통합 및 엔트리포인트

* **SDK 호환성**: `mcp==2.3.0`에서 제거된 레거시 `FastMCP` 대신 `from mcp.server.mcpserver import MCPServer`를 사용하며, `mcp_server = MCPServer(name="zerostreet-foundry", ...)`로 인스턴스를 생성합니다.
* **CLI 실행**: `pyproject.toml`의 `zerostreet-foundry-mcp` 스크립트가 `main()`을 호출해 `mcp_server.run(transport="stdio")`를 기동합니다.

## 2. 공개 MCP 툴 (6종)

`@mcp_server.tool()` 데코레이터로 등록된 6개 도구는 다음과 같습니다.

| 툴 이름 | 기능 및 내부 위임 대상 | 규제·안전 장치 |
| :--- | :--- | :--- |
| `list_zerostreet_skills` | `discover_skills()`로 5개 스킬 Level 1 메타데이터 반환 | Progressive Disclosure 요약만 노출 |
| `read_zerostreet_skill` | `load_skill_markdown()`으로 요청 스킬 전체 본문 반환 | 경로 탈출 문자 차단 |
| `build_user_policy_config` | `build_validated_policy_config()`로 `UserPolicyConfig` 검증 | `RLRewardWeights` 양수 목적함수 필수 |
| `submit_foundry_compile_job` | `PolicyCompileRequest` 구성 후 `AlphaSmithFoundryClient.compile_policy()` 호출 | Bearer 토큰 인증 및 티어 검증 |
| `run_crisis_replay` | `AlphaSmithFoundryClient.evaluate_crisis()`로 3대 위기 리플레이 실행 | 역사적 수치 평가(비추천) |
| `scaffold_sovereign_runtime_manifest` | `generate_sovereign_scaffold_manifest()`로 로컬 실행 매니페스트 생성 | `contains_company_weights: False` 고정 |

## 3. 정책 검증·원격 컴파일·스캐폴드 흐름

```
유저 목표/유니버스 ──▶ build_validated_policy_config() [zerostreet_schema 검증]
                           ├──▶ AlphaSmithFoundryClient.compile_policy() ──▶ POST /v1/foundry/compile
                           ├──▶ AlphaSmithFoundryClient.evaluate_crisis() ──▶ POST /v1/eval/crisis
                           └──▶ generate_sovereign_scaffold_manifest()   ──▶ AlphaGraph SQLite/Guardrail 명세
```

* **`AlphaSmithFoundryClient`**: `ALPHASMITH_BASE_URL`(기본 `http://127.0.0.1:8000`)과 `ZEROSTREET_API_KEY`를 읽어 `Authorization: Bearer <api_key>` 헤더로 `httpx.Client` 요청을 전송하며, `transport` 주입을 통해 `httpx.MockTransport` 기반의 오프라인 결정론적 테스트를 지원합니다 ([test_skills_and_mcp.py](file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-skills/tests/test_skills_and_mcp.py#L101-L214)).
* **스캐폴드 매니페스트 (`generate_sovereign_scaffold_manifest`)**: `compliance_mode: "Non-Advisory-Info-Provider-And-SW-Rental"`, `contains_company_weights: False`, 로컬 체크포인트(`sqlite://./.alphagraph_state.db`), 및 가드레일(`max_single_weight`, `hitl_threshold_krw`, `require_hitl_for_live: True`) 설정과 필요한 환경변수 키 목록(`ALPHASMITH_BASE_URL`, `ZEROSTREET_API_KEY`, `KIS_BROKER_ENV`)을 반환합니다.

## 관련 문서

<!-- openwiki: broken internal link [/openwiki/architecture/skills-and-architect-agent.md] link "/openwiki/architecture/skills-and-architect-agent.md" is root-absolute, which no real consumer resolves against the repository root (not a coding agent reading the page, not GitHub's Markdown renderer, not a local viewer); use a path relative to this file instead. Fix the href or restore the target, then delete this comment. -->
* [5대 Agent Skills 및 DeepAgents Architect 아키텍처](/openwiki/architecture/skills-and-architect-agent.md)
<!-- openwiki: broken internal link [/openwiki/quickstart.md] link "/openwiki/quickstart.md" is root-absolute, which no real consumer resolves against the repository root (not a coding agent reading the page, not GitHub's Markdown renderer, not a local viewer); use a path relative to this file instead. Fix the href or restore the target, then delete this comment. -->
* [zerostreet-skills 빠른 시작 및 아키텍처 맵](/openwiki/quickstart.md)
