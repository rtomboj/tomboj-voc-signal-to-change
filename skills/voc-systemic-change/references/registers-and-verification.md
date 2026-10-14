# Registers and verification

Use the CSV templates with a brief per initiative. Keep one authoritative source of truth; an existing backlog can supply these fields through a documented mapping. Use stable unique IDs and ISO 8601 event timestamps with timezone. Leave unknown facts blank and identify gaps in the brief.

## Tables and links

**Change_Register:** one row per systemic opportunity, including an evidence reference, fix type, hypothesis/confidence, decision and authority, accountable owner/acceptance, lifecycle, next milestone, measurement plan, results, review, and report-back obligations. `Brief Reference` points to the fuller plan; the compact register does not replace it. Use `Merged Into` only for a surviving Change ID and prevent self-links/cycles.

**Change_Case_Links:** one row per Change ID + Case ID relationship. Include the customer communication owner, receiving change owner, acceptance time/evidence, next update due, and obligation status. Treat `Proposed` links as unaccepted handoffs. Use `Active`, `Fulfilled`, or `Ended` only with evidence; `Ended` needs an explicit reason. No orphan IDs or duplicate pairs.

Step 3 owns the customer case and `Customer_Updates`; Step 4 owns the change and link table. Put the Change ID on customer updates when applicable. A change with no individual cases can still proceed from other evidence; record who receives its internal/customer-wide report-back. Do not invent Case IDs to satisfy a template.

For CSV exports, use decision values **Accept / Investigate / Defer / Decline / Merge / Stop / Reopen**. Leave Decision blank while a recommendation is still Proposed; put the recommendation in the brief. Record the current authorized decision and preserve prior decisions in the authoritative system's history or a dated decision log.

For standalone Step 4 use, accept references to external cases and record the authoritative system/link in the brief. Verify them where access exists; otherwise mark them unverified. Do not claim cross-system validation from a local CSV check.

## Lifecycle gates

| State | Required evidence |
| --- | --- |
| Proposed | Problem/opportunity, source evidence, proposed fix type, intake owner; not yet approved |
| Investigating | Named investigation owner, question to resolve, next decision date |
| Accepted | Dated authorized accept decision, named accountable owner and recorded acceptance |
| Planned | Approved scope/resources, dependencies, milestone, baseline, success criteria, measurement window, communication plan |
| Implementing | Execution started with a recorded milestone; preserve plan and update commitments |
| Verifying | Delivery evidence plus observed results pending against the agreed criteria |
| Sustained | Results support criteria through the observation window, adverse effects reviewed, named reviewer/date, report-back disposition recorded |
| Deferred | Decision/rationale and a dated review or objective revisit condition with owner |
| Declined | Decision/rationale and report-back disposition; not a successful improvement |
| Merged | Valid surviving Change ID; links/evidence and outstanding obligations transferred without erasing provenance |
| Stopped | Authorized stop decision/reason, impact/rollback treatment, communication disposition |
| Reopened | New contradictory evidence or failed remedy, accountable owner, revised next step; retain prior history |

Do not advance a row merely to fill a dashboard. **Sustained** is this design's verified-improvement state, not a permanent guarantee. Later recurrence can reopen it. Deferred, declined, merged, and stopped are administrative outcomes, not positive results.

## Verification plan

Specify the unit of analysis (case/account/user/transaction), baseline period, affected cohort, outcome numerator/denominator, collection route, comparison if feasible, observation window, and success/adverse-effect thresholds. Distinguish expected impact from observed results. Record source health and missingness in both periods.

Example only: a billing handoff pilot targets fewer repeat contacts within seven days of a billing case. Compare eligible cases in stated windows and show both counts and rates. If volume falls from 100 cases to 20, raw contact counts alone are insufficient. If the monitor is down during the pilot, do not interpret a lack of public complaints as confirmation. A before/after improvement without a valid comparison is descriptive, not proof of causation.

Track both delivery (milestones, adoption, training participation) and experience (task completion, recurrence, effort, complaints, customer confirmation). Include cost/workload/regressions when relevant. Avoid interpreting adoption or attendance alone as success.

## Report-back and dashboard

Show opportunities by decision/state/fix type, accepted owner gaps, aged decisions, blocked delivery, due updates, changes awaiting verification, and evidence-supported results. Show deferred/declined reasons. Keep customer case resolution in its own view; never sum “changes shipped” as “customers resolved.”

Every report-back should state the original concern, decision, action, observed result or uncertainty, and next step. A sent update needs actual delivery evidence; a proposed draft remains a draft. Keep due obligations visible after case closure or a change's administrative disposition. When a promised product update is no longer relevant, explicitly end or renegotiate it rather than silently deleting it.

## Acceptance scenarios

| Input | Required behavior |
| --- | --- |
| Five syndicated copies of one review | One independent report with five provenance links |
| One severe report with limited corroboration | Prompt investigation, without a trend/prevalence claim |
| A popular request conflicts with strategy/capacity | Explicit decision and tradeoffs; no automatic roadmap promise |
| Product fixes a defect; customer still dissatisfied | Verifying/delivered change and unresolved customer case remain distinct |
| Work shipped yesterday; observation window is 30 days | Verifying, not Sustained |
| No new reports while a source fails | Measurement gap; no claimed improvement |
| Work is deferred or declined | Reason, owner, review condition where relevant, and report-back disposition |
| Change merged into another | Valid surviving ID; all cases and update obligations retained |
| Case administratively closed with active change link | Customer communication obligation remains discoverable |
| Improvement later reverses | Reopened with evidence and owner; history preserved |

Classify each check as passed, failed, blocked, or not run. Local template validation verifies structure only. Delivery, customer communication, and business results need actual evidence from the relevant environment.
