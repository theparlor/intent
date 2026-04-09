---
id: SIG-043
timestamp: 2026-04-09T04:34:00Z
source: agent-trace
confidence: 0.95
trust: 0.75
autonomy_level: L2
status: captured
cluster: discovery-gap
author: panel-review-2026-04-09
related_intents: []
referenced_by: []
parent_signal:
---
# Discovery theater — 42 internal signals, 1 external voice (Ari, SIG-010)

Four panels (Product Strategy, Strategy/Systems, Discovery/UX, Org Design) independently flagged that Intent's claim of "continuous discovery" is an internal echo chamber. All 42 captured signals prior to this review exercise were internal — Intent building Intent. SIG-010 ("Ari") is the single external practitioner voice, cited once, promoted to INT-003 as if one conversation were a pattern.

Direct quote from Discovery panel (Torres voice): *"SIG-010 is a data point, not a pattern. Where are the 15–20 interviews with senior PMs, eng managers, and staff engineers describing the pain in their own words? Where's the opportunity solution tree?"*

Direct quote from Product Strategy panel (Fitzpatrick voice): *"This is the opposite of the Mom Test — one anecdote promoted to pattern because it confirms what the builder already believed."*

## Why this matters

- No amount of honest hypothesis framing compensates for zero external evidence.
- Intent claims to be dogfooding discovery but is actually dogfooding confirmation bias.
- This is arguably the #1 blocker for Intent credibility — it's what Cagan/Torres/Blank would each identify first.

## Required outcome

- 10 structured discovery interviews with senior ICs/PMs using Claude Code daily
- Mom Test protocol (no leading questions, observe current behavior, avoid "would you use...")
- Each interview produces a signal file with verbatim pain quotes
- New page on site: external-signals.html showing these alongside internal dogfooding
- Opportunity tree built from the synthesis

## Dependencies

- Cannot be auto-executed (L2) — requires human to schedule and conduct interviews
- Brien owns this personally
- Target timeline: 2 weeks from today

## Trust Factors

- Clarity: 0.95 (4 panels converged on exact same recommendation)
- Blast radius: 0.3 (additive, doesn't break anything)
- Reversibility: 1.0 (interviews are pure additive signal)
- Testability: 0.9 (count external signals before/after)
- Precedent: 0.9 (Torres/Blank/Fitzpatrick all prescribe this)
