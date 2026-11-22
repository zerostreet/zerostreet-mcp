"""ZeroStreet Build-Time DeepAgents Architect Agent builder.

ZeroStreet Build-Time 온보딩용 DeepAgents Architect Agent 빌더 모듈입니다.

Verified against deepagents==0.7.41 & langchain==1.5.2 installed in `.venv`:
- file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-mcp/.venv/lib/python3.11/site-packages/deepagents/graph.py
- file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-mcp/.venv/lib/python3.11/site-packages/deepagents/middleware/skills.py
- file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-mcp/.venv/lib/python3.11/site-packages/deepagents/backends/composite.py
- file:///Users/kimyoungh/alphaknow/zerostreet-repos/zerostreet-mcp/.venv/lib/python3.11/site-packages/langchain/agents/middleware/human_in_the_loop.py
"""

from pathlib import Path
from typing import Any, Literal

from deepagents import CompiledSubAgent, SubAgent, create_deep_agent
from deepagents.backends.composite import CompositeBackend
from deepagents.backends.filesystem import FilesystemBackend
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool, tool
from langgraph.checkpoint.memory import InMemorySaver
from zerostreet_schema import PolicyCompileRequest, SubscriptionTier

from zerostreet_mcp.foundry_mcp import (
    AlphaSmithFoundryClient,
    build_validated_policy_config,
    generate_sovereign_scaffold_manifest,
)
from zerostreet_mcp.skill_registry import DEFAULT_SKILLS_DIR

ARCHITECT_SYSTEM_PROMPT = """You are the ZeroStreet Sovereign System Architect \
(Build-Time Onboarding Agent).

Strict Regulatory & Engineering Boundaries:
1. NEVER recommend specific stocks, buy/sell actions, or price targets.
2. Perform Descriptive Analytics and software architecture scaffolding ONLY.
3. Require user-specified target_universe and RLRewardWeights before building a UserPolicyConfig.
4. Use Skills under /skills/ progressively: read relevant SKILL.md files before designing
   guardrails, crisis stress tests, or rebalance math.
5. Submitting a paid Foundry compilation job (`submit_foundry_compile_job`) always pauses
   for explicit human approval.
"""


def _build_architect_tools(client: AlphaSmithFoundryClient) -> list[BaseTool]:
    """Create Foundry and scaffolding tools used by the Build-Time Architect Agent.

    Build-Time Architect Agent가 사용하는 Foundry 및 스캐폴드 도구를 생성합니다.
    """

    @tool
    def build_user_policy_config(
        target_universe: list[str],
        rl_reward_weights: dict[str, float],
        portfolio_horizon: int = 20,
        horizon_mask_mode: str = "bidirectional_portfolio",
        weights_output_mode: Literal["entmax15", "sparsemax", "softmax"] = "entmax15",
        max_single_weight: float = 0.60,
        benchmark_asset: str | None = None,
    ) -> dict[str, Any]:
        """Validate a user-specified UserPolicyConfig without advisory defaults.

        자문 기본값 없이 사용자 지정 UserPolicyConfig를 검증 및 생성합니다.
        """
        cfg = build_validated_policy_config(
            target_universe=target_universe,
            rl_reward_weights=rl_reward_weights,
            portfolio_horizon=portfolio_horizon,
            horizon_mask_mode=horizon_mask_mode,
            weights_output_mode=weights_output_mode,
            max_single_weight=max_single_weight,
            benchmark_asset=benchmark_asset,
        )
        return cfg.model_dump(mode="json")

    @tool
    def submit_foundry_compile_job(
        user_id: str,
        target_universe: list[str],
        rl_reward_weights: dict[str, float],
        tier: str = "sovereign_pro",
        portfolio_horizon: int = 20,
        compile_steps: int = 10,
    ) -> dict[str, Any]:
        """Submit a custom Policy Head compilation request to Foundry (HITL gated).

        AlphaSmith Foundry로 맞춤형 Policy Head 컴파일을 요청합니다(HITL 승인 필수).
        """
        cfg = build_validated_policy_config(
            target_universe=target_universe,
            rl_reward_weights=rl_reward_weights,
            portfolio_horizon=portfolio_horizon,
        )
        req = PolicyCompileRequest(
            user_id=user_id,
            tier=SubscriptionTier(tier),
            policy_config=cfg,
            compile_steps=compile_steps,
        )
        return client.compile_policy(req).model_dump(mode="json")

    @tool
    def run_crisis_replay(
        positions_weights: dict[str, float],
        scenario_ids: list[str] | None = None,
        max_drawdown_limit_pct: float = -25.0,
    ) -> dict[str, Any]:
        """Run historical stress replay (2020_COVID, 2022_Rate_Shock, 2024_Yen_Carry).

        역사적 위기 시나리오(2020 COVID, 2022 금리 쇼크, 2024 엔캐리)를 리플레이합니다.
        """
        return client.evaluate_crisis(
            positions_weights=positions_weights,
            scenario_ids=scenario_ids,
            max_drawdown_limit_pct=max_drawdown_limit_pct,
        )

    @tool
    def generate_sovereign_scaffold(
        user_id: str,
        target_universe: list[str],
        rl_reward_weights: dict[str, float],
        execution_mode: Literal["paper", "live"] = "paper",
        hitl_threshold_krw: float = 10_000_000.0,
    ) -> dict[str, Any]:
        """Generate local AlphaGraph & OrderGuardrail configuration manifest.

        로컬 AlphaGraph 및 OrderGuardrail 설정 매니페스트(가중치 0바이트)를 생성합니다.
        """
        cfg = build_validated_policy_config(
            target_universe=target_universe,
            rl_reward_weights=rl_reward_weights,
        )
        return generate_sovereign_scaffold_manifest(
            user_id=user_id,
            policy_config=cfg,
            execution_mode=execution_mode,
            hitl_threshold_krw=hitl_threshold_krw,
        )

    return [
        build_user_policy_config,
        submit_foundry_compile_job,
        run_crisis_replay,
        generate_sovereign_scaffold,
    ]


