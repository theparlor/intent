---
title: Tasks
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-29
updated: 2026-03-30
---
# Tasks

> The living backlog. Partitioned by autonomy level, not sprint boundary.
> See `spec/product-roadmap.md` for the full four-product assessment and signal cluster analysis.

---

## Autonomous — Agents can execute now

- [ ] Execute trace propagation → `tasks/trace-propagation.md` (unlocks all Observe work)
- [ ] Execute file tail adapter → `tasks/file-tail-adapter.md` (depends: trace propagation)
- [ ] Execute Grafana dashboard → `tasks/grafana-dashboard.md` (depends: file tail adapter)
- [ ] Emit signal cluster files to `.intent/` using cluster template (6 clusters identified in product-roadmap.md)
- [ ] Add `referenced_by` field to signal schema + update amplification scoring in models.py
- [ ] Refresh VERSION → 0.7.0, update CHANGELOG with MCP servers, templates, observability spec, site separation

## Completed — Done since last update

- [x] Build Intent, Spec, Contract templates → `.intent/templates/` (13 templates total)
- [x] Build `intent-spec` CLI tool → `bin/intent-spec`
- [x] Build 3 MCP servers (notice, spec, observe) → `servers/`
- [x] Define 6 subagent architecture → `servers/AGENT_DEFINITIONS.md`
- [x] Capture 24 signals (SIG-001 through SIG-024)
- [x] Spec observability stack (27KB) → `spec/observability-stack.md`
- [x] Configure OTel Collector → `observe/otel-collector-config.yaml`
- [x] Separate site to `theparlor/intent-site` with 23 pages, 3 pillars, 10 contracts
- [x] Enable GitHub Pages → live at `theparlor.github.io/intent/`
- [x] Update CLAUDE.md with four-product framing, agent handoff protocol

## Needs Learning — Requires human voice, external input, or architecture decision

- [ ] Write the Intent Manifesto — sharp, opinionated, shareable, 1500 words max (requires Brien's voice)
- [ ] Interview 5 practitioners experiencing AI + Agile friction (start with Ari's team)
- [ ] Document Brien's personal Intent methodology as Case Study #1
- [ ] Resolve vocabulary friction: "Notice" and "Execute" naming (SIG-019)
- [ ] Decide signal ID strategy for distributed environments (SIG-022/023)
- [ ] Sharpen audience personas — add company sizes, industries, day-in-the-life detail

## Parked — Blocked on prerequisite work

- [ ] Spec-to-agent handoff format (blocked: vocabulary decision + spec validation)
- [ ] Signal intelligence: clustering, pattern detection, promotion suggestions (blocked: ID strategy + trace propagation)
- [ ] Metrics framework (blocked: Grafana dashboard must be live with real data)
- [ ] Enterprise adoption path design (blocked: practitioner validation)
- [ ] Team size boundary research beyond 5 people (blocked: practitioner validation)

---

*Updated: 2026-03-30*
