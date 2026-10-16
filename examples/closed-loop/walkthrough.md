# Northstar: one fictional example across the whole loop

All companies, sources, comments, owners, records, dates, decisions, and events in this example are **synthetic**. No company was researched, no customer was contacted, no source was checked live, and no change was deployed.

This is a compact teaching fixture for the four-part workflow and web bonus. The CSVs illustrate connected records; they do not claim to be a complete validated Step 1 workbook or a production monitoring package. Use the actual skills to create the full outputs for your company.

[See the example gallery](../../docs/example-gallery.md) · [Start your own run](../../docs/start-here.md)

## Source packet

Northstar Scheduling is an invented scheduling product. The fixture contains four comments from two fictional sources, captured on October 12 over an October 1–12 insight window:

| Source/record | Signal | What it says |
| --- | --- | --- |
| REV:R101 | Negative | Weekly export fails for the largest booking |
| REV:R102 | Negative | Export fails for a large booking |
| APP:R103 | Negative | Large schedule fails while small schedules work |
| APP:R104 | Positive | Shared schedule makes upcoming shifts easy to see |

A hypothetical repost of R101 would add provenance, not another independent report; it is not a fifth row. The three negative records justify investigation in this invented scenario. They do not establish how many real customers/accounts are affected, population prevalence, a validated root cause, or a trend.

Reserved `.example` domains mark fictional source references; do not collect from them or present them as verified public sources.

## Part 1: benchmark

The [written benchmark](benchmark/northstar-voc-benchmark.md) explains the scope, evidence, interpretations, and limitations. Its teaching tables are:

- [Source_Register.csv](benchmark/Source_Register.csv): the two fictional feedback sources.
- [Review_Data.csv](benchmark/Review_Data.csv): the four individual comments, source/record IDs, themes, and classifications.
- [Signal_to_Focus.csv](benchmark/Signal_to_Focus.csv): investigate large-booking export reliability; preserve and learn from schedule visibility.

Evidence class describes the kind of feedback being simulated. Data Class = SYNTHETIC describes its provenance. These are different fields. All classifications in this fixture are authored examples, not model findings about a real company.

The original benchmark/capture dates remain visible even when later monitoring and case events are added.

## Part 2: monitoring

The [source plan](monitoring/Monitoring_Config.csv) keeps both sources manual-only. It does not grant automation permission. The [run log](monitoring/Monitor_Run_Log.csv) contains four invented observations: two baseline captures, a later failed REV check, and a later successful APP check.

The failure has blank Records Found/New Records because they are unknown. The successful later APP check has zero additional records. The baseline records do not become new alerts when monitoring starts.

These rows are illustrative inputs, not evidence of an installed trigger or a passed fetch. A live run would need the actual source route, permission, generated adapter, and user-run test results.

## Part 3: customer follow-up

[Follow_Up_Cases.csv](registers/Follow_Up_Cases.csv) retains two customer cases:

| Case | Evidence | Delivery and outcome | Administrative state |
| --- | --- | --- | --- |
| CASE-001 | REV:R101; protected synthetic support reference | CSV workaround Delivered; next-week export still fails, so Partially resolved | Open |
| CASE-002 | REV:R102; no legitimate contact route | Not assessed; customer outcome Unknown | Closed with an explicit reason |

APP:R103 supports the company investigation but has no invented customer identity or accepted individual follow-up in this fixture. APP:R104 is a positive learning signal; it does not require an invented complaint case.

Jamie retains communication ownership for CASE-001. [ACTION-001](registers/Case_Actions.csv) is Done because the workaround was delivered. ACTION-002 is Proposed to investigate the remaining failure. Proposed is not accepted ownership.

Coaching note: acknowledge the useful workaround, then check the original customer goal. Do not close a case because an attachment was delivered. Confirm an investigation owner and next update; review whether tooling, workload, or closure targets encourage premature closure. This evidence does not establish misconduct.

## Customer update

**Draft — not sent:** “Thanks for confirming that this week's export opens. I understand that next week's schedule still fails. I will coordinate the next check and update you by October 15 at 12:00 UTC, even if the investigation is still underway.”

The [update register](registers/Customer_Updates.csv) records that draft without an occurrence timestamp or delivery evidence. CASE-002 has a Not possible communication disposition, not a fabricated contact. Internal report-back remains assigned on the company change.

## Part 4: company change

[CHANGE-001](registers/Change_Register.csv) addresses large-booking export reliability. The synthetic product lead accepted the initiative and the product owner accepted accountability. A fictional October 14 release record is present; the change remains **Verifying**.

The [case links](registers/Change_Case_Links.csv) preserve CASE-001's active update obligation and CASE-002's explicitly ended customer-contact obligation. Closing a case does not remove its evidence from the company investigation.

The compact [change brief](change-brief.md) distinguishes root-cause hypothesis, delivery, planned measurement, and missing result evidence.

## Change brief

CHANGE-001 is a product/technology investigation into large-booking export reliability. Evidence includes REV:R101, REV:R102, APP:R103 and the partial recovery in CASE-001. The exact cause is a hypothesis. The positive APP:R104 visibility experience should be preserved during changes.

The fictional decision accepts investigation and verification; it does not turn the sample into a population claim. The product owner maintains the change plan and internal report-back, while Jamie retains the customer update. The structured [change brief](change-brief.md) is the fuller teaching document linked from the register.

## Verification

The agreed synthetic observation window is 30 days after the October 14 rollout, with an initial November 13 review. The latest REV check failed, so absence of new REV reports is not evidence of success. The APP check is successful; it does not establish coverage for REV or verify the original customer task.

A proposed measure is successful large-booking exports / eligible large-booking export attempts, with sample sizes, cohort, baseline period, and checks for incomplete or incorrect output. Actual baseline values and numerical success thresholds are **not available** in this fixture. Agreement and measurement are still needed before claiming improvement. The November review is a checkpoint, not automatic closure.

## Bonus: web interface

Download [preview.html](preview.html) and open it locally to switch among Benchmark, Customer follow-up, and Web overview. GitHub displays the file as source; it does not execute it in the repository view.

The preview is generated from [example.json](example.json) and the five existing registers. It makes no network calls, contains no real identifiers, sends no messages, and makes no operational writes. It is an explanatory local page, not a ready-to-deploy Apps Script app or a tested organization-only website.

The real bonus skill inspects the user's current Sheet and script, adapts the files, supports connected/manual routes, and verifies the private deployment separately.

## Trace the joins

`REV:R101 → CASE-001 → ACTION-001 / ACTION-002 → UPDATE-001 → CHANGE-001`

`REV:R102 → CASE-002 → CHANGE-001` retains learning despite unavailable customer contact.

The source/record pair stays qualified; Case IDs remain separate from Change IDs. One company's fix can relate to multiple distinct customer cases.

## Run and validate the example

From the repository root:

```bash
python scripts/build_example.py
python scripts/validate_loop_registers.py examples/closed-loop/registers
python scripts/check_example.py
python scripts/check_repository.py
```

The generator reads the authored synthetic fixture and existing registers; it does not run a research or monitoring workflow. The checks verify selected structural/evidence gates and cross-stage joins. They cannot validate fictional claims, approve a company's policies, establish live permissions, or prove customer improvement.

CSV files can be inspected directly or imported into a disposable Google Sheet. They use header row 1; the real assistant should inspect each actual workbook rather than assuming that row. Keep these synthetic records out of operational data.
