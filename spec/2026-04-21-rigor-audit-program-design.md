---
title: Intent Framework Rigor Audit Program — Design
related:
  - SIG-033 (verification-ask drift — mid-session capture)
  - SIG-034 (entire.io partial landing + stale observability spec)
  - SIG-035 (security posture reframe — 4-layer model)
  - SIG-036 (Cast/Voices malformation as Intent discipline symptom)
  - memory/feedback_audit_vs_writethrough.md (root policy)
  - Core/frameworks/intent/spec/signal-stream.md
  - Core/frameworks/intent/knowledge-engine/templates/dor-dod-library.md
  - Core/reference/SHARING_AND_REDACTION_SCHEMA.md (de-promoted to Layer D input)
  - Core/products/witness/.intent/signals/SIG-WITNESS-001
depth_score: 4
depth_signals:
  file_size_kb: 13.0
  content_chars: 12339
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.16
date: 2026-04-21
status: draft (post-brainstorm, pre-plan)
author: Brien + Claude
---
# Intent Framework Rigor Audit Program — Design

## 1. Scope and intent

One-line thesis: **the Intent framework's discipline is currently advisory; downstream products (Cast, Voices, and future consumers) re-malform every run because there is no write-through enforcement**. This program installs the missing gates at the right altitude and grounds the fixes in landed observability and a declared security posture.

The program is **six sub-projects**, sequenced so that each has its preconditions in hand before it executes.

### Sequencing

```
#6 Security Posture (Phase a Understand)   ← here
      ↓
#5 entire.io install + propagate (D-scope)
      ↓
#2 Propagate last-week coding practices
      ↓
#1 Intent framework rigor audit
      ↓
#3 Witness forensics/event-tagging  ║  parallel  ║  #4 Dashboards
```

### Sub-project summaries

| # | Name | Key deliverable | Preconditions |
|---|---|---|---|
| 6 | Security Posture | 4-layer stance doc + access model + audit/signal surface + per-farm at-rest plan | — (starts here) |
| 5 | entire.io install + propagate | 17+ T1 repos capturing; observability-stack.md:361-367 corrected; acceptance bar = capturing | #6 Phase (a) (access model informs which farms may enable) |
| 2 | Coding practices propagation | DoR/DoD, audit-vs-writethrough, sibling-over-parent-child, decisioning, quality-baseline, aliasing first-class encoded into skills/hooks | #5 (clean observability) |
| 1 | Intent framework rigor audit | `enforcement-map.md` — every Intent primitive mapped to write-through mechanism; advisory-only gaps flagged | #2 (practices current) + #5 (observability landed) + #6 (posture clarity) |
| 3 | Witness forensics + event-tagging + drift pipeline | Per SIG-WITNESS-001 | #1 (write-through map exists) |
| 4 | Dashboards | Grafana Intent Observe + Witness forensics surface | #1 (metrics sources defined), #3 (event stream live) |

### Why this order (rationale)

- **#6 first** because every knowledge-farm addition compounds the gap without posture; Brien's own language was *"understand, define, implement"*
- **#5 second** because the audit (#1) needs the observability substrate to be landed and real, not partial; and because knowing the access model (from #6) changes which farms may enable
- **#2 third** because you cannot audit a framework (#1) against practices that have not yet been propagated into it
- **#1 fourth** because it is the upstream discipline fix that Cast/Voices (and every future product) inherit
- **#3 and #4 parallel last** because forensics/event-tagging depend on the enforcement-map being explicit, and dashboards depend on #3 emitting structured events

---

## 2. Sub-project #6 — Security Posture

### 2.1 4-layer model

| Layer | Concern | Current state | Gap |
|---|---|---|---|
| **A. At-rest encryption** | Disk-level protection of stored material | FileVault likely on (verify); macOS Keychain + SSH keys for credentials | Baseline exists; supplemental per-farm TBD |
| **B. Access control** | Credentials, rights, permissions, who/what may read each farm under which engagement | Implicit — no declared model | **Primary gap.** Cross-engagement bleed and agent exfiltration undefined |
| **C. Audit + signal** | What queries ran, by whom/what, against which farm; query log as content-discovery signal | Essentially none | **Primary gap.** Brien's own signal-driving use case unsupported |
| **D. Export redaction** | Narrow: content leaving trust boundary (client deliverable, external share) | `SHARING_AND_REDACTION_SCHEMA.md` draft, never implemented | Narrow scope; was misframed as universal |

