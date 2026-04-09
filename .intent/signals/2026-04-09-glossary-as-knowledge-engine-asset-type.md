---
id: SIG-055
timestamp: 2026-04-09T00:00:00Z
source: subaru-agile-academy-glossary-ingestion
confidence: 0.85
trust: 0.8
autonomy_level: L3
status: captured
cluster: knowledge-engine
author: glossary-ingestion-session-2026-04-09
related_intents: [knowledge-engine, compass-forge, federated-glossary, subaru-engagement]
referenced_by: []
parent_signal:
---
# Glossary is a first-class Knowledge Engine asset type, not a generic document

## Observation

During a Subaru M.A.R.S. Agile Academy glossary ingestion (2026-04-09), I converted a client .docx glossary into a structured card-per-term format in the engagement's deliverables folder. The source and output have a consistent shape that does not match the Knowledge Engine's current generic-document contract:

- **Card-native structure.** Each term is a self-contained unit with labeled fields: `term`, `category`, `definition`, `not` (anti-pattern), `when done well` (exemplary), and optionally `how it is measured` (for metrics), `status at <scope>` (for aspirational vs. current-state), and `alternate names` (for synonyms / client-specific vocabulary).
- **Federated by design.** Brien's existing architecture already federates glossaries: `memory/glossary.md` (Brien + industry + general terms), plus per-engagement `glossary.md` files at ASA, Subaru, FidelityGuaranty, Turnberry. Central vs. scoped scope is an explicit rule, not emergent.
- **Term-level provenance and freshness.** Terms drift as client vocabulary evolves (Subaru's "Leakage" for Escaped Defects, "PI Planning" as alternate for Cross Team Planning, "BRD/FRD" intake documents). A glossary card's freshness is not the same as the document's freshness — a single term can rot while the rest of the glossary stays current.
- **Disambiguation is an ontological concern.** Same term, different meanings across scopes (e.g., `SOA` = Subaru of America in Subaru, Service-Oriented Architecture industry-wide). Disambiguation is not a text-search problem; it's a scope-resolution problem that needs a canonical answer per context.
- **Downstream rendering.** Cards need to render to multiple surfaces: physical index cards, Miro sticky notes, Trello, Jira custom fields, training handouts, presentation slides. The ingested form must be extractable enough to feed all of these without manual rework.

The Knowledge Engine's current spec (at `Core/frameworks/intent/knowledge-engine/spec/`) treats documents as opaque payloads with enrichment, contracts, and federation. Glossaries are a distinct asset class where the atoms *inside* the payload are what matter — not the payload itself.

## Implication

If glossary is not recognized as a first-class asset type, three problems compound:

1. **Ingestion is a custom job every time.** The 2026-04-09 Subaru ingestion was a one-off: parse .docx, extract paragraph runs, cross-reference an older version for categories, apply typo fixes, restructure into cards. None of this is reusable. Every engagement glossary (ASA, F&G, Turnberry, Cargill) will face the same manual work.
2. **Federation boundaries blur under load.** As engagements grow, client-internal terms end up in central glossaries (NDA risk), or central terms end up duplicated inside engagement folders (drift risk). Without a first-class glossary type, the federation rule is advisory; with one, it's enforceable.
3. **Term-level operations are impossible.** Answering "which of my glossary terms are stale?" or "what terms conflict across engagements?" or "render all `core-agile` tagged cards to a Miro board" requires atomic access to individual entries. That's a different access pattern than document-level KE operations.

## Design Constraint

A Knowledge Engine glossary asset type should specify at minimum:

- **Entry schema.** Required fields: `term`, `definition`. Optional structured fields: `category`, `tags`, `not`, `when_done_well`, `how_measured`, `status`, `aliases`, `alternate_terms`, `origin` (canonical / client-adapted / client-native), `scope` (central / engagement / industry).
- **Scope resolver.** Given a term and a context (engagement), return the authoritative definition and note any conflicts with other scopes.
- **Federation rule.** Central glossary holds industry and Brien-scoped terms; engagement glossaries hold client-internal and engagement-adapted terms; a term can exist in both scopes with explicit precedence.
- **Freshness cadence per entry.** Each card carries its own `last_reviewed` timestamp; glossary-wide staleness is computed from the oldest entry, not the file mtime.
- **Ingest pipeline.** Take `.docx`, `.md`, `.html`, or direct structured input; extract entries; normalize into the schema; flag conflicts with existing entries; write to the right scope.
- **Render contracts.** Projections to Miro, Trello, index-card PDF, training handout, presentation slide — each card carries enough structure to render without manual rework.
- **Cross-reference graph.** A term can reference other terms (e.g., "see also", "alternate name for", "child of category"). Relationships are explicit edges, not prose.

## Next Hypotheses

- A single `glossary-entry` schema in the KE could formalize the existing informal pattern used across Subaru, ASA, F&G, Turnberry, and Brien's central `memory/glossary.md` without requiring any migration of existing content — the schema can be retrofit from the current card-based markdown format.
- The Subaru Agile & Jira glossary (`Work/Consulting/Engagements/Subaru/deliverables/curriculum/Agile Academy/Glossary_Agile_Jira.md`) can serve as the first structured reference implementation: 58 cards, 7 categories, alphabetical, inline metadata, parenthetical alternates, status markers, and source attribution. If the KE glossary schema can round-trip this file without loss, the schema is complete enough to ship.
- Glossary as an asset type is the bridge between the Unified Persona System (named-human registry, also card-based) and the Knowledge Engine's generic document contract — personas are specialized glossary entries with a different schema. A common "structured card" base type may underlie both.

## Referenced Artifacts

- `Work/Consulting/Engagements/Subaru/deliverables/curriculum/Agile Academy/Glossary_Agile_Jira.md` — 58-card reference implementation
- `memory/glossary.md` — Brien's central federated glossary (Brien + industry + general terms)
- `Work/Consulting/Engagements/Subaru/glossary.md` — engagement-scoped glossary (NDA-protected Subaru org terms)
- `Core/frameworks/intent/knowledge-engine/spec/federation.md` — existing federation contract (document-level, needs glossary-level extension)
- `Core/personas/registry/` — adjacent structured-card asset type (named-humans), useful as a prior art reference for the glossary schema
