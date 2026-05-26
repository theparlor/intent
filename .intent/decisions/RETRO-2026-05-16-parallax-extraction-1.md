---
decision_id: RETRO-2026-05-16-parallax-extraction-1
title: Low-rigor sources are ingested as positioning corroboration, not evidence — classify every finding
date: 2026-05-16
status: accepted
source: retroactive-extraction
session_date: 2026-05-16
references:
  - theparlor/intent:knowledge/themes/THM-005-agent-as-job-not-chat.md
  - theparlor/intent:raw/research/2026-05-16-rahul-ai-agent-team-playbook.md
---
# Low-rigor sources are ingested as positioning corroboration, not evidence — classify every finding

## Context

This session ingested a market-facing solo-founder playbook (Rahul) with no empirical method, vendor-adjacent intent (it closes by selling agent hosting). Such sources are common inputs — practitioner threads, vendor posts, conference hype. The risk is treating their agreement with Intent's theses as confirmation. A low-rigor source agreeing with a high-rigor conclusion adds zero evidential weight; it only tells you the idea has reached the market.

The "parallax read" framing handled this correctly here: the source was archived at confidence 0.55 with explicit caveat frontmatter, the theme stated up front that it carries "no independent evidential weight," and each pattern was tagged in a mapping table.

## Decision

When ingesting any source below the rigor bar (no method, vendor-adjacent, popularity-driven), the compiled artifact MUST classify every extracted finding into exactly one of three buckets:

1. **Evidence** — independent empirical support. Low-rigor sources almost never qualify; default is NOT this.
2. **Positioning corroboration** — the market is articulating a problem Intent already solved with rigor. Cite as market signal, never as confirmation. Does not raise confidence on the corroborated artifact.
3. **Rediscovery of an existing thesis** — the source restates something Intent already holds (often a founding theme). Must link back to the original artifact and be framed as *sharpening*, not discovery.

Source frontmatter carries a `caveat:` field and a confidence ceiling. The theme states evidential weight explicitly in its first paragraph.

## Alternatives Considered

1. **Reject low-rigor sources outright** — rejected. They have real value as positioning/parallax and occasionally contribute concrete techniques (this session absorbed two). The problem is misclassification, not the source.
2. **Single "relevance" tag per source** — rejected. Relevance collapses the evidence/positioning/rediscovery distinction, which is exactly the distinction that failed in this session.

## Consequences

- Ingest of low-rigor sources without per-finding classification is an incomplete artifact and should be flagged by lint.
- "Positioning corroboration" findings must not increment the confidence of the artifact they corroborate.
- The three-bucket rule pairs with the novelty-inflation guard (RETRO-2026-05-16-parallax-extraction-SIG-1): bucket 3 is the one the agent defaulted away from.
</content>
