# Design source, data contract, and Apps Script conversion

Read this at Step 0, complete the contract after inspecting the Sheet, and finish the conversion checklist before delivering installation files.

## Step 0: establish the source

Ask for the existing design first and accept a file, link, or design-project export (including a Claude Design zip). No particular design provider is required. Require inspectable source before backend work. Reuse what is already supplied. Record source/version, source-access evidence, routes/screens, responsive layout, interactions, and assets. Inspect code, including embedded bundles, to find the actual data assumptions. A screenshot is a useful visual reference; a rendered page alone cannot reveal all assumptions. Request an HTML/source export if the link does not expose inspectable source. Capability discovery and asking for that export may continue; backend generation waits.

A user without a design can create/select a minimal design with the assistant. Record that source explicitly rather than silently choosing a generic dashboard. Keep its visual intent through conversion; show any necessary visual changes and why. Do not copy an inaccessible published artifact by guessing at its internals.

## Design data-contract check

Output this table in the build record **before backend generation**. Add rows for every screen's fields, cards, counts, charts, joins, sorting/priority rules, and actions. Record exact names observed; the rows below are illustrations, not a schema to impose.

| Screen / element | Design expects: key, type, values or formula | Actual tab / header row / exact headers | Mapping, join or derivation and execution location | Missing/ambiguous behavior | Evidence / check |
| --- | --- | --- | --- | --- | --- |
| Monitoring health | `status = OK` | `Run Log`, row 4, `Result`, `Checked At` | GS maps SUCCESS to healthy; PARTIAL to partial; FAILED/BLOCKED to failed/blocked | No run is unknown; never invent OK | Reconcile with selected source rows |
| Follow-up queue | `overdue`, `owner`, `nextUpdateAt` | Inspected case/update tabs and key columns | GS joins on stable case ID; applies existing timezone and actual due-time rule | Missing due date is unknown, not overdue; critical unowned cases keep priority | Reconcile IDs, exact boundary times and priority |
| Change count | Count of active changes | Missing register | GS returns unavailable plus reason | UI shows Not available, not 0 | Missing versus empty test |

Give the designer authorized CSV exports of every relevant tab, including monitoring and Step 3/4 registers; use sanitized/synthetic exports when sharing outside the approved audience. A design's `assumedColumns` are unverified until compared with actual headers. Generate agreed missing tabs from repository templates through setup. Dropdowns and status chips must use the Step 3/4 register references (for example, Resolved confirmed, Plan agreed, No action planned, Not contactable and Cancelled), not simplified design labels.

For each derived value, specify inputs, denominator, filters, excluded/unknown records, timezone/clock, status aliases, and null/empty behavior. Identify which system already owns a rule; reuse its meaning instead of replacing it. Distinguish open cases from closed cases still owing updates, app-read time from source-check time, and public research drafts from accepted operational obligations. Resolve many-to-many links and qualified source/record IDs before counting.

Default location is **GS for business logic**, with the HTML receiving an authorized view model. Keep access checks/redaction, status normalization, joins, REAL/SYNTHETIC/unknown separation, deadlines, queues and authoritative totals on the server. Keep rendering, navigation, copy-to-clipboard and display-only filters/sorts in the browser. The browser may count visible rows as a labeled subset; it must not claim full-population totals from one page. Include filter/data-class context in server requests and responses, validate it, and preserve the selected data class across navigation. Never accept a client workbook/tab/role as authority.

Do not implement duplicate business formulas on both sides. If a design contains formulas in browser code, port them to GS or document why a display-only calculation remains there. Reconcile server results against the inspected Sheet and the design's intended behavior using identified synthetic or redacted rows. Mark contract rows mapped, unavailable, or blocked. Resolve any ambiguous field used by an active feature before generating its backend; ask only the targeted question or disable that feature. Retain unavailable screens visibly without creating production tables to satisfy the design.

Optional visual conventions for the synthetic Northstar example: a dashed edge with flat tint can distinguish proposed work; collapse empty board lanes into a one-line list. Confirm these preferences against the supplied design rather than imposing them.

## Bundle-to-Apps-Script conversion checklist

Record each item as done, not applicable, or blocked, with an artifact/check. This is the repository's explicit baseline removal list; do not imply it reproduces an unavailable external feedback item. Add any user-supplied removal list when available.

| Check | Conversion required |
| --- | --- |
| Bundle unpacking | Inspect nested/escaped HTML, Blob/data-URL loaders, packed assets and generated entry scripts. Extract the intended UI; remove export/bootstrap wrappers after replacing their responsibilities. Do not paste an opaque outer artifact shell into Index. |
| Framework/build runtime | Deliver browser-ready JS/CSS. Compile JSX/TS/module dependencies when required or port to plain JS while preserving appearance/behavior; do not paste npm imports, Node-only calls or dev-server paths into HTML Service. Document retained dependency versions/licenses. |
| Fonts | Inventory font families, weights, URLs and licenses. Prefer a declared system-font fallback for the first private pilot; retain an approved HTTPS font dependency only after verifying it loads in the actual app. Check layout with fonts blocked. |
| CDN/styles/icons | Prefer bundled CSS and local/trusted assets where practical. Replace runtime CSS compilers/dev CDNs, local paths and artifact-host-only resources. For retained external dependencies, pin versions where supported, use HTTPS, record purpose/license and test a blocked load. No real row data in third-party URLs. |
| HTML Service | Use evaluated templates and trusted partial includes for Styles/App; no generic client-controlled include endpoint. Check iframe navigation/link targets and HTTPS active content under current Google restrictions. Test actual hosted rendering, not only a local HTML file. |
| Data/RPC | Remove fixture loaders and placeholder REST/getTab calls once replaced with asynchronous google.script.run handlers. Keep loading, empty, unavailable, permission-denied and failure states distinct. Never fall back to demo rows on a failed live read. |
| Fixed clock | Remove hard-coded today/now and fixed reporting windows in live mode. Use a server-generated as-of time and the established timezone; recompute on refresh and show snapshot age. Keep any deterministic test clock confined to the explicit test harness. |
| Demo payload | Remove embedded company/customer records, fabricated trend values, random metrics, simulated outages and placeholder workbook IDs. Show synthetic rows only when explicitly classified from the mapped test data, separated before totals. |
| Prototype controls | Remove prototype toggles that conflict with the chosen policy (including REAL/SYNTHETIC in REAL-only mode), fake role/user switches, simulated save/send/success actions and cosmetic security gates. Replace role switches with server authorization and saves with the tested endpoint. Keep requested but unsupported controls disabled with a reason. No browser-only write that pretends to update the Sheet. |
| Export scaffolding | Remove artifact-host bridges, preview-only postMessage handlers, eval/unpack bootstraps, demo analytics, service-worker registration, unused mock adapters and duplicate initialization. Retain only reviewed code needed by the converted interface. |
| Storage/secrets | Remove embedded tokens, internal IDs intended to remain server-side, raw customer caches and stale demo localStorage keys. Keep harmless UI preferences isolated; no sensitive shared browser persistence by default. |
| Visual parity | Compare each retained screen, navigation, responsive layout, fonts, empty/error states, selection persistence and record details against the source. Record deviations and screenshots when possible. Do not replace the user's design with a generic UI merely because conversion is easier. |

Search the generated files for fixture constants, fixed dates, demo fallback, artifact-host URLs, external script/style/font URLs, imports/require, eval, postMessage, serviceWorker, localStorage and placeholder IDs. Inspect each hit in context; legitimate date fixtures can remain only in explicit test files. Treat this search as a review aid, not proof of correctness. Reconcile representative counts/queues with Sheet rows after conversion.
