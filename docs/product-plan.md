# Product Plan: Ambient Panchanga
### Making daily panchanga a glanceable, zero-tap experience

---

## 1. Vision & Problem Statement

**Problem:** Panchanga apps today require an active decision to open the app. Most users only check panchanga occasionally (for muhurta timing, fasting days, or festival dates), so the information doesn't reach them at the moment it matters — before a wedding invite is sent, before scheduling a flight, before starting an important task.

**Vision:** Panchanga should live where the user's eyes already go — home screen, lock screen, watch, notification shade — the same way weather and time do. The app becomes a *data engine + delivery surface manager*, not a destination.

**North Star Metric:** % of daily active panchanga "views" that happen *without* opening the app (widget glances, lock screen glances, notification reads, watch glances) — target 70%+ within 12 months.

---

## 2. Target Users & Use Cases

| Persona | Primary Need | Ambient Surface That Wins |
|---|---|---|
| Daily ritual observer (pooja, fasting) | All five angas (tithi, vara, nakshatra, yoga, karana) + rahu kalam every morning | Home widget, daily notification |
| Event planner (weddings, griha pravesh) | Muhurta windows, auspicious dates | Calendar sync, Live Activity countdown |
| Elderly / traditional users | Simplicity, large text, no navigation | Lock screen widget, AOD |
| Astrology-curious younger users | Quick daily check, shareable | Watch complication, widget, voice assistant |
| NRI / diaspora | Location-adjusted panchanga, festival reminders | Notification + calendar sync |

---

## 3. Goals & Success Metrics

**Business goals**
- Increase daily active engagement without increasing app-open friction
- Increase retention (ambient presence = passive stickiness = lower churn)
- Create premium upsell surfaces (advanced widgets, muhurta alerts, watch faces)

**Metrics**
- Widget install rate (% of users who add at least one widget within 7 days)
- D1/D7/D30 retention, segmented by widget-adopters vs non-adopters
- Notification opt-in rate and tap-through rate
- Ambient-view-to-app-open ratio (North Star)
- Premium conversion rate from ambient surfaces

---

## 4. Phased Roadmap

### Phase 0 — Foundation (Weeks 1–4)
Not user-facing, but everything else depends on it.
- Build a **Panchanga Data Engine**: precomputed all five angas — tithi, vara, nakshatra, yoga, karana — plus rahu kalam/sunrise-sunset for the user's location, cached locally for offline access and fast widget refresh.
- Location & timezone handling (GPS + manual city selection + Panchanga calculation method selection, e.g., Drik vs Vakya, if the app supports multiple traditions).
- Background refresh strategy (Android WorkManager / iOS BackgroundTasks) that respects battery constraints.

### Phase 1 — Glanceable MVP (Weeks 4–8)
Goal: get panchanga onto the home screen with minimal scope.
- **Android home screen widget** (Glance API): small (tithi + vara + nakshatra) and medium (+ yoga, karana, rahu kalam, sunrise/sunset — full five-anga panchanga) sizes.
- **iOS WidgetKit widget**: Small/Medium/Large, using TimelineProvider so it auto-updates at transition times. Small shows tithi + vara; Medium/Large show all five angas plus rahu kalam and sunrise/sunset.
- **Daily notification**: one fixed-time rich notification with full day summary.
- Success criteria: 30%+ of active users add a widget; no material battery-drain complaints.

### Phase 2 — Lock Screen & Live Presence (Weeks 8–14)
- **iOS Lock Screen widgets** (circular/rectangular/inline).
- **Android lock screen** widget support where OEM allows (Samsung One UI, etc.) — degrade gracefully where not supported.
- **Live Activities / Dynamic Island**: countdown to end of current tithi or to next muhurta window.
- **Contextual notifications**: "Rahu Kalam starts in 15 min," configurable per user preference (opt-in, not default-on, to avoid notification fatigue).

### Phase 3 — Wearables & Voice (Weeks 14–20)
- **Wear OS complication** and **Apple Watch complication**: tithi + day-quality glyph.
- Optional themed **watch face**.
- **Siri Shortcuts / Google Assistant App Actions**: "Hey Google, what's today's panchanga?"
- Smart display card (Google Nest Hub) for households with shared devices.

