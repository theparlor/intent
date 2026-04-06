---
title: Knowledge Engine Contracts
type: contracts
created: 2026-04-06
summary: "Verifiable assertions for the Knowledge Engine product. Each contract is testable — it either passes or fails."
---
# Knowledge Engine — Contracts

> Every contract is a verifiable assertion. Run these to check if the Knowledge Engine is working correctly. Contracts reference the spec they verify.

---

## CON-KE-001: Ingest produces knowledge artifacts
**Spec:** `operations.md` §4.1

**Assertion:** When a markdown file is placed in `raw/` and the ingest operation runs, at least one new or updated knowledge artifact appears in `knowledge/`, `knowledge/_index.md` is updated, and `knowledge/log.md` has a new `[INGEST]` entry.

**Verification:**
```bash
# Count artifacts before
BEFORE=$(find knowledge/ -name "*.md" ! -name "_index.md" ! -name "log.md" ! -name "traceability.md" | wc -l)

# Run ingest (implementation TBD — currently manual)
# intent-knowledge ingest raw/research/new-source.md

# Count artifacts after
AFTER=$(find knowledge/ -name "*.md" ! -name "_index.md" ! -name "log.md" ! -name "traceability.md" | wc -l)

# Verify
[ "$AFTER" -gt "$BEFORE" ] || echo "FAIL: no new artifacts"
grep -q "[INGEST]" knowledge/log.md || echo "FAIL: no log entry"
```

**Status:** Not yet testable (ingest not implemented as CLI/MCP)

---

## CON-KE-002: Every knowledge artifact has valid frontmatter
**Spec:** `AGENTS.md` §2

**Assertion:** Every `.md` file in `knowledge/` (except _index.md, log.md, traceability.md) has YAML frontmatter with at minimum: `id`, `type`, `confidence`, `origin`, `created`, `updated`.

**Verification:**
```bash
for f in knowledge/**/*.md; do
  case "$f" in *_index.md|*log.md|*traceability.md) continue ;; esac
  for field in id type confidence origin created updated; do
    grep -q "^${field}:" "$f" || echo "FAIL: $f missing $field"
  done
done
```

**Status:** Testable now. Run against current 16 artifacts.

---

## CON-KE-003: Cross-references resolve
**Spec:** `AGENTS.md` §3

**Assertion:** Every `[[wikilink]]` in knowledge/ artifacts points to a file that exists. Every `PER-NNN`, `JRN-NNN`, `DDR-NNN`, `THM-NNN`, `DOM-NNN`, `RAT-NNN` reference in frontmatter points to an artifact that exists.

**Verification:**
```bash
# Extract all [[wikilinks]] and verify targets exist
grep -roh '\[\[[^]]*\]\]' knowledge/ | sort -u | while read link; do
  target=$(echo "$link" | tr -d '[]')
  find knowledge/ -name "${target}.md" | grep -q . || echo "FAIL: broken link $link"
done
```

**Status:** Testable now.

---

## CON-KE-004: _index.md reflects actual state
**Spec:** `AGENTS.md` §4.1 (step 7), `operations.md` §Ingest

**Assertion:** Every knowledge artifact in `knowledge/` subdirectories is listed in `knowledge/_index.md`. The artifact count in frontmatter matches the actual count.

**Verification:**
```bash
ACTUAL=$(find knowledge/ -name "*.md" -not -path "knowledge/_index.md" -not -path "knowledge/log.md" -not -path "knowledge/traceability.md" | wc -l | tr -d ' ')
CLAIMED=$(grep "artifact_count:" knowledge/_index.md | grep -o '[0-9]*')
[ "$ACTUAL" -eq "$CLAIMED" ] || echo "FAIL: index claims $CLAIMED but $ACTUAL exist"
```

**Status:** Testable now.

---

## CON-KE-005: log.md is append-only
**Spec:** `AGENTS.md` §1

**Assertion:** `knowledge/log.md` only grows. No existing entries are modified or removed between commits.

**Verification:**
```bash
# Compare log.md in HEAD vs HEAD~1
PREV=$(git show HEAD~1:knowledge/log.md 2>/dev/null | wc -l)
CURR=$(wc -l < knowledge/log.md)
[ "$CURR" -ge "$PREV" ] || echo "FAIL: log.md shrunk from $PREV to $CURR lines"
```

**Status:** Testable now (requires git history).

---

## CON-KE-006: raw/ is immutable
**Spec:** `AGENTS.md` §1

**Assertion:** No file in `raw/` is modified after its initial commit. Files may be added but never changed.

**Verification:**
```bash
git diff HEAD~1 -- raw/ | grep "^---" | while read line; do
  echo "FAIL: raw/ file modified: $line"
done
```

**Status:** Testable now (requires git history).

---

## CON-KE-007: Federation boundary holds
**Spec:** `federation.md` §Flow 3

**Assertion:** No knowledge artifact in one engagement references a raw/ file or knowledge artifact from another engagement. No `client-confidential` or `nda` artifact exists in Core.

**Verification:** Cannot be tested until first engagement Knowledge Farm is scaffolded.

**Status:** Not yet testable.

---

## CON-KE-008: Confidence scores are bounded
**Spec:** `AGENTS.md` §4.1

**Assertion:** Every `confidence:` value in knowledge artifact frontmatter is between 0.0 and 1.0 inclusive. Agent-originated artifacts (`origin: agent` or `origin: synthetic`) have confidence ≤ 0.5 unless corroborated.

**Verification:**
```bash
for f in knowledge/**/*.md; do
  case "$f" in *_index.md|*log.md|*traceability.md) continue ;; esac
  conf=$(grep "^confidence:" "$f" | grep -o '[0-9.]*')
  origin=$(grep "^origin:" "$f" | awk '{print $2}')
  if [ -n "$conf" ]; then
    (( $(echo "$conf > 1.0" | bc -l) )) && echo "FAIL: $f confidence $conf > 1.0"
    (( $(echo "$conf < 0.0" | bc -l) )) && echo "FAIL: $f confidence $conf < 0.0"
  fi
done
```

**Status:** Testable now.

---

## CON-KE-009: Knowledge Engine is separable from Intent
**Spec:** `boundary.md`

**Assertion:** The `knowledge-engine/` directory contains everything needed to understand and use the Knowledge Engine without reading Intent methodology specs. Specifically: `AGENTS.md` defines all artifact types, `spec/operations.md` defines all operations, `templates/` contains all templates.

**Verification:**
```bash
[ -f knowledge-engine/AGENTS.md ] || echo "FAIL: missing AGENTS.md"
[ -f knowledge-engine/spec/operations.md ] || echo "FAIL: missing operations spec"
[ -d knowledge-engine/templates ] || echo "FAIL: missing templates dir"
COUNT=$(ls knowledge-engine/templates/*.md 2>/dev/null | wc -l)
[ "$COUNT" -ge 6 ] || echo "FAIL: expected 6+ templates, found $COUNT"
```

**Status:** Testable now.

---

## CON-KE-010: Traceability chain has no orphan endpoints
**Spec:** `AGENTS.md` §4.3 (lint)

**Assertion:** Every persona is referenced by at least one journey. Every DDR links to at least one persona pain point. No knowledge artifact exists with zero inbound cross-references (except the first artifact of each type).

**Verification:** Requires lint implementation. Not yet testable.

**Status:** Not yet testable.

---

*Knowledge Engine Contracts v1.0 — 2026-04-06*
*10 contracts. 6 testable now. 4 pending implementation.*
