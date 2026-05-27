---
title: Open Decisions — Brien Closes (2026-05-26)
created: 2026-05-26
depth_score: 4
depth_signals:
  file_size_kb: 13.6
  content_chars: 13424
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.15
closed: 2026-05-26
session_origin: Cowork Phase 1
status: closed-by-brien
owner: brien
purpose: "Phase 1 surfaces deltas before Phase 2 (Code) files anything into framework canon. These five decisions are L0/L1 (Brien sets). For each: recommendation, dependency-impact if closed otherwise, and the deliverable edit that flows from the close."
---
# Open Decisions — Closed by Brien 2026-05-26

## Closes recorded (this session)

| # | Decision | Brien close | Match recommendation? |
|---|---|---|---|
| 1 | Hosting | **Cloud (FastMCP / Cloudflare Workers)** | ✅ matches recommendation |
| 2 | Read/write scope | **Read-only first** | ✅ matches recommendation |
| 3 | Witness adapter timing | **Ship runbook now, Tier 2 conditional** | ✅ matches recommendation |
| 4 | Publish two-observabilities post | **Defaults to YES** (7-day rule, not overridden) | ✅ matches recommendation |
| 5 | Scope of "any product" | **D5-refined: tier-aware Day 1, redaction-map deferred** | ⚠ **OVERRIDE + REFINEMENT** — recommendation was "internal first"; Brien picked a third option that wasn't on the original close pass |

### Brien's reasoning on the D5 refinement (2026-05-26, post-Riley-walk)

> "Honor the structural commitment by designing tier-aware from Day 1 and shipping internal-only first — keep the architecture honest, defer the redaction-map authoring cost to when you actually need it. I want to be able to move fast now and I am not going to demo redaction or share to a source not read in, but I do not want to pay full refactor price later."

### What this means structurally

The substrate-exposure architecture is built tier-aware on Day 1, but only internal-product substrate is queryable from chat surfaces Day 1. Engagement substrate sits in scope-required-locked mode — a no-scope chat-surface session gets "no results" for engagement queries, enforced by the already-built scope-token mechanism. When Brien needs engagement-substrate query from a chat surface, he authors that engagement's redaction-map (~30 min one-time), drops it in, and the tier-aware server picks it up. No refactor.

### What lands Day 1 (per D5-refined)

- `.intent/classification.yaml` schema (declared + required at product creation; written by `bin/intent-init`)
- Scope-token mechanism in MCP client configs (Day 1 scopes: `internal`; Phase 2 scopes: `engagement:*`)
- MCP server applies binary classification check on every verb response (404/absent if no scope match)
- Witness `registered-products.yaml` carries classification field per entry
- `bin/intent-init` writes classification.yaml at scaffold time

### What's deferred to Phase 2 / on-demand

- Per-engagement `redaction-map.yaml` authoring (one per engagement; ~30 min each when needed)
- Shaped-view code (entity → role-token substitution, dollar-bucket smoothing, name tokenization)
- Inbound redaction (paired with write-back, also Phase 2)
- Engagement event federation to Witness (deferred until scope enforcement is hardened — conservation law means anything in the store stays, so this is the conservative default; can be flipped on after Phase 1 ships)

### Cost impact (revised from previous D5 framing)

- Original recommendation (internal-first, redaction Phase 2): ~2 weeks
- Previous D5 framing (engagements Day 1, redaction Phase 1): ~4-5 weeks
- **D5-refined (tier-aware Day 1, redaction-map deferred): ~2.5-3 weeks** — the architecture-Day-1 work adds ~3-4 days; the redaction-authoring + shaped-view work comes out of Phase 1 entirely.

The refinement keeps the structural commitment (substrate is genuinely tier-aware, no future refactor cost) while letting Brien move fast on the actual ship.

## Default-resolution rule

Any decision left unclosed for >7 days defaults to the recommendation. D4 (publish post) defaulted to YES per this rule. All other closes were explicit.

---

# Original decision pass (for reference)

The recommendation analysis below is preserved as the reasoning record. Closes above are canonical.

# Open Decisions — Brien Closure Required

Per §6 + §10 of the parent handoff, five decisions sit at Brien's level. Phase 1 surfaces them with recommendations and impact analysis. **Phase 2 should not file anything in framework canon until these are closed.**

## Decision 1 — Hosting (constraint crux per handoff §6.1)

**Question:** Is it acceptable to run a small always-on endpoint (FastMCP Cloud / Cloudflare Workers), or must everything stay desktop-resident with chat surfaces accepting staleness when desktop is offline?