### Phase 4 — System & Ecosystem Integration (Weeks 20–30, ongoing)
- **Calendar sync**: push tithi/nakshatra/festival data as all-day events via CalDAV (Android) / EventKit (iOS) into the native calendar — visible in Google Calendar, Apple Calendar, Outlook, etc.
- **Custom launcher widget packs** (KWGT/Zooper-style) for power users who build their own home screens.
- Explore **OEM partnerships** (Indian Android OEMs) for pre-bundled ambient panchanga on new devices.

---

## 5. Feature Prioritization (RICE-style, high level)

| Feature | Reach | Impact | Confidence | Effort | Priority |
|---|---|---|---|---|---|
| Home screen widget (Android + iOS) | High | High | High | Med | **P0** |
| Daily notification | High | Med | High | Low | **P0** |
| Lock screen widget | Med | High | Med | Med | **P1** |
| Live Activity / muhurta countdown | Med | High | Med | Med | **P1** |
| Watch complication | Med | Med | Med | Med | **P2** |
| Calendar sync | Med | Med | High | Med | **P2** |
| Voice assistant integration | Low-Med | Med | Med | Med | **P2** |
| OEM / launcher pack | Low | High (long-term) | Low | High | **P3** |

---

## 6. Technical Architecture Notes

- **Single source of truth**: a shared panchanga calculation module (ideally cross-platform, e.g., Kotlin Multiplatform or a shared Rust/C++ core) so Android, iOS, watch, and widget all compute from the same engine — avoids drift between surfaces.
- **Precompute + cache**: calculate a rolling 7–14 day window locally so widgets render instantly offline and refresh cheaply.
- **Refresh triggers**: tithi/nakshatra change times (not fixed hourly polling) to minimize battery/network use.
- **Personalization inputs**: location, calculation tradition/method, language, and which data points to surface (some users only want rahu kalam; others want full panchanga).
- **Permissions**: request location and notification permissions with clear value framing at the *moment of widget setup*, not on first app launch.

---

## 7. Monetization Hooks

- Free tier: full five-anga widget (tithi, vara, nakshatra, yoga, karana) + rahu kalam + daily notification — the core panchanga data stays free since gating it would undercut the product's basic value proposition.
- Premium tier: muhurta countdown Live Activities, watch complications, custom calendar sync, widget/complication theming, ad-free.
- Widget/complication customization (themes, fonts, deity images) as a premium visual upsell.

---

## 8. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Battery drain complaints from frequent widget refresh | Event-driven refresh at transition times, not polling |
| Android OEM fragmentation (lock screen widget support varies) | Feature-detect and gracefully hide unsupported surfaces per device |
| Notification fatigue reduces opt-in | Make contextual alerts opt-in, cap frequency, allow per-alert-type toggles |
| Calculation disputes (different traditions/schools) | Let users pick calculation method; be transparent about the source/system used |
| Widget adoption stays low without discovery flow | In-app "Add to Home Screen" prompt with visual preview + one-tap deep link to widget picker |

---

## 9. Suggested Timeline Summary

| Phase | Duration | Key Deliverable |
|---|---|---|
| Phase 0 | Weeks 1–4 | Panchanga data engine, location/tradition config |
| Phase 1 | Weeks 4–8 | Home screen widgets + daily notification |
| Phase 2 | Weeks 8–14 | Lock screen widgets + Live Activities |
| Phase 3 | Weeks 14–20 | Watch complications + voice assistant |
| Phase 4 | Weeks 20–30+ | Calendar sync, launcher packs, OEM exploration |

---

## 10. Competitive Landscape (Existing Widget/Ambient Panchanga Products)

| Product | Platform | Ambient Surfaces | Notes |
|---|---|---|---|
| **MyPanchang** | iOS/iPadOS/watchOS | Home + lock screen widgets, festival→Calendar links, AI Q&A ("Luna") | Closest existing match to this plan's vision; no Android; no watch complication or Live Activity muhurta countdown found |
| **Drik Panchang** (Adarsh Apps) | Android + iOS | Home screen widget, offline mode | Long-established data source/brand; regional calendar variants (Purnimanta/Amanta, language-specific panchangams) are a credibility bar to clear |

