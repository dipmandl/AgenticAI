# STLC Token Usage

Source: `C:\Users\DipakMandlik\.claude\projects\C--Users-DipakMandlik-Desktop-AgenticAI-Final-implementation-AgenticAI-master-stlc`

## Per Phase

| Phase | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |
|---|---|---|---|---|---|---|---|
| orchestrator | 1,037 | 438,477 | 3,672,218 | 51,780,720 | 55,892,452 | 689 | 22 |
| automation-generation | 221 | 265,596 | 830,361 | 3,870,511 | 4,966,689 | 98 | 8 |
| execution | 250 | 84,317 | 329,241 | 3,019,722 | 3,433,530 | 115 | 8 |
| automation-review | 82 | 65,037 | 278,210 | 2,445,211 | 2,788,540 | 72 | 4 |
| manual-test-generation | 53 | 160,499 | 420,375 | 1,106,301 | 1,687,228 | 40 | 4 |
| other | 163 | 27,719 | 191,286 | 1,229,512 | 1,448,680 | 49 | 3 |
| repository-discovery | 448 | 37,295 | 287,308 | 1,115,580 | 1,440,631 | 72 | 4 |
| test-review | 38 | 93,828 | 349,042 | 485,779 | 928,687 | 27 | 5 |
| reporting | 109 | 32,142 | 385,516 | 492,152 | 909,919 | 19 | 3 |
| self-healing | 60 | 17,271 | 120,597 | 721,723 | 859,651 | 30 | 3 |
| test-plan | 24 | 53,683 | 101,276 | 114,805 | 269,788 | 15 | 4 |
| requirement-analysis | 36 | 25,265 | 108,546 | 122,533 | 256,380 | 24 | 5 |
| impact-analysis | 62 | 25,670 | 108,472 | 95,367 | 229,571 | 13 | 4 |
| **TOTAL** | **2,583** | **1,326,799** | **7,182,448** | **66,599,916** | **75,111,746** | **1263** | **77** |

## Per Agent

| Agent | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |
|---|---|---|---|---|---|---|---|
| main-session (orchestrator) | 752 | 318,580 | 3,005,348 | 46,094,963 | 49,419,643 | 501 | 12 |
| stlc-orchestrator | 285 | 119,897 | 666,870 | 5,685,757 | 6,472,809 | 188 | 10 |
| automation-generation-agent | 92 | 248,608 | 578,253 | 3,594,014 | 4,420,967 | 74 | 4 |
| execution-agent | 188 | 58,722 | 204,364 | 2,692,432 | 2,955,706 | 94 | 4 |
| automation-review-agent | 82 | 65,037 | 278,210 | 2,445,211 | 2,788,540 | 72 | 4 |
| manual-test-generation-agent | 53 | 160,499 | 420,375 | 1,106,301 | 1,687,228 | 40 | 4 |
| repository-discovery-agent | 448 | 37,295 | 287,308 | 1,115,580 | 1,440,631 | 72 | 4 |
| general-purpose | 33 | 17,045 | 85,401 | 907,942 | 1,010,421 | 27 | 1 |
| test-review-agent | 38 | 93,828 | 349,042 | 485,779 | 928,687 | 27 | 5 |
| reporting-agent | 109 | 32,142 | 385,516 | 492,152 | 909,919 | 19 | 3 |
| self-healing-agent | 60 | 17,271 | 120,597 | 721,723 | 859,651 | 30 | 3 |
| framework-selection-agent | 129 | 16,988 | 252,108 | 276,497 | 545,722 | 24 | 4 |
| pr-generation-agent | 130 | 10,674 | 105,885 | 321,570 | 438,259 | 22 | 2 |
| failure-analysis-agent | 30 | 17,965 | 72,883 | 238,668 | 329,546 | 15 | 3 |
| test-planning-agent | 24 | 53,683 | 101,276 | 114,805 | 269,788 | 15 | 4 |
| requirement-analysis-agent | 36 | 25,265 | 108,546 | 122,533 | 256,380 | 24 | 5 |
| impact-analysis-agent | 62 | 25,670 | 108,472 | 95,367 | 229,571 | 13 | 4 |
| defect-analysis-agent | 32 | 7,630 | 51,994 | 88,622 | 148,278 | 6 | 1 |
| **TOTAL** | **2,583** | **1,326,799** | **7,182,448** | **66,599,916** | **75,111,746** | **1263** | **77** |
