# STLC Token Usage

Source: `C:\Users\DipakMandlik\.claude\projects\C--Users-DipakMandlik-Desktop-AgenticAI-Final-implementation-AgenticAI-master-stlc`

## Per Phase

| Phase | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |
|---|---|---|---|---|---|---|---|
| orchestrator | 835 | 374,220 | 3,307,143 | 37,908,078 | 41,590,276 | 551 | 18 |
| automation-generation | 181 | 184,337 | 710,948 | 3,097,255 | 3,992,721 | 79 | 6 |
| execution | 250 | 84,317 | 329,241 | 3,019,722 | 3,433,530 | 115 | 8 |
| automation-review | 82 | 65,037 | 278,210 | 2,445,211 | 2,788,540 | 72 | 4 |
| manual-test-generation | 43 | 127,304 | 324,694 | 877,306 | 1,329,347 | 32 | 3 |
| other | 76 | 21,172 | 171,471 | 975,395 | 1,168,114 | 34 | 2 |
| repository-discovery | 286 | 28,203 | 208,420 | 698,767 | 935,676 | 45 | 3 |
| reporting | 109 | 32,142 | 385,516 | 492,152 | 909,919 | 19 | 3 |
| self-healing | 60 | 17,271 | 120,597 | 721,723 | 859,651 | 30 | 3 |
| test-review | 32 | 76,505 | 292,126 | 432,243 | 800,906 | 23 | 4 |
| requirement-analysis | 28 | 22,961 | 94,011 | 98,563 | 215,563 | 18 | 4 |
| test-plan | 19 | 39,172 | 73,716 | 98,519 | 211,426 | 12 | 3 |
| impact-analysis | 47 | 19,684 | 77,089 | 89,274 | 186,094 | 10 | 3 |
| **TOTAL** | **2,048** | **1,092,325** | **6,373,182** | **50,954,208** | **58,421,763** | **1040** | **64** |

## Per Agent

| Agent | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |
|---|---|---|---|---|---|---|---|
| main-session (orchestrator) | 553 | 254,568 | 2,653,643 | 32,222,321 | 35,131,085 | 364 | 9 |
| stlc-orchestrator | 282 | 119,652 | 653,500 | 5,685,757 | 6,459,191 | 187 | 9 |
| automation-generation-agent | 73 | 172,269 | 503,666 | 2,874,925 | 3,550,933 | 59 | 3 |
| execution-agent | 188 | 58,722 | 204,364 | 2,692,432 | 2,955,706 | 94 | 4 |
| automation-review-agent | 82 | 65,037 | 278,210 | 2,445,211 | 2,788,540 | 72 | 4 |
| manual-test-generation-agent | 43 | 127,304 | 324,694 | 877,306 | 1,329,347 | 32 | 3 |
| general-purpose | 33 | 17,045 | 85,401 | 907,942 | 1,010,421 | 27 | 1 |
| repository-discovery-agent | 286 | 28,203 | 208,420 | 698,767 | 935,676 | 45 | 3 |
| reporting-agent | 109 | 32,142 | 385,516 | 492,152 | 909,919 | 19 | 3 |
| self-healing-agent | 60 | 17,271 | 120,597 | 721,723 | 859,651 | 30 | 3 |
| test-review-agent | 32 | 76,505 | 292,126 | 432,243 | 800,906 | 23 | 4 |
| framework-selection-agent | 108 | 12,068 | 207,282 | 222,330 | 441,788 | 20 | 3 |
| failure-analysis-agent | 30 | 17,965 | 72,883 | 238,668 | 329,546 | 15 | 3 |
| requirement-analysis-agent | 28 | 22,961 | 94,011 | 98,563 | 215,563 | 18 | 4 |
| test-planning-agent | 19 | 39,172 | 73,716 | 98,519 | 211,426 | 12 | 3 |
| impact-analysis-agent | 47 | 19,684 | 77,089 | 89,274 | 186,094 | 10 | 3 |
| pr-generation-agent | 43 | 4,127 | 86,070 | 67,453 | 157,693 | 7 | 1 |
| defect-analysis-agent | 32 | 7,630 | 51,994 | 88,622 | 148,278 | 6 | 1 |
| **TOTAL** | **2,048** | **1,092,325** | **6,373,182** | **50,954,208** | **58,421,763** | **1040** | **64** |
