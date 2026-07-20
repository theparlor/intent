---
id: SIG-TEMPLATES-HUMAN-LAYER-2026-07-20
timestamp: 2026-07-20T00:00:00Z
source: conversation
confidence: 0.9
trust: 0.7
autonomy_level: L4
status: captured
cluster: narration-primer-adoption
author: claude-opus-4-8
related_intents: []
referenced_by: []
parent_signal:
---
# Every Intent work-artifact template now opens with a plain human lede

> **In plain terms:** The templates that stamp every signal, spec, and contract were machine-first, so a person reading a filled-in artifact cold had to parse dense structure to grasp what happened. We added a plain-language lede block to the top of all 13 templates, kept the precise structure below it as the record, and wrote the convention down so future templates follow it. The gap that remains: nothing automatically checks that a filled-in artifact actually wrote a real human lede instead of leaving the placeholder text.

Brien elevated the narration primer (/Users/brien/Workspaces/Core/templates/decision-framing/NARRATION-PRIMER.md) to standing policy for all pages and artifacts, and asked that it be applied immediately to template updates and to resolving the duplicate spec template.

What changed:
- A labeled lede blockquote ("In plain terms", or "What this protects" for contracts) added to all 12 work-artifact templates in .intent/templates/ plus knowledge-engine/templates/ddr.md, tuned per artifact type to the primer's three modes.
- Dash and arrow glyphs stripped from the human-facing layer of every touched template: em-dashes throughout, one bidirectional-arrow in the DDR lineage prose, status-flow arrows in frontmatter comments, and the arrow in the SPEC_TEMPLATE title. Auto-generated library-index related_entities pairs were left as-is because they regenerate on enrichment.
- The two spec templates reconciled by role and cross-linked rather than amputated: /Users/brien/Workspaces/Core/frameworks/intent/spec/SPEC_TEMPLATE.md is the authoring guide, /Users/brien/Workspaces/Core/frameworks/intent/.intent/templates/spec.md is the operational scaffold, and each now names and links the other.
- New /Users/brien/Workspaces/Core/frameworks/intent/.intent/templates/README.md records the convention so it is discoverable, not folklore.

## Trust Factors (optional, used by trust scorer)

- Clarity: high. The primer names the exact shape; application was mechanical.
- Blast radius: low. Templates are authoring scaffolds. No CLI or server reads them (verified: bin/ and servers/ generate their markdown inline).
- Reversibility: full. Git-tracked, single commit.
- Testability: partial. Presence of a lede is greppable; the quality of a filled-in lede is not machine-checkable.
- Precedent: yes. This is the template-level application of the standing narration-primer policy.

## Open question (catch-net gap)

Fixing the template fixes every future artifact at the source, because a new signal or spec is copied from these files. But nothing verifies that the author replaced the lede placeholder with a real human sentence instead of shipping the prompt text. A lint that flags an unfilled "In plain terms" placeholder in a committed artifact would close that gap. It is not built.
