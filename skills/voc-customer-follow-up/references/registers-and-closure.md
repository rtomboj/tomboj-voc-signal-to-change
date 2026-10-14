# Registers and closure

Use the CSV header templates as portable tables. Keep each row's ID stable and unique; use ISO 8601 timestamps with timezone. Blank means unknown/not yet recorded, not zero or completed. Add fields after the supplied columns if necessary. Map existing CRM/Sheet fields instead of renaming them. These are operating records, not a replacement for restricted case notes.

## Tables

| Table | One row represents | Required information |
| --- | --- | --- |
| Follow_Up_Cases | One customer's experience needing follow-up or a research handoff | Case ID; source/record references; evidence class/audience; receipt time; trigger; severity; route; owner and backup; assignment/acceptance/due times; independent statuses; learning; closure rationale |
| Case_Actions | One customer-level action or investigation commitment | Action ID and Case ID; owner; action and intended outcome; approval basis; due time; status; completion evidence |
| Customer_Updates | One planned or actual customer communication | Update ID and Case ID; optional Change ID; owner; audience/channel; due time; status; actual sent/attempted time; content/evidence; next update |

Use semicolon-separated source/record references only for additional evidence within a case. Retain the original Source ID + Record ID pair, not an unqualified number that may collide across sources. Put private contact identifiers in the protected case system and use its reference here. Never place credentials or unnecessary personal data in an export.

Record a root cause as **Unknown**, **Hypothesis**, or **Validated**, with supporting evidence. A theme such as “billing” is not a root cause. Link any Step 4 changes through `Change_Case_Links`; the receiving skill supplies that table. One change can address many cases and one case can have multiple change dependencies.

## Independent statuses

| Dimension | Values | Evidence gate |
| --- | --- | --- |
| Engagement | Not started; Attempted; Contacted; Customer replied; Not contactable; No contact requested | A draft never advances engagement. Contacted requires a substantive authorized message/conversation; reply requires an actual customer response. |
| Delivery | Not assessed; Investigating; Plan agreed; In progress; Delivered; No action planned | Plan agreed requires recorded agreement, not an agent suggestion. Delivered requires action evidence; a company decision to decline is No action planned, not Delivered. |
| Customer outcome | Unknown; Unresolved; Partially resolved; Resolved confirmed; Disputed; Not applicable | Resolved confirmed needs explicit confirmation or agreed objective verification of the customer's outcome. Do not infer satisfaction from technical success. Use Not applicable for pure praise/research, not unreachable complaints. |
| Administrative state | Open; Waiting; Closed; Reopened | Waiting retains an owner and next check. Closed needs a reason/date and the review below. |

Use action statuses **Proposed / Approved / In progress / Done / Cancelled**, and update statuses **Draft / Scheduled / Sent / Attempted / Failed / Not possible / Cancelled**. Scheduled is not evidence of sending. Done needs completion evidence. Cancellation needs a reason and must not erase a still-owed commitment.

## Closure review

Before administrative closure, confirm:

1. The source and contact/authority position are traceable.
2. Each customer-level commitment is completed, explicitly withdrawn with a reason, or transferred to a named accepting owner and linked record. Record acceptance evidence for transfers; a proposed handoff is insufficient.
3. The customer outcome is accurately recorded. An unreachable customer can be administratively closed after the approved retry policy, but the outcome remains Unknown or Unresolved. A declined request may remain Unresolved or Disputed.
4. The decision was communicated where authorized and possible, or its limitation is documented.
5. Any longer-running change and future update obligation remain assigned and visible. Closed cases with owed updates must still appear in the update queue.
6. The lesson, root-cause confidence, closure reason, and closure date are recorded.

Reopen when new evidence or the customer contradicts the supposed outcome, or when the remedy fails. Preserve the original timestamps and prior status in history; do not reset SLA performance. Customer satisfaction, relationship health, technical completion, and case administration are separate concepts.

## Dashboard definitions

- **Acceptance compliance:** cases accepted by their due time / cases whose acceptance deadline has passed. Show missing acceptance and unassigned cases, not just accepted ones.
- **First-contact compliance:** contactable, authorized cases contacted by their due time / contactable, authorized cases whose first-contact deadline has passed. Show exclusions and not-contactable counts separately; never treat them as successful contact.
- **Time to contact:** receipt-to-first-meaningful-contact using the configured clock; show median and upper percentile alongside open overdue cases and collection delay.
- **Update compliance:** updates delivered by the promised time / updates whose due time has passed, including obligations on administratively closed cases. Exclude only reason-coded withdrawn obligations; show that count.
- **Confirmed resolution:** resolved-confirmed cases / outcome-eligible cases in a stated received cohort and observation window. Show pending, unresolved, disputed, and not-contactable counts so a closure-only denominator cannot inflate success.
- **Quality:** sampled records with complete evidence, correct status, and kept commitments; record sampling method. Show reopen counts and reasons. Do not present a satisfaction score for an individual employee.

Keep backlog age and missed commitments visible. Use a distinct Follow_Up_Dashboard if building a workbook; preserve benchmark and monitoring dashboards. Status colors must include text labels.

## Pilot acceptance scenarios

| Input | Required behavior |
| --- | --- |
| Same verified source record arrives twice | One case or explicit link to the existing case; no duplicate outreach |
| Two people describe the same problem | Separate customer cases; optional shared change |
| Public anonymous review, no response authority | Research/handoff packet; no identity inference or invented contact |
| Serious signal arrives outside staffed hours | Existing incident route or a visible coverage gap; no fabricated SLA |
| Owner absent or transfer unaccepted | Original/fallback owner and original due time remain visible |
| Message drafted but not sent | Engagement unchanged; send test not run |
| Customer silent after attempted calls | No confirmed resolution; bounded retry and reason-coded disposition |
| Technical fix delivered but customer disputes outcome | Delivered and Disputed can coexist; reopen/escalate |
| Case closed while a product update is still owed | Update remains in due queue with owner and linked change |
| Failed source returns no records | Monitoring fault; not “customers are happy” |

These are workflow acceptance checks. They require judgment and, for live communication or system integration, actual execution evidence. A template/schema check alone cannot pass them.
