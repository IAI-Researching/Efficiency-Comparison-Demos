# Efficiency Protocol (draft v0.1)

Efficiency-Comparison-Demos measures **what extra reasoning effort buys**: one model, one prompt, four effort levels, and the result read against tokens, cost and time. It shares the isolation setup of [Performance-Comparison-Demos](../Performance-Comparison-Demos/PROTOCOL.md) (protocol v1.1: Seatbelt sandbox, clean login-only home, no web tools, one run at a time), with the differences below.

## What a round is

- **One model, one harness, one harness version.** Four effort levels: `low`, `medium`, `high`, `xhigh`. Only the effort flag changes between runs; the prompt is byte-identical, and the model is never told its effort level.
- **Three runs per effort level** (12 runs in all), executed one at a time, with levels interleaved (`low, medium, high, xhigh`, then repeat) so that slow drift in the provider's service does not line up with one level.
- **The video shows each level's median run** by strategy score. All 12 runs are published.

## Results are scores, not just pass/fail

Each benchmark has a **graded score** with no fixed ceiling, so extra effort has room to show. For Last Rampart it is the mean number of waves held over five undisclosed seeds (see the benchmark's `prompt.md`). The pass/fail shell checks still run and are recorded.

## Attempt policy: every run counts (differs from Performance-Comparison-Demos)

In Performance-Comparison-Demos a failed attempt is archived and re-run. Here a run that fails its checks is **a result, not a retry**: shipping a broken deliverable at low effort is exactly what this repo measures. A failed run is published with its tokens, cost and time, scored `0`, and shown as "did not ship".

Only launches the agent did not end itself are retried (revoked login, sandbox or orchestrator fault, an overlapping job), and each is listed in `attempt_notes` and archived outside the repository, as in Performance-Comparison-Demos.

## Efficiency figures

Per run: total tokens (uncached input, cache reads, cache writes, output), API-equivalent cost from the official list price on the day of the round (`Media/scripts/pricing.json`), wall-clock time, and the score. Per level: the median of each. The headline figure is **score per dollar** and the score-versus-cost curve across the four levels.

## Secret seeds

Scoring seeds live in the git-ignored `baseline/secret_seeds.json`. Every model on a benchmark is graded on the same seeds, so they stay undisclosed until the **last planned round on that benchmark** is graded, and are then published with its results (decided 2026-11-20). Until then, anyone can re-run the published strategies against the reference engine on their own seeds.

## Grader changes

- **2026-11-20, Last Rampart, during the Sol round.** The rules-conformance check compared the model's `score` exactly. The prompt says "rounded to 2 decimals" without naming a method, and `Math.round(x * 100) / 100` and `Number(x.toFixed(2))` give results 0.01 apart when the exact value ends in 5 at the third decimal (45.925 gives 45.93 or 45.92). The check now requires the fall tick and log hash to match exactly and allows the score to differ by at most 0.01. All 12 Sol runs were re-graded with the fixed grader (`baseline/regrade.py`, recorded under `regrades` in each `metrics.json`); one result changed: Sol high run 3, from "did not ship" to 45.61 waves held (its fall tick and hash had matched).
- **2026-11-20, Last Rampart, during the Neon round.** Three Neon runs failed rules conformance with simulators that follow the rules correctly. The cause was the view handed to the strategy: the prompt lists `EnemyView.slowed` without a type, and says "All quantities are integers", but the reference passed `true`/`false`. Neon's simulators pass `1`/`0` or the remaining slow ticks, and Neon's strategies test `slowed === 0`, so the same strategy made different choices in the reference than in the model's own simulator. That broke the conformance check, and it also skewed the strategy score.

  An audit then played one fixed probe game, whose choices never depend on the view, through all 19 simulators of both rounds. It compared every field of every `plan()` and `target()` call against the reference. Two fields differ in ways the prompt allows:
  - `slowed`, as above.
  - `state.slots[].x/y`: three Sol simulators give tile numbers, the reference gives centi-tiles.

  Every other field matched in all 19.

  `score.py` now detects which reading the model's own simulator uses and gives the strategy that same view in the reference, for both the conformance check and the strategy score. A strategy is therefore always graded with the view its author wrote it for. The prompt is unchanged, so every model still gets byte-identical text. The model never sees the grader, so no run needed repeating.

  All 19 runs were re-graded:
  - The 12 Sol results are unchanged.
  - Neon low run 2, medium run 1 and high run 2 went from "did not ship" to 38.18, 45.01 and 45.56 waves held.
  - Neon medium run 2 went from 45.69 to 45.65, now scored with its own reading.

  `audit_views.py` in the benchmark folder repeats the audit for any deliverable. Every future conformance failure is checked with it before it is counted as the model's fault.
