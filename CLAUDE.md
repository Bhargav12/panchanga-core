# CLAUDE.md — panchanga-core

## What this repo is

The rule layer and precompute orchestrator for the Ambient Panchanga
product: ayanamsa correction, tithi/nakshatra/yoga/karana calculations,
rahu kalam/yamaganda/gulika rules, and the pipeline that generates the
static dataset shipped inside the mobile app.

Full product context lives in `docs/product-plan.md` — read it before
making architectural decisions, especially §11 ("Licensing Decision"),
§13 ("Deployment & Infrastructure"), §15 ("NFRs"), and §16 ("Platform
Support & Future PC Extension").

## LICENSING DECISION: FINAL — AGPL-3.0, public repo

This was a deliberate choice, made with full awareness that this repo's
complete source — including the rule layer that's the product's actual
differentiator — is open-source as a result. This is final; do not revert
to treating this repo as proprietary/closed-source unless the user
explicitly says the licensing decision has changed again.

**Practical implications:**
- This repo is (or will be) public. Don't restrict visibility unilaterally.
- `LICENSE` must contain the full, unmodified AGPL-3.0 text — if asked to
  touch this file, don't hand-write or paraphrase license text; direct the
  user to download it from https://www.gnu.org/licenses/agpl-3.0.txt.
- `NOTICE` carries copyright/attribution — keep it separate from `LICENSE`.

## Architecture convention (style preference now, not a legal requirement)

This repo still only talks to `ephemeris-service` as an HTTP client via
`panchanga_core/client/ephemeris_client.py`'s `EphemerisClient`, rather
than importing Swiss Ephemeris directly. Keep this pattern — it's good
separation of concerns even though both repos are AGPL/public either way.
There's a CI workflow (`.github/workflows/boundary-check.yml`, still named
"AGPL boundary check" so existing branch protection rules keep matching
it) that flags direct Swiss Ephemeris imports — treat findings from it as
a style nit to fix, not a licensing emergency.

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

- Do not hand-write or paraphrase AGPL license text.
- Do not make this repository private without being told the licensing
  decision has changed again.
- Do not ship/trust generated dataset output without validation against a
  reference source.
