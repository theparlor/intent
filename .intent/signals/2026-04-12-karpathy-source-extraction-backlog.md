---
id: SIG-032
timestamp: 2026-04-12T23:30:00Z
source: session-review
confidence: 0.85
trust: 0.8
autonomy_level: L3
status: "symptom-repaired, upstream-pending"
cluster: knowledge-engine
upstream_control_path: "NONE TODAY for the residue: no mechanism tracks handoff/04-SOURCE-MANIFEST-AND-ATTRIBUTION.md Section I unfetched-source backlog; the 14 lower-priority sources (items 8-21) have no owner, trigger, or extraction schedule"
catch_mechanism: "tools/closure_writeboundary_check.py (closure-discipline write-boundary checker) flagged this signal 2026-07-03; NONE TODAY at content level: nothing detects that manifest Section I sources remain unfetched"
pipeline_survival: "the extracted material survives independent of this signal: 7 high-priority sources live as raw/research/2026-04-12-*.md and were ingested into knowledge/ per knowledge/log.md INGEST entries dated 2026-04-13 (THM-004 + RAT-003 created; THM-003 + RAT-002 updated; _index.md artifact count 16 to 19)"
author: brien
related_intents: []
referenced_by:
  - SIG-025
parent_signal: SIG-025
---
# Karpathy source manifest extraction backlog — 21 unfetched + 8 high-extraction sources never processed

The April 5 handoff package included `04-SOURCE-MANIFEST-AND-ATTRIBUTION.md` cataloging 82 distinct sources from the Karpathy × Intent research session. Two files from the zip (`04-SOURCE-MANIFEST-AND-ATTRIBUTION.md` and `README.md`) were never extracted into `handoff/` — they sat in Downloads for 7 days until discovered in session review on April 12.

**The extraction backlog includes:**

High-priority (directly relevant to active dev tracks):
1. **rvk7895/llm-knowledge-bases** — working Claude Code plugin implementing full /kb-init, compile, query, lint. Directly relevant to Knowledge Engine implementation.
2. **Karpathy GitHub Gist YAML templates** — verbatim frontmatter templates for wiki schema. Relevant to KE artifact templates.
3. **Martin Fowler SDD tools survey** — spec-driven development patterns (Kiro, spec-kit, Tessl). Relevant to Intent Spec product.
4. **Chet Richards OODA paper (PDF)** — detailed multi-path feedback diagrams mapping to Intent's bidirectional flows.
5. **CHI 2024 LLM-generated Personas study** — methodology confirming LLM personas indistinguishable from human-written. Relevant to persona pipeline validation.
6. **DEV Community agent memory article** — "Compile your knowledge, don't search it" — agent memory architecture relevant to MCP server design.
7. **Karpathy "Power to the People" essay** — LLMs benefiting individuals over institutions, relevant to Intent positioning.

Plus 14 additional unfetched sources (Section I of the manifest) of lower but non-zero extraction value.

**Why now:** Dev tracks (Knowledge Engine, persona system, Intent Spec product) are in tangentially overlapping spaces. Closing this loop before the next architectural review and interviews ensures the compiled knowledge base has full provenance and no blind spots from partially-read sources.

**Action:** L3 — extract high-priority sources in parallel, compile into `raw/research/` and update `knowledge/` artifacts. Surface any architectural implications as new signals.

## Remediation note (2026-07-03)

Closure-discipline write-boundary remediation. Status downgraded from `resolved` to `symptom-repaired, upstream-pending` because the signal admitted a residual backlog that was never worked.

**What landed (verified against repo state 2026-07-03):**
- All 7 high-priority sources were fetched and compiled: `raw/research/2026-04-12-rvk7895-llm-knowledge-bases.md`, `2026-04-12-karpathy-gist-llm-wiki.md`, `2026-04-12-fowler-sdd-tools-survey.md`, `2026-04-12-chet-richards-boyds-ooda-loop.md`, `2026-04-12-chi2024-llm-generated-personas.md`, `2026-04-12-rotifer-compile-dont-search-agent-memory.md`, `2026-04-12-karpathy-power-to-the-people.md`.
- All 7 were ingested into `knowledge/` on 2026-04-13 (see `knowledge/log.md` INGEST entries citing "SIG-032 extraction backlog": THM-004 and RAT-003 created, THM-003 and RAT-002 updated, artifact count 16 to 19).
- The two stranded zip files were extracted: `handoff/04-SOURCE-MANIFEST-AND-ATTRIBUTION.md` and `handoff/README.md` exist.
- Architectural implications were surfaced as new signals per the action clause: `2026-04-13-ke-mcp-write-back.md`, `2026-04-13-overwatch-incestuous-amplification.md`, `2026-04-13-trust-as-orientation-proxy.md` all reference SIG-032.

**What remains open:** the 14 lower-priority Section I sources (manifest items 8-21: Futurum Group, DAIR.AI diagram, Antigravity idea-file guide, Steph Ango thread, autoresearch README, Data Science Dojo explainer, Wiley double-loop paper, VSM Guide, Wind4Change, LogRocket, pmbod, GoPractice, Open Repo Guide, Nanochat explainer) were never fetched. `raw/research/` contains nothing for them. No mechanism tracks this residue; if the "lower but non-zero extraction value" claim still holds, it needs an owner or an explicit dismissal.
