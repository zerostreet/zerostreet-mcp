---
name: pre-trade-risk-gate
description: Deterministic pre-trade risk gate, kill-switch, slippage cap, and HITL approval threshold designer for AlphaGraph OrderGuardrail and local broker MCP execution.
license: MIT
---

# Pre-Trade Risk Gate

## When to Use
Use this skill when configuring or reviewing deterministic pre-trade safety gates (`OrderGuardrail`, `GuardrailConfig`) prior to brokerage MCP execution in `alphagraph`.

## Mandatory Deterministic Safeguards
Every local sovereign runtime must enforce hard numerical checks before an order leaves the daemon, without invoking runtime LLMs:
1. **Target Weight Integrity**:
   - All target weights $w_i \ge 0$ (long-only spot constraint) and $\sum_i w_i \le 1.0$.
   - Every non-cash weight obeys $w_i \le \text{max\_single\_weight}$.
2. **Turnover & Delta Threshold (`max_turnover_per_step`)**:
   - Compute $\text{L1 turnover} = \sum_i |w_i^{\text{target}} - w_i^{\text{prev}}|$.
   - Block orders exceeding `max_turnover_per_step` and emit `DaemonStatus.BLOCKED_BY_GUARDRAIL`.
3. **Order Notional & Slippage Controls**:
   - Enforce `max_order_notional_krw`, minimum order dust threshold, and `max_estimated_slippage_bps`.
4. **Daily Loss & Kill-Switch (`daily_loss_kill_pct`)**:
   - Halt execution (`DaemonStatus.KILLED`) when realized daily PnL breaches the user-configured kill-switch threshold.
5. **Human-in-the-Loop (`interrupt()`)**:
   - Require interactive confirmation (`COMMAND(resume={"approved": True})`) whenever notional exceeds `hitl_threshold_krw` or live mode is enabled.
