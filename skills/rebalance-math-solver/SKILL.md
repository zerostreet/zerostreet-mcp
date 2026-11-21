---
name: rebalance-math-solver
description: Mathematical solver guide for delta portfolio rebalancing, simplex projection, multi-horizon block masking, and transaction-cost quadratic turnover penalties.
license: MIT
---

# Rebalance Math Solver

## When to Use
Use this skill when translating target weights and multi-horizon policy plans into integer share deltas, verifying simplex constraints, or tuning `quadratic_turnover_coeff` in `RLRewardWeights`.

## Mathematical Formulations
1. **Simplex & Single-Name Capping**:
   - Policy heads (`entmax15`, `sparsemax`, `softmax`) output non-negative simplex weights $\sum_i w_i = 1$.
   - Clipped weights with `max_single_weight` $u < 1$ redistribute excess weight into `CASH` or uncapped positions while preserving $\sum_i w_i = 1.0$.
2. **Delta Order Quantity Calculation**:
   - Given total equity $E$, current shares $q_i^{\text{cur}}$, current price $p_i$, and target weight $w_i^*$:
     $$\Delta n_i = \text{trunc}\left(\frac{w_i^* E}{p_i}\right) - q_i^{\text{cur}}$$
   - Drop orders whose notional $|\Delta n_i| p_i$ falls below minimum lot/dust thresholds to minimize fixed fee drag.
3. **Quadratic Turnover Penalty (`DifferentiableTrajectoryRLTrainer`)**:
   - Transaction friction is modeled end-to-end across trajectory horizon $H$ via:
     $$\mathcal{L}_{\text{turnover}} = \lambda_{\text{quad}} \cdot \mathbb{E}\left[\frac{1}{H}\sum_{t=1}^{H} \left\|w_t - w_{t-1}\right\|_2^2\right]$$
   - Selecting sparse activations (`entmax15` / `sparsemax`) plus non-zero `quadratic_turnover_coeff` naturally suppresses whip-saw rebalancing without arbitrary ad-hoc heuristics.
4. **Horizon Mask Modes (`HorizonMaskMode`)**:
   - `bidirectional_portfolio`: simultaneous multi-horizon weight coherence across horizon blocks.
   - `causal_portfolio` / `backward_dp`: temporal causality across rebalancing steps.
