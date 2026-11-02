# Northstar classification rubric — v1.0 (2026-11-02)

This is the confirmed taxonomy the classifier must apply. It is the only instruction a model run receives besides the input records. The answer key (`answer_key.csv`) is labeled against this rubric and is never shown to the model.

All records are **SYNTHETIC**. Northstar is a fictional scheduling SaaS used across this repository's examples.

## Fields to return for each record

| Field | Allowed values |
|---|---|
| `primary_theme` | One theme from the list below, spelled exactly |
| `signal_type` | `Positive`, `Negative`, `Mixed`, `Request`, `Question`, `N/A` |
| `operational_impact` | `Blocker`, `High`, `Medium`, `Low`, `Unknown` |
| `escalate` | `Y` or `N` |

## Themes

| Theme | Include | Exclude |
|---|---|---|
| `Large-booking export reliability` | Export or download of schedules/hours, including wrong or missing data in exported files | Northstar's own invoices to the customer (use Billing) |
| `Schedule visibility` | Seeing shifts, the shared schedule, change history, reminders and notifications about shifts | App speed or crashes (use Mobile) |
| `Billing and invoicing accuracy` | What Northstar charges the customer: seats, rates, discounts, duplicate charges, refunds, pricing questions | The customer's own payroll or financial data produced by an export |
| `Onboarding and setup` | Getting started: imports, configuration, go-live, implementation calls | Ongoing support tickets after go-live |
| `Support responsiveness` | Speed and quality of help from Northstar support | Data exposure by support staff (use Privacy) |
| `Mobile app performance` | Mobile app speed, crashes, logouts | Missing features that are not performance (use the feature's theme) |
| `Data privacy and security` | Exposure of another customer's data, access control failures, security concerns | — |
| `Other` | Generic praise or complaint with no specific theme | Records about a different product (use `Out of scope`) |
| `Out of scope` | Not about Northstar scheduling at all | — |

## Signal type

- `Positive` / `Negative`: one clear direction.
- `Mixed`: the record contains both positive and negative experience.
- `Request`: asks for a capability without describing a failure that blocks current work.
- `Question`: asks for information.
- `N/A`: use only for `Out of scope` records.

## Operational impact

- `Blocker`: the customer cannot use a core function at all.
- `High`: a core workflow produces wrong or failed output, **or any charge or financial amount is incorrect or owed**.
- `Medium`: degraded, slow, or unreliable, with a workable fallback.
- `Low`: minor, cosmetic, resolved, a question, or a request.
- `Unknown`: no problem described (positive-only, generic, or out of scope).

## Primary theme when a record has more than one issue

1. Choose the issue with the highest operational impact.
2. If tied, use this order: Privacy, Billing, Export, Onboarding, Visibility, Mobile, Support, Other.
3. For a `Mixed` record, the primary theme is the negative issue, not the praised one.

## Escalate to a human (`escalate = Y`) when any of these apply

- Any incorrect, duplicate, missing, or owed charge, discount, or refund.
- Any financial figure the customer relies on (payroll, invoicing, reconciliation) is wrong because of Northstar output.
- Any data privacy or security exposure.
- An explicit threat to cancel, switch, or leave.

Questions, requests, praise, and ordinary product defects are **not** escalated on their own. Do not escalate just because you are unsure; state low confidence in `notes` instead.
