# panchanga-core

**License: Proprietary (private repo)**

Contains all panchanga-specific business logic:
- Ayanamsa correction
- Tithi / nakshatra / yoga / karana boundary calculations
- Rahu Kalam / Yamaganda / Gulika Kalam (pure rule-based, no ephemeris call needed)
- Muhurta / festival rule definitions
- Precompute orchestrator that generates the static dataset shipped in the app

## Hard rule: no Swiss Ephemeris code in this repo

This repo must **only** talk to `ephemeris-service` as an HTTP client
(see `panchanga_core/client/ephemeris_client.py`). It must never import
`swisseph`/`pyswisseph`, link against Swiss Ephemeris, or bundle any `.se1`
ephemeris data files. If that boundary gets blurred, the AGPL isolation
described in the product plan (§11.1) no longer holds.

## Layout

```
panchanga_core/
  client/         # HTTP client for ephemeris-service — the ONLY point of contact
  rules/          # tithi, nakshatra, yoga, karana, rahu_kalam, ayanamsa
  orchestrator/   # location grid, date range loop, dataset writer
tests/            # unit tests + validation against a trusted reference panchanga
```

## Setup

```bash
pip install -r requirements.txt
export EPHEMERIS_SERVICE_URL=http://localhost:8000
python -m panchanga_core.orchestrator.generate_dataset --start 2026-01-01 --days 365
```

## Before trusting generated output

Validate a sample of generated dates/cities against a known-correct printed
panchangam or reputable existing source before shipping — see product plan
§0.6 "Suggested Phase 0 Exit Criteria."
