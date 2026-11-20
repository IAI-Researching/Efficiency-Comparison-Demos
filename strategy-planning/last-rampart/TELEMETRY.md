# Efficiency Telemetry: strategy-planning/last-rampart

One model, four reasoning-effort levels, three runs per level. Every run counts: a run that fails any check
is published with its tokens, cost and time and scores 0 ("did not ship"). See PROTOCOL.md.

| Model | Run | Harness | Effort | Verification | Waves Held | Round Score | Wall-Clock | Input Tokens | Cached Tokens | Reasoning Tokens | Output Tokens | Code Size | SHA-256 |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Codex GPT 6.2 Sol (Low)** | run-1 | Codex CLI 0.170.0 | `Low` | **PASS** (21/21) | 45.33 | **45.33** | 912.2s | 4,223,701 | 4,122,368 | 5,542 | 38,916 | 47,789 B | `b208a1ebccdb...` |

- **Waves Held** is the strategy score (mean over five undisclosed seeds), measured even when a shell check failed;
  **Round Score** is the published figure and is 0 for a run that did not ship.
- Token columns are as reported by the harness.
