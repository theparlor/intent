---
title: 05 Dec 011 Intent Init Scaffold Script
type: framework
maturity: final
confidentiality: internal
reusability: adaptable
created: 2026-05-27
companies:
  - subaru
depth_score: 4
depth_signals:
  file_size_kb: 8.0
  content_chars: 7884
  entity_count: 1
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.13
---
# DEC-011 — bin/intent-init scaffold script + Witness registered-products.yaml

> **Routing note for Phase 2 (Code):** When filing, append this decision to `Core/frameworks/intent/spec/decision-log.md` immediately after DEC-010.

## Decided

2026-05-26

## Context

The 2026-05-26 audit (SIG-ENTIRE-SCOPE-2026-05-26 → DEC-009) named the four composition tiers (Entire / events.jsonl / Witness federation / OTel runtime) but did not produce the operational scaffold. Today the Tier 0 + Tier 1 climb is ~6 minutes of manual setup per product, and the Tier 2 registration is ad-hoc.

The 2026-05-26 Cowork Phase 1 runbook (`handoff/cowork-phase1-2026-05-26/02-track-b-spawn-a-product-runbook.md`) proposes consolidating that setup into a single CLI: `bin/intent-init`.

## Decision (revised per Brien's D5-refined close, 2026-05-26)

The framework adopts a scaffold CLI at `Core/frameworks/intent/bin/intent-init` that takes a new product **or client engagement** through the Tier 0 + Tier 1 climb in one command. Per D5-refined: **classification is universal Day 1; Witness federation is selective by tier** — internal-tier federates Day 1, engagement-tier federation is deferred until Phase 2 (when scope enforcement has run hot and per-engagement redaction-maps are authored on demand).

```bash
bin/intent-init <product-name> \
  --path <relative-path> \
  --enable entire,events \
  --classification <tier> \         # REQUIRED — public | internal | confidential:<engagement>
  --register-with witness            # default ON for internal; auto-deferred for confidential:*
```

**Behavior:**

1. Create `<path>/.intent/{events,signals,intents,specs}` and `<path>/.entire/`.
2. Run `entire enable` in the new product directory.
3. Install the session-end hook (`hooks/session-end.sh`) into the product's `.claude/hooks/`.
4. **Write `<path>/.intent/classification.yaml`** with the declared tier. Schema is enforced — the CLI errors out on engagement-shaped paths (`Core/engagements/*`) without an explicit `--classification confidential:<engagement>`. Default `internal` for product-shaped paths (`Core/products/*`).
5. Append to `Core/products/products.json` (or `Core/engagements/engagements.json` for `confidential:*`-tier work).
6. **Witness registration logic:**
   - `public` or `internal` tier → append to `Core/products/witness/.intent/registered-products.yaml` Day 1 (federation ON).
   - `confidential:*` tier → **NOT** appended to Witness registry Day 1. Federation deferred to Phase 2. Conservation-law-respecting default (per Witness CONTEXT.md: events ingested into Witness's store are append-only and cannot be deleted, so we don't ingest confidential content until scope enforcement has hot-run).
7. Echo classification + federation status so the operator sees what just happened: e.g., `"Engagement 'subaru-q3-2026' at local Tier 0+1, classification 'confidential:subaru'. Federation: DEFERRED."`

**Companion artifacts:**
- `Core/products/witness/.intent/registered-products.yaml` — per-product registration with classification tier preserved (internal tier only Day 1).
- `<product>/.intent/classification.yaml` — universal per-product classification declaration. Read by the Track A substrate-exposure MCP on every query to apply binary scope enforcement Day 1; read again in Phase 2 to apply shaped-view substitutions from per-engagement redaction-maps.

## Alternatives considered

