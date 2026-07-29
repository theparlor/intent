---
title: Spacecraft Industry Scan — Disruption Vectors
id: DSR-IND-002
type: dossier
maturity: draft
confidentiality: public
created: 2026-06-10
updated: 2026-06-10
frameworks:
  - disruption-theory
  - porter-five-forces
  - product-operating-model
depth_score: 6
depth_signals:
  file_size_kb: 24.7
  content_chars: 18861
  entity_count: 3
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.11
related_entities:
  - pair: marty-cagan ↔ product-operating-model
    count: 116
    strength: 0.181
  - pair: product-operating-model ↔ teresa-torres
    count: 76
    strength: 0.129
  - pair: matthew-skelton ↔ product-operating-model
    count: 48
    strength: 0.068
  - pair: jeff-patton ↔ product-operating-model
    count: 44
    strength: 0.109
  - pair: manuel-pais ↔ product-operating-model
    count: 42
    strength: 0.077
subtype: industry
name: Spacecraft
slug: spacecraft
angle: disruption_vectors
depth: standard
confidence: 0.70
origin: agent
origin_surface: cowork (no hook fabric — draft by definition)
sources: inline (Sources & Confidence section); compiled from 3 parallel research passes, 2026-06-10
last_researched: 2026-06-10
---
# Industry Scan: Spacecraft

**Generated:** 2026-06-10 | **Angle:** Disruption vectors | **Depth:** Standard | **Engagement context:** None — reusable Core scan

> **Scope note:** "Spacecraft" here means the vehicles — satellites, capsules, stations, tugs, landers — their design, manufacture, and operation. Launch is treated as an exogenous force acting on spacecraft economics, not the subject. Where the industry is too broad, the scan privileges the satellite segment, which is where the disruption is concentrated.

## Compression (start here)

