---
id: SIG-031
timestamp: 2026-04-06T14:00:00Z
source: conversation
confidence: 0.9
trust: 0.85
autonomy_level: L3
status: promoted
cluster: workspace-operations
author: brien
related_intents: [INT-004]
referenced_by: []
parent_signal: SIG-025
---

# Engagement workspaces lack lifecycle hygiene for stale drafts

During the placement resolver build (2026-04-06), Brien identified that the new working/drafts/ directory will accumulate prior versions of deliverables by design — content cut from deliverables is preserved there per AGENTS.md §3 Hard Gate #6. However, there is no process to periodically review these accumulated drafts to: (1) identify unique material not present in the delivered version, (2) distinguish "record of what was cut" from "genuinely stale noise," (3) archive or eliminate content that adds no value. The same gap applies to working/notes/ and working/collaborative/ over time.

This is a lifecycle problem, not a placement problem. The placement resolver tells files WHERE to go. What's missing is a process that asks "should this file STILL be here?"

Brien noted: "we can separately establish a process to ferret through drafts or prior versions that have gone stale to truly assess if there is any unique material in there."

Evidence: Subaru engagement root had 7+ misplaced files accumulated over ~2 weeks. Pattern will repeat in working/ without hygiene.
