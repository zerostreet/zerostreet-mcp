"""ZeroStreet Foundry MCP Server conforming to mcp>=2.0 MCPServer.

mcp>=2.0 MCPServer 규격을 준수하는 ZeroStreet Foundry MCP 서버입니다.
"""

import os
from typing import Any, Literal

import httpx
from loguru import logger
from mcp.server.mcpserver import MCPServer
from zerostreet_schema import (
    HorizonMaskMode,
    PolicyCompileRequest,
    PolicyCompileResult,
    RLRewardWeights,
    SubscriptionTier,
    UserPolicyConfig,
)

from zerostreet_skills.skill_registry import discover_skills, load_skill_markdown


class AlphaSmithFoundryClient:
    """HTTP client communicating with the AlphaSmith Layer 2 control plane.

    AlphaSmith Layer 2 컨트롤 플레인과 통신하는 HTTP 클라이언트입니다.
    """

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        raw_url = base_url or os.getenv("ALPHASMITH_BASE_URL", "http://127.0.0.1:8000")
        self.base_url = raw_url.rstrip("/")
        self.api_key = api_key or os.getenv("ZEROSTREET_API_KEY", "zs_pro_live")
        self.timeout = timeout
        self.transport = transport

    def _build_client(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            transport=self.transport,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )

    def compile_policy(self, req: PolicyCompileRequest) -> PolicyCompileResult:
        """Submit a PolicyCompileRequest to /v1/foundry/compile with Bearer auth.

        Bearer 인증을 사용해 /v1/foundry/compile로 정책 컴파일 요청을 전송합니다.
        """
        with self._build_client() as client:
            resp = client.post("/v1/foundry/compile", json=req.model_dump(mode="json"))
            resp.raise_for_status()
            return PolicyCompileResult.model_validate(resp.json())

    def evaluate_crisis(
        self,
        *,
        positions_weights: dict[str, float],
        scenario_ids: list[str] | None = None,
        max_drawdown_limit_pct: float = -25.0,
    ) -> dict[str, Any]:
        """Run historical stress replay via /v1/eval/crisis over HTTP.

        HTTP /v1/eval/crisis 엔드포인트로 역사적 위기 스트레스 평가를 실행합니다.
        """
        payload: dict[str, Any] = {
            "positions_weights": positions_weights,
            "max_drawdown_limit_pct": max_drawdown_limit_pct,
        }
        if scenario_ids is not None:
            payload["scenario_ids"] = scenario_ids
        with self._build_client() as client:
            resp = client.post("/v1/eval/crisis", json=payload)
            resp.raise_for_status()
            return dict(resp.json())


def build_validated_policy_config(
    *,
    target_universe: list[str],
    rl_reward_weights: dict[str, float],
    portfolio_horizon: int = 20,
    horizon_mask_mode: HorizonMaskMode | str = HorizonMaskMode.BIDIRECTIONAL_PORTFOLIO,
    weights_output_mode: Literal["entmax15", "sparsemax", "softmax"] = "entmax15",
    max_single_weight: float = 0.60,
    benchmark_asset: str | None = None,
) -> UserPolicyConfig:
    """Validate and construct UserPolicyConfig against zerostreet_schema invariants.

    zerostreet_schema 불변식에 맞춰 UserPolicyConfig를 검증 및 생성합니다.
    """
    weights = RLRewardWeights.model_validate(rl_reward_weights)
    return UserPolicyConfig(
        target_universe=target_universe,
        rl_reward_weights=weights,
        portfolio_horizon=portfolio_horizon,
        horizon_mask_mode=HorizonMaskMode(horizon_mask_mode),
        weights_output_mode=weights_output_mode,
        max_single_weight=max_single_weight,
        benchmark_asset=benchmark_asset,
    )


def generate_sovereign_scaffold_manifest(
    *,
    user_id: str,
    policy_config: UserPolicyConfig,
    execution_mode: Literal["paper", "live"] = "paper",
    hitl_threshold_krw: float = 10_000_000.0,
) -> dict[str, Any]:
    """Generate a local AlphaGraph daemon + Guardrail + Broker MCP scaffold manifest.

    로컬 AlphaGraph 데몬, Guardrail 및 Broker MCP 스캐폴드 매니페스트를 생성합니다.
    """
    return {
        "user_id": user_id,
        "execution_mode": execution_mode,
        "compliance_mode": "Non-Advisory-Info-Provider-And-SW-Rental",
        "contains_company_weights": False,
        "alphagraph_runtime": {
            "target_universe": policy_config.target_universe,
            "portfolio_horizon": policy_config.portfolio_horizon,
            "weights_output_mode": policy_config.weights_output_mode,
            "guardrail": {
                "max_single_weight": policy_config.max_single_weight,
                "hitl_threshold_krw": hitl_threshold_krw,
                "require_hitl_for_live": True,
            },
            "checkpoint_store": "sqlite://./.alphagraph_state.db",
        },
        "env_keys_required": [
            "ALPHASMITH_BASE_URL",
            "ZEROSTREET_API_KEY",
            "KIS_BROKER_ENV",
        ],
    }


