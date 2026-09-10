# Company-specific benchmark output

Use this reference after the user confirms the source register and scope.

## Workbook design

Tailor labels and optional columns to the company, but preserve these six core tabs.

### `Company_Profile`

One row per company, brand, product, or market entity needed to interpret the benchmark.

- Entity ID
- Company
- Parent
- Brand/Product
- Official URL
- Business Model
- Buyer Type
- User/Customer Type
- Delivery Model
- Country/Market
- Location Model
- In Scope
- Evidence URL
- Evidence Type
- User Confirmed
- Last Validated

### `Source_Register`

One row per potential feedback profile or channel.

- Source ID
- Source
- Profile URL
- Source Type (`Rated Review`, `Location Review`, `App Review`, `Marketplace`, `Discussion`, `Complaint`, `Other`)
- Company/Brand/Product
- Country/Market
- Location
- Audience
- Verification Status
- Verification Evidence
- Identity Confidence
- Recommendation
- Inclusion Status
- Week 2 Collection Method
- Access or Permission Notes
- Last Validated

### `Baseline_Snapshot`

One row per source/profile/location captured on a specific date. Preserve raw fields.

- Snapshot Date
- Source ID
- Company/Brand/Product
- Country/Market
- Location
- Rating Value
- Rating Scale
- Review Count
- Latest Review Date
- Reviews Last 30 Days
- Reviews Last 90 Days
- Reviews Last 365 Days
- Company Responses Visible
- Response Rate
- Measure Status (`Observed`, `Calculated`, `User-provided`, `Not publicly available`)
- Evidence URL
- Notes

Do not invent period counts when a platform does not expose them. If normalizing a rating for cross-source display, retain the raw value and scale and label the normalized value as calculated.

### `Discussion_Snapshot`

Keep unrated conversation separate.

- Snapshot Date
- Source ID
- Community/Forum
- Search Scope
- Relevant Threads Found
- Most Recent Relevant Date
- Representative Thread URLs
- Participant Identity Caveat
- Evidence Status
- Notes

### `Coverage_Gaps`

- Channel or Audience
- Expected/Relevant
- Covered
- Gap Description
- Impact on Interpretation
- Recommended Next Step
- Step (`Benchmark`, `Monitor`, or `Closed Loop`)

Include missing internal VOC channels here. Public review coverage must not be presented as complete enterprise VOC.

### `Evidence_Log`

- Evidence ID
- Claim or Measure
- Source Name
- Direct URL
- Accessed Date
- Evidence Type (`Official`, `Platform Profile`, `Directory`, `Discussion`, `User-provided`)
- Observed/Calculated/Inferred
- Notes

## Baseline dashboard

Create a simple, non-deceptive dashboard only from comparable fields. Recommended elements:

- benchmark capture date;
- source coverage by Core/Secondary/Watchlist;
- raw rating and review count by rated source;
- review recency by source;
- market/location coverage;
- company-response visibility where available;
- discussion activity shown separately;
- known external and internal coverage gaps.

Avoid a single blended “VOC score” unless the user defines and approves a weighting method. Ratings across sources may represent different audiences, scales, time periods, and selection effects.

## Written benchmark package

Use this order:

1. **Confirmed company profile** — what is being benchmarked.
2. **Scope and capture date** — included brands, products, markets, locations, and source classes.
3. **Validated source map** — Core, Secondary, Watchlist, and Excluded sources with reasons.
4. **Baseline snapshot** — source-by-source observed measures.
5. **What the benchmark suggests** — careful observations, not causal conclusions.
6. **Coverage and representativeness limits** — what public sources do and do not reveal.
7. **Internal VOC inventory** — unassessed channels required for a fuller view.
8. **Week 2 monitoring-readiness specification** — collection method, frequency, identifier, baseline key, permissions, failure risk, and expected output for each included source.
9. **Assumptions and open questions.**
10. **Evidence and attribution log.**

## Week 2 readiness fields

For every included source, record:

- access method: official API, platform notification email, export, manual capture, or unknown;
- authentication or ownership requirement;
- proposed schedule;
- stable record identifier or deduplication candidate;
- first-run baseline rule;
- accessible data fields;
- likely limitations;
- whether automation is permitted or still requires terms review;
- failure signal so “no new feedback” is not confused with “source was not checked.”

Do not generate the monitoring script in Step 1.
