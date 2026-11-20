# Efficiency Telemetry: strategy-planning/last-rampart

One model, four reasoning-effort levels, three runs per level. Every run counts: a run that fails any check
is published with its tokens, cost and time and scores 0 ("did not ship"). See PROTOCOL.md.

| Model | Run | Harness | Effort | Verification | Waves Held | Round Score | Wall-Clock | Input Tokens | Cached Tokens | Reasoning Tokens | Output Tokens | Code Size | SHA-256 |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Codex GPT 6.2 Sol (Low)** | run-1 | Codex CLI 0.170.0 | `Low` | **PASS** (21/21) | 45.33 | **45.33** | 912.2s | 4,223,701 | 4,122,368 | 5,542 | 38,916 | 47,789 B | `b208a1ebccdb...` |
| **Codex GPT 6.2 Sol (Medium)** | run-1 | Codex CLI 0.170.0 | `Medium` | **PASS** (21/21) | 45.73 | **45.73** | 1209.4s | 4,193,025 | 4,091,264 | 11,256 | 52,642 | 63,078 B | `5ea9a1b09f00...` |
| **Codex GPT 6.2 Sol (High)** | run-1 | Codex CLI 0.170.0 | `High` | **PASS** (21/21) | 43.91 | **43.91** | 1574.4s | 4,788,340 | 4,642,560 | 19,602 | 69,616 | 84,478 B | `30aa75dc28cf...` |

- **Waves Held** is the strategy score (mean over five undisclosed seeds), measured even when a shell check failed;
  **Round Score** is the published figure and is 0 for a run that did not ship.
- Token columns are as reported by the harness.
