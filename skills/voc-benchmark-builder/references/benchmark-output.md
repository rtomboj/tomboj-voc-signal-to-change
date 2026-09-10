# Company-specific benchmark output

Use this reference after the user confirms the source register, geography, audiences, insight window, and sampling approach.

## Workbook contract

Create the following core tabs. Keep the exact tab names and required fields so later monitoring can build on the same workbook. Optional company-specific columns may be added after the required columns.

### `Executive_Dashboard`

Lead with meaning rather than source counts. Show:

- platform baseline date;
- review-level insight window;
- records analyzed by source, audience, geography, and coverage type;
- “What customers value,” “Where customers struggle,” “What is emerging,” and “Where to focus” summaries;
- the required charts from `insight-analysis.md`;
- a visible coverage and representativeness warning.

### `Company_Profile`

One row per company, brand, product, or market entity:

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

One row per potential feedback profile or channel:

- Source ID
- Source
- Profile URL
- Source Type
- Company/Brand/Product
- Requested Country/Market
- Source Aggregate Geography
- Geography Filterable
- Location
- Audience
- Identity Status
- Verification Evidence
- Identity Confidence
- Audience Fit
- Benchmark Role
- Accessible History
- Sample Method
- Inclusion Status
- Week 2 Collection Method
- Access or Permission Notes
- Last Validated

### `Baseline_Snapshot`

One row per source/profile/location captured on a specific date:

- Snapshot Date
- Source ID
- Company/Brand/Product
- Country/Market Claimed
- Source Aggregate Geography
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

Preserve raw fields. Do not invent period counts. If a source aggregate is global or unknown, do not label it as country-specific.

### `Review_Data`

One row per accessible review or discussion record:

- Record ID
- Source ID
- Stable Source Record ID
- Source Type
- Direct URL
- Capture Date
- Record Date
- Company/Brand/Product
- Requested Country/Market
- Source-Reported Geography
- Geography Confidence
- Location
- Rating Value
- Rating Scale
- Audience
- Audience Fit
- Short Evidence Excerpt
- Company Response Visible
- Collection Coverage (`Full accessible period`, `Platform aggregate only`, `Sample`)
- Journey Stage
- Primary Theme
- Secondary Theme
- Signal Type
- Operational Impact
- Classification Confidence
- Human Review Needed
- Notes

### `Theme_Taxonomy`

One row per company-specific theme:

- Theme ID
- Theme
- Parent Theme
- Definition
- Include When
- Exclude When
- Relevant Journey Stages
- Relevant Audiences
- Example Terms
- User Confirmed
- Last Updated

### `Discussion_Snapshot`

Keep unrated conversation separate:

- Snapshot Date
- Source ID
- Community/Forum
- Search Scope
- Relevant Threads Found
- Most Recent Relevant Date
- Representative Thread URLs
- Participant Identity Caveat
- Geography Caveat
- Evidence Status
- Notes

### `Signal_to_Focus`

One row per material theme:

- Theme
- Audience
- Journey Stage
- Positive Count
- Negative Count
- Mixed/Request Count
- Total Classified Records
- Most Recent Signal
- Impact
- Cross-Source Support
- Classification Confidence
- Coverage Limitation
- Focus Category
- Rationale
- Internal Evidence Needed

### `Coverage_Gaps`

- Channel or Audience
- Expected/Relevant
- Covered
- Geography Covered
- Period Covered
- Gap Description
- Impact on Interpretation
- Recommended Next Step
- Step (`Benchmark`, `Monitor`, or `Closed Loop`)

Include missing internal VOC channels. Public review coverage must not be presented as complete enterprise VOC.

### `Week2_Readiness`

- Source ID
- Source
- Access Method
- Authentication/Ownership Requirement
- Proposed Schedule
- Stable Identifier/Deduplication Key
- First-Run Baseline Rule
- Accessible Fields
- Known Limitations
- Automation Permission Status
- Failure Signal
- Readiness Status

### `Evidence_Log`

- Evidence ID
- Claim or Measure
- Source Name
- Direct URL
- Accessed Date
- Evidence Type
- Observed/Calculated/Inferred/User-provided
- Geography Supported
- Audience Supported
- Notes

## Validation before delivery

Before exporting the workbook:

1. Verify that every required tab exists with the exact name.
2. Verify that every required column exists.
3. Check formulas for errors and charts for broken or empty ranges.
4. Confirm that dashboard statements trace to `Review_Data` or `Evidence_Log`.
5. Confirm that every geographic claim is supported by the corresponding source field.
6. Confirm that platform totals and review-level sample counts are not confused.
7. Confirm that discussion and complaint measures are not blended into rating calculations.

## Written benchmark package

Use this order:

1. **What this means** — strengths, friction, emerging signals, focus, and uncertainty.
2. **Confirmed company profile.**
3. **Scope, platform date, insight window, sample sizes, and geography.**
4. **Validated source map.**
5. **Platform baseline snapshot.**
6. **Review-level findings and starter taxonomy.**
7. **Signal-to-Focus Map.**
8. **Coverage and representativeness limits.**
9. **Internal VOC inventory.**
10. **Week 2 monitoring-readiness specification.**
11. **Assumptions, open questions, evidence, and attribution.**

Do not generate the monitoring script in Step 1.