**Recommendation:** **Yes — FastMCP Cloud / Cloudflare Workers.**

**Rationale (this is the constraint crux's resolution):**
- The Max-subscription / April-2026 routing-restriction constraint binds **third-party API routing** (services Anthropic would route requests to on the user's behalf). FastMCP-Cloud-hosted MCP servers consumed via Anthropic's official MCP transport are **user-owned endpoints**, not third-party API routing.
- The framework's existing infrastructure pre-validates this path: `intent-notice.fastmcp.cloud/mcp`, `intent-spec.fastmcp.cloud/mcp`, `intent-observe.fastmcp.cloud/mcp` are already deployed at $0/month per `ARCHITECTURE.md` lines 303-307. Adding `intent-knowledge.fastmcp.cloud/mcp` is a fourth member of the same family — no new hosting decision.
- This **unblocks the binding gate** the parent handoff flagged.

**If you close otherwise (desktop-resident):**
- Track A Phase 1 ships at degraded value — chat surfaces only work when desktop is online and reachable.
- The substrate-as-sibling principle (WS-DDR-025 / §2b of handoff) is structurally not delivered — the desktop remains a single point of failure.
- The architecture brief's hosting answer flips to a Tailscale + local MCP server configuration. Track A still has value (chat surfaces with sometimes-stale data are still better than no access), but the foundational architectural commitment changes.

**Deliverable impact of close:**
- WS-DDR-099 status: `proposed` → `accepted` (if cloud) or `proposed` → `superseded` and rewritten (if desktop-resident).
- DEC-010 validation criterion 5 stands either way (no new hosting bill).

---

## Decision 2 — Substrate exposure read/write scope (handoff §6.2)

**Question:** Read-only first, or read/write from day one?

**Recommendation:** **Read-only first.**

**Rationale:**
- Read-only is the fast win. The motivating use case (chat-surface Claude not-a-stranger when traveling) is satisfied by read-only.
- Write-back carries three meaningful sub-design loops: (a) auth — who can write?; (b) redaction — does the chat surface see PII or client-confidential content?; (c) conflict resolution — what if two surfaces write the same path? Each is a Phase 2 design loop in its own right.
- Write-back is shippable later via PR-as-arbiter (MCP write verb emits PR, not direct commit) — preserves DEC-003 (build in the open) and gives Brien a review surface. The Phase 1 design has not foreclosed this.

**If you close otherwise (read/write Day 1):**
- Phase 1 shipping target extends from ~2 weeks to ~5-6 weeks.
- Auth + redaction + conflict design must be solved before deploy.
- The PR-as-arbiter design is the natural fit either way — choosing now vs. later doesn't change the destination, just the sequencing.

**Deliverable impact of close:**
- Track A brief §"Phase 1 / Phase 2 cut" — if Day 1 write-back, fold Phase 2 verbs into Phase 1 with the auth/redaction milestones added as Phase 1 sub-tasks.
- DEC-010 verb table: add `capture_signal`, `propose_intent` (with PR-emit semantics) if Day 1 write-back.

---

## Decision 3 — Witness adapter completion timing (handoff §6 derivative)

**Question:** Is Track B blocked on the `engine/adapters/entire-io.py` stub becoming production, or can Track B's runbook ship with Tier 2 marked "ready when stub lands"?

**Recommendation:** **Ship the runbook now; Tier 2 marked "ready when stub lands."**

**Rationale:**
- The runbook explicitly carries the dependency: Tier 2 federation works **today** for the `.intent/events/events.jsonl` stream via the implemented `intent-events-jsonl.py` adapter. Tier 2 federation of the `.entire/` stream is gated on WIT-004 #5.
- Withholding the runbook until the stub ships doesn't accelerate the stub. It just delays the documented composition pattern.
- New products spawning today get Tier 0 and Tier 1 immediately; Tier 2 (`.intent/events/` flow) immediately; Tier 2 (Entire flow) when the stub lands. The runbook documents this honestly.

**If you close otherwise (block on stub completion):**
- Track B's runbook waits for WIT-004 #5 — which is itself dependent on Witness Phase 5 → Phase 6 transition (per WIT-004 migration order).
- Net effect: the operational scaffold sits in handoff/ for an indeterminate period while new products keep climbing the tiers manually. Documentation drift risk.

**Deliverable impact of close:**
- Track B runbook §"Tier 2 — Federation" already carries the honest framing. No edit needed if recommendation accepted. If you want a stronger framing ("Tier 2 fully live"), that requires deferring Phase 2 filing until the stub lands.

---

## Decision 4 — Publish the "two observabilities" framework-site post (handoff §6.4)

**Question:** Ship a short framework-site post on the cockpit/aircraft metaphor (DEC-009's authoring-vs-running-system distinction)?

**Recommendation:** **Yes — short, ~600-800 words, cockpit/aircraft metaphor as the hook.**

**Rationale (carried from the audit signal §"Open decisions"):**
- The distinction is clean and useful to practitioners who confuse session-trace with runtime-telemetry.
- It frames the OTel/Entire boundary correctly without exposing the over-trust history the audit identified — readers see the *current* framing, not the prior conflation.
- The cockpit/aircraft metaphor is the publishable hook — concrete and visual (which matches the framework's audience preferences, including the user's own visual-thinking orientation).
- Publishes downstream of DEC-009 — gives the ratified decision a public surface.

**If you close otherwise (don't publish):**
- DEC-009 lives in the decision log; the audit signal lives in `.intent/signals/`. Both are internally addressable. The framing reaches future framework readers but does not reach external practitioners.

**Deliverable impact of close:**
- Adds a deliverable to Phase 2 filing: a draft post (likely `Core/frameworks/intent-site/posts/two-observabilities.md` or similar — pending site structure). Not in Phase 1 scope unless you want me to draft it now; if so, say the word and the post drafts before this Cowork session ends.

---

## Decision 5 — Scope of "any product" (handoff §6.5)

**Question:** Does this composition pattern include client engagements (Subaru, ASA, etc.) or only Brien-internal products (Forge, Cast, Witness, Throughline, etc.)?

**Recommendation:** **Internal first; client engagements gated on Phase 2 redaction shim.**

**Rationale:**
- Confidentiality and redaction asymmetries are real. Subaru's signals, Subaru's decisions, Subaru's `.intent/` content cannot federate into a substrate that's exposed by an MCP endpoint reachable from the public internet, even if auth-gated.
- The internal-first sequencing is structurally simpler: every internal product can opt into Tier 2 federation via `bin/intent-init --register-with witness`. Client engagements opt **out** by default — they sit at Tier 0 + Tier 1 (purely local) until a redaction story exists.
- The redaction shim is a Phase 2 add: outbound (substrate → chat) and inbound (chat → substrate) carry a redaction pass keyed to a per-engagement classification rule. This belongs in the same Phase 2 milestone as substrate-exposure write-back (Decision 2).
- `bin/intent-init`'s `--register-with witness` flag defaults to **off** for engagements (with a per-engagement override at registration time).

**If you close otherwise (client engagements included Day 1):**
- The redaction story becomes Phase 1 scope. Significant complexity add — needs per-product classification rules, redaction primitives, and per-engagement audit.
- Likely doubles Phase 1 shipping target.

**Deliverable impact of close:**
- DEC-011's `--register-with witness` default semantics: if "internal only," default is "on for internal, off for engagement"; if "include engagements," default flips and redaction shim becomes Phase 1.
- WS-DDR-099 §"Consequences" — if engagements included Day 1, the redaction shim becomes a load-bearing Phase 1 dependency.

---

## How to close these decisions

Two acceptable ways:

1. **Reply with a one-line answer per decision** (e.g., "1: yes cloud; 2: read-only; 3: ship now; 4: yes publish; 5: internal first") — fast path, Phase 2 files immediately.

2. **Convene a brief decision pass** (Cowork or Code) on any decisions that need more discussion, leaving the rest at recommendation defaults.

**Any decision left unclosed for >7 days defaults to the recommendation** — this avoids the Phase 2 filing track stalling on an unclosed open decision. Brien can override at any time before or after default activation.

## Phase 2 filing readiness

Once decisions are closed:

- WS-DDR-099 status flips `proposed` → `accepted` (or rewritten if Decision 1 goes otherwise).
- DEC-010 + DEC-011 file into the decision log.
- Architecture brief files to `Core/frameworks/intent/spec/substrate-exposure-architecture.md`.
- Runbook files to `Core/frameworks/intent/playbooks/spawn-a-product.md`.
- Optional: two-observabilities post drafts and files per Decision 4 close.

All Phase 2 filing is mechanical given Brien's closes. Recommended dispatch: Sonnet sub-agent if Brien is occupied, with `00-README.md` + Brien's closes as the brief.
