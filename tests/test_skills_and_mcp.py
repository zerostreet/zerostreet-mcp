"""Offline unit & integration tests for ZeroStreet MIT skills, Foundry MCP, and Architect Agent."""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx
import pytest
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langgraph.types import Command
from pydantic import Field
from zerostreet_schema import PolicyCompileRequest

from zerostreet_skills import (
    EXPECTED_SKILL_NAMES,
    AlphaSmithFoundryClient,
    build_validated_policy_config,
    create_zerostreet_architect_agent,
    discover_skills,
    load_skill_markdown,
    mcp_server,
    validate_skills_compliance,
)


class _OfflineArchitectModel(BaseChatModel):
    """Deterministic offline BaseChatModel to verify SkillsMiddleware and HITL interrupt flow."""

    observed_system_prompts: list[str] = Field(default_factory=list)
    bound_tool_names: list[str] = Field(default_factory=list)

    @property
    def _llm_type(self) -> str:
        return "offline-architect-fake"

    def bind_tools(self, tools: Any, **kwargs: Any) -> "_OfflineArchitectModel":
        names = [getattr(t, "name", str(t)) for t in tools]
        self.bound_tool_names = names
        return self

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        sys_texts = [
            str(m.content) for m in messages if getattr(m, "type", "") == "system"
        ]
        if sys_texts:
            self.observed_system_prompts.append("\n".join(sys_texts))

        tool_msgs = [m for m in messages if isinstance(m, ToolMessage)]
        if not tool_msgs:
            ai = AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "submit_foundry_compile_job",
                        "args": {
                            "user_id": "usr_arch_01",
                            "target_universe": ["ASSET_A", "ASSET_B", "CASH"],
                            "rl_reward_weights": {"sortino_20": 1.0, "cvar_20": 0.5},
                            "tier": "sovereign_pro",
                            "portfolio_horizon": 4,
                            "compile_steps": 3,
                        },
                        "id": "call_compile_1",
                        "type": "tool_call",
                    }
                ],
            )
        else:
            last_content = str(tool_msgs[-1].content)
            ai = AIMessage(
                content=f"Architecture compile verified cleanly: {last_content}",
            )
        return ChatResult(generations=[ChatGeneration(message=ai)])


def test_skill_registry_discovery_and_compliance() -> None:
    entries = discover_skills()
    assert tuple(e.name for e in entries) == EXPECTED_SKILL_NAMES
    assert validate_skills_compliance() == []

    architect_md = load_skill_markdown("sovereign-system-architect")
    assert "Zero Investment Advisory" in architect_md

    with pytest.raises(ValueError):
        load_skill_markdown("../pyproject.toml")


def test_foundry_mcp_tools_and_mock_transport() -> None:
    tools = asyncio.run(mcp_server.list_tools())
    tool_names = {t.name for t in tools}
    assert {
        "list_zerostreet_skills",
        "read_zerostreet_skill",
        "build_user_policy_config",
        "submit_foundry_compile_job",
        "run_crisis_replay",
        "scaffold_sovereign_runtime_manifest",
    }.issubset(tool_names)

    valid_cfg = build_validated_policy_config(
        target_universe=["ASSET_A", "ASSET_B", "CASH"],
        rl_reward_weights={"sortino_20": 1.0, "cvar_20": 0.4},
    )
    assert valid_cfg.portfolio_horizon == 20

    with pytest.raises(ValueError):
        build_validated_policy_config(
            target_universe=["ASSET_A", "CASH"],
            rl_reward_weights={"sortino_20": 0.0, "cvar_20": 0.0},
        )

    def _handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer zs_test_token"
        if request.url.path == "/v1/foundry/compile":
            return httpx.Response(
                200,
                json={
                    "job_id": "fjob_mock01",
                    "policy_checkpoint_id": "usr_ckpt_mock01",
                    "status": "COMPLETED",
                    "checkpoint_sha256": "a" * 64,
                    "artifact_uri": "/tmp/mock.pt",
                    "compiled_at": datetime.now(UTC).isoformat(),
                    "metrics": {"final_loss": 0.02},
                },
            )
        if request.url.path == "/v1/eval/crisis":
            return httpx.Response(200, json={"all_passed": True, "results": []})
        return httpx.Response(404)

    client = AlphaSmithFoundryClient(
        base_url="http://mock-alphasmith",
        api_key="zs_test_token",
        transport=httpx.MockTransport(_handler),
    )
    res = client.compile_policy(
        PolicyCompileRequest(user_id="usr_01", policy_config=valid_cfg)
    )
    assert res.status == "COMPLETED"
    assert res.policy_checkpoint_id == "usr_ckpt_mock01"
    crisis = client.evaluate_crisis(positions_weights={"ASSET_A": 0.5, "CASH": 0.5})
    assert crisis["all_passed"] is True


def test_architect_agent_skills_loading_and_hitl_interrupt(tmp_path: Path) -> None:
    seen_paths: list[str] = []

    def _foundry_handler(request: httpx.Request) -> httpx.Response:
        seen_paths.append(request.url.path)
        body = json.loads(request.content.decode("utf-8"))
        assert body["user_id"] == "usr_arch_01"
        return httpx.Response(
            200,
            json={
                "job_id": "fjob_hitl01",
                "policy_checkpoint_id": "usr_ckpt_hitl01",
                "status": "COMPLETED",
                "checkpoint_sha256": "b" * 64,
                "artifact_uri": "/tmp/hitl.pt",
                "compiled_at": datetime.now(UTC).isoformat(),
                "metrics": {"final_loss": 0.01},
            },
        )

    client = AlphaSmithFoundryClient(
        base_url="http://mock-alphasmith",
        api_key="zs_pro_live",
        transport=httpx.MockTransport(_foundry_handler),
    )
    model = _OfflineArchitectModel()
    agent = create_zerostreet_architect_agent(
        model=model,
        workspace_dir=tmp_path / "workspace",
        foundry_client=client,
    )

    config = {"configurable": {"thread_id": "arch-hitl-01"}}
    first_result = agent.invoke(
        {"messages": [{"role": "user", "content": "Scaffold and compile my sovereign policy."}]},
        config=config,
    )

    # 1. Verify SkillsMiddleware loaded all 5 skills from /skills/ via CompositeBackend
    assert model.observed_system_prompts
    sys_prompt = model.observed_system_prompts[0]
    assert "sovereign-system-architect" in sys_prompt
    assert "portfolio-risk-audit" in sys_prompt

    # 2. Verify HumanInTheLoopMiddleware interrupted before submit_foundry_compile_job
    assert "__interrupt__" in first_result
    interrupt_val = first_result["__interrupt__"][0].value
    assert interrupt_val["action_requests"][0]["name"] == "submit_foundry_compile_job"
    assert seen_paths == []

    # 3. Approve execution via Command(resume={"decisions": [{"type": "approve"}]})
    resumed = agent.invoke(
        Command(resume={"decisions": [{"type": "approve"}]}),
        config=config,
    )
    assert "__interrupt__" not in resumed
    assert seen_paths == ["/v1/foundry/compile"]
    final_msg = str(resumed["messages"][-1].content)
    assert "usr_ckpt_hitl01" in final_msg
