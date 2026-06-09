---
title: Pre-Send Assertion Audit — enforcement spec
created: 2026-06-05
depth_score: 2
depth_signals:
  file_size_kb: 2.8
  content_chars: 2360
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.00
status: active
origin: SIG-2026-06-04-assert-from-inference-drift (Subaru engagement)
approved_by: "Brien (2026-06-05 — \"a presend assertion would be a good conservative check to have\")"
mechanism: Core/frameworks/intent/hooks/presend-assertion-check.sh (Stop hook)
---
# Pre-Send Assertion Audit

## Problem it closes
Client-facing assertions were being made from **inference or absence of evidence** and presented as verified fact (e.g., "the recommendation doesn't touch Build" — concluded from *not finding* a live Build board, never verifying what Build was). Memory and the existing OBSERVED/IMPLIED/GAP discipline did not prevent it; the only catch was human challenge. This promotes the discipline to a mechanism.

## The audit (run before any client-facing content is presented send-ready)
For every **load-bearing factual claim** in a draft meant to be sent/pasted to another human, state its basis:
- **VERIFIED** — name the source you actually checked (file path, ticket key, transcript, query result). Not "I ran the script" — the artifact.
- **INFERRED** — label it as inference; do not phrase it as fact.
- **UNKNOWN** — cut it, or turn it into a question to the recipient.

**Absence is not verification.** A claim drawn from *not finding* something ("I couldn't find X, so Y") is INFERRED at best — flag it explicitly.

Then: revise unsourced assertions to be sourced or hedged, add a short `assertion-audit` / `verified note` line, and re-present.

## Enforcement (Stop hook)
`presend-assertion-check.sh` fires when the response contains a **send-ready marker** (paste-ready, ready to send, "send this to <person>", a quoted reply block to a named recipient) AND **no assertion-audit marker** anywhere in the body. Conservative by design: suppresses only on an explicit audit marker, so loose "verified" usage still trips it. Errs toward firing.

- **Blocks** with a reminder to run the audit.
- **Bypass:** `PRESEND_ASSERTION_BYPASSED=1` (only when the content carries no factual claims).
- **Audit log:** `~/.claude/audit/presend-assertion-detections.log`

## Honest limit (no-catch-net boundary)
This hook catches the **blatant** case — send-ready client content with no sourcing language at all. It **cannot** detect a claim that is loosely labeled "verified" but wasn't actually checked; that remains judgment-level and is not mechanically lintable. The mechanism narrows the failure surface; it does not eliminate it. Authoring-time discipline (label every load-bearing claim verified/inferred/unknown; surface GAPs rather than smoothing them) remains required.
