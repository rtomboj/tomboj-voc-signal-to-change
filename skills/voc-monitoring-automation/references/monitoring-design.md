# Monitoring design

Use this reference after inspecting both Part 1 files and before changing the workbook or generating collection code.

## The jobs are different

| Job | What it answers | What it does |
| --- | --- | --- |
| Collection | What did this source report at this check? | Reads a permitted API, feed, export, notification, or manual capture; records the source and capture time. |
| Monitoring | What changed since the agreed baseline or prior successful check? | Compares IDs and measures, deduplicates, appends new records, handles allowed edits, and records source health. |
| Classification | What might these records mean? | Applies confirmed categories or measures, marks uncertainty, and routes items for human review. |
| Follow-up | What should an organization do with the signal? | Investigates, responds, resolves, and learns. This is Part 3, and a signal alone does not prove fault. |

A single Apps Script run can perform multiple jobs, but each job's inputs and outputs must remain visible. A retrieval failure is a failed check, not an empty result. Keep the last successful state after an error.

## Inspect the Part 1 workbook

Use the current Part 1 contract and validator as references, then inspect the actual workbook. A passing validator is useful but does not decide which sources are appropriate to monitor; a failing validator means map or repair the working copy deliberately.

Preserve the original .xlsx and Markdown files. Create a dated backup before editing the converted Google Sheet. Excel-to-Sheets conversion can change formatting, charts, formulas, or validation; check important workbook areas after conversion.

Map aliases by header name. Do not rename or reorder existing tabs or columns. Some tabs have title/note rows before their headers, so inspect the first 20 rows rather than assuming row 1 is the header. Show the user a brief schema map: tab/header found, mapped meaning, missing field, and action.

The reviewed examples demonstrate three cases: Harri is a legacy workbook with contract mismatches; Nory is closer to the contract but still has validation errors; Toast is missing monitoring-critical data tabs. Do not state that any of them is ready without checking its present contents.

Use `Week2_Readiness` as the monitoring source plan only if it has a clear row per external source, its own source decisions, and collection/access fields. If it is an internal data readiness checklist or does not identify external sources, map `Source_Register` into a new `Monitoring_Config`. Keep one editable source-of-truth table; do not create two conflicting source lists.

## Agree the source plan

Prefill a source table from Part 1 and ask the user to confirm unresolved rows and exceptions:

| Field | Purpose |
| --- | --- |
| Source ID, name, profile URL | Identifies the source and its target |
| Evidence class and audience | Separates direct customer feedback from vendor-selected examples, press, and other context |
| Part 1 treatment and readiness note | Gives the user's prior choice and the remaining question |
| Collection route | Approved API/feed/export/notification, manual capture, watchlist, deferred, or excluded |
| Permission evidence URL, checked date, confirmed by | Records how the route was approved and by whom/which role |
| Profile access and response route | Owned-profile access, public viewing only, or no response route; investigation/handoff can still be separate |
| Cadence and timezone | Determines when a source is due for a check |
| ID approach and origin | Platform ID, canonical URL, fingerprint, synthetic, or unknown |
| Data fields and alert choice | Makes the collection and notification scope explicit |
| Process-owner role | Role that handles operational follow-up; not an evaluated individual |

Ask for one global cadence, time zone, and digest destination when possible, then identify exceptions by source. A named customer-support or profile owner may be needed for access or response, but do not send an alert to that person's manager or present a measure as their performance.

A visible page is not enough to authorize automated collection. Confirm the source's current permitted route and limits. If the route is unknown, unreliable, or disallowed, keep it manual, on a watchlist, deferred, or excluded. Never bypass login, CAPTCHAs, paywalls, rate limits, or platform controls.

## Workbook additions

Add only what's missing in the Google Sheets working copy. Preserve Part 1 values, formulas, headers, dashboard, and source notes.

### Monitoring configuration

