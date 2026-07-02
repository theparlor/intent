---
title: Intent Repo Hygiene Convention
id: CONV-REPO-HYGIENE-001
type: convention
created: 2026-07-02
status: canonical
origin: human
motivation: >
  "What does a hardcore staff engineer see on first clone — a mess, or something they recognize?"
  This convention is the checklist that makes the answer "something they recognize." Derived from the
  2026-07-02 first-clone audit of frameworks/intent (see PR #6).
applies_to: every Intent-native repo (and any repo we want a senior engineer to trust on first clone)
---
# Intent Repo Hygiene Convention

> A repo gets ~60 seconds of first impression. A skeptical senior engineer clones, opens the README,
> and runs the tests. This convention governs those 60 seconds. It is **presentation and hygiene only** —
> it never deletes working memory (signals, decisions, knowledge) and never mass-rewrites content.

Each check has: **what good looks like**, **how to verify** (a command), and **the fix**. Treat the
checks as invariants. **Zero-violation-start posture:** on a repo that already conforms, every check
reports clean on day one.

---

## H1 — Runs on first clone

**Good:** a `Makefile` (or `justfile`) with `make setup` and `make test`. From a fresh clone, `make test`
either passes or is honestly scoped (see H6). Third-party deps go in a venv/lockfile, never system-global.

**Verify:**
```bash
test -f Makefile || test -f justfile && echo "has bootstrap" || echo "MISSING bootstrap"
make test    # must exit 0
```
**Fix:** add a `Makefile` whose `setup` builds an isolated env and `test` runs every suite through it.
Prove it green before committing. (Non-Python repos: same shape with the native toolchain — `npm ci &&
npm test`, `cargo test`, etc.)

## H2 — No module drift / duplicate source

**Good:** exactly one canonical location per source module. No same-named source file living in two
directories with diverged content (the coherence anti-pattern).

**Verify:**
```bash
git ls-files '*.py' '*.ts' '*.js' | xargs -n1 basename | sort | uniq -d   # dup basenames → inspect
```
**Fix:** determine the canonical copy (what the docs/imports actually reference), confirm nothing imports
the other, then remove the stale one. **Investigate before deleting** — never delete a file another file
imports. Report which you kept and why.

## H3 — README leads with substance, not metadata

**Good:** frontmatter trimmed to functional fields (no auto-generated `depth_signals`, `vocab_density`,
`related_entities` blocks bloating the top). First rendered content is: one-line what-it-is → quickstart
→ reading path → code-vs-working-memory. Links the plain-language explainer if one exists.

**Verify:** open `README.md`; the first screenful should answer "what is this and how do I run it,"
not show a wall of machine-generated YAML.
**Fix:** trim cosmetic frontmatter (lint regenerates derived fields); add the "Start here" block (H4+H5).

## H4 — A reading path for a skeptical senior

**Good:** the README names 3–5 files, in order, that show the actual engineering — the tested core module
+ its test suite, the load-bearing spec, one worked decision record.

**Fix:** add a "Reading path (read in this order)" list pointing at the strongest, tested code first —
never at the signal pile first.

## H5 — Code vs. working-memory is legible

**Good:** the README states which directories are the running system (`servers/`, `tools/`, `bin/`, …)
vs. which are dogfood/working-memory (`.intent/`, `knowledge/`, `spec/`) — so 180 signals read as
*evidence of method*, not as noise the reader must wade through.

**Fix:** add the one-paragraph "what's code vs. what's working memory" note. **Do not delete or archive
signals to reduce the count** — make them navigable instead.

## H6 — Tests are honest, not silently red or hidden

**Good:** every test suite either passes on a standalone clone, or — if it requires a superset context
(monorepo, live service, secrets) — is quarantined behind a **separately-named target with a documented
reason** (e.g. `make test-invariants`). Never silently failing; never deleted to force green.

**Verify:** `make test` is green AND any excluded suite is reachable via a named target with a comment
explaining the dependency.
**Fix:** split context-dependent suites out of the default `test` target; document why in the Makefile.

## H7 — No binaries in git

**Good:** `.zip`, `.docx`, `.pdf`, exports, and other binaries are gitignored; source-of-truth is text.

**Verify:**
```bash
git ls-files | grep -iE '\.(zip|docx|pdf|xlsx|pptx|bin)$' && echo "BINARIES TRACKED" || echo "clean"
```
**Fix:** `git rm --cached <file>` (keeps it on disk), add the pattern to `.gitignore`.

## H8 — Scope note if the repo hosts more than one thing

**Good:** if a repo contains two products/concerns, the README says so up top and points to the
authority doc, so a newcomer doesn't conflate them.

**Fix:** add a one-line "N products share this repo — see X" note.

---

## Rollout posture (per repo)

1. Work on a branch; open a **draft PR**; **never merge** without the owner.
2. **Autofix the safe checks** (H1, H3, H4, H5, H7, H8, H6-quarantine, and H2 *only after* confirming
   canonical + no importers). Prove `make test` green before committing.
3. **Never** delete signals/knowledge (H5) or mass-rewrite prose (jargon sweeps are out of scope here).
4. For any judgment call (which duplicate is canonical is unclear, a test failure looks *real*), **stop
   and surface it** rather than guessing.
5. Output a **hygiene scorecard** (H1–H8: pass / fixed / needs-decision) in the PR body.
