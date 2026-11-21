---
name: portfolio-risk-audit
description: Technical descriptive analytics and ex-post RunTrace factor attribution auditor (Beta, Factor, Slippage, Residual Alpha, HHI concentration). Strictly descriptive analytics; never issues buy/sell advice.
license: MIT
---

# Portfolio Risk Audit (Descriptive Analytics Only)

## When to Use
Use this skill when analyzing historical execution telemetry (`RunTrace`), factor attribution breakdowns (`AttributionBreakdown`), or concentration risks of an existing portfolio configuration.

## Regulatory Guardrail
- Strictly **Descriptive Analytics Only**: report historical measurements, drawdowns, factor exposures, slippage, and structural imbalances.
- Never issue prescriptive buy/sell suggestions, market direction forecasts, or asset selection advice.

## Audit Workflow
1. **Ex-Post Decomposition (`compute_run_attribution`)**:
   - Inspect `gross_return_bps`, `beta_return_bps`, `factor_return_bps`, `slippage_bps`, and `residual_alpha_bps`.
   - Flag cases where `slippage_bps` consumes more than 25% of positive gross return.
2. **Concentration & Tail Risk Metrics**:
   - Compute Herfindahl-Hirschman Index ($\text{HHI} = \sum w_i^2$) and effective bet count ($1 / \text{HHI}$).
   - Check single-name weights against `UserPolicyConfig.max_single_weight`.
3. **Distribution Drift Check (`DriftDetector`)**:
   - Compare live execution return windows against backtest baseline expectations using the $3\sigma$ standard error test (`|z| >= 3.0 -> DRIFT_ALERT`).
4. **Report Format**:
   - Present factual tables with `run_id`, `policy_checkpoint_id`, and structural observations only.
