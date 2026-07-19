---
id: RETRO-2026-05-16-parallax-extraction-SIG-1
type: signal
category: process-gap
severity: medium
source: session-analysis
detected: 2026-05-16
topic: parallax-extraction
status: open
---

# Agent novelty-inflation: ingest claimed "new" without reconciling against founding themes

## Signal

During this session the agent compiled SIG-038 and labeled it "a genuinely new consideration, not corroboration." It was the opposite: a near-verbatim rediscovery of Intent's founding bottleneck-shift thesis (THM-002) applied to the human approval gate. Brien caught it ("the human gate review capacity is literally the original callout in intent"). The agent had to be corrected before the artifact was right.

## Evidence

- THM-005 mapping table originally read: "**New consideration → SIG-038.** Human review capacity is a finite resource not currently modeled."
- THM-002 (created 2026-04-05, confidence 0.90) already states the founding thesis the "new" signal restated.
- The agent read THM-002's sibling themes during the session but did not cross-check the new signal against them before asserting novelty.
- Correction required a human turn; the misframing would otherwise have entered the knowledge base and hidden a real architectural risk (Intent rebuilding the Jira/ceremony tax in its own pipeline).

## Implication

Novelty inflation is a recurring agent failure mode when compiling against an existing knowledge base: a new input feels new because the agent is not holding the founding themes in working context. This is the inverse of the contamination risk — instead of agent content masquerading as human-curated, an old thesis masquerades as a new finding, which buries lineage and weakens the very theme it should have sharpened.

## Recommended Action

Before any ingest artifact asserts a finding is "new," the compile step must reconcile it against the founding themes (THM-001, THM-002) and the Key Decisions list, and either (a) link as a sharpening of the existing thesis or (b) state explicitly which existing artifact it was checked against and why it differs. Add this as a lint check: a signal/theme containing "new" / "novel" / "not corroboration" with no link to a founding theme is flagged for reconciliation. Pairs with RETRO-2026-05-16-parallax-extraction-1 (bucket 3: rediscovery).

## Triage, 2026-07-08

Disposition: still pending. No novelty-inflation lint check exists anywhere in `knowledge-engine/` or `bin/` (grep for "novelty" / "founding theme" across those trees returns nothing). The only lint-style tooling found (`hooks/spec-age-lint.sh`) checks spec staleness, not novelty claims against founding themes. Needed control: the lint rule this signal specified, wired into whatever compiles ingest artifacts.
</content>
