---
type: workflow
title: Foundry MCP 서버 및 로컬 런타임 스캐폴딩 워크플로우
description: mcp>=2.0 MCPServer 기반 6개 Foundry 및 스킬 도구, AlphaSmithFoundryClient HTTP 연동, UserPolicyConfig 스키마 검증 및 가중치 0바이트 로컬 런타임 청사진 생성 워크플로우를 한국어로 설명합니다.
tags: [workflows, mcp, foundry, scaffolding, zerostreet-schema]
verified:
  - by: openwiki/0.7.2
    at: 2026-11-22T13:08:15.756Z
sources:
  - id: openwiki-source-f6d7762b242723b33719f7bc
    resource: repo://src/zerostreet_skills/foundry_mcp.py
  - id: openwiki-source-660754668846d949ebc10551
    resource: repo://tests/test_skills_and_mcp.py
generated: { by: "antigravity", at: "2026-11-22T13:08:15.756Z" }
---

# Foundry MCP 서버 및 로컬 런타임 스캐폴딩 워크플로우

`zerostreet_skills.foundry_mcp`([`foundry_mcp.py`](../../src/zerostreet_skills/foundry_mcp.py#L1-L280))는 외부 코딩 에이전트(Claude Desktop/Code, Codex, Antigravity 등)가 `stdio` MCP 프로토콜로 제로스트리트 5대 스킬을 조회하고, 사용자 투자 정책을 검증한 뒤 `alphasmith` GPU 정책 헤드 컴파일·위기 평가·로컬 `alphagraph` 청사진 생성까지 자동 처리할 수 있게 연결합니다.

---

## 1. `mcp>=2.0` `MCPServer` 통합 및 실행 엔트리포인트

- **최신 MCP SDK 호환**: 레거시 `FastMCP`가 제거된 `mcp>=2.0` 규격에 맞춰 `from mcp.server.mcpserver import MCPServer`를 사용하며 `mcp_server = MCPServer(name="zerostreet-foundry", ...)` 인스턴스를 생성합니다.
- **CLI 실행 엔트리포인트**: [`pyproject.toml`](../../pyproject.toml#L30-L32)이 `zerostreet-foundry-mcp` 명령을 노출하며, 실행 시 `main()`이 `mcp_server.run(transport="stdio")`로 MCP 서버를 띄웁니다.

---

## 2. 공개된 6종 MCP 도구

`@mcp_server.tool()` 데코레이터로 등록된 6가지 도구는 모두 스키마 불변식과 비투자자문 원칙을 강제합니다.

| 도구 이름 | 동작 및 위임 대상 | 안전장치 |
| :--- | :--- | :--- |
| `list_zerostreet_skills` | `discover_skills()`로 1단계 스킬 메타데이터 목록 조회 | 요약 정보만 먼저 노출해 컨텍스트 절약 |
| `read_zerostreet_skill` | `load_skill_markdown()`으로 선택한 `SKILL.md` 전체 본문 로드 | 경로 탈출 문자 즉시 차단 |
| `build_user_policy_config` | `build_validated_policy_config()`로 `UserPolicyConfig` 검증·직렬화 | 양수 목적함수 및 최소 2개 고유 종목 강제 |
| `submit_foundry_compile_job` | `AlphaSmithFoundryClient.compile_policy()`로 컴파일 요청 전송 | Bearer 토큰 인증 및 티어 검사 |
| `run_crisis_replay` | `AlphaSmithFoundryClient.evaluate_crisis()`로 역사적 위기 리플레이 실행 | 과거 위기 수치 시뮬레이션 전용 |
| `scaffold_sovereign_runtime_manifest` | `generate_sovereign_scaffold_manifest()`로 로컬 실행 청사진 생성 | `contains_company_weights: False` 0바이트 고정 |

---

## 3. 정책 검증 · 컴파일 및 스캐폴딩 데이터 흐름

```mermaid
flowchart LR
    USR["투자자 대상 종목 · 보상 가중치"] --> VAL["build_validated_policy_config() (zerostreet-schema 검증)"]
    VAL --> COMP["AlphaSmithFoundryClient.compile_policy() (POST /v1/foundry/compile)"]
    VAL --> EVAL["AlphaSmithFoundryClient.evaluate_crisis() (POST /v1/eval/crisis)"]
    VAL --> MANI["generate_sovereign_scaffold_manifest() (로컬 AlphaGraph 청사진)"]
```

- **`AlphaSmithFoundryClient`**: `ALPHASMITH_BASE_URL`(기본 `http://127.0.0.1:8000`)과 `ZEROSTREET_API_KEY` 환경변수를 읽어 `Authorization: Bearer <api_key>` 헤더를 붙여 요청하며, `httpx.MockTransport` 주입을 지원해 [`test_skills_and_mcp.py`](../../tests/test_skills_and_mcp.py#L101-L214)로 오프라인 검증이 가능합니다.
- **스캐폴드 매니페스트 (`generate_sovereign_scaffold_manifest`)** ([`foundry_mcp.py`](../../src/zerostreet_skills/foundry_mcp.py#L110-L150)): `compliance_mode: "Non-Advisory-Info-Provider-And-SW-Rental"`, `contains_company_weights: False`, 로컬 SQLite 체크포인트 경로(`sqlite://./.alphagraph_state.db`), 방화벽 한도, 그리고 실제 비밀값 대신 필요한 환경변수 키 이름 목록만 담아 돌려줍니다.

---

## 관련 문서

- [zerostreet-skills v0.1.0 개요 및 빠른 시작](../quickstart.md)
- [5대 에이전트 스킬 및 DeepAgents 아키텍트 구조](../architecture/skills-and-architect-agent.md)
