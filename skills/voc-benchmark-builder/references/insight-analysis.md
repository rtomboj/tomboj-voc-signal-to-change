# Review-level insight analysis

Use this reference after the user confirms the source scope and insight window.

## Two-layer benchmark

Keep two evidence layers distinct:

1. **Platform baseline:** point-in-time rating, total volume, response visibility, and available recent-period totals.
2. **Insight window:** dated review-level records used for theme, journey, and focus analysis.

Default the insight window to the most recent 12 months. If complete permitted access is unavailable, use a transparent recent sample and state the exact number of records and date range for every source. Never describe a sample as the full period.

## Review-level capture

Capture one row per accessible review or discussion record. Retain the source’s raw fields before adding classifications. Use short excerpts only; do not reproduce full reviews.

Required analytical fields:

- record ID and stable source identifier when available;
- source, direct URL, and capture date;
- review or discussion date;
- company, brand, product, app, market, or location;
- source-reported geography and geography confidence;
- rating value and scale when applicable;
- audience: buyer, merchant, consumer, employee, partner, or unknown;
- audience-fit class: Primary, Mixed, Secondary, or Unknown;
- short evidence excerpt;
- company response visible;
- collection status: full accessible period, platform aggregate only, or sample.

## Build a starter taxonomy

Use a small cross-source sample to draft a company-specific taxonomy before classifying the full accessible dataset. Avoid forcing generic themes when the customer’s language suggests more useful categories.

The taxonomy should normally include:

- customer journey stage;
- primary and optional secondary theme;
- signal type: Positive, Negative, Mixed, Request, or Question;
- operational impact: Blocker, High, Medium, Low, or Unknown;
- classification confidence: High, Medium, or Low;
- supporting inclusion and exclusion notes for each theme.

Present the draft taxonomy for user confirmation when material changes would alter the interpretation. After confirmation, apply the stable taxonomy consistently. Mark borderline records for human review rather than forcing precision.

## Classification workflow

Use this sequence so the analysis remains auditable:

1. State the exact period, sources, audiences, geographies, and records available.
2. Preserve observed source fields before adding any AI classification.
3. Classify each record against the confirmed taxonomy and flag low-confidence cases.
4. Calculate counts and proportions only from the classified records, always showing the numerator and denominator.
5. Separate repeated signals from isolated or emerging observations.
6. Translate the evidence into what to protect, improve, investigate, or watch.
7. State what internal or additional external evidence would confirm or challenge each focus recommendation.

Label the analytical layer clearly:

- **Observed:** directly reported by a source or captured from a record.
- **Calculated:** derived transparently from observed fields.
- **AI-classified:** a theme, journey stage, signal type, or impact label assigned by the analysis.
- **Recommended:** a directional management response derived from the evidence and its limitations.

## Quantify carefully

Every frequency statement must identify its numerator, denominator, window, audience, and sources. Example:

> Support appeared in 18 of 62 primary-audience reviews captured from G2 and Capterra between October 2025 and September 2026.

Do not compare theme percentages across sources when their accessible samples were collected differently without clearly labeling the limitation. Do not infer population prevalence from public-review frequency.

## Connect signals to meaning

Summarize four kinds of findings:

1. **Keep doing:** recurring strengths customers explicitly value.
2. **Protect:** important strengths that appear vulnerable to adjacent friction.
3. **Fix first:** recent, repeated, high-impact problems supported by traceable evidence.
4. **Investigate:** potentially material signals with insufficient, mixed, or low-confidence evidence.
5. **Monitor:** isolated or emerging signals worth watching without implying that action is yet justified.

State what is important to the customer in their language, which audience and journey stage is affected, why the finding matters, and what evidence would be needed to validate or challenge the conclusion internally.

## Signal-to-Focus Map

Create a directional focus table with one row per material theme:

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
- Focus Category (`Keep doing`, `Protect`, `Fix first`, `Investigate`, `Monitor`)
- Evidence Pattern
- Rationale
- What Would Confirm or Challenge It
- Internal Evidence Needed

Do not create a hidden or arbitrary priority score. If the user wants a numeric weighting method, show the proposed factors and obtain approval before calculating it.

## Required visuals

Create these charts when the underlying data supports them:

1. **Source landscape:** raw rating, volume, audience, geography, and coverage shown without averaging unlike sources.
2. **Feedback over time:** monthly accessible record volume and rating/signal distribution within the insight window.
3. **Theme view:** positive, negative, mixed, and request counts for the most material themes.
4. **Signal-to-Focus view:** frequency and impact with recency and confidence visible through labels or an adjacent table.

Keep complaint counts and discussions separate from star-rating comparisons. If data is too sparse for a chart, say so and use a table instead.

The platform baseline can support a source-by-source rating and volume view even when review-level history is unavailable. Do not fabricate a time trend, theme distribution, or sentiment breakdown from platform totals alone. Every chart must show its date range, sample size or population basis, audience, and geography where relevant.

## Executive interpretation

Lead the final package with a concise page answering:

- What customers appear to value
- Where they appear to struggle
- What seems to be changing or emerging
- Which audiences and journey stages are affected
- Where attention should go first
- What cannot yet be concluded

Each material statement must link back to the review-level dataset or evidence log.
