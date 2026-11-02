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

Install Python 3.10+ and open a terminal in the repository's root folder. No additional Python packages are required. To score both included runs:

```bash
python evals/classification/score.py evals/classification/runs/2026-11-02_haiku_rubric-v1.0.csv evals/classification/runs/2026-11-02_sonnet_rubric-v1.0.csv
```

Use `python3` or `py -3` instead of `python` if that is your Python 3 command. The explicit filenames work in Windows PowerShell without relying on wildcard expansion.

It prints the record pass rate (all four fields correct), escalation recall, pass rate by cohort, field accuracy, and each failed record with expected vs actual values. It exits non-zero if any run misses an escalation. Exit code zero does not mean every label matched: the included Sonnet run exits successfully with one mismatch. Always read the printed results.

These are saved predictions; running the scorer does not call either model or require an API key.

## How runs are produced

Each model gets only `RUBRIC.md` and the excerpts (no cohort, no key) and returns `record_id,primary_theme,signal_type,operational_impact,escalate,confidence,notes`.

1. Supply the complete rubric and only the `record_id` and `excerpt` columns from `inputs.csv`. Keep the answer key, rationales, cohort names, and existing predictions hidden from the model.
2. Save the response as a UTF-8 CSV with the header above, one row per input ID, and exact allowed values from the rubric. Quote CSV cells containing commas. Use a new filename; preserve existing runs.
3. Score the new file with `python evals/classification/score.py path/to/your-run.csv` from the repository root.
4. Review mismatches against the rubric and source excerpt. Record the exact model identifier, settings, prompt, and run date alongside new results so others can reproduce the setup.

## Results, 2026-11-02 (key v1.0)

| Run | Record pass | Escalation recall | Failed |
|---|---|---|---|
| Claude Haiku | 25/25 | 8/8 | none |
| Claude Sonnet | 24/25 | 8/8 | E07 impact: expected High, got Medium |

E07 ("export still breaks, so we print by hand") fits both "failed output" (High) and "workable fallback" (Medium). This is a mismatch against key v1.0; the overlapping impact rules need adjudication before calling it a model error. Clarify precedence in a future rubric version before relabeling. The same overlap deserves review for other fallback cases, including E06 and E23.

## Limits

- 25 records is a demonstration set, not a production benchmark. These two saved runs provide little separation and do not establish a general model ranking. Add harder cases and evaluate more runs before drawing broader conclusions.
- Labels were written by one author. A second reviewer and a recorded agreement rate are needed before treating the key as authoritative.
- Some impact labels need clearer rubric support, including privacy severity (E19) and slow support without a stated fallback (E08). Agreement with the key measures consistency with these labels, not independent correctness.
- The scorer currently overwrites duplicate record IDs and ignores unexpected IDs. It also does not make every invalid value a failing exit code. Check that prediction files contain exactly the input IDs once each and use valid field values before relying on a score.
- Change a label only by publishing a new key version; never edit rows in place.
