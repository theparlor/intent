---
title: Spawn Prompt — Repo Hygiene Rollout
id: SPAWN-REPO-HYGIENE-ROLLOUT
type: spawn-prompt
created: 2026-07-02
status: canonical
implements: playbooks/repo-hygiene-convention.md (CONV-REPO-HYGIENE-001)
upstream_control_path: Core/frameworks/intent/spawn-prompts/repo-hygiene-rollout.md (this file)
catch_mechanism: "safety rails below forbid deletion of working-memory and mass content rewrites; every autofix is gated on `make test` (or native equivalent) passing; work lands on a branch as a draft PR, never merged; judgment calls are surfaced, not guessed"
pipeline_survival: "self-contained pasteable artifact; one paste per target repo; adapts to any language/stack; output is a committed PR + scorecard, durable in git"
usage: "cat this file | pbcopy → paste into a new Claude Code session opened IN the target repo, after filling TARGET. One session per repo (or dispatch one sub-agent per repo)."
---
# Spawn Prompt: Repo Hygiene Rollout

> Copy this entire file into a new Claude Code session running **inside the target repo**.
> Fill in TARGET before pasting. Run one per repo, or fan out one sub-agent per repo.

---

## TARGET (fill in before pasting)

```
TARGET_NAME:  [e.g., Loom, Voices, Topography, Subaru-engagement]
TARGET_PATH:  [absolute path to the repo root]
BRANCH:       [e.g., chore/repo-hygiene-rollout]
```

---

## Your job

Apply the **Intent Repo Hygiene Convention** (`playbooks/repo-hygiene-convention.md`, CONV-REPO-HYGIENE-001)
to this repo so a skeptical senior engineer who clones it sees *something they recognize*, not a mess.
The convention has eight checks, H1–H8. Read it first if it's reachable; the full text is summarized below
so this prompt is self-contained.

**H1** Runs on first clone (`make setup` / `make test`, isolated env, green or honestly-scoped).
**H2** No duplicate/drifted source modules (one canonical copy each).
**H3** README leads with substance, not machine-generated frontmatter.
**H4** A 3–5 file reading path pointing at tested code first.
**H5** README makes "running code vs. working-memory" legible.
**H6** Tests are honest — context-dependent suites quarantined behind a named target with a reason, never silently red or deleted.
**H7** No binaries tracked in git (`.zip/.docx/.pdf/...` gitignored + untracked).
**H8** Scope note if the repo hosts more than one product/concern.

## Safety rails (do not violate)

1. **Branch + draft PR only. NEVER merge.** Create `BRANCH`, push there, open a draft PR.
2. **Never delete or archive working-memory** — signals, decisions, knowledge, specs. H5 is about making
   the sprawl *navigable*, not smaller. Reducing a signal count is out of scope.
3. **No mass content rewrites.** Trimming cosmetic README frontmatter and adding the "Start here" block is
   in scope. Rewriting prose / jargon sweeps across many files is OUT of scope.
4. **Investigate before deleting anything (H2).** Confirm the canonical copy via docs + imports; confirm
   nothing imports the copy you'd remove. If it's not unambiguous, DON'T delete — surface it.
5. **Every autofix is gated on tests passing.** After changes, `make test` (or the native equivalent)
   must exit 0. If it doesn't, and the failure is real, stop and report — do not force green by deleting
   or excluding a legitimately-failing suite.
6. **Adapt to the stack.** Not every repo is Python. Use the native bootstrap/test toolchain (npm/cargo/
   go/etc.). The *shape* (one-command setup + honest test) is what's portable, not the literal Makefile.
7. **Distinguish pre-existing real failures from context-mismatch.** A suite that needs a monorepo/live
   service/secrets is H6-quarantine (document + name a separate target). A suite that reveals an actual
   bug is NOT yours to hide — report it in the PR as a finding.

## Procedure

1. **Baseline audit.** Walk the repo as a first-time senior engineer. Produce an H1–H8 scorecard of the
   current state *before* touching anything.
2. **Autofix the safe checks** in this order: H7 (binaries) → H2 (drift, only if unambiguous) → H1/H6
   (bootstrap + honest tests) → H3/H4/H5/H8 (README). Prove tests green after H1/H6.
3. **Surface judgment calls** via the PR body (and, if the repo uses `.intent/`, a `status: blocked`
   disambiguation signal) — don't guess.
4. **Commit** in small, reviewable commits with clear messages. Push to `BRANCH`. Open a **draft PR**.
5. **PR body = the scorecard**, before/after, per check: `pass` (already clean) / `fixed` (what you did) /
   `needs-decision` (what you're asking). Link CONV-REPO-HYGIENE-001.

## Definition of done

- Draft PR open on `BRANCH`; nothing merged.
- `make test` (or native equivalent) exits 0 on a fresh clone, or the only failures are documented
  context-mismatch suites reachable via a named target.
- No tracked binaries; no unambiguous duplicate source modules.
- README opens with what-it-is + quickstart + reading path + code-vs-working-memory (+ scope note if H8).
- H1–H8 scorecard in the PR body, judgment calls surfaced not guessed.