**Implication:** the ambient-widget thesis is already validated market behavior, not a novel bet. Differentiation should come from surfaces nobody has fully done yet: Android lock screen parity, watch complications, and Live Activity/Dynamic Island muhurta countdowns — plus first-class multi-tradition (Purnimanta/Amanta, regional panchangam) support from day one.

**Build note:** if using Flutter instead of fully native Android/iOS, cross-platform widget plugins (e.g., `glance_widget`, `native_home_widgets`) already solve widget rendering, background refresh, and lock-screen support on both platforms — worth evaluating to cut Phase 1 timeline versus building two native widget codebases.

---

## 11. Licensing Decision: Swiss Ephemeris (AGPL vs. Professional License)

**Context:** the core calculation engine (Phase 0) needs an ephemeris library. Swiss Ephemeris is the industry-standard choice but is dual-licensed:
- **AGPL** — free, but its network-use clause is broader than plain GPL: it can require open-sourcing "the whole software project" if the software powers a public service, not just if the binary is distributed. Astrodienst's own license text says the choice must be made "before any public service using the developed software is activated" — language that appears to reach even a backend-only, non-API batch pipeline.
- **Professional Edition license** — one-time fee (reported ~CHF 700–1550 / ~$500–1700 depending on tier; confirm current price at astro.com before budgeting), valid 99 years, no source-disclosure obligation, closed-source use permitted.

**Decision process:**
1. Get a licensing attorney (or Astrodienst directly, via the drafted email) to confirm whether a backend-only batch-precompute architecture (no live API exposing Swiss Ephemeris) counts as a "public service" under their AGPL terms.
2. If AGPL must apply: isolate the Swiss-Ephemeris-calling code into its own repo/service, separate from the proprietary rule layer (tithi/nakshatra boundary logic, muhurta definitions) and app code, to minimize what must be open-sourced.
3. Weigh the strategic cost of open-sourcing the rule layer (competitors could reuse it) against the Professional License fee.

**Recommendation:** given the Professional License's low one-time cost relative to the risk of exposing proprietary rule logic, default to purchasing the Professional License unless legal/Astrodienst clarification comes back clearly favorable to the AGPL batch-only interpretation. Resolve this **before** Phase 0 engineering begins, since it affects repo/service architecture from the start.

**Status:** clarification email drafted (see attached), pending send + response before final decision.

**Note on monetization model:** whether the app is free, ad-supported, or paid does not change this decision. AGPL has no commercial/non-commercial carve-out — its obligations trigger on network/public-service use, not on whether revenue is generated. A free, ad-supported app has the same AGPL exposure as a paid one, and would pay the same flat Professional License fee if that route is chosen instead. Ad monetization itself (SDKs, data policies) is a separate business consideration, unrelated to the Swiss Ephemeris licensing question.

### 11.1 Phase 0 Architecture — If Proceeding Under AGPL

If the decision is to use the AGPL option rather than pay for the Professional License, Phase 0 must be architected to isolate AGPL's obligations to the smallest possible slice of the system. The guiding principle: AGPL's copyleft attaches to the program that contains/links Swiss Ephemeris; it does not automatically extend to a genuinely separate program that talks to it over a network via a generic protocol. The separation must be real, not cosmetic.

**Component split:**

```
[Ephemeris Microservice]  --HTTP-->  [Rule Layer + Orchestrator]  -->  [Static Dataset]  -->  [Mobile App]
   (AGPL, public repo)              (proprietary, private repo)      (data, proprietary)     (closed-source)
```

