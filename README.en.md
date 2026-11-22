<div align="center">

[![한국어](https://img.shields.io/badge/%ED%95%9C%EA%B5%AD%EC%96%B4-Switch-e5e7eb?style=for-the-badge)](./README.md)
[![English](https://img.shields.io/badge/English-Active-111827?style=for-the-badge)](./README.en.md)

[🇰🇷 한국어](./README.md) · [🇺🇸 English](./README.en.md)

</div>

# zerostreet-mcp (`v0.1.0`) — FastMCP Server, Agent Skills & Build-Time Architect (Layer 0.5 Public MIT)

> **More than a static prompt folder: an installable `FastMCP` (`fastmcp>=4.0`) server bundling 5 MIT Agent Skills and a DeepAgents build-time architect to design, stress-test, and scaffold your local trading daemon.**

---

## Why `zerostreet-mcp`?

1. **FastMCP (`fastmcp>=4.0`) Tooling With Schema Validation**: Exposes 6 structured MCP tools (`name="zerostreet-mcp"`) over `stdio` so Claude Desktop, Cursor, and Antigravity validate `UserPolicyConfig`, invoke `alphasmith` Foundry compilation and crisis replay, and emit local runtime manifests (`contains_company_weights=False`).
2. **Built-In Domain Guardrail Skills**: Ships 5 Progressive-Disclosure MIT Agent Skills (`skills/*/SKILL.md`) covering rebalance math, pre-trade risk gates, portfolio risk audits, macro crisis simulation, and sovereign runtime architecture.

---

## FastMCP Server, Skills & Build-Time Architect Flow

```mermaid
flowchart LR
    USER["Investor or AI Client (Claude Desktop)"] -->|"stdio MCP"| MCP["zerostreet-mcp FastMCP Server"]
    MCP --> SK["skill_registry.py (5 Built-In MIT Skills)"]
    MCP --> VAL["build_user_policy_config (zerostreet_schema Check)"]
    VAL --> FND["submit_foundry_compile_job and run_crisis_replay (alphasmith)"]
    VAL --> SCF["scaffold_sovereign_runtime_manifest (Zero Company Weights)"]
    ARCH["architect_agent.py (DeepAgents Architect)"] --> SK
    ARCH --> VAL
```

### Package & Skills

- **Agent Skills (`skills/`)**: `sovereign-system-architect`, `rebalance-math-solver`, `pre-trade-risk-gate`, `portfolio-risk-audit`, `macro-crisis-sim`
- **Python Modules (`src/zerostreet_mcp/`)**:
  - [`foundry_mcp.py`](./src/zerostreet_mcp/foundry_mcp.py): `FastMCP` (`fastmcp>=4.0`) server exposing 6 MCP tools, `AlphaSmithFoundryClient`, and `zerostreet-mcp` (`zerostreet-foundry-mcp` alias) entrypoint
  - [`skill_registry.py`](./src/zerostreet_mcp/skill_registry.py): `discover_skills`, `load_skill_markdown`, `validate_skills_compliance`
  - [`architect_agent.py`](./src/zerostreet_mcp/architect_agent.py): `create_zerostreet_architect_agent`
- **Client Config Example**: [`claude_desktop_config.example.json`](./claude_desktop_config.example.json)

---

## Verification & Launch

```bash
uv sync --dev
uv run ruff check .
uv run pytest -q
uv run zerostreet-mcp
```

- Repository Wiki (Korean-primary): [./openwiki/quickstart.md](./openwiki/quickstart.md)
