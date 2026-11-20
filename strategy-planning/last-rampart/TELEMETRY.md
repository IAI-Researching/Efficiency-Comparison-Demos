# Efficiency Telemetry: strategy-planning/last-rampart

One model, four reasoning-effort levels, three runs per level. Every run counts: a run that fails any check
is published with its tokens, cost and time and scores 0 ("did not ship"). See PROTOCOL.md.

| Model | Run | Harness | Effort | Verification | Waves Held | Round Score | Wall-Clock | Input Tokens | Cached Tokens | Reasoning Tokens | Output Tokens | Code Size | SHA-256 |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Codex GPT 6.2 Sol (Low)** | run-1 | Codex CLI 0.170.0 | `Low` | **PASS** (21/21) | 45.33 | **45.33** | 912.2s | 4,223,701 | 4,122,368 | 5,542 | 38,916 | 47,789 B | `b208a1ebccdb...` |
| **Codex GPT 6.2 Sol (Low)** | run-2 | Codex CLI 0.170.0 | `Low` | **PASS** (21/21) | 42.24 | **42.24** | 786.8s | 2,378,599 | 2,296,320 | 3,667 | 33,233 | 51,673 B | `cc209ecaf38b...` |
| **Codex GPT 6.2 Sol (Medium)** | run-1 | Codex CLI 0.170.0 | `Medium` | **PASS** (21/21) | 45.73 | **45.73** | 1209.4s | 4,193,025 | 4,091,264 | 11,256 | 52,642 | 63,078 B | `5ea9a1b09f00...` |
| **Codex GPT 6.2 Sol (Medium)** | run-2 | Codex CLI 0.170.0 | `Medium` | **FAIL** (20/21) | 45.12 | **0.00** | 975.9s | 2,605,025 | 2,500,096 | 4,980 | 43,555 | 66,131 B | `e12f9045b365...` |
| **Codex GPT 6.2 Sol (High)** | run-1 | Codex CLI 0.170.0 | `High` | **PASS** (21/21) | 43.91 | **43.91** | 1574.4s | 4,788,340 | 4,642,560 | 19,602 | 69,616 | 84,478 B | `30aa75dc28cf...` |
| **Codex GPT 6.2 Sol (High)** | run-2 | Codex CLI 0.170.0 | `High` | **PASS** (21/21) | 45.03 | **45.03** | 1635.0s | 5,870,946 | 5,687,680 | 17,474 | 71,061 | 80,738 B | `ea7e7fba6efb...` |
| **Codex GPT 6.2 Sol (XHigh)** | run-1 | Codex CLI 0.170.0 | `XHigh` | **PASS** (21/21) | 44.99 | **44.99** | 1657.7s | 5,383,479 | 5,227,008 | 15,788 | 73,605 | 79,420 B | `18d0575cd674...` |

- **Waves Held** is the strategy score (mean over five undisclosed seeds), measured even when a shell check failed;
  **Round Score** is the published figure and is 0 for a run that did not ship.
- Token columns are as reported by the harness.