Use the existing row-per-source `Week2_Readiness` as the source of truth only if it is actually shaped for this purpose. Otherwise create `Monitoring_Config` from `Source_Register` and show the field map. Avoid maintaining both as independent editable lists.

Suggested fields:

- Source ID, source name, profile URL
- Evidence class, audience, Part 1 treatment
- Monitoring decision: Automatic, Manual, Watchlist, Deferred, Excluded
- Collection route and allowed fields
- Permission evidence URL, confirmed date, confirmer role
- Profile access/response route
- Cadence, timezone, next due date
- Stable ID field and ID Origin policy
- Baseline date/rule
- Source health and last successful check
- Investigation alert rule and possible-pattern rule
- Digest destination and process-owner role
- Notes and review-by date

Do not enable automatic collection while source identity, access, route, or record matching is unresolved.

### Manual capture

If a source has no safe automated route, offer a `Manual_Capture` tab or an optional Google Form, plus a recurring reminder. Suggested fields:

- observed/captured date and source;
- source ID, canonical record URL, platform ID if visible, and ID Origin;
- review date, audience and evidence class;
- rating and scale as reported (do not infer a rating);
- short excerpt and capture person/role;
- suggested theme or signal type, clearly marked as a suggestion;
- human-review status and notes.

Manual records should enter the same deduplication, baseline, classification, alert, and dashboard pipeline as automatically collected records. Add a due/overdue indicator to source health. A manual reminder is a missed-check notice, not evidence that feedback changed.

### Run log

Use `Monitor_Run_Log` for one source-check attempt per row:

- Run ID, Source ID, Started At, Completed At
- Status: Success, No New Records, Partial, Failed, or Skipped
- Records fetched, New Records, Updated Records, Duplicates Skipped, Out-of-Scope Records
- Alerts Sent, concise Error Summary, Next Check

“No New Records” is valid only after a successful check. Partial, failed, stale, and skipped checks must remain distinct from customer feedback.

### Review data and change history

Append to the existing Part 1 `Review_Data` table when its schema can represent the records. Otherwise create a monitor-specific data tab and document the mapping; do not silently change Part 1 headers.

Where available, retain source ID, platform record ID, ID Origin, canonical URL, original URL, record date, capture date, source-reported geography, audience, evidence class, rating, scale, excerpt, language, source notes, and classification fields. Do not fill unknown values with guesses. Keep platform-specific rating scales separate.

An optional `Review_Change_Log` can preserve changes to an existing review or aggregate measure. Store detected time, source ID, stable record ID, field name, old/new values, change type, and alert decision. Avoid duplicating full review text if a short changed field is enough.

## Identity, baseline, and syndication

A Part 1 ID may be a true platform ID, a canonical URL, a content fingerprint, or a synthetic placeholder. Add an explicit `ID Origin` field when it is absent. Treat unknown and synthetic IDs as unreliable until reconciled.

Use a deduplication key built from Source ID + ID Origin + record ID. Do not use URL alone as the identity key. If a source has no reliable ID, keep it manual or capture a dated current-state baseline, then monitor additions after that date. A change in a synthetic placeholder must not create a new customer alert.

For syndicated copies, select one canonical source for counting after a human confirms the relationship. Preserve secondary URLs as provenance, but count the record once and do not route the same event as two independent reports. Never assume two similar excerpts are the same review without evidence.

On first run, choose explicitly between:
1. **Part 1 baseline:** treat Part 1 rows and the stated benchmark date as historical; only items newer than the confirmed date can be new.
2. **Fresh current-state baseline:** capture what is currently visible and begin alerting from that date.

In either route, suppress historical matches, including synthetic-ID records after a current-state snapshot. Do not silently import a larger history or replay old records. If a user requests backfill, label its date range and alert behavior separately.

If the source edits or removes a record, follow the approved edit policy. A record disappearing from one page or search result is not proof of deletion; only record a removal when the source confirms it.

## Measures and labels

Automate transparent measures when inputs support them:

