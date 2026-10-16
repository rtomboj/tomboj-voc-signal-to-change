# The four-part workflow

The repository provides portable AI-guided skills, templates, and validation utilities. It is not a hosted VOC platform or a preconfigured production deployment. Each skill can produce reviewable artifacts without new account access; Step 2's scheduled monitoring specifically needs a user-configured Google Workspace environment.

| Step | Inputs | Authoritative output | Handoff |
| --- | --- | --- | --- |
| 1. Benchmark | Company website and confirmed research scope | Dated Markdown report and Excel benchmark | Source IDs, Record IDs, evidence classes, audiences, taxonomy, readiness decisions |
| 2. Monitor | Both Step 1 files plus confirmed routes/cadence | Preserved working copy, source-specific monitoring code, run log, new records, monitoring dashboard | Individual signals and possible patterns, provenance, source health, response-route limits |
| 3. Customer follow-up | Signals or directly supplied feedback; user role and authority | Case, action, and update records; operating/coaching plan | Accepted or proposed company-change packet, source/case links, continuing customer commitments |
| 4. Company change | Evidence packets, linked cases, strategic constraints, decision authority | Change register, decisions, delivery/verification plans, results and report-back | Verified learning and approved changes to operations and monitoring |

Step 3 contains three research workstreams: immediate response mechanics, training/coaching, and internal action planning with customer report-back. Step 4 handles larger product, policy, process, team, department, and organizational changes. These workstreams do not replace Steps 1 and 2.

An optional [Sheet Web App bonus](../skills/voc-sheet-web-app/SKILL.md) follows the four parts. It adds an interface to their current outputs rather than introducing another business stage. The assistant inspects the actual Google Sheet and Apps Script, maps their structure, and adds a private organization-only web layer. The earlier contracts guide meaning; the existing system determines its concrete mapping. A design export is optional. See [the provider-neutral starting prompt](../skills/voc-sheet-web-app/assets/web-app-test-prompt.md).

The assistant inspects the capabilities available in the current user's session, offers supported connection/authorization or manual routes for missing capabilities, and remembers the chosen route per job. For example, it can read the working Sheet through a connector while delivering complete Apps Script files for the user to paste. Returned editor/test output feeds the next correction and test. A change of assistant provider does not require rebuilding the prior stages.

## Preserve the joins and the evidence

Keep Source ID + Record ID as a pair across stages; include the original evidence reference. Never use a display name or profile URL as a unique customer/review identifier. Case IDs identify customer experiences. Change IDs identify company improvements. The Change_Case_Links table provides the many-to-many relationship without collapsing separate customers into one case.

Keep evidence class, audience, confidence, frequency, and operational impact separate. A public sample does not establish population prevalence. Official news or vendor-selected stories can support research but are not independent customer complaints. A failed source check is a monitoring problem, not a positive experience result.

Prefer one source of truth for each operational object. Link to an existing CRM case or product backlog when available. Avoid two editable copies of the same plan. Keep the original Step 1 benchmark intact and do not repurpose its historical dashboard as a current case queue.

## Start at the appropriate point

For the full sequence, complete Steps 1 and 2 first. For an urgent complaint or a supplied improvement packet, start at Step 3 or 4 with clearly stated evidence gaps. Do not delay useful customer help merely to rebuild a benchmark.

The user can work as an authorized operator or an external researcher. Research mode produces drafts and proposed handoffs. It does not imply customer identity, acceptance of responsibility, or permission to contact a reviewer.

## Keep completion honest

- A collected record is not an investigated fact.
- Assignment is not accepted ownership.
- A draft is not a sent message.
- A delivered workaround is not a confirmed customer outcome.
- An administratively closed case can still have an unresolved outcome or an owed update.
- A shipped change is not a verified improvement.
- A quiet feed is not proof of success when collection or coverage is missing.

See the [synthetic walkthrough](../examples/closed-loop/walkthrough.md) for connected records and [validation guide](validation.md) for checks and limits.

## Research basis and source limits

The new skills use a deliberately compact, checked evidence base:

| Source | What it supports | What it does not establish |
| --- | --- | --- |
| [Bain inner loop, 2015](https://www.bain.com/insights/the-net-promoter-systems-inner-loop/) | Timely feedback, follow-up, and employee learning | A universal callback owner or guaranteed loyalty uplift |
| [XM Institute closed-loop guide, 2023](https://www.qualtrics.com/m/www.xminstitute.com/wp-content/uploads/2023/08/XMI_HTG_ClosedLoopProgram_PDF-1.pdf) | Practical program design and response guidance | A binding 24–72-hour SLA or a universal 30-day closure requirement |
| [Bain huddles, 2015](https://www.bain.com/insights/huddle-up/) | Team learning and escalation; documented Apple, Telstra, and Zappos practices | Independent proof that a particular coaching cadence causes retention |
| [Bain outer loop, 2015](https://www.bain.com/insights/the-net-promoter-systems-outer-loop/) | Cross-functional decisions, prioritization, ownership, and communication | Automatic roadmap approval or evidence that deployment equals impact |

These are originator/practitioner and vendor-affiliated sources, not a systematic academic review. Sources were checked October 14, 2026. The templates, status model, coaching exercises, suggested timing tiers, and acceptance gates are original Tomboj operating design. No numerical retention or revenue claim is used to justify them.
