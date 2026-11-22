---
name: sovereign-system-architect
description: Interactive sovereign execution architecture scaffold designer for AlphaGraph local runtime, ZeroSteer backbone, and AlphaSmith Foundry compilation. Generates compliant code skeletons without any buy/sell recommendations.
license: MIT
---

# Sovereign System Architect

## When to Use
Use this skill when designing or scaffolding a customer's sovereign local trading runtime built on the ZeroStreet B2A stack (`zerostreet-schema`, `zerosteer`, `alphagraph`, and `alphasmith`).

## Architecture & Compliance Rules
1. **Zero Investment Advisory**: Never recommend specific stocks, cryptocurrencies, buy/sell actions, or price targets. All runtime targets (`target_universe`), reward weights (`RLRewardWeights`), and risk thresholds (`UserPolicyConfig`) must be explicitly specified or approved by the user.
2. **Zero Pre-trained Weights in Open-Source Packages**: Do not embed company-trained `.pt` policy checkpoints in MIT code. User policy checkpoints (`policy_checkpoint_id`) are compiled strictly per user via AlphaSmith Serverless RL Foundry.
3. **Hybrid Layer Separation**:
   - **Data Plane & Control Plane (`alphasmith`)**: Delivers Point-in-Time `MultimodalFeatureBatch` (`z_mm` sliced by tier: `32d` / `128d` / `256d`) and compiles `WeightAllocatorHead` via `DifferentiableTrajectoryRLTrainer` (`freeze_backbone=True`).
   - **Trading Hot-Path (`alphagraph`)**: Executes the 7-stage deterministic LangGraph state machine (`0` runtime LLM tokens) guarded by `SqliteSaver` and `interrupt()` HITL approval.
   - **Research Cold-Path (`alphagraph.deep_research`)**: Runs DeepAgents research pipelines strictly for Descriptive Analytics.

## Scaffolding Checklist
- Validate `UserPolicyConfig` and `RLRewardWeights` via `zerostreet-schema` before invoking `submit_foundry_compile_job`.
- Require explicit HITL approval whenever submitting a paid Foundry GPU compilation job or switching `live` execution adapters.
- Wire `AlphaGraphConfig` to local SQLite checkpointing (`ALPHASMITH_BASE_URL`, `ZEROSTREET_API_KEY` read from environment variables only, never hardcoded).
