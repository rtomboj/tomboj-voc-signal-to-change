# Synthetic closed-loop walkthrough

All names, records, dates, decisions, and operational evidence in this example are fictional. No customer was contacted and no change was deployed. The populated CSVs illustrate valid record relationships; they do not demonstrate real business improvement.

## Source packet

Northstar Scheduling has reports of failed exports for large bookings. REV:R101 belongs to a customer verified in synthetic support case SUPPORT-17; REV:R102 is an anonymous reviewer with no legitimate response route. A repost of R101 is duplicate provenance, not an additional independent report. The broader incidence and affected-account count are unknown.

The [registers](registers/Follow_Up_Cases.csv) retain two cases. CASE-001 received a CSV workaround and confirmed that this week's export opened, but next week's still failed. CASE-002 was administratively closed because no contact route existed; its customer outcome remains **Unknown**. Its evidence still contributes to CHANGE-001.

Dates and role acceptance in the CSVs are deliberately filled with synthetic example facts. In a real run, leave unconfirmed facts blank and mark the relevant check blocked. The example due times do not establish an SLA for another company.

## Customer follow-up

Jamie retains communication ownership for CASE-001. [ACTION-001](registers/Case_Actions.csv) is done because the workaround was delivered; ACTION-002 remains proposed to investigate the remaining failure. Delivery is **Delivered**, customer outcome is **Partially resolved**, and administrative state is **Open**. These dimensions are intentionally different.

Coaching note: acknowledge the useful workaround, then check the customer's original goal. Do not close a case simply because an attachment was delivered. Confirm an investigation owner, preserve the update commitment, and review whether team closure targets or tooling encourage premature closure. This example does not establish misconduct.

## Customer update

**Draft — not sent:** “Thanks for confirming that this week's export opens. I understand that next week's schedule still fails. I will coordinate the next check and update you by October 15 at 12:00 UTC, even if the investigation is still underway.”

The [update register](registers/Customer_Updates.csv) records the draft without an occurrence timestamp or delivery evidence. The unknown reviewer has a **Not possible** communication disposition, not a fabricated contact. An internal report-back remains assigned on the change.

## Change brief

[CHANGE-001](registers/Change_Register.csv) addresses export reliability. The synthetic product lead accepted it, a product owner accepted accountability, and a release record exists. Root cause remains a hypothesis; shipping the change does not validate the causal explanation or the customer outcome.

The change remains **Verifying**. Its [case links](registers/Change_Case_Links.csv) preserve the active update obligation for CASE-001 and the explicitly ended customer-contact obligation for CASE-002. The company still owes an internal result through the change owner. If the same issue affects another customer, add a separate case link rather than merging customers.

## Verification

The agreed observation window is 30 days from the October 14 rollout, with an initial November 13 review. The public monitor has failed for three days, so absence of new reports cannot confirm success. Assign monitor repair separately, recover missing observations where permitted, and record remaining coverage gaps. An accountable reviewer must decide whether the window provides sufficient evidence or needs extension.

A proposed measure is successful large-booking exports / eligible large-booking export attempts, with sample sizes, cohort definition, baseline period, and adverse checks for incomplete or incorrect data. Baseline values and numerical success thresholds are **not available** in this example. They require agreement before claiming improvement; no favorable result is invented. The November review is a checkpoint, not an automatic closure date.

Next decisions: accept the remaining investigation, confirm success criteria and baseline, repair monitoring, verify the original customer task, and report what is known. A customer could be resolved before the company change is verified; the two records remain independent.

## Run the structural check

From the repository root:

```bash
python scripts/validate_loop_registers.py examples/closed-loop/registers
```

A structural pass verifies that the required record fields and selected evidence gates are present. It does not validate fictional evidence, approve due times, or prove that any customer outcome improved.