- **`~/.claude/scripts/intent-init`.** Rejected — developer-local rather than framework-canonical. New scaffold should ship with the framework, not with one developer's local config.
- **`Core/products/scaffolding/`** as a new product housing the scaffold. Rejected — creates a meta-product with one tool and no other inhabitants, violating product-shape conventions (every other product has its own substantive surface).
- **Auto-discovery (scan `Core/products/*/.entire/`)** instead of explicit `registered-products.yaml`. Rejected — some products (client engagements with confidentiality constraints) will need to opt out of federation. Explicit registration is the safer default. Revisitable if portfolio grows past ~50 products.
- **`bin/intent-init` only, no Witness registry file** — products auto-register by writing to a Witness-watched path. Rejected as more complex than needed at current scale.

## Rationale

- **Reduces per-product cost** from ~6 minutes manual + ~2 minutes Witness registration to ~30 seconds single command.
- **Sibling of the existing `bin/` family** (`bin/intent-knowledge` planned per E3 track, `bin/lib/id_gen.sh` already shipping). The CLI suite already exists; intent-init slots in as one more entry.
- **Explicit registration matches WS-DDR-025's structural commitments.** Sibling composition with declared interfaces — Witness's registered-products.yaml is the declared interface.
- **Tier-aware scaffold Day 1, engagement federation deferred (D5-refined).** Every product gets a classification declaration at birth. The structural commitment to multi-consumer substrate is honored Day 1 — but Witness federation for confidential-tier substrate waits until Phase 2 because Witness's append-only conservation law makes "let's just put it in and figure scope out later" a non-recoverable mistake. Internal-tier products federate immediately; engagement-tier products sit at local Tier 0+1 until the scope-enforcement path has run hot.
- **Confidentiality is declared, not inferred.** `--classification confidential:<engagement>` is the explicit lock. Default `internal` is safe for Brien's own product work; engagements must declare their tier at creation. The CLI errors out if it detects engagement-shaped path patterns (`Core/engagements/*`) without explicit `--classification`.
- **No refactor cost later.** When Brien needs chat-surface query against an engagement substrate, the work is: (a) author the engagement's `redaction-map.yaml` (~30 min one-time); (b) flip the engagement's Witness-registration switch on (one config line); (c) the already-built tier-aware MCP server picks up the engagement-scope token. No code change in the scaffold or the server.

## Consequences

- **Positive.** Spinning up a new product becomes a 30-second operation. Lowers the activation cost of new product creation — encourages signal-rich product proliferation in line with the methodology.
- **Positive.** Tier 2 registration becomes auditable (the yaml is git-tracked, decisions about which products federate are recorded).
- **Cost.** One CLI to maintain. Bash or Python; recommend Python for portability with the rest of the framework.
- **Risk.** If the products.json schema evolves, `bin/intent-init` must evolve with it. Mitigation: products.json already has a manual-curation discipline; one more writer is not a structural risk.

## Validation criteria

This decision is validated when:

1. `bin/intent-init my-new-product --path Core/products/my-new-product/ --enable entire,events --register-with witness` succeeds end-to-end.
2. The product gets a working Tier 1 setup (verifiable via `tail -1 .intent/events/events.jsonl` after a test session).
3. The Witness registered-products.yaml gets a correctly-shaped entry.
4. `Core/products/products.json` gets a correctly-shaped entry.
5. The Tier 2 federation activates once `engine/adapters/entire-io.py` lands (independent track, WIT-004 #5).

## Related

- WS-DDR-099 (substrate exposure — Track A sibling)
- DEC-010 (intent-knowledge MCP scope extension — Track A sibling)
- DEC-009 (Entire scoped as authoring provenance — upstream)
- WIT-004 #5 (`engine/adapters/entire-io.py` stub completion — Tier 2 dependency)
- Runbook: `handoff/cowork-phase1-2026-05-26/02-track-b-spawn-a-product-runbook.md`

## Supporting evidence

`/Users/brien/Workspaces/Core/frameworks/intent/handoff/cowork-phase1-2026-05-26/02-track-b-spawn-a-product-runbook.md`