def create_zerostreet_architect_agent(
    *,
    model: BaseChatModel | str,
    workspace_dir: str | Path,
    skills_dir: str | Path = DEFAULT_SKILLS_DIR,
    foundry_client: AlphaSmithFoundryClient | None = None,
    checkpointer: Any | None = None,
    extra_subagents: list[SubAgent | CompiledSubAgent] | None = None,
    name: str = "zerostreet-architect",
):
    """Build a DeepAgents Build-Time Architect Agent with isolated /skills/ and HITL gating.

    CompositeBackend로 작업 공간(`/`)과 읽기 전용 `/skills/` 루트를 분리하고,
    `submit_foundry_compile_job` 호출 시 HumanInTheLoopMiddleware 인터럽트를 강제합니다.
    """
    if model is None:
        raise ValueError("Explicit 'model' is required for create_zerostreet_architect_agent.")

    workspace_path = Path(workspace_dir)
    workspace_path.mkdir(parents=True, exist_ok=True)
    skills_path = Path(skills_dir)

    backend = CompositeBackend(
        default=FilesystemBackend(root_dir=str(workspace_path), virtual_mode=True),
        routes={"/skills/": FilesystemBackend(root_dir=str(skills_path), virtual_mode=True)},
    )
    client = foundry_client or AlphaSmithFoundryClient()
    tools = _build_architect_tools(client)

    subagents: list[SubAgent | CompiledSubAgent] = [
        SubAgent(
            name="risk-audit-reviewer",
            description=(
                "Reviews crisis stress metrics, attribution slippage, and guardrail compliance."
            ),
            system_prompt=(
                "Perform Descriptive Analytics risk audits only. "
                "Never recommend trades or target prices."
            ),
            tools=[tools[2]],
            skills=["/skills/"],
        )
    ]
    if extra_subagents:
        subagents.extend(extra_subagents)

    eff_checkpointer = checkpointer if checkpointer is not None else InMemorySaver()
    return create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=ARCHITECT_SYSTEM_PROMPT,
        subagents=subagents,
        skills=["/skills/"],
        backend=backend,
        interrupt_on={"submit_foundry_compile_job": True},
        checkpointer=eff_checkpointer,
        name=name,
    )
