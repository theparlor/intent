---
id: SIG-INTENT-BROKEN-LINKS-FIXED-2026-05-20
title: Intent spec/ — 8 broken cross-reference links repaired (CON-COH-004 finding)
date: 2026-05-20
framework: intent
category: cross-reference-repair
status: resolved
upstream_control_path: Core/frameworks/coherence-engineering/contracts/CON-COH-004-cross-reference-integrity.yaml
catch_mechanism: CON-COH-004 contract re-run will detect any new broken relative links across the Intent spec corpus; site-page links (../docs/*.html) are now commented out so a regression would re-add a parseable broken link the contract catches
pipeline_survival: link edits land in versioned .md files under spec/; no pipeline stage rewrites these (the docs/ render target lives in the separate theparlor/intent-site repo, not this one)
spec_ref: N/A (cleanup task, no spec)
parent_signal: ../../coherence-engineering/.intent/signals/SIG-CON-COH-RUN-2026-05-20.md
closes: CON-COH-004 broken-link item from SIG-CON-COH-RUN-2026-05-20 (Gate 2 advancement)
---

# SIG-INTENT-BROKEN-LINKS-FIXED-2026-05-20 — Cross-Reference Repairs

## Summary

CON-COH-004 (cross-reference integrity) flagged 8 broken relative links across
6 files in `Core/frameworks/intent/spec/`. All 8 repaired in this session.

## Repairs

### Path A — Updated link target (file exists at new path)

Both targets in `spec/SPEC_TEMPLATE.md` exist at known Workspaces locations
discovered via `find`; the link paths were stale (incorrect relative depth).

| File | Old target | New target |
|------|-----------|-----------|
| `spec/SPEC_TEMPLATE.md` | `DEVELOPMENT_OPERATING_SYSTEM.md` (same-dir, not present) | `../../../reference/DEVELOPMENT_OPERATING_SYSTEM.md` (resolves to `Core/reference/`) |
| `spec/SPEC_TEMPLATE.md` | `../../Work/Lab/Pipeline/ideas/INTENT_CONCEPT_BRIEF.md` (resolves to `Core/frameworks/Work/...`, doesn't exist) | `../../../../Work/Lab/Pipeline/ideas/INTENT_CONCEPT_BRIEF.md` (resolves to `Workspaces/Work/...`) |

### Path B — Removed link with comment (target structurally absent)

The 6 `../docs/*.html` links pointed at a site-page render target that does
not exist in this repo. Per `Core/frameworks/intent/CLAUDE.md`:

> The marketing site lives in `theparlor/intent-site` and deploys to
> https://theparlor.github.io/intent-site/. This repo has no `docs/` folder.

The `.md` source for each render is the spec file itself (self-render), so
there is no in-repo `.md` to redirect to. Replaced the link with a
`<!-- broken link removed: ../docs/...html -->` comment plus a plain-text
pointer to the intent-site repo.

| File | Original target | Disposition |
|------|----------------|-------------|
| `spec/decision-log.md` | `../docs/decisions.html` | Removed (self-render; site lives elsewhere) |
| `spec/signal-stream.md` | `../docs/signals.html` | Removed (self-render; site lives elsewhere) |
| `spec/repo-pattern.md` | `../docs/native-repos.html` | Removed (self-render; site lives elsewhere) |
| `spec/flow-diagram.md` | `../docs/flow-diagram.html` | Removed (self-render; site lives elsewhere) |
| `spec/event-catalog.md` | `../docs/event-catalog.html` | Removed (self-render; site lives elsewhere) |
| `spec/work-ontology.md` | `../docs/work-system.html` | Removed (self-render; site lives elsewhere) |

## Closure assertion (Three-gate check)

1. **Upstream control:** CON-COH-004 contract at
   `Core/frameworks/coherence-engineering/contracts/CON-COH-004-cross-reference-integrity.yaml`.
   Future broken links re-introduced into Intent spec/ will be caught by the
   next contract run — this signal is closing a contract-flagged item, and
   the same contract is the catch-net for any regression.

2. **Catch-net:** Same as above. The contract IS the catch-net; no new
   invariant needs to be authored. The next CON-COH-004 run should report
   zero broken links across these 6 files.

3. **Pipeline survival:** Markdown link edits in `spec/*.md` survive any
   pipeline run. The `docs/` render target was always a sibling-repo
   responsibility (`theparlor/intent-site`); no stage in this repo can
   regenerate or wipe the link comments.

All three gates hold → `status: resolved`.

## Related

- Parent contract-run signal: `Core/frameworks/coherence-engineering/.intent/signals/SIG-CON-COH-RUN-2026-05-20.md`
- Contract: `Core/frameworks/coherence-engineering/contracts/CON-COH-004-cross-reference-integrity.yaml`
- CLAUDE.md statement about site repo: `Core/frameworks/intent/CLAUDE.md` (§Site)