### 2.2 Phase decomposition

Accepted sequencing: **(a) → (c) → (d) → (b)**.

| Phase | Work | Duration posture |
|---|---|---|
| **(a) Understand** | Asset inventory + threat model + use-case enumeration + current-posture audit | Active — until converged |
| **(c) Access model** | Credentials/rights/permissions/who-can-read-what-under-which-engagement | After (a) |
| **(d) Audit + signal** | Query-log capture surface + content-discovery signal pipeline | After (c) — needs actors defined |
| **(b) At-rest supplemental** | Per-farm supplemental encryption if threat-model demands | After (d) — defense-in-depth |

### 2.3 Phase (a) — Understand (detailed)

**Purpose:** produce the inputs that Phases (c), (d), and (b) consume. No implementation in this phase.

**Deliverables:**
1. **Knowledge-farm asset inventory** — list every farm with: path, type (registry / corpus / archetype output / index / corpus raw / session capture), size, sensitivity tier (candidate), current consumers (skills, agents, products), current access mode (unrestricted / implicit-tool-gated / manual-only), source(s) of content (public / scraped / ingested-from-engagement / generated-by-persona)
2. **Threat model** — enumerate live and latent risks: (i) cross-engagement bleed (content from engagement A surfaces in engagement B context), (ii) agent exfiltration (an agent reads farm X and emits in an external channel — email, Slack, PR, web), (iii) export-without-redaction (deliverable includes engagement-confidential content outside trust boundary), (iv) farm poisoning (unvalidated ingestion), (v) supply-chain disclosure (farm pointers in public repos)
3. **Use-case enumeration** — for each farm, list the canonical uses that MUST work (e.g., Cast registry → persona rendering into Forge; corpus → freshening; library-index → query-for-influence). These are the baseline that Phases (c)+(d) must preserve.
4. **Current-posture audit** — document what is already in place: FileVault status, Keychain scope, SSH key inventory, existing access controls, any implicit gates (filesystem perms, MCP boundaries, CLAUDE.md rules like external-comm L0). Note what works, what is coincidental.
5. **Gap list** — synthesize 1–4 into explicit gaps, each tagged to the layer it lives in (A/B/C/D).

**DoR (entry gate):**
- [x] Sub-project scope agreed
- [x] 4-layer model ratified (SIG-035)
- [x] Sequencing (a) → (c) → (d) → (b) ratified
- [ ] Placement decision: where does the posture doc live long-term? (spec/ for now; may promote to `Core/products/security-posture/`)

**DoD (exit gate):**
- [ ] Asset inventory committed at `Core/frameworks/intent/spec/security-posture/assets.md` (or equivalent)
- [ ] Threat model committed at `…/threat-model.md`
- [ ] Use-case list committed at `…/use-cases.md`
- [ ] Current-posture audit committed at `…/current-posture.md`
- [ ] Gap list committed at `…/gaps.md` with each gap tagged A/B/C/D
- [ ] Phase (c) pre-reads identified (credentials infrastructure, per-engagement access rules already in `Workspaces/AGENTS.md`)

**Out of scope for (a):**
- Any classifier implementation
- Any schema changes to existing farms
- Any redaction work (Layer D) — deferred
- Encryption changes (Layer A/B) — defer to (b) unless threat model forces earlier action

### 2.4 Phase (c) — Access Model (stubbed)

**Intent:** declare who/what can read which farm under which engagement, with enforcement mechanism named per rule.

**Anticipated outputs:**
- `access-model.md` — actors × farms × engagements matrix
- `enforcement.md` — per-rule mechanism (filesystem perm, MCP config boundary, skill gate, agent policy)
- Changes to `Workspaces/AGENTS.md` if needed
- Candidate integration with CLAUDE.md Autonomy Grants

**Detail deferred until (a) closes.**

### 2.5 Phase (d) — Audit + Signal (stubbed)

**Intent:** capture what queries hit which farms, emit content-discovery signals, make that observable.

**Anticipated outputs:**
- Query-log schema + capture path (likely leverages Witness per SIG-WITNESS-001)
- Signal-emission rules (what query patterns signal content-discovery opportunities vs. routine use)
- Dashboard slice in #4

**Detail deferred until (c) closes.**

### 2.6 Phase (b) — At-rest Supplemental (stubbed)

**Intent:** defense-in-depth encryption above FileVault if threat model (Phase a) demands.

