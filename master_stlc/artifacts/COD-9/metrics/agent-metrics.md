# STLC Token Usage

Source: `C:\Users\DipakMandlik\.claude\projects\C--Users-DipakMandlik-Desktop-AgenticAI-Final-implementation-AgenticAI-master-stlc`

## Per Phase

| Phase | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |
|---|---|---|---|---|---|---|---|
| orchestrator | 1,549 | 607,074 | 5,186,563 | 77,250,936 | 83,046,122 | 1046 | 31 |
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
| **TOTAL** | **4,254** | **1,966,217** | **10,686,279** | **101,643,252** | **114,300,002** | **1983** | **118** |

## Per Agent

| Agent | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |
|---|---|---|---|---|---|---|---|
| main-session (orchestrator) | 1,093 | 428,210 | 4,183,372 | 67,994,518 | 72,607,193 | 729 | 15 |
| stlc-orchestrator | 456 | 178,864 | 1,003,191 | 9,256,418 | 10,438,929 | 317 | 16 |
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
| **TOTAL** | **4,254** | **1,966,217** | **10,686,279** | **101,643,252** | **114,300,002** | **1983** | **118** |
