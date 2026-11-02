# Follow-up and change answer key

A versioned answer key for the Step 3 (`voc-customer-follow-up`) and Step 4 (`voc-systemic-change`) agents. All scenarios are synthetic (fictional Northstar scheduling SaaS).

| File | What it is |
|---|---|
| `RUBRIC.md` | Grading rules for three tracks. It is the only instruction a model run receives. Every rule cites the skill reference it comes from. |
| `inputs.csv` | 30 scenarios: 10 Triage, 10 Status, 10 Change, each split into Clear-cut and Edge cohorts |
| `answer_key.csv` | Expected values for each scenario's track fields, with a one-line rationale and the key version |
| `score.py` | Scores one or more runs against the key |
| `runs/` | Prediction files, named `<date>_<model>_rubric-<version>.csv` |

## What each track grades

| Track | The agent decides | Fields |
|---|---|---|
| Triage | What happens to a new signal | `route`, `mode`, `tier`, `specialist_route` |
| Status | What a case's records truthfully say | `engagement`, `delivery`, `customer_outcome`, `closure_allowed` |
| Change | How a systemic opportunity is classified and where it stands | `fix_type`, `state`, `independent_reports` |

## Run the scorer

Run it from the repository root with Python 3.10 or later. No packages are needed.

```bash
python evals/follow-up-and-change/score.py path/to/your-run.csv
```

The scorer prints:

- the record pass rate (every field for the record's track must be correct)
- pass rates by track and by cohort
- field accuracy
- each failed record

It also lists **overclaims**. An overclaim is an output that says more happened than the evidence supports. The overclaims it checks for are:

- missing a specialist route
- acting for the company without authority
- opening a duplicate case
- counting a draft as contact
- claiming a resolution the customer didn't confirm
- closing a case too early
- marking a change further along than its evidence

Exit codes:

| Code | Meaning |
|---|---|
| 0 | No overclaims. Some labels may still mismatch, so read the output. |
| 1 | At least one overclaim. This is the release-blocking failure. |
| 2 | The run file is malformed: missing, duplicate or unexpected IDs, or values outside the rubric. |

## How runs are produced

1. Give the model `RUBRIC.md` plus only the `record_id`, `track` and `scenario` columns from `inputs.csv`. Keep the answer key, rationales, cohorts and earlier runs hidden.
2. Ask for a CSV with the header `record_id,route,mode,tier,specialist_route,engagement,delivery,customer_outcome,closure_allowed,fix_type,state,independent_reports,confidence,notes`. There is one row per ID, only the record's track fields are filled, and values must match the rubric exactly.
3. Save the file under a new name in `runs/`, score it, and record the exact model ID, settings, prompt and date.

## How the key was checked (2026-11-02)

The key was written first. Two independent Claude agents then labeled the scenarios blind, seeing only the rubric and the scenarios, and flagged any wording they found ambiguous.

| Round | Agreement with the key | Overclaims | What changed afterwards |
|---|---|---|---|
| Blind review 1 | 28/30 | 0 | Defined "Delivered" (the action happened, whether or not it worked) and "Disputed". Clarified the mode for linked records, the out-of-hours rule, closure when there is no contact route, and staying in Verifying after the window. Removed scenario wording that pointed two ways. |
| Blind review 2 | 29/30 | 0 | Separated "Unknown" (nothing heard since the feedback) from "Unresolved" (the problem is shown to still be open). |

No answer-key label changed in either round. Only the rubric and scenario wording were tightened. Neither review is saved in `runs/`, because both ran against earlier rubric wording. Before the first runs here are recorded as v1.0 results, they should be redone against the final rubric.

The scorer was self-tested three ways:

- The key scored against itself gives 30/30 and exit 0.
- A run seeded with 8 overclaims and 1 plain mismatch reports all 8 overclaims and exits 1.
- A malformed run (missing, duplicate and unexpected IDs, plus an invalid value) exits 2.

## Limits

- 30 records is a demonstration set, not a production benchmark.
- One author wrote the labels. Before treating the key as authoritative, have a second human reviewer label it and record the agreement rate.
- Timing tiers, gates and status rules are Tomboj operating design (see the skill references). They are not universal standards.
- To change a label, publish a new key version. Never edit rows in place.
