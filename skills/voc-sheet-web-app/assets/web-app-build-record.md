# Sheet-to-web build record

## Existing system and inspection

- Workbook/project references (keep private):
- Inspected source version / date:
- Live tools available; exports used; reported versus observed facts:
- Existing entry points, global functions, scopes, menus, and deployment:
- Trigger handlers / cadence / owners / visibility limits:
- Existing tests and actual results:

| Logical object | Actual workbook/tab | Header row | Key and relationships | Aliases / status mapping | Data class | Read / write | Gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

## Interface and patch

- Design source and asset provenance:
- Supported views / unavailable views:
- Approved editing actions, if any:
- Files to add / exact patches / name-collision treatment:
- Server-configured test/production targets:
- Date serialization / escaping / selected fields / read limits:
- Demo removal / live error and freshness treatment:
- Legacy public function authorization / trigger compatibility:
- Manifest additions and why:

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
| Actual Sheet reads and reconciliation | | | |
| Web context without active Sheet | | | |
| Permitted internal user | | | |
| External signed-in user denied | | | |
| Anonymous user denied | | | |
| Unauthorized direct RPC / restricted fields | | | |
| Existing trigger and monitor regression | | | |
| Authorized writes, if in scope | | | |

- Installation and scope instructions:
- Known limitations / not-run checks:
- Previous code/deployment and rollback steps:
- Owner accepting maintenance:
