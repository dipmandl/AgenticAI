# Impact Analysis Skill

## Purpose
Guide structured impact classification from requirement and repository evidence.

## Classification approach

### Step 1: Map requirement to repository areas
From `requirement-analysis.md`, extract the functionality described.
From `repository-discovery.md`, identify which modules, routes, or services implement that functionality.

### Step 2: Classify test categories
Only mark a category as applicable if the requirement directly involves it:

| Category | Applicable when |
|----------|----------------|
| UI | Requirement involves a user interface element, page, or visual output |
| API | Requirement involves an HTTP endpoint, webhook, or external service call |
| E2E | Requirement describes a complete user flow across multiple steps or pages |
| Integration | Requirement involves communication between two or more services |
| Functional | Core business logic is being tested |
| Regression | A change may break existing functionality |
| Smoke | Critical path that must work before any other test runs |
| Negative | Requirement explicitly defines invalid input or error behavior |
| Boundary | Requirement mentions limits, min/max, or edge conditions |
| Security | Authentication, authorization, or data protection is involved |
| Accessibility | WCAG/A11y compliance is required |
| Performance | Response time, load, or throughput requirements exist |

### Step 3: Risk assessment
Assign overall risk based on:
- Number of impacted modules (HIGH: >3, MEDIUM: 2–3, LOW: 1)
- Presence of Security or E2E categories → minimum MEDIUM
- Core authentication or payments → CRITICAL

## Evidence requirement
Every impacted area must cite evidence:
- File path or module name from discovery
- Acceptance criterion or requirement statement that implicates it
- Do not list areas as impacted based on name similarity alone

## Output format
```markdown
## Impacted Areas
| Area | Type | Evidence | Risk |
|------|------|----------|------|
| AuthService | Service | discovery: src/auth/ | HIGH |

## Test Categories
| Category | Applicable | Reason |
|----------|-----------|--------|
| API | YES | REQ-001 defines POST /auth/login endpoint |
| UI | YES | REQ-002 defines login form behavior |

## Overall Risk: HIGH
Reason: Core authentication, 2 impacted services.
```
