# STLC Token Usage

Source: `C:\Users\DipakMandlik\.claude\projects\C--Users-DipakMandlik-Desktop-AgenticAI-Final-implementation-AgenticAI-master-stlc`

## Per Phase

| Phase | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |
|---|---|---|---|---|---|---|---|
| orchestrator | 1,329 | 543,019 | 4,451,278 | 65,610,503 | 70,606,129 | 896 | 27 |
| automation-generation | 284 | 357,477 | 1,003,800 | 5,379,230 | 6,740,791 | 127 | 10 |
| execution | 334 | 105,884 | 422,302 | 4,529,001 | 5,057,521 | 157 | 10 |
| automation-review | 92 | 94,536 | 364,290 | 2,653,244 | 3,112,162 | 80 | 5 |
| repository-discovery | 604 | 48,963 | 357,647 | 1,527,378 | 1,934,592 | 99 | 5 |
| manual-test-generation | 59 | 178,492 | 456,846 | 1,164,502 | 1,799,899 | 44 | 5 |
| reporting | 188 | 52,582 | 540,875 | 1,103,651 | 1,697,296 | 31 | 4 |
| other | 163 | 27,719 | 191,286 | 1,229,512 | 1,448,680 | 49 | 3 |
| test-review | 43 | 108,286 | 442,858 | 497,065 | 1,048,252 | 30 | 6 |
| self-healing | 60 | 17,271 | 120,597 | 721,723 | 859,651 | 30 | 3 |
| requirement-analysis | 48 | 34,902 | 143,170 | 206,466 | 384,586 | 33 | 7 |
| test-plan | 28 | 70,985 | 126,748 | 142,506 | 340,267 | 18 | 5 |
| impact-analysis | 76 | 32,514 | 153,066 | 101,414 | 287,070 | 16 | 5 |
| **TOTAL** | **3,308** | **1,672,630** | **8,774,763** | **84,866,195** | **95,316,896** | **1610** | **95** |

## Per Agent

| Agent | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |
|---|---|---|---|---|---|---|---|
| main-session (orchestrator) | 894 | 369,177 | 3,493,644 | 56,590,875 | 60,454,590 | 594 | 12 |
| stlc-orchestrator | 435 | 173,842 | 957,634 | 9,019,628 | 10,151,539 | 302 | 15 |
| automation-generation-agent | 119 | 337,361 | 702,702 | 5,019,988 | 6,060,170 | 97 | 5 |
| execution-agent | 262 | 76,168 | 260,354 | 4,117,752 | 4,454,536 | 131 | 5 |
| automation-review-agent | 92 | 94,536 | 364,290 | 2,653,244 | 3,112,162 | 80 | 5 |
| repository-discovery-agent | 604 | 48,963 | 357,647 | 1,527,378 | 1,934,592 | 99 | 5 |
| manual-test-generation-agent | 59 | 178,492 | 456,846 | 1,164,502 | 1,799,899 | 44 | 5 |
| reporting-agent | 188 | 52,582 | 540,875 | 1,103,651 | 1,697,296 | 31 | 4 |
| test-review-agent | 43 | 108,286 | 442,858 | 497,065 | 1,048,252 | 30 | 6 |
| general-purpose | 33 | 17,045 | 85,401 | 907,942 | 1,010,421 | 27 | 1 |
| self-healing-agent | 60 | 17,271 | 120,597 | 721,723 | 859,651 | 30 | 3 |
| framework-selection-agent | 165 | 20,116 | 301,098 | 359,242 | 680,621 | 30 | 5 |
| failure-analysis-agent | 40 | 22,086 | 109,954 | 322,627 | 454,707 | 20 | 4 |
| pr-generation-agent | 130 | 10,674 | 105,885 | 321,570 | 438,259 | 22 | 2 |
| requirement-analysis-agent | 48 | 34,902 | 143,170 | 206,466 | 384,586 | 33 | 7 |
| test-planning-agent | 28 | 70,985 | 126,748 | 142,506 | 340,267 | 18 | 5 |
| impact-analysis-agent | 76 | 32,514 | 153,066 | 101,414 | 287,070 | 16 | 5 |
| defect-analysis-agent | 32 | 7,630 | 51,994 | 88,622 | 148,278 | 6 | 1 |
| **TOTAL** | **3,308** | **1,672,630** | **8,774,763** | **84,866,195** | **95,316,896** | **1610** | **95** |
