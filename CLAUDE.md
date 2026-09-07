# CLAUDE.md — panchanga-core

## What this repo is

The proprietary rule layer and precompute orchestrator for the Ambient
Panchanga product: ayanamsa correction, tithi/nakshatra/yoga/karana
calculations, rahu kalam/yamaganda/gulika rules, and the pipeline that
generates the static dataset shipped inside the mobile app.
License: proprietary/private.

Full product context lives in `docs/product-plan.md` — read it before
making architectural decisions, especially the sections "Phase 0
Architecture — If Proceeding Under AGPL," "Licensing Decision," and
"Deployment & Infrastructure." Treat it as the source of truth for *why*
things are structured the way they are, not just *what* to build next.

## The one rule that overrides everything else

**This repo must never import, link, or bundle Swiss Ephemeris.**
No `import swisseph`, no `import pyswisseph`, no `.se1` data files, no
copy-pasted logic from the Swiss Ephemeris source. The only permitted
contact with ephemeris calculation is through
`panchanga_core/client/ephemeris_client.py`'s `EphemerisClient`, which
talks to the separate `ephemeris-service` repo over HTTP.

This repo has a CI workflow (`.github/workflows/boundary-check.yml`) that
fails the build if a Swiss Ephemeris import or `.se1` file is detected.
If a task seems to require Swiss Ephemeris directly (e.g. "just import it
here, it's faster"), stop and say so instead of doing it — the fix is
always "call EphemerisClient," never "import the library directly, just
this once."

## Why this boundary exists

See `docs/product-plan.md` §11/§11.1. Short version: Swiss Ephemeris is
AGPL-licensed (unless/until we buy the Professional License). Keeping this
repo as a pure network client of a separate, generic ephemeris service is
what lets this rule layer — the actual product differentiator — stay
closed-source.

## Current state / what's stubbed

- `panchanga_core/rules/ayanamsa.py` — placeholder offset values, not
  validated. Needs a proper date-dependent ayanamsa calculation before
  production use.
- `panchanga_core/rules/tithi.py`, `nakshatra.py`, `yoga.py` —
  `current_*_index()` functions work on a single instant; the
  `find_*_end_time()` functions are `NotImplementedError` stubs. These need
  iterative/root-finding queries against `EphemerisClient` to find the
  exact boundary-crossing timestamp (tithi = 12° segments, nakshatra/yoga
  = 13°20' segments). This is the most important unfinished piece — do
  not consider Phase 0 "done" without it.
- `panchanga_core/rules/karana.py` — the fixed/movable karana lookup
  table (`karana_name_for_index`) is not implemented. See the module
  docstring for the sequencing rule.
- `panchanga_core/orchestrator/grid.py` — only 4 placeholder cities.
  Needs the real supported-city list before Phase 1.
- `panchanga_core/orchestrator/generate_dataset.py` — samples a single
  point per day (local ~06:30) rather than capturing true segment
  boundaries. This is a known simplification for the scaffold; the real
  implementation needs to write actual `segment_start`/`segment_end`
  values into `tithi_segment`, `nakshatra_segment`, `yoga_segment` using
  the boundary-finding functions above, not `NULL`.

## Validation requirement — do not skip

Before trusting any generated output, validate a sample of dates/cities
against a known-correct printed panchangam or reputable existing source
(see product plan §0.6 "Suggested Phase 0 Exit Criteria"). If asked to
"finish" the tithi/nakshatra/yoga/karana logic, also propose or write a
validation test comparing output against reference values — don't treat
"it runs without errors" as "it's correct." These are astrological
boundary calculations; a subtly wrong root-finding implementation will
produce plausible-looking but incorrect output.

## Working conventions

- Python, `requests` for the HTTP client, `pytest` for tests, SQLite for
  the output dataset.
- `EPHEMERIS_SERVICE_URL` env var points at the ephemeris-service instance
  (defaults to `http://localhost:8000` in the orchestrator script).
- Run `pip install -r requirements.txt`, then
  `python -m panchanga_core.orchestrator.generate_dataset --start YYYY-MM-DD --days N`.

## Do not do without being asked

- Do not import Swiss Ephemeris code directly, under any justification.
- Do not ship/trust generated dataset output without validation against a
  reference source.
- Do not remove or weaken the CI boundary check.
