---
title: "ULID-based ID generation for all entity IDs"
id: DEC-INTENT-020
type: decision-atom
created: 2026-04-09
date_inferred: false
scope: Core/frameworks/intent — entity ID scheme
status: ratified
ratified_at: 2026-04-09
ratified_by: "brien (2026-04-09; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #20; bin/lib/id_gen.sh; .intent/specs/SPEC-003-sig-022-ulid-migration.md"
catch_mechanism: "id_gen.sh is the only wired ID generation path; lint detects sequential counter patterns; backward-compat regex accepts legacy SIG-NNN IDs"
pipeline_survival: "id_gen.sh enforces ULID at every CLI tool call; sequential counter code removed"
source: "2026-04-09; SPEC-003; SIG-022"
---

# Decision: ULID-based ID generation for all entity IDs

> Ratified 2026-04-09. All 4 autonomy-grant gates pass. See SPEC-003, SIG-022.

## Context

Sequential counter IDs (`SIG-001`, `SIG-002`, etc.) broke under concurrent writers and server restarts. Two agents writing simultaneously would claim the same ID. Server restart would reset the counter. Global uniqueness was not guaranteed.

## Decision

All entity IDs (SIG, INT, SPEC, CON, DEC) are Crockford base32 ULIDs: `{PREFIX}-{26-char-ulid}`. Globally unique without coordination, timestamp-sortable, grep-friendly. Generated via `bin/lib/id_gen.sh` using `generate_id PREFIX`. Legacy `SIG-NNN` IDs remain valid via backward-compat regex — no migration of existing IDs required.

## Scope

Governs all new entity creation in the CLI suite and MCP server. Legacy IDs are preserved as-is; backward-compat regex handles both formats.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Sequential counter (per-entity reset prevention) | Still breaks under true concurrency; not globally unique | L3 — migration back |
| UUID4 (random) | Not timestamp-sortable; less grep-friendly; Crockford base32 is more readable | L4 |
| Database-assigned IDs | Requires always-on service; violates file-native principle | L2 |

## Reversibility

L4 — ULID generation is in `id_gen.sh`. Can add new ID scheme without removing ULID; backward-compat regex already demonstrates multi-format tolerance.

## Ratification Action

`bin/lib/id_gen.sh` with `generate_id PREFIX` function. All CLI tools source this library. Sequential counter code removed. SPEC-003 and SIG-022 document the migration. Backward-compat regex: `/^(SIG|INT|SPEC|CON|DEC)-([0-9]{3}|[0-9A-HJKMNP-TV-Z]{26})$/`.
