# Efficiency Comparison Demos

One model, four reasoning-effort levels, the same prompt: what does more thinking buy, and what does it cost?

| Benchmark | What the model builds | Score |
| :--- | :--- | :--- |
| [`strategy-planning/last-rampart`](strategy-planning/last-rampart/) | A self-playing wave-defense game whose outcome is decided by the model's own strategy code | Mean waves held over five undisclosed seeds |

See [PROTOCOL.md](PROTOCOL.md) for how rounds are run and scored.

## Last Rampart layout

| File | Role |
| :--- | :--- |
| `prompt.md` | The prompt every run receives |
| `reference/engine.js` | Reference rules engine (integer-only, deterministic); the grader scores strategies with it |
| `reference/baselines.js`, `reference/calibrate.html` | Baseline strategies and the search used to tune difficulty |
| `score.py` | Rules-conformance check and strategy score (headless Chrome) |

**Calibration (2026-11-19, five seeds):** bolt-only spam 24.9 waves, a fixed mixed build 27.6, the same with smarter targeting 29.6, a search-tuned build order 40.2. The replay shows 100 s (49.5 waves).

## Running a round

Runs are launched by the local-only orchestrator (`baseline/`, git-ignored, adapted from Performance-Comparison-Demos): one run slot at a time across the four effort levels, e.g. `python3 baseline/run_benchmark.py strategy-planning/last-rampart --run 1 --models codex-gpt-6.2-sol-low codex-gpt-6.2-sol-medium codex-gpt-6.2-sol-high codex-gpt-6.2-sol-xhigh`. Each run is written to `<model-key>/run-<N>/` with its deliverable, `metrics.json` and `report.md`; the benchmark's `telemetry.json` and `TELEMETRY.md` collect every run. The runner refuses to mix harness versions within a benchmark.