mcp_server = MCPServer(
    name="zerostreet-foundry",
    instructions=(
        "ZeroStreet B2A Foundry MCP Server. Provide non-advisory engineering scaffolding, "
        "Agent Skills inspection, user-supplied RL policy compilation, and crisis replay."
    ),
)


@mcp_server.tool()
def list_zerostreet_skills() -> list[dict[str, Any]]:
    """List MIT ZeroStreet Agent Skills (Progressive Disclosure Level 1 metadata).

    MIT ZeroStreet 에이전트 스킬 Level 1 메타데이터 목록을 반환합니다.
    """
    return [entry.model_dump() for entry in discover_skills()]


@mcp_server.tool()
def read_zerostreet_skill(skill_name: str) -> str:
    """Read full SKILL.md instructions for a specific ZeroStreet Agent Skill.

    특정 ZeroStreet 에이전트 스킬의 전체 SKILL.md 본문을 조회합니다.
    """
    return load_skill_markdown(skill_name)


@mcp_server.tool()
def build_user_policy_config(
    target_universe: list[str],
    rl_reward_weights: dict[str, float],
    portfolio_horizon: int = 20,
    horizon_mask_mode: str = "bidirectional_portfolio",
    weights_output_mode: Literal["entmax15", "sparsemax", "softmax"] = "entmax15",
    max_single_weight: float = 0.60,
    benchmark_asset: str | None = None,
) -> dict[str, Any]:
    """Validate and serialize UserPolicyConfig from user-supplied universe and rewards.

    사용자가 지정한 유니버스와 보상 가중치로 UserPolicyConfig를 검증·직렬화합니다.
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


@mcp_server.tool()
def submit_foundry_compile_job(
    user_id: str,
    target_universe: list[str],
    rl_reward_weights: dict[str, float],
    tier: str = "sovereign_pro",
    portfolio_horizon: int = 20,
    compile_steps: int = 10,
) -> dict[str, Any]:
    """Submit a custom Policy Head trajectory RL compile job to AlphaSmith Foundry.

    사용자 맞춤형 Policy Head 궤적 RL 컴파일 작업을 AlphaSmith Foundry로 전송합니다.
    """
    policy_cfg = build_validated_policy_config(
        target_universe=target_universe,
        rl_reward_weights=rl_reward_weights,
        portfolio_horizon=portfolio_horizon,
    )
    req = PolicyCompileRequest(
        user_id=user_id,
        tier=SubscriptionTier(tier),
        policy_config=policy_cfg,
        compile_steps=compile_steps,
    )
    client = AlphaSmithFoundryClient()
    result = client.compile_policy(req)
    return result.model_dump(mode="json")


@mcp_server.tool()
def run_crisis_replay(
    positions_weights: dict[str, float],
    scenario_ids: list[str] | None = None,
    max_drawdown_limit_pct: float = -25.0,
) -> dict[str, Any]:
    """Run historical macro crisis stress replay via AlphaSmith /v1/eval/crisis.

    AlphaSmith /v1/eval/crisis를 통해 역사적 거시경제 위기 스트레스 테스트를 실행합니다.
    """
    client = AlphaSmithFoundryClient()
    return client.evaluate_crisis(
        positions_weights=positions_weights,
        scenario_ids=scenario_ids,
        max_drawdown_limit_pct=max_drawdown_limit_pct,
    )


@mcp_server.tool()
def scaffold_sovereign_runtime_manifest(
    user_id: str,
    target_universe: list[str],
    rl_reward_weights: dict[str, float],
    execution_mode: Literal["paper", "live"] = "paper",
    hitl_threshold_krw: float = 10_000_000.0,
) -> dict[str, Any]:
    """Generate a local AlphaGraph + Guardrail configuration manifest (0 company weights).

    로컬 AlphaGraph + Guardrail 설정 매니페스트(회사 가중치 0바이트)를 생성합니다.
    """
    policy_cfg = build_validated_policy_config(
        target_universe=target_universe,
        rl_reward_weights=rl_reward_weights,
    )
    return generate_sovereign_scaffold_manifest(
        user_id=user_id,
        policy_config=policy_cfg,
        execution_mode=execution_mode,
        hitl_threshold_krw=hitl_threshold_krw,
    )


def main() -> None:
    """Run ZeroStreet Foundry MCPServer over stdio transport.

    stdio 전송 방식으로 ZeroStreet Foundry MCP 서버를 실행합니다.
    """
    logger.info("Starting ZeroStreet Foundry MCPServer (stdio transport)")
    mcp_server.run(transport="stdio")


if __name__ == "__main__":
    main()