1. **Ephemeris Microservice (fully AGPL-3.0, public repo)**
   - Own repository, own deployable unit — never merged into the main codebase.
   - Narrow, generic API returning only raw astronomical facts (e.g. `POST /position { datetime_utc, lat, long } → { sun_longitude, moon_longitude, sunrise_utc, sunset_utc }`) — deliberately generic, not panchanga-specific, so the separation reads as a real independent service rather than an artificial copyleft workaround.
   - Published publicly with: AGPL-3.0 license file, preserved Astrodienst/Koch/Treindl copyright notices, any Swiss Ephemeris modifications also released under AGPL, and a Corresponding Source offer mechanism (e.g. a `/source` endpoint or static notice), even though the only caller is the internal pipeline.
   - No use of Astrodienst/author names in product marketing or promotion.

2. **Proprietary Rule Layer (closed-source, private repo)**
   - Ayanamsa correction, tithi/nakshatra boundary math (12° / 13°20' segments), Rahu Kalam/Yamaganda/Gulika Kalam rules (pure day-of-week + sunrise-sunset logic, no ephemeris call needed), muhurta/festival rule definitions.
   - Calls the Ephemeris Microservice only as an external network client — never imports its code or shares a process/binary with it.

3. **Precompute Orchestrator (closed-source)**
   - Loops over the location grid × date range, calls the microservice for raw positions, feeds results into the rule layer, writes the output dataset. Glue code only — never touches Swiss Ephemeris directly, so not AGPL.

4. **Generated Dataset (closed-source, ships in app)**
   - Static SQLite/JSON output (timestamps, labels) is data, not software — not covered by AGPL copyleft. This is what bundles into the mobile app.

**Compliance checklist:**
- [ ] Public repo for the microservice live before it is ever run against real data (treat first deployment as the license's "public service ... activated" trigger point)
- [ ] LICENSE file + preserved copyright notices in that repo
- [ ] Any Swiss Ephemeris source modifications tracked and published under AGPL
- [ ] Corresponding-source offer mechanism present, even for internal-only use
- [ ] Repo-level access control / CI check preventing proprietary rule-layer code from ever being committed into the microservice repo
- [ ] Engineering doc telling future contributors "this repo is AGPL — nothing proprietary goes here"

**Residual risk:** this "separate network client" pattern is standard industry practice but not legally bulletproof. If the two services are always co-deployed, never used independently, and exist purely to route around copyleft, an aggressive legal challenge could argue they're really one combined work artificially split — untested in court specifically for AGPL. Astrodienst's own license phrasing ("before any public service using the developed software is activated") is broader than plain AGPL text and could be read to expect the whole pipeline open, not just the microservice — reinforcing the need for the Astrodienst clarification email regardless of which path is chosen.

**Timeline/cost impact of choosing AGPL over the Professional License:** adds a second deployable service, network auth between services, a public repo to maintain, and ongoing code-review discipline to prevent proprietary code leaking across the boundary — recurring overhead that generally outweighs the one-time CHF 700–1550 Professional License fee. This is why the Professional License remains the default recommendation; the AGPL architecture above is provided for teams that want to proceed with AGPL regardless (e.g. open-source philosophy or budget constraints).

---

## 13. Deployment & Infrastructure

### 13.1 Phased Infrastructure Approach

Rather than committing to one cloud platform for the entire roadmap, infrastructure choice should follow the workload's actual shape at each phase — Phase 0's workload (a small, periodic batch job) has very different requirements than Phase 2's (precise, per-user, per-location scheduled push delivery).

**Phase 0–1: Oracle Cloud Always Free tier**
- The ephemeris microservice + precompute orchestrator is a small, non-real-time batch job (small city grid × date range). Oracle's Always Free Ampere A1 instance (2 OCPU / 12GB RAM as of the June 2026 reduction) comfortably handles this, plus 200GB block storage and 10TB/month egress at zero cost.
- Widgets and the daily fixed-time notification (Phase 1) read from a locally-cached, on-device dataset — minimal server load, still comfortably within the free tier.
- **Alternative pattern for the orchestrator specifically:** a scheduled GitHub Actions workflow (cron-triggered, calls the ephemeris service, runs the rule layer, commits the generated dataset) — zero infrastructure to manage, free on public repos / included minutes on private ones.

**Phase 2 onward: reassess — move notification/Live Activity triggering to a managed platform**
- Phase 2's contextual alerts ("Rahu Kalam starts in 15 min") and Live Activity updates require precise, per-user, per-location scheduled push delivery — potentially many users each needing a push at a different exact local moment. This needs a reliable scheduler/queue, not just a cron job on a VM.
- Oracle Always Free has no managed scheduling primitive (no equivalent to AWS EventBridge, GCP Cloud Scheduler, or Azure Notification Hubs) — hand-rolling this is possible but adds engineering burden and a single-VM point of failure for a time-sensitive feature.
- Oracle has also shown a pattern in 2026 of quietly reducing Always Free limits (ARM compute allocation halved in June 2026 with no announcement) and intermittent regional capacity issues on provisioning — acceptable risk for a zero-cost dev/Phase 0 environment, less acceptable as the sole backend for a user-facing, time-sensitive feature.
- **Recommendation:** treat Phase 2 as the deliberate infrastructure decision point. Migrate notification/Live Activity trigger logic to whichever of AWS (EventBridge + SNS), GCP (Cloud Scheduler + FCM), or Azure (Notification Hubs) is already in use elsewhere, or pick based on which startup credit program is most accessible at that time (see §13.2).
- Phase 3 (voice assistant webhooks, watch complications) and Phase 4 (calendar sync — largely client-side; OEM partnerships — not an infra concern) are infra-light and don't independently force a platform decision.

### 13.2 Startup Credit / Free-Tier Programs (verify current terms before applying — offers change frequently)

| Program | What you get | Gate | Notes |
|---|---|---|---|
| AWS Activate — Founders tier | Up to $1,000 | Self-serve, no VC needed | Easiest to claim immediately |
| AWS Activate — Portfolio tier | Up to $100,000 | Needs an Org ID from an accelerator/VC/partner | Relevant only if accelerator/VC-backed |
| Google for Startups Cloud — Start tier | Up to $2,000 | Self-serve, unfunded, <5 years old | Includes Firebase credits |
| Google for Startups Cloud — Scale tier | Up to $200,000 over 2 years | Requires institutional equity funding | Not relevant pre-funding |
| Microsoft for Startups — Founders Hub | $1,000 instant, staged up to $150,000 | **No funding/VC gate to start** | Most accessible large program; bundles GitHub Enterprise + Microsoft 365 |
| Oracle Cloud — Always Free tier | Permanent free resources (not credits) | No application | 2 OCPU/12GB Ampere VM (reduced June 2026), 200GB storage, 10TB egress/month |
| Oracle for Startups | Up to $100,000 | Mostly accelerator/VC-partnership-driven for higher tiers | Smaller/less commonly used than AWS/GCP/Azure programs |
| YC Startup School / Stripe Atlas | +$2,500 / +$5,000, stackable | Free enrollment / US incorporation | Worth claiming regardless of cloud choice |

**Practical read:** given Phase 0's actual compute needs are small enough to stay inside free tiers indefinitely, these credits matter more for *later* phases (managed push/scheduling infra, calendar sync service, analytics) than for Phase 0 itself. Worth claiming the self-serve, no-commitment ones (AWS Founders, GCP Start, Microsoft Founders Hub) now regardless, since they stack and cost nothing to claim.

---

## 14. Next Steps
1. Send the Swiss Ephemeris licensing clarification email and get a licensing attorney's read in parallel; resolve AGPL vs. Professional License before Phase 0 engineering starts.
2. Provision Oracle Cloud Always Free tier for Phase 0/1 hosting; claim AWS Activate Founders, GCP Start, and Microsoft Founders Hub credits now (self-serve, no cost) as a hedge for later phases.
3. Validate Phase 1 scope with a small user survey: "Would you add a home screen widget for panchanga?"
4. Prototype the Android Glance widget and iOS WidgetKit timeline in parallel (they can share the same backend data engine).
5. Instrument analytics for the North Star metric (ambient-view-to-app-open ratio) before launch, so Phase 1 impact can be measured immediately.
6. Revisit infrastructure choice at the start of Phase 2 — plan the move to managed push/scheduling (AWS EventBridge+SNS, GCP Cloud Scheduler+FCM, or Azure Notification Hubs) before contextual alerts/Live Activities are built.
