# Routing and timing

Use this reference to turn signals into a small, workable response policy. The following is a proposed pilot design, not a published standard. Existing contractual, regulatory, incident, or customer commitments take precedence; obtain those from the responsible owner rather than guessing.

## Signals and routing

| Signal | First decision | Proposed receiving role |
| --- | --- | --- |
| Unresolved experience, explicit request for contact, or repeat failure | Is there a verified contact route and an existing case? | Account/experience owner or service supervisor |
| Low score or meaningful score movement | Check the comment and context; a score alone does not establish cause | Account/experience owner |
| Serious harm, widespread outage, privacy/security concern | Invoke the existing specialist/incident route immediately | Incident/specialist owner plus customer communication owner |
| Constructive suggestion or meaningful praise | Thank/clarify where appropriate; consider learning or an improvement opportunity | Experience owner; change intake if broader |
| Several independent reports of a similar issue | Check source, audience, window, duplicates, and operational evidence | Case owners plus proposed change owner |
| Failed collection, wrong company, duplicated evidence | Repair or reconcile monitoring; do not fabricate a customer case | Monitoring maintainer |

Apply confirmed Step 2 signal rules; do not silently add recurring alerts or trend thresholds. Keep feedback about competitors as research, not cases implying authority over those customers.

## Pilot timing options

Choose a policy the team can staff. XM Institute's 2023 guide suggests first contact within 24–72 hours; that is guidance, not a universal resolution deadline. The table below is Tomboj's proposed starting policy and must be confirmed before being called an SLA.

| Tier | Assignment/acceptance proposal | First meaningful contact proposal | Update proposal |
| --- | --- | --- | --- |
| Critical | Route immediately through the existing incident/on-call process | Use the incident policy; surface any missing coverage immediately | Use incident policy and named communication lead |
| High: blocked outcome, repeated failure, significant ongoing impact | Accept within 4 staffed hours | Within 1 business day | At least each business day while actively blocked, or sooner if promised |
| Standard: isolated complaint or unresolved issue | Accept within 1 business day | Within 2 business days | Agree the next update during first contact, normally within 3 business days |
| Learning: suggestion or praise without an open problem | Triage within 2 business days | Within 3 business days if follow-up is useful and possible | Give a decision/update date if an investigation is accepted |

Do not make a universal “close within 30 days” rule. Set resolution targets after understanding the issue; define a separate next-update deadline when resolution is uncertain.

## Define clocks explicitly

- Store feedback time, detection/receipt time, case-created time, assignment, acceptance, attempted contact, first meaningful contact, and customer reply separately.
- Start the operational response clock at detection/receipt. Show collection delay separately so a weekly monitor does not look instantaneous. Preserve the original clock through reassignment.
- Record policy version, timezone, staffed hours, holidays, what “business day” means, and any permitted pause reason. Use ISO 8601 timestamps with UTC offset for events and due times. Do not assume “24 hours” means one business day.
- Example only: staffed hours are Monday–Friday, 09:00–17:00 America/New_York, with no holiday. A four-staffed-hour acceptance target received Friday at 16:00 is due Monday at 12:00 local time. A 24-elapsed-hour target is due Saturday at 16:00. Store the date-specific offset, including daylight-saving changes.
- Count a substantive, authorized outgoing message or completed conversation as first meaningful contact when it addresses the specific issue and explains a next step. Log unanswered calls as attempts. A customer reply is a separate event; do not wait for it to hide an outgoing-response breach.
- A missing contact route is **Not contactable**, not “responded.” Report these cases separately. Respect explicit no-contact preferences; do not keep retrying.

## Ownership and escalation

Name a customer communication owner, backup/fallback, remedy decision-maker, and escalation role. For B2B, coordinate across account contacts without disclosing one person's confidential comments to others. An existing CSM can coordinate while a trained specialist handles the conversation.

Allow centralized, distributed, or hybrid teams based on context. Do not require the employee named in a complaint to make the callback. Competence, authority, impartiality, language/accessibility needs, and customer preference matter.

Escalate when the owner has not accepted by the due time, a promised update is missed, the remedy exceeds authority, the issue recurs, the impact changes, or the customer disputes resolution. Notify the fallback according to the approved route; keep the original owner accountable until acceptance is recorded. Log reassignment reason and acceptance. Never silently reset a deadline.

Propose a bounded retry policy: two further attempts on separate staffed days through the permitted channel, then an administrative review. Treat this as a configurable pilot choice. Record attempt times and the final reason; unanswered contact is not customer resolution. Keep any still-owed company decision/update assigned even if outreach ends.

## Decision rights

| Role | Define before launch |
| --- | --- |
| Follow-up owner | Approved remedies, credit/waiver limit if any, approved workarounds, access to records |
| Supervisor | Exceptions, reassignment, support for difficult conversations, quality review |
| Specialist or product owner | Technical facts, investigation commitments, authorized release information |
| Change decision-maker | Cross-team policy, funding, staffing, or product-priority decisions |

Use **Unknown — approval required** rather than inventing a monetary allowance or roadmap authority.