1. **The 60-year design constraint is collapsing.** Starship-class launch (9m fairing, 100+ t to LEO, $100–200/kg target vs. ~$1,000/kg on Falcon 9) inverts the optimization that defined spacecraft engineering since the 1960s — mass and volume stop being the binding constraints, so the bus commoditizes and value migrates to payloads, components, and software.
2. **A spacecraft category is eating a terrestrial industry for the first time.** Direct-to-device is commercially live (T-Satellite since July 2025; AST guiding $150–200M 2026 revenue), and the FCC's May 12, 2026 approval of SpaceX's $17B EchoStar spectrum purchase structurally locked the market before most competitors fielded hardware.
3. **Demand is bifurcating toward a single customer.** Defense proliferation (Golden Dome's $3.2B interceptor awards across 12 companies in April 2026; FY27 Space Force request of $71.3B, +123%) is the growth engine while civil/science demand shrinks (second consecutive ~23% NASA cut proposed) — concentration risk on the USG is rising exactly as the sector's valuations price in diversification.

**Strategic implication:** The industry is mid-transition from artisanal program engineering (one exquisite vehicle, decade timelines, cost-plus) to a product operating model (production lines, recurring service revenue, software-defined capability). The firms winning — SpaceX, Rocket Lab, Apex, Anduril — run product organizations; the firms losing run program offices. For consulting purposes, the entry point into this vertical is **operating-model and product-discipline transformation, not aerospace domain expertise** — the same transformation playbook as automotive's SDV shift (see DSR-IND-001), at higher velocity.

## What's Changing Right Now (90-Day View)

| Change | Evidence | Impact | Timeline |
|--------|----------|--------|----------|
| FCC approves SpaceX–EchoStar $17B spectrum deal (~65 MHz) | FCC DA 26-471, May 12, 2026 | 100x D2D capacity; locks spectrum moat; AT&T/T-Mobile/Verizon answered with a spectrum-pooling JV (May 14) | Immediate |
| Golden Dome space-based interceptor awards: up to $3.2B, 12 firms incl. SpaceX, Anduril, True Anomaly | DefenseScoop, Apr 24, 2026 | New spacecraft category (kinetic defense); software-native entrants seated beside primes | Immediate–12mo |
| Starship Flight 12: first V3 stack; ship succeeded, booster lost | SpaceX/Space.com, May 22, 2026 | V3 Starlink (~2 t/sat) deployment path opens; design-constraint relaxation becomes operational | 6–12mo |
| FCC waives Amazon Leo's 50% deadline with 20-month spectrum demotion (331 of 1,616 sats flown) | FCC DA 26-553; Via Satellite, Jun 5, 2026 | Kuiper survives but subordinated; Starlink's lead institutionalized by regulation | Immediate |
| New Glenn booster explodes on pad; LC-36 damaged ~1yr; Blue Moon MK1 stranded | CNBC, May 29; Spaceflight Now, Jun 4, 2026 | Launch-diversity thesis weakened; NASA urging alternate launchers; Kuiper manifest further squeezed | 6–12mo |
| SpaceX IPO prices ~Jun 11–12, 2026: ~$75B raise at ~$1.75T | CNBC/Axios, Jun 2026 | Largest IPO ever; public-market referendum on whole sector's economics | Immediate |
| Artemis II crewed lunar flyby succeeds (Apr 1–10) | NASA, Apr 2026 | Political cover for Artemis line-items even as FY27 proposes deep science cuts | 6–12mo |
| Rocket Lab record Q1 ($200M rev, $2.2B backlog); closes Mynaric, buys Motiv | GlobeNewswire, May 7, 2026 | Components/subsystems confirmed as the margin pool; consolidation of merchant supply | Immediate |
| Space Capital: Q1 2026 = $36B invested, largest quarter on record | Space Capital SIQ, Q1 2026 | Capital abundance; orbital compute "graduated from concept to capitalized competition" | Immediate |

---

## Market Structure (skeleton — context for the vectors)

### Value chain

```
Components & subsystems → Bus manufacture → Payload & integration → [Launch: exogenous] → Operations → In-orbit & downstream services
```

- **Margin concentration:** moving OUT of the bus, INTO components (optical terminals, rad-tolerant compute, propulsion, actuators — Rocket Lab's Space Systems is 68% of its Q1 2026 revenue) and INTO services (D2D wholesale, life extension, data).
- **Disintermediation pressure:** vertical integrators (SpaceX above all) collapse the whole chain internally — bus, payload, launch, operations, retail. Quilty estimates SpaceX builds >4,000 satellites/yr (~340/month), more than the rest of the western industry combined.
- **GEO→LEO migration:** active commercial GEO fleet essentially flat (539→573, 2022→Jan 2026) while LEO is ~80% of bus demand; Eutelsat LEO revenue +59.7% YoY vs. GEO −4.5% — revenue migration, not forecast.

### Player taxonomy

| Type | Key players | Role | Power | Trajectory |
|------|------------|------|-------|-----------|
| Vertically integrated hyperscaler | SpaceX (+xAI, merged Feb 2, 2026) | Sets cost floor across chain; ~10,400 sats on orbit | Launch + spectrum + manufacturing scale moat | Strengthening (IPO Jun 2026) |
| Incumbent primes | Lockheed, Northrop, Boeing, L3Harris, Airbus, Thales | Exquisite defense/civil programs; GEO legacy | Cleared facilities, program incumbency | Holding in defense, weakening in commercial |
| Challenger manufacturers | Rocket Lab, Apex (12 buses/mo), K2 ($15M 2-t bus), Firefly, Terran (now Lockheed) | Productized buses, merchant components | Speed + price; production-line economics | Gaining (RKLB +400% 12mo) |
| Software-native defense entrants | Anduril, Palantir, True Anomaly, Quindar | Mission software, autonomy, now Golden Dome hardware | Software talent + OTA contracting | Entering fast |
| Services & logistics | Northrop SpaceLogistics, Astroscale, Orbit Fab, Impulse ($200M+ backlog), Starfish | Refueling, life extension, orbit transfer | First-mover ops experience; USG-funded | Demos → early revenue |
| Adjacent entrants | Amazon (Leo + Globalstar), NVIDIA/Google/Starcloud (orbital compute), telcos (spectrum JV) | Importing cloud/telecom capital and demand | Balance sheets, customer bases | Entering; Amazon stumbling |
| Regulators | FCC, FAA (Part 450), Space Force/SDA, Commerce | Spectrum, debris, licensing, anchor demand | FCC is now market-structure kingmaker | Activist |

### Concentration

| Stage | Concentration | Trend | Implication |
|-------|--------------|-------|-------------|
| Launch (exogenous) | Near-monopoly (SpaceX) | New Glenn setback worsens it | Spacecraft designers rationally design *for SpaceX vehicles* — second-order lock-in |
| Bus manufacture | Fragmenting | Bespoke→production lines | Price/lead-time competition; bus commoditizes |
| Components | Consolidating | Rocket Lab roll-up (Mynaric, Motiv); CACI/ARKA $2.6B | Margin pool; supply bottlenecks (reaction wheels 12→52-wk lead times) |
| Constellation ops | Concentrated | Starlink 12M+ subs; China's Guowang+Qianfan ~350 sats combined | Scale operators set price umbrellas |
| In-orbit services | Embryonic oligopoly | 4 USG-funded missions in 2026 | Standards (e.g., RAFTI ports) will pick winners |

---

## Disruption Vectors

### Vector 1: Launch-cost and volume collapse → design-paradigm inversion

**Force:** Technology (Starship class) · **Direction:** Mass/volume-optimized exquisite buses → cheap, heavy, power-rich platforms · **Timeline:** Operative now for design decisions; broadly disruptive 2028–2031 at Starship cadence.
**Evidence:** Flight 12 (May 22, 2026) flew the first V3 stack and deployed V3 test articles; Starlink V3 (~2 t, ~1 Tbps) is Starship-native; K2's Gravitas (2 t, 20 kW, $15M, $60M STRATFI) launched March 2026 explicitly betting on this future; $100–200/kg target vs. ~$1,000/kg Falcon 9 (target unconfirmed by SpaceX tariff — confidence M).
**Who benefits:** payload innovators, power-hungry missions (compute, radar, D2D), new-design manufacturers. **Who loses:** legacy bus lines whose moat is miniaturization craft; composite/deployable specialists optimized for the old constraint.
**Signal strength:** Strong — actual flight hardware + $3B valuation (K2) staked on it.

### Vector 2: Mass manufacturing → the production line displaces the program office

**Force:** Business model / manufacturing · **Direction:** Cost-plus program engineering → rate production with product roadmaps · **Timeline:** Already happened at the constellation tier; mid-tier 1–3 years.
**Evidence:** SpaceX >4,000 sats/yr (Quilty, Apr 2026); Apex Factory One at 12 buses/month with 55k sq ft expansion; Lockheed buying Terran Orbital and winning SDA Tranche 3 with its buses; Airbus's 440-satellite digital-payload award; hiring data tilting to manufacturing/integration technicians (~2,200 open US spacecraft-manufacturing postings; "experience cliff" in mid-career program talent).
**Who benefits:** firms with factories and product managers. **Who loses:** primes' bespoke commercial lines; European GEO suppliers carrying legacy engineering overhead on stagnant order books.
**Signal strength:** Strong — revenue, backlog, and labor-market confirmation all align.

### Vector 3: Direct-to-device → spacecraft displace terrestrial telecom infrastructure

**Force:** Technology + regulatory (spectrum) · **Direction:** Cell towers/backhaul in coverage-gap and rural markets → wholesale satellite capacity inside carrier plans · **Timeline:** Commercial now; 5G-class service ~2027 (V2 DTC via Starship).
**Evidence:** T-Satellite live since Jul 2025 at $10/mo (free on top tiers); 650+ DTC satellites; FCC approval of the $17B EchoStar spectrum transfer (May 12, 2026) = exclusive contiguous 5G spectrum, ~100x capacity headroom; carriers' defensive spectrum JV (May 14); AST: FCC clearance for 248 sats (Apr 21), $14.7M Q1 revenue, $150–200M FY26 guidance, AT&T/Verizon/FirstNet deals — despite losing BlueBird-7 to New Glenn's wrong orbit.
**Who benefits:** Starlink overwhelmingly; AST as the carrier-aligned alternative; consumers at the edge. **Who loses:** rural tower economics, legacy MSS (Iridium-class), and any D2D hopeful without spectrum — the FCC just made spectrum the moat.
**Signal strength:** Strongest in the scan — real revenue, real regulatory lock-in, named counter-moves.

### Vector 4: Defense proliferation + software-native entrants → prime displacement

**Force:** Customer behavior (DoD) + geopolitics · **Direction:** Few exquisite assets from cleared primes → hundreds of cheap, replaceable sats and autonomy software from mixed vendors · **Timeline:** Now through FY2029 (SDA Tranche 3 launches).
**Evidence:** Golden Dome: $24.4B directed via reconciliation; April 2026 interceptor prototypes to 12 firms — SpaceX, Anduril, GITAI, True Anomaly, Quindar alongside Lockheed/Northrop/RTX; Palantir+Anduril own the software layer. SDA Tranche 3 Tracking: $3.5B/72 sats split across Lockheed, **Rocket Lab**, Northrop, L3Harris (Dec 2025). FY27 Space Force request $71.3B (+123%). Congress restored Tranche 3 Transport after the administration zeroed it — demand is robust but politically volatile.
**Who benefits:** challengers with rate production (Rocket Lab's first prime-tier win) and software houses. **Who loses:** primes' margin structure — they keep revenue but on commoditized buses with software value captured elsewhere.
**Signal strength:** Strong — contract awards, not press releases.

### Vector 5: Serviceable spacecraft → from disposable to durable asset class

**Force:** Technology + USG funding · **Direction:** Launch-and-abandon → refuel, repair, reposition, extend · **Timeline:** 2026 is the proof year; commercial normalcy 2028–2030.
**Evidence:** Four separately-funded US servicing/refueling missions in 2026 (SSC, DARPA, DIU, AFRL); Astroscale APS-R $61M first DoD hydrazine refueling (summer 2026); Orbit Fab's first GEO xenon depot (Jun 2026); Northrop MRV with three pre-sold pods after MEV's five revenue-years on Intelsat-901; Starfish Otter Pup 2 attempting first commercial docking with an unprepared LEO sat; Impulse $200M+ backlog, SES Helios agreement.
**Who benefits:** operators (asset life extension), servicers, and whoever owns the fueling-port standard. **Who loses:** replacement-sale revenue models; insurers must reprice; "cheap disposable constellation" logic partially undercut.
**Signal strength:** Medium-strong — government-funded demos with early commercial pull; watch conversion to non-USG revenue.

### Vector 6 (emergent): Orbital compute and in-space industrialization

**Force:** Adjacent technology spillover (AI power crunch) · **Direction:** Terrestrial data centers / labs → power-rich orbital platforms · **Timeline:** Speculative-to-3-years; capital is moving now.
**Evidence:** Starcloud flew an H100 (Nov 2025), trained an LLM on orbit (Dec 2025), raised $170M Series A (Mar 30, 2026), filed for 88,000 sats; SpaceX's stated merger rationale for xAI (Feb 2, 2026) was orbital data centers, with an FCC filing for up to 1M satellites / 100 GW; NVIDIA "Space Computing" initiative; Space Capital calls it a "capitalized competition" (SpaceX, Blue Origin, NVIDIA, Google). Varda: W-5 reentry for the US Navy (Jan 29, 2026) and first pharma collaboration (United Therapeutics, May 13, 2026).
**Who benefits:** high-power bus makers (K2 thesis), launch, energy-constrained AI players if economics close. **Who loses:** nobody yet — revenue ≈ 0; the bear case (terrestrial compute efficiency improves faster) is live.
**Signal strength:** Capital-strong, revenue-absent. Track Starcloud-2 (Blackwell, late 2026).

---

## Regulatory Landscape (brief — but load-bearing)

**Direction: regulation has shifted from constraining the industry to allocating its market structure.** The FCC picked winners twice in 30 days: the EchoStar spectrum approval (May 12) handed SpaceX the D2D moat; the Leo waiver (Jun 5) saved Amazon's license while demoting its spectrum priority until 50% deployment or March 2028 — institutionalizing Starlink's lead. The 5-year deorbit rule (effective Sep 2024) is now the de facto global LEO standard via US market access. ITAR: Categories IV/XV partially moved to EAR in 2024; DDTC signals further 2026 revisions — loosening, slowly. FAA Part 450 hit its March 10, 2026 compliance deadline amid industry complaints; SpARC reform pending. **Key risk:** demand-side whiplash — the same administration proposing Golden Dome billions proposed zeroing SDA Tranche 3 and cutting NASA 23% two years running; Congress keeps restoring. Spacecraft demand is increasingly a single politically-volatile customer.

## Investment Signals

| Signal | Direction | Evidence | Implication |
|--------|-----------|----------|-------------|
| VC/PE | Record | Q1 2026: $36B / 148 companies — largest quarter ever (Space Capital); GEOINT $3.8B in one quarter | Capital abundance; late-cycle exuberance risk |
| IPO | Watershed | SpaceX ~$75B at ~$1.75T (Jun 12); Firefly (FLY) May 2026 | Public-market repricing of whole sector — both ways |
| M&A | Capability roll-up | CACI/ARKA $2.6B; Rocket Lab: Mynaric ($155M, Apr 14) + Motiv (May 7); Lockheed/Terran; Amazon/Globalstar; A&D deals +41% (2025) | Components and spectrum are what's being bought — confirms where value sits |
| Public comps | Hot | RKLB +400% 12-mo, record $2.2B backlog; ASTS +324%; Planet RPO +361% | Defense/components names re-rated; execution misses punished (Redwire −23% on dilution) |

## Talent Signals

| Signal | Evidence | Implication |
|--------|----------|-------------|
| Manufacturing > design hiring | ~2,200 open US spacecraft-manufacturing roles; technician shortage "as severe as engineering" (SpaceNexus 2026) | Industry retooling from program offices to production lines — Vector 2 confirmed in the labor market |
| NASA brain drain | 2,100+ senior staff took voluntary separation (Goddard 607, JSC 366, KSC 311) | Civil-space institutional knowledge flowing to VC-backed defense space; science industrial base eroding |
| Mid-career "experience cliff" | Shortage of people who've run a full spacecraft program lifecycle | Premium on operating-model coaching and codified process — a consulting opening |
| Blue Origin | ~10% layoffs (Feb 2025 — pre-window, flagged) before New Glenn scale-up; then May 2026 pad loss | Execution risk concentrating launch power further in SpaceX |

---

## Contrarian View

**Consensus:** Space is a generational bull market — record Q1 funding, the largest IPO in history, defense superfunding, D2D's trillion-dollar telecom TAM.

**Bear case (strongest form):** The sector's economics are one company's economics, and that company loses money. Dan Primack (Axios, Jun 9, 2026): SpaceX 2025 = $4.9B net loss on ~$18.7B revenue with $20.7B capex — "the Rivian pattern before its IPO"; only 10–20% of the $1.75T is defensible from cash-generating business today; Starlink ARPU is *declining*; key-man risk is absolute ("premium goes poof"). Q1 2026 deepened the loss (−$4.28B in one quarter, CNBC). Morningstar fair-value estimates of $500B–1.1T imply 36–71% downside. Tim Farrar (TMF Associates): the core business doesn't support the valuation, and current pricing reflects absent competition, not durable economics. Quilty: Amazon Leo gen-1 costs ballooning to $16.5–20B vs. ~$10B planned. History rhymes: Teledesic, Iridium, Globalstar all proved LEO broadband can be technically right and financially dead. Insurance can't price the tail — debris/Kessler scenarios "exceed current reinsurance modeling" (IIS), with 36,500+ tracked objects; and the marginal demand driver (defense) is one customer whose own budget office tried to cancel the flagship programs Congress keeps rescuing.

**Falsifiability test:** Consensus is wrong if, by mid-2027: Starship cadence stalls below ~monthly (V3 economics don't materialize), Starlink ARPU decline outpaces subscriber growth, Golden Dome funding slips in FY28 appropriations, and SPCX trades materially below $135. Consensus is right if V3 deploys at rate, D2D revenue scales past $1B/yr, and a second commercial servicing customer class emerges beyond USG.

## Cross-Industry Implications

| Finding | Implies | For which domain |
|---------|---------|------------------|
| D2D + spectrum lock-in | Rural/edge connectivity strategy must assume satellite-in-the-bundle; tower/backhaul capex theses impaired | Telecom, private networks, rural utilities |
| Un-modelable orbital tail risk + servicing | New insurance products (life-extension warranties, debris liability); P&C exposure to correlated space loss | Insurance (adjacent context for F&G-type clients: asset-intensive risk pricing) |
| Varda + United Therapeutics | Microgravity formulation entering pharma R&D pipelines as a paid service | Pharma/biotech ops |
| Orbital compute capital wave | AI power constraint is severe enough to fund off-planet alternatives — terrestrial energy/data-center scarcity is the real signal | Energy, data-center real estate, AI infrastructure |
| Software-native entrants winning hardware programs (Anduril/Palantir on Golden Dome) | The "software company eats the integrator's margin" pattern repeats in any procurement-heavy industry | Automotive (SDV — see DSR-IND-001), med-tech, industrial |
| Program office → production line transition pain | Demand for product operating model, empowered teams, and continuous discovery practices in engineering-led orgs | Brien's consulting core |

---

## Depth Guarantee Audit

| Guarantee | Applied? | Key finding |
|-----------|----------|-------------|
| Adjacent sources | Y | Job postings (manufacturing-technician tilt), FCC dockets (DA 26-471/26-553), conference agenda (Space Symposium: "manufacturing at scale" now a headline theme), patent scan (diffuse AI-onboard activity; no bus-design surge — corroborates commoditization) |
| Temporal (90-day) | Y | Every vector anchored to Mar–Jun 2026 events; pre-window items flagged inline (Blue Origin layoffs, Varda Series C, T-Satellite launch) |
| Contrarian | Y | Named bears: Primack (Jun 9), Farrar, Morningstar; falsifiability test stated |
| Network (2nd-degree) | Y | Telecom carriers' defensive JV; insurers' modeling limits; pharma entering via Varda; NVIDIA/Google entering via compute — the disruption is visible in *adjacent* industries' counter-moves |
| Implications | Y | Six cross-boundary implications, two mapped to existing dossiers/engagement contexts |

## Sources & Confidence (load-bearing claims)

| Claim | Source | Date | Confidence |
|-------|--------|------|------------|
| FCC approves SpaceX–EchoStar $17B / ~65 MHz | FCC DA 26-471 | 2026-05-12 | H |
| FCC waives Leo 50% deadline; 20-mo spectrum demotion to Mar 2028; 331 sats | FCC DA 26-553; Via Satellite | 2026-06-05 | H |
| Golden Dome interceptor awards ≤$3.2B, 12 firms | DefenseScoop; Fortune | 2026-04-24/25 | H |
| SDA Tranche 3 Tracking $3.5B → LMT/RKLB/NOC/LHX, 72 sats | Spaceflight Now; SDA | 2025-12-20 | H |
| FY27 Space Force request $71.3B (+123%) | Breaking Defense; DefenseScoop | 2026-04 | H |
| NASA FY26 held ~flat at $24.4B; FY27 proposes $18.8B (−23%), science −47% | Planetary Society; NASA FY27 request; SpaceNews | 2026-04-03 | H |
| Starship Flight 12 first V3 test; ship ok, booster lost | SpaceX; Space.com | 2026-05-22 | H |
| Starship $100–200/kg target | Analyst estimates (exterrajsc et al.) | 2026-04 | M |
| SpaceX >4,000 sats/yr; ~10,400 on orbit; 10.3–12M subs | Quilty via Advanced Television; McDowell; IPO coverage | 2026-04/06 | M-H (sub counts vary by source) |
| SpaceX IPO ~$75B at ~$1.75T, lists Jun 12 (SPCX); 2025 loss $4.94B; Q1-26 loss $4.28B | CNBC; Axios (Primack) | 2026-06-09 | H |
| SpaceX–xAI all-stock merger ($250B for xAI), orbital-DC rationale | CNBC; D&O Diary | 2026-02-02 | H |
| AST: FCC 248-sat clearance; BB-7 lost; $14.7M Q1 rev; $150–200M FY26 guide | SpaceNews; AST Q1 | 2026-04-21 | H |
| K2 Gravitas launched (2 t, 20 kW, $15M; $60M STRATFI; $3B valuation) | TechCrunch; SpaceNews; PRNewswire | 2026-03-19 | H |
| Rocket Lab Q1 $200M rev / $2.2B backlog; Mynaric closed $155M; Motiv acquired | GlobeNewswire; Rocket Lab PR | 2026-05-07 | H |
| Four USG servicing/refueling missions in 2026; Astroscale APS-R $61M | Air & Space Forces Magazine | 2025-12-24 | H |
| Vast Haven-1 slips to NET Q1 2027; NASA CLD Phase 2 on hold | Payload; SpaceNews | 2026-01-20/28 | M-H |
| Artemis II success (Apr 1–10); New Glenn pad explosion (May 28) | NASA; CNBC; Spaceflight Now | 2026-04/05 | H |
| Starcloud $170M Series A; LLM trained on orbit Dec 2025 | TechCrunch; Starcloud | 2026-03-30 | H |
| Varda–United Therapeutics pharma collaboration | PRNewswire; MIT Tech Review | 2026-05-13 | H |
| Q1 2026 space investment $36B record | Space Capital SIQ | 2026-04 | H |
| China: Qianfan ~200 + Guowang ~190 sats | Orbital Radar; SpaceNews | 2026-04/06 | M |
| Primack bear case; Morningstar FV $500B–1.1T | Axios; secondary attribution | 2026-06-09 | H / M |

> **Known weak spots:** several Starlink consumer stats route through aggregator sites (confidence M); the $/kg target is analyst inference, not a SpaceX tariff; ispace M2 landing outcome unverified; Morningstar figure is second-hand. None are load-bearing for the vector conclusions.

---

*Draft produced in Cowork (no hook fabric). Pending Claude Code session: verify placement, recompile `knowledge/_index.md` (artifact count 23→24, Entity Dossiers 1→2), capture signals, commit.*
