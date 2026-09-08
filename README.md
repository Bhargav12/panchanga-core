# panchanga-core

**License: AGPL-3.0-only. This repo is public.** See `LICENSE` and `NOTICE`.

This was a deliberate, final decision made with full awareness of what it
means: this repo's complete source — the rule layer that's the actual
product differentiator — is open-source and reusable by anyone, including
competitors. See `docs/product-plan.md` §11 for the full reasoning,
Astrodienst's clarification that led to it, and the earlier isolation
architecture that was considered and ruled out.

Contains all panchanga-specific business logic:
- Ayanamsa correction
- Tithi / nakshatra / yoga / karana boundary calculations
- Rahu Kalam / Yamaganda / Gulika Kalam (pure rule-based, no ephemeris call needed)
- Muhurta / festival rule definitions
- Precompute orchestrator that generates the static dataset shipped in the app

## Architecture note (no longer a legal requirement, kept as good practice)

This repo still only talks to `ephemeris-service` as an HTTP client
(see `panchanga_core/client/ephemeris_client.py`) rather than importing
Swiss Ephemeris directly. That's now a separation-of-concerns choice, not
a licensing requirement — both repos are AGPL/public either way — but it's
still worth keeping, since it means domain logic lives in exactly one place.

## Layout

```
panchanga_core/
  client/         # HTTP client for ephemeris-service
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

## Before this repo is considered fully compliant

- [ ] Replace `LICENSE` with the real, unmodified AGPL-3.0 text (see that file)
- [ ] Fill in the project-specific copyright line in `NOTICE`
- [ ] Confirm the repo is actually public on GitHub
