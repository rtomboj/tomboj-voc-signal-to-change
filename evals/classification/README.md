# Classification answer key

A versioned answer key for the Benchmark Builder's repeatable classification step: applying a confirmed taxonomy to feedback records. All records are synthetic (fictional Northstar scheduling SaaS).

| File | What it is |
|---|---|
| `RUBRIC.md` | The taxonomy and escalation rules. The only instructions a model run receives. |
| `inputs.csv` | 25 feedback excerpts in five cohorts: Clear-cut, Mixed, Money, Edge, Multi-issue |
| `answer_key.csv` | Expected theme, signal, impact and escalation for each record, with a one-line rationale and key version |
| `score.py` | Scores one or more runs against the key |
| `runs/` | Prediction files, named `<date>_<model>_rubric-<version>.csv` |

## Run the scorer

```
python3 evals/classification/score.py evals/classification/runs/*.csv
```

It prints the record pass rate (all four fields correct), escalation recall, pass rate by cohort, field accuracy, and each failed record with expected vs actual values. It exits non-zero if any run misses an escalation.

## How runs are produced

Each model gets only `RUBRIC.md` and the excerpts (no cohort, no key) and returns `record_id,primary_theme,signal_type,operational_impact,escalate,confidence,notes`.

## Results, 2026-11-02 (key v1.0)

| Run | Record pass | Escalation recall | Failed |
|---|---|---|---|
| Claude Haiku | 25/25 | 8/8 | none |
| Claude Sonnet | 24/25 | 8/8 | E07 impact: expected High, got Medium |

E07 ("export still breaks, so we print by hand") fits both "failed output" (High) and "workable fallback" (Medium). The disagreement points to an ambiguous impact rule rather than a model error. Clarify it in rubric v1.1 before relabeling.

## Limits

- 25 records is a demonstration set, not a production benchmark. Both models scoring near 100% means the set is too easy to separate them; v1.1 should add harder cases and prune records every model passes.
- Labels were written by one author. A second reviewer and a recorded agreement rate are needed before treating the key as authoritative.
- Change a label only by publishing a new key version; never edit rows in place.
