# Validation and pilot guide

Run from the repository root using Python 3.10 or later. The repository utilities use only the Python standard library and do not edit, upload, or send input data.

```bash
python scripts/check_repository.py
python scripts/validate_loop_registers.py examples/closed-loop/registers
python -m unittest discover -s tests -v
git diff --check
```

GitHub Actions runs these checks on pushes and pull requests. `check_repository.py` checks local inline Markdown file targets, basic skill metadata, and header-only CSV template shape. It does not check remote URLs, Markdown anchors, every YAML rule, or the truth of research claims.

## Validate a working export

Export the five operational tables as UTF-8 CSVs to one private directory, using the template filenames. Preserve existing system schemas through an export mapping; the validator accepts extra columns and any column order but requires the named headers. Blank rows are ignored; populated rows must have the correct width. No customer data belongs in this public repository.

```bash
python scripts/validate_loop_registers.py /path/to/private/registers
python scripts/validate_loop_registers.py /path/to/private/registers --stage follow-up
python scripts/validate_loop_registers.py /path/to/private/registers --stage change
```

Default `--stage all` checks local cross-stage IDs. Partial-stage modes explicitly leave cross-stage links unchecked. A standalone Step 4 run can link to external cases, but their existence/authority requires manual review. A header-only template may pass structure; it is not a populated or deployed program.

The register validator catches missing files/headers, malformed rows, duplicate IDs, unknown states, invalid timestamps, missing evidence fields for selected transitions, dangling local references, unaccepted active handoffs, unsupported success states, and invalid merge references. It returns exit code 1 on errors.

It cannot establish that evidence is true, a recipient is correct, a clock calculation follows the staffing calendar, a transfer was actually accepted, a source is healthy, a decision is authorized, or a change improved customer outcomes. Review those conditions using the skill's acceptance scenarios. It also does not compute live overdue queues, send reminders, or migrate a CRM/Sheet.

## Validation layers

| Layer | Evidence needed | Current coverage |
| --- | --- | --- |
| Packaging | Readable skills, valid metadata, local references | Repository checks plus skill-format validation during development |
| Registers | IDs, states, required evidence fields, relationships | Synthetic CSV fixture and automated negative tests |
| Workflow judgment | Correct ownership, closure, source interpretation, and verification | Synthetic walkthrough and scenario checks in each skill |
| Live operation | Authorized access, actual customer contact, trigger/delivery results | User-specific pilot required; not established by repository tests |
| Business outcome | Actual baseline, observation window, results and review | Must be measured after implementation; no result claimed here |

During development, an independent skill walkthrough used a fictional export failure, a partly useful workaround, unreachable public reviewers, a shipped fix, and a failed monitor. It kept the unresolved customer case separate from delivery, retained the company change under verification, rejected duplicate-report inflation, and produced drafts without sending messages. This is one qualitative scenario check, not a provider comparison or production validation.

## Pilot before operational use

Choose one team and a small confirmed trigger set. Confirm authority, contacts, staffing clocks, decision rights, and escalation. Run the Step 3 and Step 4 acceptance scenarios with synthetic data first. Then use a small authorized live cohort, review missed updates and premature closures, and adjust the process before expanding. Preserve evidence of results and keep not-run checks visible.

Step 1 keeps its separate workbook validator. Step 2 retains its Apps Script test mode and user-run live test gate. These new checks do not replace either one or claim Google Workspace integration has passed.
