---
title: Spawn Prompt — Repo Hygiene Portfolio Rollout (self-discovering)
id: SPAWN-REPO-HYGIENE-PORTFOLIO
type: spawn-prompt
created: 2026-07-02
status: canonical
implements: playbooks/repo-hygiene-convention.md (CONV-REPO-HYGIENE-001)
composes: spawn-prompts/repo-hygiene-rollout.md (SPAWN-REPO-HYGIENE-ROLLOUT — the per-repo unit this fans out)
upstream_control_path: Core/frameworks/intent/spawn-prompts/repo-hygiene-portfolio-rollout.md (this file)
catch_mechanism: "self-discovers targets so no stale hardcoded list can misfire; classifies into tracks before acting; per-repo sub-agents inherit SPAWN-REPO-HYGIENE-ROLLOUT rails (branch+draft-PR-only, no working-memory deletion, investigate-before-delete, tests-gate-every-fix); forks/archived/unsure are skipped or surfaced, not touched"
pipeline_survival: "self-contained pasteable artifact; one paste into an org-scoped session; produces draft PRs + a portfolio scorecard, durable in git"
usage: "Don't paste this whole file — it's committed. In a NEW org-scoped session (Opus, fast mode) paste the 2-line launcher: `Read theparlor/intent/spawn-prompts/repo-hygiene-portfolio-rollout.md and execute it against the theparlor org. Follow it exactly (including its GROUND TRUTH files). Show me the STEP 2 inventory and wait for my go-ahead before STEP 3.`"
model_guidance:
  orchestrator: opus-4.8 (fast mode) — classification judgment, safety gating, portfolio synthesis
  track_a_build: opus-4.8 — get a green build/test, investigate drift without breaking imports
  track_c_site: sonnet-5 — mechanical README + binary light pass
  not: "fable (prose-shaped, not hygiene) / haiku (too light for repo-write stakes)"
---
# Spawn Prompt: Repo Hygiene Portfolio Rollout

> Paste into a NEW session that has **org-wide GitHub access** (scope the environment to the whole org, or
> the discovery step only sees public repos). Run the orchestrator on **Opus 4.8 (fast mode)**.

---

You are running the Intent Repo Hygiene Rollout across my entire GitHub org, **theparlor**.
This session has org-wide GitHub access. Discover the repos yourself — do not assume a list.

## GROUND TRUTH (read first, from the `intent` repo)
- Convention:   `playbooks/repo-hygiene-convention.md`   (CONV-REPO-HYGIENE-001, checks H1–H8)
- Per-repo unit: `spawn-prompts/repo-hygiene-rollout.md`  (SPAWN-REPO-HYGIENE-ROLLOUT, procedure + safety rails)

Read both so you have the 8 checks and the non-negotiable rails. Everything below assumes them.
(If the `intent` repo is not checked out here, ask me to paste the convention text before proceeding.)

## STEP 1 — SELF-DISCOVER
Call `get_me` to confirm identity/permissions. Then list EVERY repository under the `theparlor` org —
public AND private — paginating until you have them all (expect ~70). For each capture:
name, visibility, primary language, description, is_fork, archived, pushed_at, default_branch.
Print the full inventory as a table before doing anything else.

## STEP 2 — CLASSIFY each repo into a track (state your reasoning per repo)
- **SKIP** — `is_fork == true` (upstream owns conventions, e.g. google_workspace_mcp); `archived == true`;
  or already done (`intent`, PR #6).
- **TRACK A** — real software (source + tests/build). Full H1–H8, stack-adapted
  (`npm ci && npm test` / `cargo test` / pytest-via-venv / `go test`). e.g. codeburn = TypeScript.
- **TRACK C** — static site (HTML-only, `-site` suffix, or "pressure-test"/"noindex" in description).
  LIGHT pass only: H3 (README leads with substance), H7 (no tracked binaries), H8 (scope note).
  Do NOT force a Makefile/test target onto a static site (H1/H2/H6 are N/A).
- **UNSURE** — can't confidently bucket → list it and ASK me. Don't guess.

Note for me (don't act on it): my PRODUCT code (loom, voices, topography, forge, cast, pulse, …) lives in
my LOCAL Workspaces monorepo, not as GitHub repos — the GitHub `*-site` repos are their marketing surfaces.
So Track A on GitHub is mostly standalone tools; the full product rollout is a separate LOCAL job. Flag if
a `*-site` repo actually contains app code (then it's Track A, not C).

## STEP 3 — EXECUTE (fan out; parallelize)
**Prep — clone first (this is how a sub-agent gets its repo on disk).** Sub-agents share one filesystem,
so before dispatching, `git clone` each actionable repo into its own directory `./_hygiene/<repo>/`
(clone over HTTPS with this session's token; shallow clone is fine). Parallel sub-agents each work in
their own clone dir → no collisions. Add `_hygiene/` to your session's ignore so it never gets committed
into `intent`.

**Dispatch — one sub-agent per actionable repo (parallel).** Model: **Sonnet 5** for Track C and simple
Track A; **Opus 4.8** for any Track A repo with a real build/test to get green. Hand each sub-agent the
full SPAWN-REPO-HYGIENE-ROLLOUT text with TARGET filled (TARGET_NAME; TARGET_PATH=absolute path to
`./_hygiene/<repo>/`; BRANCH=`chore/repo-hygiene-rollout`) and its assigned TRACK. Each sub-agent:
works ONLY inside its own clone dir; commits there; pushes the branch to its origin; opens a DRAFT PR for
**that** repo via GitHub (correct owner/repo); returns its H1–H8 scorecard as its final message.
Repeat these rails to every sub-agent, verbatim:
- Branch + DRAFT PR only. NEVER merge.
- Never delete/archive working-memory (signals, decisions, knowledge, specs). Make sprawl navigable, not smaller.
- No mass prose/jargon rewrites. Trimming cosmetic README frontmatter + adding "Start here" is fine.
- Investigate before deleting anything (H2): confirm canonical + no importers, else surface — don't delete.
- Every autofix gated on tests passing (native toolchain). Real failure → report as a finding, don't hide it.
- Track C repos get the LIGHT pass only (H3/H7/H8).
- Any ambiguity → stop and surface in the PR body.

## STEP 4 — REPORT
One portfolio table: repo × track × H1–H8 (pass / fixed / n-a / needs-decision), with every draft PR link.
List all UNSURE repos and needs-decision items for me to rule on. Merge NOTHING.

Start with STEP 1 now and show me the inventory before proceeding to STEP 3.
