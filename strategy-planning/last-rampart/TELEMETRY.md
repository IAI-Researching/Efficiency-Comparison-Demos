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
| **Codex GPT 6.2 Astra (Low)** | run-1 | Codex CLI 0.172.0 | `Low` | **PASS** (21/21) | 43.13 | **43.13** | 602.2s | 1,190,884 | 1,157,888 | 1,648 | 24,508 | 39,478 B | `248eb3560325...` |
| **Codex GPT 6.2 Astra (Low)** | run-2 | Codex CLI 0.172.0 | `Low` | **FAIL** (20/21) | 43.38 | **0.00** | 675.3s | 1,621,051 | 1,593,344 | 2,109 | 26,248 | 38,017 B | `ba3c71b36d2e...` |
| **Codex GPT 6.2 Astra (Low)** | run-3 | Codex CLI 0.172.0 | `Low` | **PASS** (21/21) | 41.82 | **41.82** | 678.5s | 1,414,416 | 1,391,744 | 1,051 | 23,885 | 34,851 B | `12bd4bf06c4a...` |
| **Codex GPT 6.2 Astra (Medium)** | run-1 | Codex CLI 0.172.0 | `Medium` | **PASS** (21/21) | 44.99 | **44.99** | 970.6s | 3,223,803 | 3,179,008 | 4,920 | 36,066 | 44,849 B | `2f219e59317d...` |
| **Codex GPT 6.2 Astra (Medium)** | run-2 | Codex CLI 0.172.0 | `Medium` | **PASS** (21/21) | 42.75 | **42.75** | 875.2s | 2,876,471 | 2,834,688 | 5,742 | 32,023 | 45,230 B | `44f7f945e2c9...` |
| **Codex GPT 6.2 Astra (Medium)** | run-3 | Codex CLI 0.172.0 | `Medium` | **FAIL** (20/21) | 47.46 | **0.00** | 1156.1s | 2,751,029 | 2,713,728 | 6,636 | 39,811 | 48,575 B | `d55327f57c69...` |
| **Codex GPT 6.2 Astra (High)** | run-1 | Codex CLI 0.172.0 | `High` | **PASS** (21/21) | 45.85 | **45.85** | 1662.7s | 5,878,369 | 5,822,848 | 14,865 | 56,559 | 67,324 B | `fdbdb7287de8...` |
| **Codex GPT 6.2 Astra (High)** | run-2 | Codex CLI 0.172.0 | `High` | **FAIL** (20/21) | 45.27 | **0.00** | 1652.7s | 5,401,578 | 5,351,680 | 15,437 | 65,427 | 69,920 B | `466424e98ade...` |
| **Codex GPT 6.2 Astra (High)** | run-3 | Codex CLI 0.172.0 | `High` | **PASS** (21/21) | 46.94 | **46.94** | 2777.8s | 4,642,766 | 4,594,560 | 15,429 | 56,632 | 66,566 B | `a480128e903b...` |
| **Codex GPT 6.2 Astra (XHigh)** | run-1 | Codex CLI 0.172.0 | `XHigh` | **PASS** (21/21) | 47.27 | **47.27** | 1570.9s | 4,973,880 | 4,928,640 | 17,684 | 62,023 | 76,497 B | `73ffd2fcbbcd...` |
| **Codex GPT 6.2 Astra (XHigh)** | run-2 | Codex CLI 0.172.0 | `XHigh` | **PASS** (21/21) | 45.59 | **45.59** | 1479.2s | 3,579,011 | 3,530,624 | 14,370 | 53,556 | 72,590 B | `57485b69a23f...` |
| **Codex GPT 6.2 Astra (XHigh)** | run-3 | Codex CLI 0.172.0 | `XHigh` | **PASS** (21/21) | 45.69 | **45.69** | 1704.2s | 3,654,945 | 3,615,104 | 16,733 | 56,031 | 71,700 B | `036f82fd28e3...` |
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
| **Kimi Code K3.1 Pro (Low)** | run-1 | Kimi Code 2.7.3 | `Low` | **FAIL** (18/21) | 31.22 | **0.00** | 1103.0s | 69,004 | 2,396,499 | 0 | 32,380 | 44,073 B | `9a6e96b1c0ef...` |
| **Kimi Code K3.1 Pro (Low)** | run-2 | Kimi Code 2.7.3 | `Low` | **FAIL** (19/21) | 37.33 | **0.00** | 1049.4s | 80,437 | 4,758,784 | 0 | 44,716 | 46,424 B | `f2239bad8ef5...` |
| **Kimi Code K3.1 Pro (High)** | run-1 | Kimi Code 2.7.3 | `High` | **FAIL** (19/21) | 32.80 | **0.00** | 2995.4s | 151,916 | 9,169,676 | 0 | 84,284 | 63,762 B | `7b5db041dcee...` |
| **Kimi Code K3.1 Pro (High)** | run-2 | Kimi Code 2.7.3 | `High` | **FAIL** (20/21) | 40.55 | **0.00** | 2898.9s | 132,983 | 7,226,112 | 0 | 85,466 | 64,412 B | `4d992bd40cbc...` |
| **Kimi Code K3.1 Pro (Max)** | run-1 | Kimi Code 2.7.3 | `Max` | **PASS** (21/21) | 31.36 | **31.36** | 4183.1s | 168,486 | 9,667,927 | 0 | 112,875 | 55,459 B | `3deb90c16e2f...` |
| **Kimi Code K3.1 Pro (Max)** | run-2 | Kimi Code 2.7.3 | `Max` | **PASS** (21/21) | 43.72 | **43.72** | 3254.0s | 199,118 | 12,820,274 | 0 | 110,996 | 73,991 B | `b7ecb7740ea9...` |
| **DeepSeek v4.1 Flash (Off)** | run-1 | DeepSeek CLI 0.2.2-rc.5 | `Off` | **FAIL** (17/21) | 37.05 | **0.00** | 3350.9s | 239,677 | 130,138,752 | 0 | 319,375 | 104,581 B | `e55447f89b61...` |
| **DeepSeek v4.1 Flash (Off)** | run-2 | DeepSeek CLI 0.2.2-rc.5 | `Off` | **FAIL** (18/21) | 36.48 | **0.00** | 9445.6s | 1,349,063 | 512,633,600 | 0 | 511,151 | 134,743 B | `8ab3f7060d4c...` |
| **DeepSeek v4.1 Flash (Low)** | run-1 | DeepSeek CLI 0.2.2-rc.5 | `Low` | **PASS** (21/21) | 44.78 | **44.78** | 2251.7s | 135,505 | 37,578,496 | 0 | 236,569 | 109,308 B | `1cb008313144...` |
| **DeepSeek v4.1 Flash (Low)** | run-2 | DeepSeek CLI 0.2.2-rc.5 | `Low` | **PASS** (21/21) | 43.69 | **43.69** | 2622.2s | 127,152 | 48,361,728 | 0 | 315,364 | 111,330 B | `b11ee4f8a213...` |
| **DeepSeek v4.1 Flash (High)** | run-1 | DeepSeek CLI 0.2.2-rc.5 | `High` | **PASS** (21/21) | 45.65 | **45.65** | 3308.0s | 160,895 | 64,923,392 | 0 | 289,943 | 104,075 B | `eb62f404bca0...` |
| **DeepSeek v4.1 Flash (High)** | run-2 | DeepSeek CLI 0.2.2-rc.5 | `High` | **PASS** (21/21) | 43.89 | **43.89** | 2630.7s | 101,202 | 45,787,904 | 0 | 287,725 | 108,780 B | `612eb7908e1f...` |
| **DeepSeek v4.1 Flash (Max)** | run-1 | DeepSeek CLI 0.2.2-rc.5 | `Max` | **PASS** (21/21) | 45.17 | **45.17** | 3370.6s | 117,229 | 39,866,624 | 0 | 341,560 | 153,361 B | `6e9790ccd50f...` |
| **DeepSeek v4.1 Flash (Max)** | run-2 | DeepSeek CLI 0.2.2-rc.5 | `Max` | **PASS** (21/21) | 44.36 | **44.36** | 3709.2s | 240,441 | 74,743,808 | 0 | 390,258 | 127,418 B | `e19ae869c858...` |
| **Gemini 4 Hydrogen (Low)** | run-1 | Antigravity CLI 1.5.14 | `Low` | **PASS** (21/21) | 24.04 | **24.04** | 308.4s | 112,205 | 568,969 | 5,893 | 70,758 | 56,456 B | `02667d1feab5...` |
| **Gemini 4 Hydrogen (Low)** | run-2 | Antigravity CLI 1.5.14 | `Low` | **FAIL** (19/21) | 24.97 | **0.00** | 176.4s | 50,014 | 56,116 | 4,396 | 25,836 | 54,311 B | `15736f89045b...` |
| **Gemini 4 Hydrogen (Low)** | run-3 | Antigravity CLI 1.5.14 | `Low` | **PASS** (21/21) | 23.33 | **23.33** | 234.1s | 82,621 | 207,222 | 5,884 | 56,141 | 51,128 B | `549146235c6d...` |
| **Gemini 4 Hydrogen (Medium)** | run-1 | Antigravity CLI 1.5.14 | `Medium` | **PASS** (21/21) | 36.14 | **36.14** | 351.9s | 128,809 | 619,333 | 10,966 | 88,495 | 75,053 B | `2ff67b964c80...` |
| **Gemini 4 Hydrogen (Medium)** | run-2 | Antigravity CLI 1.5.14 | `Medium` | **PASS** (21/21) | 37.82 | **37.82** | 509.6s | 169,331 | 1,351,713 | 12,772 | 107,858 | 78,580 B | `17acb69b67c1...` |
| **Gemini 4 Hydrogen (Medium)** | run-3 | Antigravity CLI 1.5.14 | `Medium` | **PASS** (21/21) | 33.07 | **33.07** | 543.7s | 168,031 | 897,787 | 11,172 | 125,237 | 93,532 B | `2ceaf9f40574...` |
| **Gemini 4 Hydrogen (High)** | run-1 | Antigravity CLI 1.5.14 | `High` | **FAIL** (14/21) | 40.58 | **0.00** | 614.5s | 207,241 | 2,488,040 | 26,483 | 141,133 | 104,373 B | `78c607bcf859...` |
| **Gemini 4 Hydrogen (High)** | run-2 | Antigravity CLI 1.5.14 | `High` | **PASS** (21/21) | 43.91 | **43.91** | 594.2s | 178,047 | 1,826,286 | 23,111 | 120,893 | 101,446 B | `2ccee20d8a84...` |
| **Gemini 4 Hydrogen (High)** | run-3 | Antigravity CLI 1.5.14 | `High` | **PASS** (21/21) | 42.31 | **42.31** | 521.5s | 140,107 | 1,171,973 | 23,512 | 98,719 | 101,516 B | `0f81cc3cf07b...` |
| **Gemini 4 Hydrogen (XHigh)** | run-1 | Antigravity CLI 1.5.14 | `XHigh` | **PASS** (21/21) | 45.45 | **45.45** | 29778.3s | 585,087 | 8,406,026 | 51,325 | 215,296 | 105,300 B | `7b7015e1c06c...` |
| **Gemini 4 Hydrogen (XHigh)** | run-2 | Antigravity CLI 1.5.14 | `XHigh` | **PASS** (21/21) | 44.01 | **44.01** | 1402.7s | 377,961 | 9,285,164 | 78,224 | 274,316 | 115,074 B | `ed8fa7cfb1be...` |
| **Gemini 4 Hydrogen (XHigh)** | run-3 | Antigravity CLI 1.5.14 | `XHigh` | **FAIL** (20/21) | 46.00 | **0.00** | 1437.1s | 412,038 | 9,669,156 | 63,449 | 296,840 | 104,171 B | `a6310579d179...` |
| **Gemini 4 Carbon (Low)** | run-1 | Antigravity CLI 1.5.18 | `Low` | **PASS** (21/21) | 41.51 | **41.51** | 3976.4s | 413,115 | 4,632,952 | 0 | 215,629 | 126,373 B | `774523d71180...` |
| **Claude Opus 5.5 (Low)** | run-1 | Claude Code 2.1.330 | `Low` | **PASS** (21/21) | 35.95 | **35.95** | 542.5s | 38 | 1,050,941 | 13,717 | 61,054 | 65,536 B | `fb4e37eef443...` |
| **Claude Opus 5.5 (Low)** | run-2 | Claude Code 2.1.330 | `Low` | **PASS** (21/21) | 42.93 | **42.93** | 694.1s | 54 | 1,639,937 | 15,487 | 65,921 | 67,178 B | `4b3ae275743d...` |
| **Claude Opus 5.5 (Low)** | run-3 | Claude Code 2.1.330 | `Low` | **PASS** (21/21) | 41.29 | **41.29** | 694.0s | 40 | 1,160,743 | 12,974 | 63,470 | 65,316 B | `d1ba05f38cd2...` |
| **Claude Opus 5.5 (Medium)** | run-1 | Claude Code 2.1.330 | `Medium` | **PASS** (21/21) | 45.55 | **45.55** | 2086.3s | 124 | 7,620,170 | 41,444 | 122,401 | 83,383 B | `ade14523e8cc...` |
| **Claude Opus 5.5 (Medium)** | run-2 | Claude Code 2.1.330 | `Medium` | **PASS** (21/21) | 44.70 | **44.70** | 1601.0s | 138 | 9,198,849 | 43,249 | 121,804 | 79,777 B | `caff5243a6ff...` |
| **Claude Opus 5.5 (Medium)** | run-3 | Claude Code 2.1.330 | `Medium` | **PASS** (21/21) | 45.02 | **45.02** | 2269.0s | 160 | 9,228,063 | 30,978 | 103,030 | 80,764 B | `c18172e6f59f...` |
| **Claude Opus 5.5 (High)** | run-1 | Claude Code 2.1.330 | `High` | **PASS** (21/21) | 46.65 | **46.65** | 2268.2s | 162 | 12,583,694 | 68,644 | 161,306 | 87,434 B | `bd9cee6fc1b3...` |
| **Claude Opus 5.5 (High)** | run-2 | Claude Code 2.1.330 | `High` | **PASS** (21/21) | 47.09 | **47.09** | 2932.0s | 222 | 22,001,135 | 90,267 | 202,973 | 105,062 B | `38c9c4cc6736...` |
| **Claude Opus 5.5 (High)** | run-3 | Claude Code 2.1.330 | `High` | **PASS** (21/21) | 46.06 | **46.06** | 1719.3s | 160 | 11,125,173 | 50,306 | 138,499 | 97,653 B | `461868d5aeb4...` |
| **Claude Opus 5.5 (XHigh)** | run-1 | Claude Code 2.1.330 | `XHigh` | **PASS** (21/21) | 45.92 | **45.92** | 2634.4s | 162 | 15,616,786 | 107,442 | 227,842 | 104,845 B | `f47c9c0317d1...` |
| **Claude Opus 5.5 (XHigh)** | run-2 | Claude Code 2.1.330 | `XHigh` | **PASS** (21/21) | 46.93 | **46.93** | 2961.7s | 216 | 22,759,705 | 151,530 | 276,890 | 110,240 B | `cc1818ebfc75...` |
| **Claude Opus 5.5 (XHigh)** | run-3 | Claude Code 2.1.330 | `XHigh` | **PASS** (21/21) | 47.22 | **47.22** | 3457.2s | 232 | 27,094,511 | 138,763 | 279,691 | 119,339 B | `eb425d92838e...` |
| **Claude Sonnet 5.5 (Low)** | run-1 | Claude Code 2.1.330 | `Low` | **PASS** (21/21) | 38.44 | **38.44** | 650.6s | 30 | 948,605 | 22,912 | 66,457 | 51,318 B | `729db49c5b4a...` |
| **Claude Sonnet 5.5 (Low)** | run-2 | Claude Code 2.1.330 | `Low` | **PASS** (21/21) | 33.47 | **33.47** | 758.5s | 48 | 2,154,157 | 39,542 | 90,089 | 64,296 B | `e4e02970acf4...` |
| **Claude Sonnet 5.5 (Low)** | run-3 | Claude Code 2.1.330 | `Low` | **FAIL** (19/21) | 29.20 | **0.00** | 583.7s | 58 | 1,877,770 | 27,773 | 71,812 | 57,023 B | `c935619f8f7f...` |
| **Claude Sonnet 5.5 (Medium)** | run-1 | Claude Code 2.1.330 | `Medium` | **PASS** (21/21) | 42.83 | **42.83** | 1319.6s | 134 | 9,009,016 | 61,680 | 135,242 | 77,445 B | `17368b6a7fbd...` |
| **Claude Sonnet 5.5 (Medium)** | run-2 | Claude Code 2.1.330 | `Medium` | **PASS** (21/21) | 45.28 | **45.28** | 1011.6s | 56 | 2,886,634 | 49,997 | 119,223 | 73,377 B | `c5425eabe3ad...` |
| **Claude Sonnet 5.5 (Medium)** | run-3 | Claude Code 2.1.330 | `Medium` | **PASS** (21/21) | 41.16 | **41.16** | 1525.2s | 78 | 4,270,582 | 46,265 | 121,097 | 82,353 B | `46b04757791d...` |
| **Claude Sonnet 5.5 (High)** | run-1 | Claude Code 2.1.330 | `High` | **PASS** (21/21) | 45.54 | **45.54** | 5863.7s | 220 | 21,555,702 | 96,703 | 196,883 | 96,280 B | `906a12f7a86d...` |
| **Claude Sonnet 5.5 (High)** | run-2 | Claude Code 2.1.330 | `High` | **PASS** (21/21) | 44.66 | **44.66** | 4355.2s | 138 | 10,811,751 | 71,760 | 152,564 | 91,754 B | `bc933a94a48f...` |
| **Claude Sonnet 5.5 (High)** | run-3 | Claude Code 2.1.330 | `High` | **PASS** (21/21) | 45.84 | **45.84** | 2383.3s | 152 | 14,294,699 | 104,663 | 203,718 | 100,296 B | `1ca22a07c9b2...` |
| **Claude Sonnet 5.5 (XHigh)** | run-1 | Claude Code 2.1.330 | `XHigh` | **PASS** (21/21) | 46.26 | **46.26** | 5362.1s | 298 | 44,615,064 | 196,603 | 350,676 | 108,323 B | `33088a2b36d7...` |
| **Claude Sonnet 5.5 (XHigh)** | run-2 | Claude Code 2.1.330 | `XHigh` | **PASS** (21/21) | 46.48 | **46.48** | 6226.8s | 292 | 45,607,910 | 204,183 | 355,282 | 105,150 B | `0ec7b6166e4a...` |
| **Claude Sonnet 5.5 (XHigh)** | run-3 | Claude Code 2.1.330 | `XHigh` | **FAIL** (19/21) | 46.77 | **0.00** | 4276.9s | 254 | 34,255,170 | 207,386 | 334,220 | 112,095 B | `79dd34014fa9...` |
| **Claude Fable 5.2 (Low)** | run-1 | Claude Code 2.1.330 | `Low` | **PASS** (21/21) | 46.04 | **46.04** | 1757.0s | 82 | 5,518,848 | 54,683 | 133,953 | 76,758 B | `be5639e970e0...` |
| **Claude Fable 5.2 (Low)** | run-2 | Claude Code 2.1.330 | `Low` | **PASS** (21/21) | 47.00 | **47.00** | 3064.7s | 118 | 9,167,911 | 58,776 | 150,276 | 83,880 B | `c0f82aa8b56f...` |
| **Claude Fable 5.2 (Low)** | run-3 | Claude Code 2.1.330 | `Low` | **PASS** (21/21) | 44.61 | **44.61** | 1616.7s | 46 | 2,226,575 | 45,114 | 119,899 | 76,727 B | `d6407ba58779...` |
| **Claude Fable 5.2 (Medium)** | run-1 | Claude Code 2.1.330 | `Medium` | **PASS** (21/21) | 46.80 | **46.80** | 2762.3s | 100 | 7,132,471 | 59,879 | 139,184 | 83,972 B | `bf0993d79e35...` |
| **Claude Fable 5.2 (Medium)** | run-2 | Claude Code 2.1.330 | `Medium` | **PASS** (21/21) | 45.02 | **45.02** | 1678.2s | 56 | 2,817,333 | 49,216 | 123,727 | 92,470 B | `70c1ed56bf54...` |
| **Claude Fable 5.2 (Medium)** | run-3 | Claude Code 2.1.330 | `Medium` | **PASS** (21/21) | 47.68 | **47.68** | 2243.7s | 118 | 9,012,353 | 62,933 | 145,773 | 87,175 B | `35eea6e9a1b1...` |
| **Claude Fable 5.2 (High)** | run-1 | Claude Code 2.1.330 | `High` | **PASS** (21/21) | 47.79 | **47.79** | 5213.1s | 218 | 26,510,348 | 123,595 | 254,398 | 105,816 B | `3f3adcf6ed23...` |
| **Claude Fable 5.2 (High)** | run-2 | Claude Code 2.1.330 | `High` | **PASS** (21/21) | 45.83 | **45.83** | 2849.2s | 114 | 10,467,353 | 104,078 | 218,972 | 114,404 B | `3d8866314fe4...` |
| **Claude Fable 5.2 (High)** | run-3 | Claude Code 2.1.330 | `High` | **PASS** (21/21) | 46.87 | **46.87** | 2810.4s | 146 | 14,645,836 | 118,472 | 224,876 | 100,940 B | `c377fae83f0e...` |
| **Claude Fable 5.2 (XHigh)** | run-1 | Claude Code 2.1.330 | `XHigh` | **PASS** (21/21) | 47.64 | **47.64** | 5670.7s | 208 | 35,694,053 | 250,046 | 417,237 | 130,050 B | `15461fcbc90c...` |
| **Claude Fable 5.2 (XHigh)** | run-2 | Claude Code 2.1.330 | `XHigh` | **PASS** (21/21) | 47.89 | **47.89** | 5675.7s | 232 | 39,970,670 | 223,659 | 391,341 | 123,225 B | `03f54551ae5f...` |
| **Claude Fable 5.2 (XHigh)** | run-3 | Claude Code 2.1.330 | `XHigh` | **PASS** (21/21) | 46.96 | **46.96** | 4895.3s | 190 | 31,172,501 | 218,787 | 385,669 | 127,644 B | `9458c4469357...` |

- **Waves Held** is the strategy score (mean over five undisclosed seeds), measured even when a shell check failed;
  **Round Score** is the published figure and is 0 for a run that did not ship.
- Token columns are as reported by the harness.