**Anticipated outputs:**
- Per-farm encryption decision (yes/no/when)
- Key management plan (likely Keychain-anchored)
- Recovery/resilience plan

**Detail deferred until (d) closes. May be a no-op if threat model shows FileVault + access controls are sufficient.**

---

## 3. DoR/DoD — Program level

### 3.1 Program DoR (already met)

- [x] Cast/Voices malformation diagnosed as Intent discipline symptom (SIG-036)
- [x] Sub-project decomposition agreed (6 items)
- [x] Sequencing ratified (#6 → #5 → #2 → #1 → #3+#4)
- [x] Security posture reframed from redaction to 4-layer (SIG-035)
- [x] entire.io partial-landing state verified (SIG-034)
- [x] Design doc committed (this file)

### 3.2 Program DoD

- [ ] #1 `enforcement-map.md` lands and flags advisory-only Intent primitives as gaps
- [ ] #2 propagated practices are observable in Intent skill outputs (DoR/DoD gates enforced, audit-vs-writethrough discipline surfaces as write-through hooks, not scanners)
- [ ] #5 entire.io capturing in 17+ T1 repos with verified acceptance bar
- [ ] #6 Security posture 4 phases complete; access model + audit/signal layers operational
- [ ] #3 Witness forensics emitting structured events per SIG-WITNESS-001
- [ ] #4 Dashboards live with progress + current-state surfaces
- [ ] **Post-program acceptance test:** Cast and Voices run without malformation across ≥5 sessions without retrospective audit repair — the upstream fix resolved the downstream symptom

---

## 4. Risks and assumptions

### 4.1 Key assumptions

- **Intent framework is the right altitude for these gates.** If it turns out some gates belong in a lower layer (specific skills, specific products), the enforcement-map (#1 deliverable) will surface that.
- **entire.io v0.5.5 will install cleanly in T1 repos.** Verified on library-index. Untested on others; #5 Phase 1 is verification.
- **FileVault is on** — to be verified in Phase (a) current-posture audit.
- **Cast/Voices malformation is purely downstream** — post-#1 re-audit will confirm; if residual, localized fix follows.

### 4.2 Key risks

| Risk | Mitigation |
|---|---|
| Phase (a) expands indefinitely (understand-forever) | Hard stop: (a) has 5 named deliverables; once all committed, (a) closes |
| Sub-project #1 surfaces too many gaps to fix in one pass | Prioritize by blast-radius; queue lower-priority gaps as follow-up signals |
| entire.io 0.5.5 incompatible with current `.entire/` in library-index | Test migration path before propagating; rewind/reset available per v0.5 commands |
| Security posture Phase (c) requires changes to existing farm consumers | Accept scope expansion; this is the point of posture-first |
| Parallel #3 + #4 collide on metric definitions | Metric schema defined in #1's enforcement-map as a precondition |

### 4.3 Out of scope (program-level)

- Cast/Voices internal redesign (frozen until #1 closes)
- T2 (products, knowledge farms) entire.io propagation — follows posture (#6)
- Any new product creation — this program is fixing the discipline substrate, not building new products on it
- Existing SHARING_AND_REDACTION_SCHEMA.md implementation — it becomes a Layer D input, not a program output

---

## 5. Open questions

1. **Placement of security posture docs** — `Core/frameworks/intent/spec/security-posture/` (intent framework owns it) vs. `Core/products/security-posture/` (promote to product). Default: start under intent/spec, promote when it grows beyond single-phase scope.
2. **Does #6 Phase (d) — audit/signal layer — merge with #3 Witness forensics?** Both emit structured events. Candidate consolidation. Decision deferred to (d) detail.
3. **Intent-ification queue** — 13 Core frameworks missing `.intent/` entirely. Which are substrate (no `.intent/` needed), which are products (need `.intent/`), which are engagement-scoped? Triage as part of #1.
4. **`SHARING_AND_REDACTION_SCHEMA.md` lifecycle** — retain as Layer D input document? Fold into Phase (d) output? Decision in Phase (d) detail.

---

## 6. Immediate next

Sub-project #6 Phase (a) Understand begins. First deliverable: asset inventory. Output location: `Core/frameworks/intent/spec/security-posture/assets.md` (directory to be created).

This design doc is pre-plan. The writing-plans skill will convert this into an executable implementation plan for Phase (a), once the user reviews.
