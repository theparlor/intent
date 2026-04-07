---
id: SIG-040
timestamp: 2026-04-06T18:00:00Z
source: conversation
confidence: 0.8
trust: 0.7
autonomy_level: L3
status: active
cluster: methodology-adoption
author: brien
related_intents: []
referenced_by: []
parent_signal: null
---
# Pawel Huryn identified as persona candidate — synthesizer-practitioner, Builder PM

## Observation

Brien identified Pawel Huryn (Product Compass, productcompass.pm) as a persona to add to the Skills Engine personality roster. Research completed via web scraping of his Substack and LinkedIn.

Key findings:
- **Positioning:** "#1 AI & PM newsletter" — 133K+ free subscribers, ~$25K/month revenue
- **Originality:** Primarily a synthesizer-practitioner. His PM Skills Marketplace (65 skills as Claude plugins) is his most original IP. His most-cited framework (AI Strategic Lens) is explicitly attributed to Miqdad Jaffer (OpenAI).
- **Key frameworks:** Triple Diamond (extends Double Diamond), Extended OST (extends Torres), ICE prioritization, Risk-Centric PM (4 risk categories)
- **Voice:** Hook-driven, visual frameworks, learn-by-doing, anti-complexity
- **Recent pivot:** From pure PM educator to AI-native Builder PM — Claudathon event, Claude Code tutorials, "Vibe Engineering" framing
- **Relationship to existing personas:** Extends Torres (OST), aligns with Cagan (risk-centric discovery), but positioned as practitioner-builder rather than theorist

Subscription is $120/year (Brien mentioned $85 — may be promotional). Bundle value ~$2,646 stated. Four video courses included.

## Implication

Huryn should be ingested through the new persona intake pipeline as first test case. He belongs in the personality roster as a Builder PM voice — the practitioner who actually ships with AI tools, complementing Torres (discovery theorist), Cagan (organizational model), and Singer (shaping discipline).

Subscription assessment: the $85-120/year is worth it primarily for the PM Skills Marketplace access — understanding his 65-skill architecture informs our own Skills Engine design. The courses themselves are synthesis of existing canon (Torres discovery, strategy masterclass) and are lower value given Brien's depth.

## Design Constraint

- Must be ingested through the new unified pipeline, not manually authored like existing personas
- Corpus should include Substack archive (public posts) + LinkedIn activity
- Primary freshening channel: productcompass.pm (weekly publication)
- Disambiguation anchors: "Product Compass", "Warsaw Poland", "#1 AI PM newsletter"
