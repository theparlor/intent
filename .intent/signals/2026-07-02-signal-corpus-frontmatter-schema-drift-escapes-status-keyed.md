---
id: SIG-01KWH9B43AVC51T6DM9AYE7CW0
timestamp: 2026-07-02T11:27:35Z
source: agent-trace
author: unknown
confidence: 0.9
trust: 0.6
autonomy_level: L3
status: captured
cluster:
parent_signal:
related_intents: []
---
# Signal-corpus frontmatter schema drift escapes status-keyed enforcement

Across the 182-file .intent/signals/ corpus, frontmatter has drifted from any single schema: lifecycle is keyed off 'status:' in most files but 'maturity:' in others (SIG-INTENT-STATUS-ENUM-2026-07-02 carries BOTH maturity: active AND status: resolved); IDs split across id: / signal_id: / title-only; dates across created: / date: / timestamp:. 14 files carried NO status field at all (fixed in the 2026-07-02 intake drain). Same anti-pattern SIG-INTENT-STATUS-ENUM flagged for the value-term registry, one level up: any status-keyed enforcement (closure-discipline hooks, a future signal-corpus audit) silently skips files using an alternate/absent key. Also: the intent-signal CLI's canonical enum is {captured, active, clustered, promoted, dismissed} but the live corpus uses resolved/open/decided/needs-shaping too, so the tool and the corpus have themselves diverged. Proposed control: a canonical signal-frontmatter schema + a chain_audit-style linter that fails on out-of-schema keys/missing lifecycle field, normalized zero-violation-start. Noticed during intake-pipeline backlog drain; NOT fixed in this pass per decision to signal-ize before mass-editing 182 files.
