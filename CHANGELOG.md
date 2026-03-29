# Changelog

## [0.6.0] - 2026-03-29

### Added
- **Signal Trust Schema**: Updated signal template with new fields: `trust` (0.0-1.0), `autonomy_level` (L0-L4), `status` (captured/active/dismissed/promoted), `cluster` (semantic grouping), `parent_signal` (relationships), `author`
- **intent-signal CLI**: Expanded management subcommands:
  - `intent-signal review [SIG-ID]` — Interactive or targeted signal triage
  - `intent-signal dismiss SIG-ID --reason "..."` — Mark signal as non-actionable
  - `intent-signal cluster SIG-ID1,SIG-ID2 --name "cluster"` — Assign semantic grouping
  - `intent-signal promote SIG-ID` — Escalate signal to intent track
  - `intent-signal list [--status captured|active|all]` — List signals with status filter
  - `intent-signal show SIG-ID` — Display full signal details with file path
- **13 Founding Signals Scored**: All signals in `.intent/signals/` updated with trust values (0.35-0.85), autonomy levels (L0-L2), and cluster assignments

### Changed
- **Signal Frontmatter Normalization**:
  - `date` → `timestamp` (ISO 8601)
  - `confidence: high|medium` → `confidence: 0.0-1.0` (numeric)
  - Added required `author` field
  - Moved `status`, `cluster`, `autonomy_level` to standard positions
- **Cluster Assignments**:
  - `work-ontology-design`: SIG-002, SIG-004, SIG-005, SIG-006
  - `signal-capture-surfaces`: SIG-003, SIG-007, SIG-010
  - `bootstrap-tooling`: SIG-011, SIG-013
  - `autonomous-infrastructure`: SIG-001, SIG-008, SIG-009, SIG-012

### Documentation
- Updated `CLAUDE.md` with expanded CLI documentation and checked off completed items
- Added Signal Management section to feature matrix

## [0.5.0] - 2026-03-27

### Initial Release
- Signal capture framework
- Trust scoring baseline
- Work ontology reference
