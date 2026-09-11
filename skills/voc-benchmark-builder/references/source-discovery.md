# Source discovery and validation

Use this reference after the company profile is confirmed.

## Search from the company outward

Create search terms from the confirmed name, aliases, brands, products, locations, countries, and languages. Search combinations such as company or product reviews, complaints, Reddit, forums, communities, industry directories, location reviews, and official app-store listings.

Use the company profile to discover category-specific sources rather than relying on a universal list. Employee reviews are not customer VOC unless the user explicitly includes employee voice as a separate audience.

## Source-completeness gate

Before presenting the proposed source scope, create an expected-source checklist based on the confirmed company model. Every expected source class must have a documented disposition: `Verified`, `Probable`, `Needs confirmation`, `Not found`, or `Rejected`.

Use these as minimum source classes to check when relevant, not as a universal inclusion list:

| Company model | Minimum source classes to check |
| --- | --- |
| B2B software | G2, Capterra/GetApp/Software Advice, Trustpilot, TrustRadius, applicable app stores, public communities, and industry directories |
| Local or multi-location | Google Business Profile, Yelp, Facebook, Trustpilot, relevant booking or marketplace profiles, and industry directories |
| Mobile product | Apple App Store, Google Play, product-review platforms, public communities, and support/status channels |
| Consumer service or marketplace | Google, Trustpilot, BBB or relevant complaint sources, marketplace profiles, app stores, and public communities |

For each class, record the query or candidate URL checked, the result, the identity evidence, and the reason for its disposition. Use at least these discovery patterns where applicable:

- company, brand, product, and domain plus `reviews`;
- the source name plus the company, product, domain, or app publisher;
- company aliases, former names, parent brands, and legal or app-developer names;
- direct inspection of an obvious candidate platform profile rather than relying only on a search snippet.

If a high-relevance source appears likely but cannot be verified on the first pass, recheck it using the domain, aliases, publisher, and source-specific search before marking it `Not found`. If ambiguity remains and exclusion would materially change the benchmark, ask the user.

When rerunning a benchmark, compare the new checklist with the previous `Source_Register`. Explain every source added, removed, or given a different status. Do not silently change the source universe.

The gate passes only when every expected source class has a recorded disposition. `Not found` means the documented search did not locate a verifiable profile; it does not prove that no profile exists.

## Validate profile identity

Use multiple signals where possible: linked official domain, matching company or product name, publisher, address, service area, market, language, category, logo, description, and current subject matter.

Assign an **Identity Status**:

- **Verified:** strong direct match.
- **Probable:** several matching signals but no definitive link.
- **Needs confirmation:** plausible ambiguity could materially affect the benchmark.
- **Not found:** the expected source class was checked but no verifiable candidate profile was located.
- **Rejected:** wrong entity, market, product, location, or audience.

Only Verified and user-confirmed Probable profiles may enter the baseline.

## Separate audience fit from source identity

A profile can belong to the correct company while containing feedback from the wrong or mixed audience. Assign an **Audience Fit** independently:

- **Primary:** aligned to the confirmed benchmark population.
- **Mixed:** contains the primary population plus other audiences that cannot always be separated.
- **Secondary:** a relevant user or stakeholder population that must remain separate from the primary conclusion.
- **Unknown:** participant identity is not supported by the available evidence.

Record whether audience roles can be filtered or classified at the individual-record level.

## Enforce geography and market scope

For every source, record:

- geography represented by the aggregate measure;
- whether reviews can be filtered to the confirmed country, market, language, or location;
- geography visible for individual review records;
- the geography that may be claimed in the final benchmark.

If a source cannot be filtered to the requested market, mark its geographic scope **Global/unknown**. It may provide context, but its aggregate rating, volume, or theme frequency must not be described as specific to a country or region.

## Assign an analytic role

Assign a **Benchmark Role** independently of identity and audience:

- **Quantitative baseline:** comparable platform measures or review-level data suitable for the stated scope.
- **Contextual signal:** useful for topics, language, or hypotheses but not population measurement.
- **Watchlist:** plausible or emerging, but not sufficiently verified, accessible, or useful for the current baseline.
- **Excluded:** wrong entity/audience, prohibited access, duplicative, or irrelevant.

Explain the role in one sentence. A verified source with mixed or unknown participants can still be contextual, but it is not automatically a quantitative baseline.

## Assess accessible history

For each included source, document:

- visible review or discussion volume and recency;
- earliest and latest accessible dates;
- whether a 12-month window is available;
- whether access represents a full population, platform-provided aggregate, or recent sample;
- company responses and stable record identifiers when visible;
- duplicate-syndication risk;
- likely Week 2 access route.

Do not attempt exhaustive collection through prohibited or evasive methods. If only a recent public sample is accessible, disclose the exact item count and date span.

## Discussion sources

Reddit, forums, and public communities can reveal language and issues that rated-review sites miss. They can also contain prospects, employees, competitors, or unidentified participants.

Keep them as `Discussion` and normally assign `Contextual signal`. Capture relevant thread dates and direct URLs when feasible. Do not translate discussion activity into ratings or claim representativeness.

## Sources checked but not found

Log meaningful negative discovery results. “No verified profile found” is different from “not checked.” Include the search date and ambiguity that prevented confirmation.