- distinct new or changed records by source and period;
- source-specific ratings and rating-scale movement;
- last successful check, overdue status, failure, and retry state;
- counts by audience, evidence class, theme, and positive/negative signal;
- volume and coverage alongside the underlying time window and denominator.

Keep raw values and calculated values separate. Keep source ratings separate: do not average different platforms, scales, audiences, or collection routes into one company score. Prefer “measure,” “signal,” and “possible change” to language that sounds like a grade. Never rank individual employees.

The monitor exists to help people and organizations find opportunities to improve. It should surface positive as well as negative shifts. A process owner is a role accountable for follow-up, not a person whose performance is being scored.

## Classification choices

Let the user choose the level:

1. **Collection only:** store permitted records and source-health results.
2. **Deterministic measures:** counts, rating movement within one source, recency, and approved thresholds.
3. **Rule suggestions:** user-approved keyword or rating rules can suggest a theme/signal, but retain the suggestion and confidence separately until reviewed.
4. **Optional AI:** classify or summarize new records. Use only new records by default and show that review text leaves Google for the selected provider. State token estimate/cost, key storage, retention/data-use assumptions, and per-run budget before recurring AI runs.

No recurring AI by default. A person may use AI during setup or request a one-off digest. If AI output is used, retain source URL, short evidence excerpt, model/provider, run time, and confidence where appropriate. Do not treat generated labels as verified facts.

## Guardrails for alerts and trends

A single comment is not a trend. It may still be worth investigating when the content, safety, or customer impact warrants a prompt. The alert should say “individual signal—review requested,” preserve evidence and source, and never imply that the statement is representative or proves fault.

Separate the following:

- **Individual incident:** one potentially serious signal that a human may investigate under an explicitly approved rule. Route only to the agreed operational recipient.
- **Possible pattern:** repeated independent records matching an agreed theme, evidence class, audience, and time window. Label as possible until reviewed.
- **Sustained change:** a possible pattern persists across more than one monitoring window or another user-confirmed test; record the start/end and the basis for calling it sustained.
- **Temporary incident/burst:** a short concentration of records that may be linked to an event or release. Preserve the incident window; do not call it systemic without more evidence.
- **Positive movement:** repeated or notable improvements worth understanding and protecting, using the same source/audience and evidence discipline.
- **Source health:** failed, stale, blocked, or overdue checks are operational alerts, separate from customer feedback.
- **Digest:** group routine signals; reserve immediate notices for explicitly approved high-impact items.

Offer a transparent starter rule as a decision aid, not a universal standard. Example for confirmation: “At least 3 independent records with the same reviewed theme, source, and audience inside a rolling 90-day window creates a *possible pattern*; it becomes *sustained* only if it appears in two consecutive review windows.” The user may choose different counts/windows or keep trend alerts off. If volume is below the agreed floor, show counts and records without percentage changes or trend labels.

Do not equate silence with resolution. A theme with no new records should be described as “no new reports in this window.” Say “improved” only when comparable measures support that conclusion, and “fixed” only after a specific resolution has been checked.

Use alerts to prompt inquiry, not punishment. Do not send employee-level comparisons, names, or performance rankings. Avoid email/Chat notification bodies that expose sensitive review text; send a limited summary and link to the access-controlled Sheet where possible.

## Monitoring view

Build a separate `Monitor_Dashboard`; leave the Part 1 `Executive_Dashboard` unchanged because it may be a frozen benchmark or fixed-range display.

Show:

- last successful check, due/overdue state, and errors by source;
- records collected, new, changed, and deduplicated by source and time window;
- source, audience, evidence class, and rating scale filters;
- positive and negative signals, individual incidents, possible patterns, and reviewed sustained changes as separate views;
- evidence window, denominator, coverage gaps, confidence, and review status;
- process-owner role and next follow-up where configured.

Check that dashboard totals reconcile to monitor data. Failure or stale status must never appear as zero feedback. Do not claim causality or organization-wide prevalence from a limited, self-selected web sample.
