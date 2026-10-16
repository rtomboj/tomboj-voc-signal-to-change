# Inspect and adapt the current system

Use this reference before writing the web adapter. Earlier VOC steps define meanings and quality expectations; they do not guarantee the current workbook matches a fixed schema.

## Inspect once, then map

| Area | Establish | Preserve |
| --- | --- | --- |
| Workbook | Actual tab/header names, header row per tab, column types, key quality, working versus historical tables | Values, formulas, protected ranges, titles, existing IDs |
| Relationships | Source/record to case; action/update to case; case to change | Separate customers and many-to-many change links |
| Operational status | Actual status vocabularies, due-time semantics, source health, data-class treatment | Unknown, missing, failed, and unverified distinctions |
| Script | Existing globals, helpers, entry points, scopes, configuration conventions | Monitoring logic, notification recipients, trigger names/schedules |
| Design | Screen list, routes, data adapters, assumed fields, demo data | Visual direction and supported behavior |
| Deployment | Current versions, access policy, execution identity, maintainer | Existing working deployments until a replacement is tested |

Use existing read helpers only after checking their assumptions. A helper that assumes header row 4 for every tab is unsuitable when newer operational tables begin on row 1. Detect required headers in a bounded range such as the first 20 rows, show any ambiguity, and record the selected row per table.

Build a mapping with: logical object, workbook reference, exact tab, header row, stable key, selected fields, aliases, data class, read/write choice, validation result. Store private workbook IDs server-side. Resolve duplicate IDs, duplicate headers, ambiguous aliases, or inconsistent evidence classes before using them for joins or conclusions.

Distinguish a missing table from an empty existing table and an inaccessible existing table. Keep unsupported screens in a clear unavailable state; do not create empty production registers to make the UI look complete. Add a new table only if needed for a user-approved function and document it as an additive change.

## Adapt meanings, not only labels

- Match actual run-log timestamp/result columns and status values. For example, a UI expecting "Run Status = OK" must adapt when the monitor emits "Result = SUCCESS / PARTIAL / FAILED / BLOCKED". Partial is not full success.
- Do not classify monitoring rows as real/synthetic from their LIVE/TEST execution mode alone: an installed fixture check can run against a test workbook, while real records may have been captured manually. Define data class per table/source and keep unclassified data visible.
- Resolve Source ID + Record ID pairs, including multiple references. Do not assume every record reference contains a single colon or a globally unique numeric suffix.
- Preserve the received/due time and timezone policy already in use. Replace fixed prototype "now" and date windows with live/configured values; do not retroactively invent staffed-hour SLAs.
- Derive freshness from real successful reads/checks. Track app-read time separately from source-check time, original feedback date, and snapshot time.
- Give unavailable metrics an explanation rather than calculating zero from absent columns.

## Design intake

A downloaded design may be a packed HTML bundle with embedded scripts/assets instead of editable source. Inspect/unpack it locally when necessary; do not assume it can be pasted unchanged into an Apps Script HTML file. Inventory third-party assets and licenses before redistributing them.

Replace embedded customer records, sample-data fallback, fixed dates, simulated outages, fake role controls, and placeholder workbook IDs in live mode. Do not let a failed live read silently fall back to demo records labeled real. Cache only if deliberately designed: keep identity, permissions, company, data class, version, and freshness boundaries, and do not persist sensitive raw rows in shared browser storage by default.

Preserve escaping and validate links. Never interpolate untrusted feedback as executable HTML. Keep data out of script-template contexts where it could terminate a script element. Exclude secrets and unnecessary contact data from browser responses, exports, and screenshots.

## Handoff when tools are limited

Proceed with available exports and report which facts are inferred versus observed. Provide complete files and line-independent patches against the inspected version. Supply exact editor steps and ask only for missing information that changes the mapping or deployment. A Drive connector reading a file does not prove it can edit a bound Apps Script project or inspect its triggers.
