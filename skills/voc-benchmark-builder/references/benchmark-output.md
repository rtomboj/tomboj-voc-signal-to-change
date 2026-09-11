# Company-specific benchmark output

Use this reference after the user confirms the source register, geography, audiences, insight window, and sampling approach.

## Workbook contract

Create the following core tabs. Keep the exact tab names and required fields so later monitoring can build on the same workbook. Optional company-specific columns may be added after the required columns.

Apply the workbook rules in [visual-style.md](visual-style.md). The workbook should help a person connect the evidence to meaning; it is not only a data export.

### `Executive_Dashboard`

Lead with meaning rather than source counts. Show:

- a concise “What this means” interpretation as the first view;
- platform baseline date;
- review-level insight window;
- records analyzed by source, audience, geography, and coverage type;
- a compact evidence-class coverage table showing record counts for independent reviews, vendor-selected customer stories, official operational evidence, public discussions, complaints, and other collected evidence; show zero or `Not available` rather than omitting a class;
- separate “What looks good,” “Where friction appears,” “What may be emerging,” and “Where to focus next” summaries;
- the required charts from `insight-analysis.md`;
- a compact Signal-to-Focus view showing evidence pattern, confidence, and what would confirm or challenge each recommendation;
- a visible coverage and representativeness warning.

Do not place vendor-selected customer stories and independent feedback into one sentiment total or chart. Vendor stories may illustrate reported outcomes or what good can look like, but they must not visually or numerically offset independent negative feedback.

Use current platform measures immediately when they are useful, such as source-by-source rating and review volume. Do not create theme-frequency or time-series charts until review-level data supports them. Replace an unsupported chart with a clearly labeled evidence-gap table.

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
- Evidence Class
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
- Evidence Class(es)
- Independent Cross-Source Support
- Corroboration Status
- Classification Confidence
- Evidence Strength
- Prevalence Confidence
- Coverage Limitation
- Focus Category
- Evidence Pattern
- Rationale
- What Would Confirm or Challenge It
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
8. Confirm that observed facts, AI classifications, calculated measures, and recommendations are visibly distinguishable.
9. Confirm that the workbook follows `visual-style.md`, including fonts, wrapping, alignment, chart colors, and status labels.
10. Confirm that no chart implies unavailable history, theme frequency, or market representativeness.
11. Confirm that every expected source class has a documented disposition and that source additions or removals from any prior benchmark are explained.
12. Confirm that vendor-selected customer stories are not combined with independent feedback in sentiment totals or charts.
13. Confirm that material signals were checked for public corroborating evidence when available, without treating corroboration as proof of prevalence or impact.
14. Confirm that classification confidence, evidence strength, and prevalence confidence are separately defined and populated.
15. Confirm that every `Verified` source has a direct, stable platform profile or listing URL; a search-results page, snippet, or platform homepage is not sufficient.
16. Confirm that `Independent Cross-Source Support` counts only comparable independent customer feedback sources, not vendor-selected stories or official operational evidence.
17. Confirm that the dashboard includes the evidence-class coverage table and does not omit collected vendor-selected or operational records.
18. Confirm that any theme or category chart with a displayed label longer than 24 characters uses horizontal bars.

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
