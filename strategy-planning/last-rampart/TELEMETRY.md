# Efficiency Telemetry: strategy-planning/last-rampart

One model, four reasoning-effort levels, three runs per level. Every run counts: a run that fails any check
is published with its tokens, cost and time and scores 0 ("did not ship"). See PROTOCOL.md.

| Model | Run | Harness | Effort | Verification | Waves Held | Round Score | Wall-Clock | Input Tokens | Cached Tokens | Reasoning Tokens | Output Tokens | Code Size | SHA-256 |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Codex GPT 6.2 Sol (Low)** | run-1 | Codex CLI 0.170.0 | `Low` | **PASS** (21/21) | 45.33 | **45.33** | 912.2s | 4,223,701 | 4,122,368 | 5,542 | 38,916 | 47,789 B | `b208a1ebccdb...` |
| **Codex GPT 6.2 Sol (Low)** | run-2 | Codex CLI 0.170.0 | `Low` | **PASS** (21/21) | 42.24 | **42.24** | 786.8s | 2,378,599 | 2,296,320 | 3,667 | 33,233 | 51,673 B | `cc209ecaf38b...` |
| **Codex GPT 6.2 Sol (Low)** | run-3 | Codex CLI 0.170.0 | `Low` | **PASS** (21/21) | 43.30 | **43.30** | 923.6s | 2,223,963 | 2,139,904 | 3,338 | 35,357 | 52,718 B | `85b0689342c1...` |
| **Codex GPT 6.2 Sol (Medium)** | run-1 | Codex CLI 0.170.0 | `Medium` | **PASS** (21/21) | 45.73 | **45.73** | 1209.4s | 4,193,025 | 4,091,264 | 11,256 | 52,642 | 63,078 B | `5ea9a1b09f00...` |
| **Codex GPT 6.2 Sol (Medium)** | run-2 | Codex CLI 0.170.0 | `Medium` | **FAIL** (20/21) | 45.12 | **0.00** | 975.9s | 2,605,025 | 2,500,096 | 4,980 | 43,555 | 66,131 B | `e12f9045b365...` |
| **Codex GPT 6.2 Sol (Medium)** | run-3 | Codex CLI 0.170.0 | `Medium` | **PASS** (21/21) | 44.05 | **44.05** | 944.1s | 3,743,342 | 3,617,152 | 5,839 | 41,287 | 60,489 B | `9177b3efe0f8...` |
| **Codex GPT 6.2 Sol (High)** | run-1 | Codex CLI 0.170.0 | `High` | **PASS** (21/21) | 43.91 | **43.91** | 1574.4s | 4,788,340 | 4,642,560 | 19,602 | 69,616 | 84,478 B | `30aa75dc28cf...` |
| **Codex GPT 6.2 Sol (High)** | run-2 | Codex CLI 0.170.0 | `High` | **PASS** (21/21) | 45.03 | **45.03** | 1635.0s | 5,870,946 | 5,687,680 | 17,474 | 71,061 | 80,738 B | `ea7e7fba6efb...` |
| **Codex GPT 6.2 Sol (High)** | run-3 | Codex CLI 0.170.0 | `High` | **PASS** (21/21) | 45.61 | **45.61** | 1817.9s | 7,201,775 | 7,060,096 | 21,843 | 76,803 | 76,297 B | `e7826710a46f...` |
| **Codex GPT 6.2 Sol (XHigh)** | run-1 | Codex CLI 0.170.0 | `XHigh` | **PASS** (21/21) | 44.99 | **44.99** | 1657.7s | 5,383,479 | 5,227,008 | 15,788 | 73,605 | 79,420 B | `18d0575cd674...` |
| **Codex GPT 6.2 Sol (XHigh)** | run-2 | Codex CLI 0.170.0 | `XHigh` | **PASS** (21/21) | 45.47 | **45.47** | 1456.2s | 4,060,575 | 3,901,952 | 14,719 | 64,166 | 80,487 B | `7b77494bbfad...` |
| **Codex GPT 6.2 Sol (XHigh)** | run-3 | Codex CLI 0.170.0 | `XHigh` | **PASS** (21/21) | 41.66 | **41.66** | 1480.5s | 4,597,553 | 4,443,520 | 13,105 | 65,636 | 76,662 B | `e06338c58027...` |
| **Gemini 4 Neon (Low)** | run-1 | Antigravity CLI 1.5.13 | `Low` | **FAIL** (20/21) | 41.05 | **0.00** | 599.3s | 158,566 | 372,373 | 9,566 | 70,877 | 73,751 B | `ea2fe677d4df...` |
| **Gemini 4 Neon (Low)** | run-2 | Antigravity CLI 1.5.13 | `Low` | **PASS** (21/21) | 38.18 | **38.18** | 599.0s | 200,357 | 628,191 | 8,789 | 64,592 | 79,411 B | `df3b1c555a0c...` |
| **Gemini 4 Neon (Low)** | run-3 | Antigravity CLI 1.5.13 | `Low` | **PASS** (21/21) | 42.00 | **42.00** | 424.4s | 85,550 | 333,239 | 8,486 | 58,447 | 82,149 B | `e5345ad64cc6...` |
| **Gemini 4 Neon (Medium)** | run-1 | Antigravity CLI 1.5.13 | `Medium` | **PASS** (21/21) | 45.01 | **45.01** | 1032.1s | 256,929 | 1,636,809 | 18,124 | 110,176 | 107,975 B | `434ae5581ae9...` |
| **Gemini 4 Neon (Medium)** | run-2 | Antigravity CLI 1.5.13 | `Medium` | **PASS** (21/21) | 45.65 | **45.65** | 1032.6s | 266,510 | 1,412,121 | 16,020 | 118,472 | 106,740 B | `3b5fee8509e5...` |
| **Gemini 4 Neon (Medium)** | run-3 | Antigravity CLI 1.5.13 | `Medium` | **PASS** (21/21) | 44.01 | **44.01** | 877.7s | 241,805 | 1,538,458 | 20,566 | 101,829 | 108,655 B | `ce53c12397c9...` |
| **Gemini 4 Neon (High)** | run-1 | Antigravity CLI 1.5.13 | `High` | **PASS** (21/21) | 45.47 | **45.47** | 1838.5s | 290,620 | 3,994,612 | 41,392 | 219,146 | 124,195 B | `333c0a146dea...` |
| **Gemini 4 Neon (High)** | run-2 | Antigravity CLI 1.5.13 | `High` | **FAIL** (20/21) | 45.56 | **0.00** | 2290.8s | 579,569 | 6,894,869 | 56,850 | 264,606 | 122,855 B | `7895cb5384a6...` |
| **Gemini 4 Neon (High)** | run-3 | Antigravity CLI 1.5.13 | `High` | **PASS** (21/21) | 45.14 | **45.14** | 2103.4s | 336,300 | 6,367,207 | 47,722 | 252,337 | 121,228 B | `ef4f453f4dba...` |
| **Gemini 4 Neon (XHigh)** | run-1 | Antigravity CLI 1.5.13 | `XHigh` | **PASS** (21/21) | 47.84 | **47.84** | 2821.6s | 695,317 | 8,338,766 | 77,049 | 311,393 | 140,335 B | `19f871d4b4a3...` |
| **Gemini 4 Neon (XHigh)** | run-2 | Antigravity CLI 1.5.13 | `XHigh` | **PASS** (21/21) | 47.83 | **47.83** | 2450.3s | 379,967 | 10,622,314 | 78,530 | 254,984 | 136,415 B | `78bda6cabbcd...` |
| **Gemini 4 Neon (XHigh)** | run-3 | Antigravity CLI 1.5.13 | `XHigh` | **FAIL** (20/21) | 46.01 | **0.00** | 3154.9s | 537,414 | 15,652,916 | 84,432 | 388,243 | 134,813 B | `929ba90c6d4a...` |
| **DeepSeek v4.1 Flash (Off)** | run-1 | DeepSeek CLI 0.2.2-rc.5 | `Off` | **FAIL** (17/21) | 37.05 | **0.00** | 3350.9s | 239,677 | 130,138,752 | 0 | 319,375 | 104,581 B | `e55447f89b61...` |
| **DeepSeek v4.1 Flash (Off)** | run-2 | DeepSeek CLI 0.2.2-rc.5 | `Off` | **FAIL** (18/21) | 36.48 | **0.00** | 9445.6s | 1,349,063 | 512,633,600 | 0 | 511,151 | 134,743 B | `8ab3f7060d4c...` |
| **DeepSeek v4.1 Flash (Low)** | run-1 | DeepSeek CLI 0.2.2-rc.5 | `Low` | **PASS** (21/21) | 44.78 | **44.78** | 2251.7s | 135,505 | 37,578,496 | 0 | 236,569 | 109,308 B | `1cb008313144...` |
| **DeepSeek v4.1 Flash (Low)** | run-2 | DeepSeek CLI 0.2.2-rc.5 | `Low` | **PASS** (21/21) | 43.69 | **43.69** | 2622.2s | 127,152 | 48,361,728 | 0 | 315,364 | 111,330 B | `b11ee4f8a213...` |
| **DeepSeek v4.1 Flash (High)** | run-1 | DeepSeek CLI 0.2.2-rc.5 | `High` | **PASS** (21/21) | 45.65 | **45.65** | 3308.0s | 160,895 | 64,923,392 | 0 | 289,943 | 104,075 B | `eb62f404bca0...` |
| **DeepSeek v4.1 Flash (High)** | run-2 | DeepSeek CLI 0.2.2-rc.5 | `High` | **PASS** (21/21) | 43.89 | **43.89** | 2630.7s | 101,202 | 45,787,904 | 0 | 287,725 | 108,780 B | `612eb7908e1f...` |
| **DeepSeek v4.1 Flash (Max)** | run-1 | DeepSeek CLI 0.2.2-rc.5 | `Max` | **PASS** (21/21) | 45.17 | **45.17** | 3370.6s | 117,229 | 39,866,624 | 0 | 341,560 | 153,361 B | `6e9790ccd50f...` |
| **DeepSeek v4.1 Flash (Max)** | run-2 | DeepSeek CLI 0.2.2-rc.5 | `Max` | **PASS** (21/21) | 44.36 | **44.36** | 3709.2s | 240,441 | 74,743,808 | 0 | 390,258 | 127,418 B | `e19ae869c858...` |
| **Claude Opus 5.5 (Low)** | run-1 | Claude Code 2.1.330 | `Low` | **PASS** (21/21) | 35.95 | **35.95** | 542.5s | 38 | 1,050,941 | 13,717 | 61,054 | 65,536 B | `fb4e37eef443...` |
| **Claude Opus 5.5 (Low)** | run-2 | Claude Code 2.1.330 | `Low` | **PASS** (21/21) | 42.93 | **42.93** | 694.1s | 54 | 1,639,937 | 15,487 | 65,921 | 67,178 B | `4b3ae275743d...` |
| **Claude Opus 5.5 (Medium)** | run-1 | Claude Code 2.1.330 | `Medium` | **PASS** (21/21) | 45.55 | **45.55** | 2086.3s | 124 | 7,620,170 | 41,444 | 122,401 | 83,383 B | `ade14523e8cc...` |
| **Claude Opus 5.5 (High)** | run-1 | Claude Code 2.1.330 | `High` | **PASS** (21/21) | 46.65 | **46.65** | 2268.2s | 162 | 12,583,694 | 68,644 | 161,306 | 87,434 B | `bd9cee6fc1b3...` |
| **Claude Opus 5.5 (XHigh)** | run-1 | Claude Code 2.1.330 | `XHigh` | **PASS** (21/21) | 45.92 | **45.92** | 2634.4s | 162 | 15,616,786 | 107,442 | 227,842 | 104,845 B | `f47c9c0317d1...` |

- **Waves Held** is the strategy score (mean over five undisclosed seeds), measured even when a shell check failed;
  **Round Score** is the published figure and is 0 for a run that did not ship.
- Token columns are as reported by the harness.
