---
name: voc-benchmark-builder
description: Research a company, confirm its business and market profile, discover and validate relevant public customer-feedback sources, and establish a cited external Voice of Customer benchmark. Use when starting a company-specific VOC baseline before monitoring or closed-loop automation. Do not use this skill to automate ongoing collection, scrape restricted sites, or treat public reviews as the complete Voice of Customer.
---

# VOC Benchmark Builder

Build a company-specific external Voice of Customer benchmark through progressive research and confirmation. Begin with the smallest useful user input, infer what can be researched, and ask the user to confirm or correct findings before the next stage.

This is Step 1 of a broader progression:

1. **Benchmark:** identify where customers speak and establish the current position.
2. **Monitor:** automate permitted ongoing collection and change detection.
3. **Close the loop:** route, resolve, communicate, and learn from feedback.

Complete only Step 1 unless the user explicitly asks to continue.

## Interaction model

Lead the user through a natural conversation rather than presenting a long intake form.

1. Ask for the company website. If the website is unavailable or ambiguous, also ask for the company name and primary market.
2. Research the company before asking for information that can be inferred reliably.
3. Present a concise draft company profile and ask the user to confirm it or correct specific fields.
4. After confirmation, discover likely public feedback sources and present a proposed source map.
5. Clearly separate verified sources, plausible candidates, and sources checked but not found.
6. Ask the user to confirm the sources and benchmark scope before collecting the baseline.
7. Build the company-specific benchmark deliverable and monitoring-readiness specification.

Ask one focused confirmation question at a time when possible. Batch only closely related corrections. Do not require the user to re-enter facts already supported by reliable sources.

## Stage 1: Draft and confirm the company profile

Read [company-profile.md](references/company-profile.md) and follow it to identify:

- company and website identity;
- parent company, brands, products, and material aliases;
- B2B, B2C, B2B2C, marketplace, nonprofit, or mixed model;
- customer and user types;
- physical-location, web, mobile-app, marketplace, or hybrid delivery;
- countries, markets, regions, languages, and location footprint;
- material distinctions between buyers, users, consumers, partners, and locations.

Use current web research. Cite the official company sources used. Treat the profile as a draft until the user confirms it. Ask “Is this the right company, and is this profile accurate?” rather than asking the user whether it is a “good” company.

Do not judge reputation at this stage. Use identity confidence, profile completeness, and evidence quality, not a subjective company-quality label.

## Stage 2: Discover and validate public VOC sources

After the company profile is confirmed, read [source-discovery.md](references/source-discovery.md).

Search broadly enough to find both expected and less-obvious sources, including:

- general and category-specific review platforms;
- physical-location and marketplace reviews;
- software review sites and app stores;
- Reddit, relevant forums, public communities, and discussion sites;
- industry directories and sector-specific marketplaces;
- complaint, accreditation, or consumer-protection sources when relevant.

Let the confirmed company profile determine the search. Do not force every company into the same source list.

For every candidate, verify that it belongs to the correct company, brand, product, location, or app. Never invent a profile because the source seems likely. If identity remains ambiguous, label it **Needs confirmation** and ask the user.

Classify each source as:

- **Core:** verified, relevant, and useful for the benchmark;
- **Secondary:** verified but lower-volume, narrower, or less representative;
- **Watchlist:** plausible or emerging, but not yet strong enough for the baseline;
- **Exclude:** wrong entity, employee-only feedback, duplicative, inaccessible, or irrelevant.

Separate rated review sources from discussion sources. Do not combine Reddit threads, forum conversations, and star ratings into a single score.

## Stage 3: Confirm scope

Present the proposed source register before capturing the benchmark. For each source show:

- source and verified profile URL;
- brand, product, market, or location covered;
- source type;
- why it matters;
- verification status and confidence;
- likely Week 2 collection method: official API, notification email, export, manual capture, or unknown;
- recommended inclusion: Core, Secondary, Watchlist, or Exclude.

Then ask the user to confirm:

- which brands, products, countries, markets, and physical locations are in scope;
- whether Core sources alone or Core plus Secondary sources should be benchmarked;
- whether competitor comparison is wanted now or later.

Default to benchmarking the company against itself. Do not choose competitors without user confirmation.

## Stage 4: Capture the benchmark

After scope confirmation, read [benchmark-output.md](references/benchmark-output.md) and create a dated snapshot. Preserve the source’s raw measures before calculating normalized or derived fields.

Record unavailable metrics as `Not publicly available`; do not estimate them. Distinguish:

- **Observed:** directly visible in a cited source;
- **Calculated:** derived from observed data with the calculation stated;
- **User-provided:** supplied or corrected by the user;
- **Inferred:** reasoned from evidence but not directly stated.

Public reviews are an external VOC channel, not the whole Voice of Customer. Include an internal-channel inventory showing important sources that were not assessed, such as surveys, support cases, calls, emails, churn reasons, implementation feedback, product usage, advisory boards, and account notes.

## Required output

Create a custom company benchmark package containing:

1. Confirmed Company Profile
2. Source Register
3. Baseline Snapshot
4. External VOC Coverage and Gaps
5. Benchmark Observations, with cautious language
6. Week 2 Monitoring-Readiness Specification
7. Evidence and Attribution Log
8. Assumptions and Open Questions

If spreadsheet creation is available, create a tailored workbook using the tab and field definitions in [benchmark-output.md](references/benchmark-output.md). Otherwise provide copy-ready Markdown or CSV tables. Do not create automation code during Step 1.

The finished output must be specific to the confirmed company. Create a written brief named `[company-slug]-voc-benchmark.md` (or the nearest supported document format) plus the workbook when available. Do not merely return this skill’s generic template or rewrite the skill itself.

## Evidence and safety rules

- Use live web research; cite every profile and material company fact with a direct URL.
- If current web search is unavailable, say so and ask the user to enable it or provide source URLs; do not fabricate a researched benchmark.
- Record the benchmark capture date because ratings, counts, markets, and products change.
- Prefer official company pages and the review platform’s own profile over aggregators or search snippets.
- State when a site was checked but no verified profile was found.
- Do not bypass authentication, CAPTCHAs, robots controls, paywalls, or platform restrictions.
- Do not recommend scraping when an official API, notification, export, or manual method is the permitted route.
- Do not reproduce full reviews. Capture only the fields and short excerpts needed for analysis, respecting source terms and applicable rights.
- Do not infer customer sentiment, market representativeness, or company quality from star ratings alone.
- Do not expose personal reviewer information beyond what is necessary and already public.

## Stop condition

End Step 1 when the user has a confirmed company profile, confirmed source scope, dated benchmark, coverage-gap statement, and source-by-source readiness notes for Week 2. Offer monitoring automation as the next step, but do not implement it unless requested.
