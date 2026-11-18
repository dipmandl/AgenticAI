# STLC Token Usage

Source: `C:\Users\DipakMandlik\.claude\projects\C--Users-DipakMandlik-Desktop-AgenticAI-Final-implementation-AgenticAI-master-stlc`

## Per Phase

| Phase | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |
|---|---|---|---|---|---|---|---|
| orchestrator | 1,669 | 642,803 | 5,422,272 | 80,739,429 | 86,806,173 | 1130 | 35 |
| automation-generation | 436 | 487,116 | 1,441,155 | 7,897,443 | 9,826,150 | 191 | 15 |
| execution | 473 | 157,339 | 571,228 | 5,824,948 | 6,553,988 | 219 | 15 |
| automation-review | 113 | 123,603 | 489,498 | 3,064,066 | 3,677,280 | 97 | 7 |
| repository-discovery | 941 | 74,131 | 621,483 | 2,747,935 | 3,444,490 | 156 | 7 |
| manual-test-generation | 83 | 211,087 | 614,762 | 1,627,916 | 2,453,848 | 64 | 7 |
| reporting | 259 | 64,935 | 715,159 | 1,450,838 | 2,231,191 | 45 | 6 |
| other | 254 | 37,571 | 323,021 | 1,666,105 | 2,026,951 | 65 | 4 |
| test-review | 56 | 134,049 | 541,304 | 593,186 | 1,268,595 | 39 | 8 |
| requirement-analysis | 77 | 58,247 | 292,076 | 533,155 | 883,555 | 56 | 10 |
| self-healing | 60 | 17,271 | 120,597 | 721,723 | 859,651 | 30 | 3 |
| test-plan | 40 | 91,603 | 170,043 | 201,469 | 463,155 | 26 | 7 |
| impact-analysis | 116 | 44,728 | 237,236 | 156,024 | 438,104 | 24 | 7 |
| **TOTAL** | **4,577** | **2,144,483** | **11,559,834** | **107,224,237** | **120,933,131** | **2142** | **131** |

## Per Agent

| Agent | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |
|---|---|---|---|---|---|---|---|
| main-session (orchestrator) | 1,136 | 438,809 | 4,267,946 | 69,350,575 | 74,058,466 | 756 | 17 |
| stlc-orchestrator | 533 | 203,994 | 1,154,326 | 11,388,854 | 12,747,707 | 374 | 18 |
| automation-generation-agent | 172 | 453,779 | 967,804 | 7,331,506 | 8,753,261 | 144 | 7 |
| execution-agent | 360 | 112,364 | 350,701 | 5,247,158 | 5,710,583 | 180 | 8 |
| automation-review-agent | 113 | 123,603 | 489,498 | 3,064,066 | 3,677,280 | 97 | 7 |
| repository-discovery-agent | 941 | 74,131 | 621,483 | 2,747,935 | 3,444,490 | 156 | 7 |
| manual-test-generation-agent | 83 | 211,087 | 614,762 | 1,627,916 | 2,453,848 | 64 | 7 |
| reporting-agent | 259 | 64,935 | 715,159 | 1,450,838 | 2,231,191 | 45 | 6 |
| test-review-agent | 56 | 134,049 | 541,304 | 593,186 | 1,268,595 | 39 | 8 |
| framework-selection-agent | 264 | 33,337 | 473,351 | 565,937 | 1,072,889 | 47 | 8 |
| pr-generation-agent | 221 | 20,526 | 237,620 | 758,163 | 1,016,530 | 38 | 3 |
| general-purpose | 33 | 17,045 | 85,401 | 907,942 | 1,010,421 | 27 | 1 |
| requirement-analysis-agent | 77 | 58,247 | 292,076 | 533,155 | 883,555 | 56 | 10 |
| self-healing-agent | 60 | 17,271 | 120,597 | 721,723 | 859,651 | 30 | 3 |
| failure-analysis-agent | 56 | 32,802 | 141,012 | 460,586 | 634,456 | 28 | 5 |
| test-planning-agent | 40 | 91,603 | 170,043 | 201,469 | 463,155 | 26 | 7 |
| impact-analysis-agent | 116 | 44,728 | 237,236 | 156,024 | 438,104 | 24 | 7 |
| defect-analysis-agent | 57 | 12,173 | 79,515 | 117,204 | 208,949 | 11 | 2 |
| **TOTAL** | **4,577** | **2,144,483** | **11,559,834** | **107,224,237** | **120,933,131** | **2142** | **131** |
