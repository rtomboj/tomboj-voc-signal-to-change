# Sheet-to-web build record

## Step 0: design source gate

- Design file/link and version/date (keep private when appropriate):
- Actual source inspected versus rendered appearance only; missing export:
- Screens, interactions and visual reference:
- Gate: ready / blocked; reason and next action (no backend before ready):

## Existing system and inspection

- Workbook/project references (keep private):
- Inspected source version / date:
- Live tools available; exports used; reported versus observed facts:
- Existing entry points, global functions, scopes, menus, and deployment:
- Trigger handlers / cadence / owners / visibility limits:
- Existing tests and actual results:

| Job | Observed capability and target permission | Selected route: direct / connect / manual | Missing evidence / next step |
| --- | --- | --- | --- |
| Drive discovery/content | | | |
| Sheet reads | | | |
| Sheet edits | | | |
| Apps Script source reads | | | |
| Apps Script edits | | | |
| Trigger inventory | | | |
| Deployment/versioning | | | |
| Browser and account access tests | | | |

## Workbook mapping

| Logical object | Actual workbook/tab | Header row | Key and relationships | Aliases / status mapping | Data class | Read / write | Gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

## Interface and patch

- Design source and asset provenance:
- Design data-contract gate: mapped / unavailable / blocked per row; ready for backend:

| Screen / element | Expected key/type/status or derivation | Actual tab / header row / exact headers | Mapping / join / formula / execution location | Null, unavailable and ambiguity handling | Evidence / reconciliation |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

- Logic allocation: GS business rules/authorization; browser presentation; justified exceptions:
- Derivation filters, denominators, timezone/as-of, data-class separation and pagination totals:
- Conversion checklist results (done / not applicable / blocked, with evidence): bundle; runtime; fonts; CDN/assets; HTML Service; RPC; fixed clock; demo data; prototype controls; export scaffolding; storage; visual parity:
- Supported views / unavailable views:
- Approved editing actions, if any:
- Files to add / exact patches / name-collision treatment:
- Server-configured test/production targets:
- Date serialization / escaping / selected fields / read limits:
- Demo removal / live error and freshness treatment:
- Legacy public function authorization / trigger compatibility:
- Manifest additions and why:
- Scope report before paste: existing -> required, explicit/inferred scopes, OnlyCurrentDoc conflicts:
- Trigger creators requiring editor reauthorization; target project; actual consent evidence / limits:

| Paste order | Exact resolved filename/type | Add or inspected-source patch | Version | Generated / supplied / installed-reported / installed-verified | Evidence / next action |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## Private deployment

- Workspace deploying account/domain (verified or not):
- Intended audience / additional roles:
- Organization-only access option:
- Execution identity and Sheet permissions:
- Server identity/redaction policy:
- Deployment authority, version, test URL, deployed URL:

## Tests and handoff

| Check / environment / version | Status | Evidence | Next action and owner |
| --- | --- | --- | --- |
| Local/static checks | | | |
| Design-to-Sheet derivations and representative rows | | | |
| Hosted visual parity, font/CDN failure and data-class navigation | | | |
| Actual Sheet reads and reconciliation | | | |
| Web context without active Sheet | | | |
| Permitted internal user | | | |
| External signed-in user denied | | | |
| Anonymous user denied | | | |
| Unauthorized direct RPC / restricted fields | | | |
| Existing trigger and monitor regression | | | |
| Scope consent per affected owner/project and scheduled result | | | |
| Authorized writes, if in scope | | | |

- Installation and scope instructions:
- Known limitations / not-run checks:
- Previous code/deployment and rollback steps:
- Owner accepting maintenance:

## Interactive checkpoint

- Last completed step and evidence:
- Files generated / supplied / installed-reported / installed-verified:
- Tested scope/results and deployed version (distinct from file installation):
- User-run function and expected output:
- Returned result, diagnosis, and corrected file/version:
- Connection choices already made (do not ask again):
- Next unresolved step / targeted question / work that can continue:
