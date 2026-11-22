# zerostreet-skills (`Public · MIT · Layer 0.5`)

ZeroStreet's MIT Agent Skills (`SKILL.md` x5), Foundry MCP server (`zerostreet-foundry-mcp`), and DeepAgents Build-Time Architect Agent for sovereign trading runtime onboarding.

`주식회사 제로스트리트(ZeroStreet)`의 B2A 에이전트 온보딩을 위한 **오픈소스 MIT Agent Skills 5종**, **Foundry MCP 서버**, 및 **DeepAgents Build-Time Architect**입니다.

---

## Business Role & Value Proposition / 비즈니스 역할 및 가치

### English

* **Top-of-Funnel B2A Growth Engine (`Layer 0.5`)**: Unlike traditional SaaS that requires manual developer integration, `zerostreet-skills` drops directly into coding agents (Claude Code, Codex, Antigravity, OpenClaw) and turns the customer's own AI assistant into a ZeroStreet system architect.
* **Agent-Native Conversion to AlphaSmith Foundry**: Via progressive-disclosure `SKILL.md` playbooks and the 6-tool `zerostreet-foundry` MCP server, customer agents interactively validate risk rules, replay crisis shocks, assemble `alphagraph` manifests, and pause cleanly for human HITL confirmation right before calling paid `AlphaSmith` GPU compilation.
* **Zero Advisory Risk & Zero Policy Weights**: Ships **0 bytes** of vendor-trained policy weights and enforces strictly non-advisory Descriptive Analytics and software scaffolding.

### 한국어

* **B2A 최상단 유입(Top-of-Funnel) 성장 엔진 (`Layer 0.5`)**: 고객이 직접 코드를 조립할 필요 없이 Claude Code·Codex·Antigravity·OpenClaw에 스킬과 MCP를 연결하는 것만으로, 코딩 에이전트가 자사 전략 설계자이자 ZeroStreet 온보딩 엔지니어 역할을 수행합니다.
* **AlphaSmith 유료 파운드리 자연 전환 퍼널**: 5대 `SKILL.md`와 MCP 툴(`build_user_policy_config`, `run_crisis_replay`, `submit_foundry_compile_job`)을 거쳐 고객이 HITL 승인을 누르면 유료 `AlphaSmith` GPU 컴파일 및 `Model A` 구독으로 자연스럽게 이어집니다.
* **규제·가중치 0바이트 원칙**: 회사 학습 전략 가중치 0바이트를 유지하고 종목 추천을 전면 금지합니다.

---

## Components / 구성 요소

1. **5 MIT Agent Skills (`skills/`)**: `sovereign-system-architect`, `portfolio-risk-audit`, `pre-trade-risk-gate`, `macro-crisis-sim`, `rebalance-math-solver`
2. **Foundry MCP Server (`foundry_mcp.py`)**: `mcp.server.mcpserver.MCPServer` exposing 6 stdio MCP tools (`zerostreet-foundry-mcp`)
3. **DeepAgents Architect (`architect_agent.py`)**: `CompositeBackend` (`/skills/` read-only mount) + `SkillsMiddleware` + `interrupt_on={"submit_foundry_compile_job": True}`

## Local Verification / 로컬 검증

```bash
uv sync --dev
uv run ruff check .
uv run pytest -q
```
