# Monitoring design

Use this reference after inspecting the Part 1 files and before adding workbook structure or writing collection code.

## The three jobs

| Job | Question | What the system does |
| --- | --- | --- |
| Collection | What can we retrieve from this source now? | Uses the permitted method to retrieve accessible aggregate measures or review records and preserves source identity and capture time. |
| Monitoring | What changed since the baseline or last successful check? | Compares stable IDs and measures, detects new or changed records, deduplicates, updates records, and logs source health and run results. |
| Classification | What might this record or group of records mean? | Applies the agreed taxonomy, score or optional AI interpretation, then marks uncertainty and human-review needs. |

These jobs can run in one scheduled Apps Script execution, but their inputs and results must remain distinguishable. A source retrieval failure is a failed check, not an empty result. Do not erase the last successful state after an error.

## Inspect and map Part 1 schemas

Use the Step 1 workbook contract as the reference, then inspect the actual workbook. Preserve existing tab names, data, formulas, and headers. Map aliases into the existing columns rather than creating duplicate fields.

For example, the Harri workbook uses Stable ID where the Step 1 contract uses Stable Source Record ID, and Short Excerpt where the contract uses Short Evidence Excerpt. A mapper can connect these fields without changing the source workbook. Harri's Review_Data also already has Primary Theme, Secondary Theme, Signal Type, Operational Impact, Classification Confidence, and Human Review Needed.

The source register describes identity, audience, baseline status, inclusion, and possible collection route. It does not necessarily confirm that an automated route is permitted. Confirm the source method and permission with the user.

## Workbook additions

Create only missing structures in the designated Google Sheets working copy.

### Monitoring_Config

One row per source selected for monitoring. Required fields:

- Source ID
- Source
- Profile URL
- Monitoring Decision
- Collection Method
- Permission Status
- Cadence
- Stable ID Field
- First-Run Rule
- Fields Collected
- Alert Rule
- Alert Recipient
- Last Successful Check
- Source Health
- Notes

Use controlled statuses such as Automatic, Manual, Watchlist, Deferred, and Excluded. Make cadence editable per source. Do not make a source automatic while its identity, method, permission, or stable ID is unresolved.

### Monitor_Run_Log

One row per source-check execution. Required fields:

- Run ID
- Source ID
- Started At
- Completed At
- Status
- Records Fetched
- New Records
- Updated Records
- Duplicates Skipped
- Out-of-Scope Records
- Alerts Sent
- Error Summary
- Next Check

Use explicit statuses such as Success, No New Records, Partial, Failed, and Skipped. No New Records is valid only after the source check succeeded.

### Review_Data

Use the existing Step 1 review-data schema where present. Map collected source fields into its existing columns. Preserve the source URL, stable source ID, capture date, record date, source-reported geography, audience, rating and scale, evidence excerpt, source class, classification fields, and notes as available. Do not invent unavailable values.

For stable identifiers:

- Prefer the platform's review or record ID.
- Otherwise use a canonical record URL if stable.
- Use a documented fingerprint fallback only when the source exposes no stable ID.
- Keep Source ID and Stable Source Record ID together; IDs need not be globally unique without the source key.

For existing stable IDs, compare captured fields. Skip exact duplicates. If a source edits a record, update the current Review_Data row according to the agreed policy and, if enabled, append a before-and-after row to Review_Change_Log. Do not treat a review disappearing from a limited page as a deletion unless the source explicitly confirms removal.

### Review_Change_Log

Optional. Use when edited records or aggregate measures need before-and-after history. Store detected time, Source ID, stable record ID, field changed, old and new values, change type, and alert decision. Avoid copying full review text when a field-level change record is enough.

## First-run behavior

Ask whether the user wants to:

1. use the existing Part 1 Review_Data and Baseline_Snapshot as the historical baseline; or
2. capture the current public source state and start monitoring only from this date.

Default to the existing Part 1 dataset as baseline and suppress historical alerts. Do not silently backfill a larger review history than Part 1 collected. If an authorized API can supply more history, ask before importing it and label its capture window.

Record baseline date, last successful check, and the first new stable ID per source. A source with no stable ID or unreliable pagination may remain manual or watchlist.

## Classification and scores

Ask which level to automate:

- **Change measures:** new-record count, per-source rating or volume change, recency, last-check age, and source failure. These are deterministic when inputs are available.
- **Rule suggestions:** rating bands or user-approved keywords can propose Signal Type, Primary Theme, or Human Review Needed. Keep the suggested label distinct until the user approves it.
- **Taxonomy classification:** reuse the existing Theme_Taxonomy; do not create new categories without approval. Existing classifications can remain untouched while new records receive proposed labels.
- **AI classification or summaries:** optional. Process new records only by default, attach confidence, retain traceable excerpts and URLs, and estimate token use before enabling recurring calls.

Show source ratings and volumes separately. Do not average or rank platforms with unlike audiences, scales, or collection methods. Do not invent a composite VOC or employee performance score. When practical, show separate dimensions such as frequency, impact, evidence strength, prevalence confidence, and most recent signal.

## Alert guardrails

Use user-approved rules, not a universal threshold.

- **Individual signal:** a specific critical customer issue may trigger a prompt to investigate or follow up, even if it is the only record.
- **Possible trend:** require the user's chosen recurrence or change threshold, the applicable time window, and audience/source context. Label it as a possible pattern until validated.
- **Temporary incident:** preserve incident dates or release context so a short-lived spike is not presented as a sustained shift.
- **Positive change:** surface improvements and themes worth protecting alongside negative changes.
- **Source health:** alert on failed or stale checks separately from customer feedback.
- **Digest:** group routine items to reduce alert fatigue.

VOC is a learning input for products, services, processes, and organizational conditions. Do not frame an alert as proof that an individual or team failed.
