# Review instructions

## Licensing context

This repo is AGPL-3.0 and public (final decision — see docs/product-plan.md
§11). Direct Swiss Ephemeris imports are no longer a licensing violation,
just an architecture-convention deviation — treat as Nit (🟡), not Important,
unless the PR description suggests it's undermining the ephemeris-service
separation intentionally at scale.

## What Important means here

Treat these as Important (🔴):

- Tithi/nakshatra/yoga/karana boundary logic that ships without a
  corresponding validation test comparing output against a trusted
  reference panchangam. "Runs without errors" is not sufficient evidence
  of correctness for these calculations — flag any PR that adds or
  changes boundary-finding logic without also adding or updating a
  validation test.
- Any dataset-generation code path that would ship ungenerated/unvalidated
  output to the app bundle.
- Modifications to Swiss Ephemeris's own source (if ever vendored here)
  that aren't also released under AGPL-3.0.

## Always check

- Does new rule-layer logic (ayanamsa, tithi, nakshatra, yoga, karana,
  rahu kalam/yamaganda/gulika) include or update a test with an expected,
  reference-checked value — not just an assertion that the function returns?
- Does the location grid (`orchestrator/grid.py`) or dataset schema change
  in a way that would break the on-device SQLite schema documented in
  `docs/product-plan.md`?

## Do not report

- Anything CI already enforces: lint, formatting, type errors
- Style/naming nits in stub/TODO code explicitly marked as scaffolding
- Direct Swiss Ephemeris imports as a licensing issue — it isn't one anymore

## Summary shape

Lead the review summary with whether any unvalidated-astronomical-logic
issue was found, before general code quality notes.

