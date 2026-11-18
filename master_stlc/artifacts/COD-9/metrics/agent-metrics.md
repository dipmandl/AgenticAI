# STLC Token Usage

Source: `C:\Users\DipakMandlik\.claude\projects\C--Users-DipakMandlik-Desktop-AgenticAI-Final-implementation-AgenticAI-master-stlc`

## Per Phase

| Phase | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |
|---|---|---|---|---|---|---|---|
| orchestrator | 1,589 | 616,529 | 5,282,525 | 78,472,008 | 84,372,651 | 1071 | 34 |
| automation-generation | 381 | 422,922 | 1,208,142 | 6,499,957 | 8,131,402 | 163 | 13 |
| execution | 473 | 157,339 | 571,228 | 5,824,948 | 6,553,988 | 219 | 15 |
| automation-review | 104 | 106,012 | 409,270 | 2,911,879 | 3,427,265 | 90 | 6 |
| repository-discovery | 847 | 64,472 | 514,732 | 2,474,403 | 3,054,454 | 141 | 6 |
| reporting | 259 | 64,935 | 715,159 | 1,450,838 | 2,231,191 | 45 | 6 |
| manual-test-generation | 71 | 196,878 | 528,868 | 1,430,864 | 2,156,681 | 54 | 6 |
| other | 254 | 37,571 | 323,021 | 1,666,105 | 2,026,951 | 65 | 4 |
| test-review | 51 | 120,908 | 494,456 | 584,358 | 1,199,773 | 36 | 7 |
| self-healing | 60 | 17,271 | 120,597 | 721,723 | 859,651 | 30 | 3 |
| requirement-analysis | 70 | 53,913 | 269,807 | 500,770 | 824,560 | 51 | 9 |
| test-plan | 34 | 78,544 | 143,256 | 176,305 | 398,139 | 22 | 6 |
| impact-analysis | 101 | 38,378 | 201,180 | 150,166 | 389,825 | 21 | 6 |
| **TOTAL** | **4,294** | **1,975,672** | **10,782,241** | **102,864,324** | **115,626,531** | **2008** | **121** |

## Per Agent

| Agent | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |
|---|---|---|---|---|---|---|---|
| main-session (orchestrator) | 1,131 | 437,386 | 4,265,399 | 69,215,590 | 73,919,506 | 753 | 17 |
| stlc-orchestrator | 458 | 179,143 | 1,017,126 | 9,256,418 | 10,453,145 | 318 | 17 |
| automation-generation-agent | 147 | 392,298 | 791,336 | 5,955,831 | 7,139,612 | 121 | 6 |
| execution-agent | 360 | 112,364 | 350,701 | 5,247,158 | 5,710,583 | 180 | 8 |
| automation-review-agent | 104 | 106,012 | 409,270 | 2,911,879 | 3,427,265 | 90 | 6 |
| repository-discovery-agent | 847 | 64,472 | 514,732 | 2,474,403 | 3,054,454 | 141 | 6 |
| reporting-agent | 259 | 64,935 | 715,159 | 1,450,838 | 2,231,191 | 45 | 6 |
| manual-test-generation-agent | 71 | 196,878 | 528,868 | 1,430,864 | 2,156,681 | 54 | 6 |
| test-review-agent | 51 | 120,908 | 494,456 | 584,358 | 1,199,773 | 36 | 7 |
| pr-generation-agent | 221 | 20,526 | 237,620 | 758,163 | 1,016,530 | 38 | 3 |
| general-purpose | 33 | 17,045 | 85,401 | 907,942 | 1,010,421 | 27 | 1 |
| framework-selection-agent | 234 | 30,624 | 416,806 | 544,126 | 991,790 | 42 | 7 |
| self-healing-agent | 60 | 17,271 | 120,597 | 721,723 | 859,651 | 30 | 3 |
| requirement-analysis-agent | 70 | 53,913 | 269,807 | 500,770 | 824,560 | 51 | 9 |
| failure-analysis-agent | 56 | 32,802 | 141,012 | 460,586 | 634,456 | 28 | 5 |
| test-planning-agent | 34 | 78,544 | 143,256 | 176,305 | 398,139 | 22 | 6 |
| impact-analysis-agent | 101 | 38,378 | 201,180 | 150,166 | 389,825 | 21 | 6 |
| defect-analysis-agent | 57 | 12,173 | 79,515 | 117,204 | 208,949 | 11 | 2 |
| **TOTAL** | **4,294** | **1,975,672** | **10,782,241** | **102,864,324** | **115,626,531** | **2008** | **121** |
