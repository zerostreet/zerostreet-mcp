---
name: macro-crisis-sim
description: Historical stress-replay simulator covering 2020 COVID, 2022 Rate Shock, and 2024 Yen Carry unwind scenarios via AlphaSmith /v1/eval/crisis. Quantitative stress metrics only.
license: MIT
---

# Macro Crisis Simulation

## When to Use
Use this skill to stress-test proposed portfolio weights (`positions_weights`, including cash buffer) against historical shock regimes via `evaluate_crisis_replay` / `POST /v1/eval/crisis`.

## Supported Historical Regimes
- `2020_COVID`: Pandemic liquidity crunch shock path.
- `2022_Rate_Shock`: Sustained tightening drawdown regime.
- `2024_Yen_Carry`: Abrupt global deleveraging tail shock.

## Evaluation Protocol
1. Confirm `positions_weights` sums cleanly with explicit `CASH` buffer allocation so `risky_exposure` is unambiguous.
2. Execute `run_crisis_replay` against AlphaSmith `/v1/eval/crisis` (or offline scenario harness during sandbox testing).
3. Verify each scenario's:
   - `cumulative_return_pct`
   - `max_drawdown_pct` (must remain `>= max_drawdown_limit_pct`, default `-25.0%`)
   - `cvar_15_pct` (tail 15% conditional value at risk)
   - `passed_stress_gate` boolean
4. **No Predictive Advice**: Frame stress outputs as historical sensitivity accounting ("under the 2024 Yen Carry path, risky exposure of X% yields Y% MDD"), never as market timing advice.
