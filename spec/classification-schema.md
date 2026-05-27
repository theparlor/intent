---
title: .intent/classification.yaml — Schema & Tier Semantics
type: framework
maturity: ratified
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-05-26
depth_score: 4
depth_signals:
  file_size_kb: 7.0
  content_chars: 6339
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.16
ratifies:
  - DEC-011 (2026-05-26)
upstream_control_path: "Core/frameworks/intent/bin/intent-init (writes this file) + Core/frameworks/intent/spec/classification-schema.md (this spec) + Core/products/witness/.intent/registered-products.yaml (per-tier federation registry)"
catch_mechanism: "bin/test-intent-init.sh asserts schema fields on every CI run; substrate-exposure MCP (Track A) reads tier on every query and returns 'absent' on scope mismatch Day 1."
pipeline_survival: "YES — schema enforced at creation by bin/intent-init and read at runtime by substrate-exposure MCP. Federation gated on tier value, not on file presence."
---
# `.intent/classification.yaml` — Schema & Tier Semantics

> Every product and engagement spawned by `bin/intent-init` (DEC-011) gets a per-instance classification declaration at creation. The file is the load-bearing per-product confidentiality contract — read on every substrate query, gates Witness federation, gates chat-surface visibility.

## Why this file exists

Confidentiality is **declared, not inferred.** Auto-discovery of a product's contents (file-tree scan, content sniffing) cannot reliably classify substrate that the framework will federate into a cross-portfolio event store with append-only conservation law. Once a confidential event lands in Witness without a tier marker, removing it violates the conservation law. So classification is written at birth, and the federation decision derives from it.

This is the operational encoding of DEC-011's "tier-aware Day 1, engagement federation deferred" pattern.

## Schema (v1, 2026-05-26)

```yaml
# .intent/classification.yaml
tier: internal                 # REQUIRED — see Tier vocabulary
declared_at: 2026-05-26        # REQUIRED — ISO date (UTC) of first declaration
declared_by: brien             # REQUIRED — operator who scaffolded the product
notes: ""                      # OPTIONAL — free-form context (rationale, exceptions)
```

### Field reference

| Field | Type | Required | Description |
|---|---|---|---|
| `tier` | string | yes | One of: `public`, `internal`, `confidential:<engagement-slug>`. See vocabulary below. |
| `declared_at` | ISO date | yes | UTC date of first declaration. Never overwritten on re-run; immutable once set. |
| `declared_by` | string | yes | Operator identity (typically `$USER`). Audit trail for who classified the product. |
| `notes` | string | no | Free-form rationale. Default empty string. Use for exceptions, escalations, or scope qualifiers. |

### Tier vocabulary

| Value | Meaning | Witness federation Day 1 | Chat-surface visibility (Track A MCP) |
|---|---|---|---|
| `public` | Open-source, externally shareable. No engagement constraint. | ON | All scopes |
| `internal` | The Parlor-internal but not engagement-confidential. Framework defaults to this for product-shaped paths. | ON | Internal scope and above |
| `confidential:<engagement-slug>` | Bound to a single engagement (e.g. `confidential:subaru`). | DEFERRED (Phase 2 light-up) | Engagement scope only; absent to no-scope chat surfaces Day 1 |

The `<engagement-slug>` MUST match `[a-z0-9][a-z0-9\-_]*` — lowercase ASCII, hyphens/underscores allowed, no spaces.

## Where it's written

| Path shape | Default tier | Classification required on CLI? |
|---|---|---|
| `Core/products/<slug>/` | `internal` | No (defaults applied) |
| `Core/engagements/<slug>/` | none — must declare explicitly | **Yes** — CLI exits 1 if `--classification` omitted |
| Anywhere else | none | **Yes** |

`bin/intent-init` writes the file as step 4 of the scaffold sequence (DEC-011 Behavior #4). The CLI refuses to overwrite an existing file with a different `tier` value — operator must explicitly remove or correct the existing declaration first.

## Where it's read

| Reader | Phase | Use |
|---|---|---|
| `bin/intent-init` (re-run guard) | Day 1 | Refuse tier mismatch on re-scaffold. |
| Witness ingest pipeline | Day 1 (internal) / Phase 2 (engagement) | Decide whether to pull the product's `.intent/events/events.jsonl` and `.entire/metadata/*` into the cross-portfolio event store. |
| Substrate-exposure MCP server (Track A — DEC-010) | Every query, Day 1 | Apply binary scope enforcement: return entity bodies only if the caller's scope token matches the product's tier. Engagement-tier substrate returns "absent" to no-scope callers Day 1; shaped-view substitution lights up in Phase 2 once per-engagement redaction-maps are authored. |

## Federation semantics

The tier value is **the only structural signal** Witness uses to decide whether to federate a product's substrate. The CLI codifies this in `step_register_witness`:

```python
if is_confidential(classification):
    return ("deferred (confidential tier)", registry_path, False)
```

For internal/public tiers, the CLI appends an entry to `Core/products/witness/.intent/registered-products.yaml`. For confidential tiers, the entry is **not** appended — federation is deferred to Phase 2 when:

1. Track A's substrate-exposure MCP scope enforcement has hot-run successfully (no leaks observed across N engagement queries);
2. The engagement's `redaction-map.yaml` has been authored (one-time, ~30 min per engagement);
3. Brien flips the engagement's Witness-registration switch on (one config line).

No retroactive code change is required — the tier-aware MCP server picks up the engagement-scope token once redaction-maps exist.

## Re-classification policy

Once `declared_at` is set, the file is immutable from the CLI's perspective. To re-classify:

1. Operator manually edits `.intent/classification.yaml` (or removes it).
2. If federation status changes (e.g., engagement → internal, or internal → confidential), operator must also reconcile the Witness registry by hand and capture a signal at `Core/frameworks/intent/.intent/signals/SIG-YYYY-MM-DD-reclassification-<slug>.md`.
3. Witness conservation law makes "demote tier from internal to confidential" a non-recoverable operation — events already federated cannot be unfederated. Treat demotion as a no-op for already-emitted events; only new events respect the new tier.

## Validation

- `bin/test-intent-init.sh` asserts the schema on every run (Test 1, Test 2, Test 5).
- The substrate-exposure MCP (Track A) will assert tier presence + scope on every query at runtime; missing or malformed `classification.yaml` causes the substrate to be treated as `confidential:unknown` (absent from no-scope chat surfaces).

## Related decisions

- **DEC-011** — `bin/intent-init` scaffold + per-product registry (this schema's parent).
- **DEC-010** — `intent-knowledge` MCP scope extended to substrate exposure (the file's primary reader at runtime).
- **DEC-009** — Entire.io scoped as authoring provenance (upstream — gives the federation pipeline its event sources).
- **WS-DDR-099** — Substrate exposure governance (Workspaces-level placement of redaction-maps and scope tokens).
