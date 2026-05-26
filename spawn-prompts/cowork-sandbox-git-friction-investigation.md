---
title: Spawn Prompt — Investigate Cowork sandbox git-write friction
id: SPAWN-COWORK-GIT-FRICTION-INVESTIGATION
type: spawn-prompt
created: 2026-05-20
depth_score: 4
depth_signals:
  file_size_kb: 9.9
  content_chars: 8943
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.22
target: cowork-or-cc
status: open-investigation
upstream_control_path: Core/frameworks/intent/spawn-prompts/cowork-sandbox-git-friction-investigation.md (this file)
catch_mechanism: "this spawn prompt is the investigation surface; findings should land at Core/frameworks/intent/learnings/process-drift-catalog.md as a new anti-pattern entry if the hypothesis confirms"
pipeline_survival: "self-contained pasteable artifact; the reproducer is concrete; the L0 boundary (Brien-only host commits) is the symptom this investigation is naming"
usage: "cat ~/Workspaces/Core/frameworks/intent/spawn-prompts/cowork-sandbox-git-friction-investigation.md | pbcopy Then open a fresh Cowork or Claude Code session (CC preferred for filesystem-level investigation). Pin Sonnet for the investigation; Opus only if root-cause analysis needs judgment."
---
# Investigation — Cowork sandbox git-write friction in IDD flow

## The hypothesis Brien is naming

**The Cowork sandbox is introducing friction to intent-driven building** by making every IDD cycle that lands a tracked artifact into a two-step process: (1) Cowork session writes the file, (2) Brien manually runs the commit from his host shell. The L0-escalation surface for "git commit" is structural, not policy — and that structural escalation is the friction.

If this hypothesis confirms, the friction is in the seam between Cowork's filesystem capabilities (can read and write through mounted folders) and its git-index limitations (cannot release `.git/index.lock` even when the lock is owned by the sandbox user).

## Reproducer (concrete, repeatable)

In a Cowork session with the user's Workspaces folder mounted:

```bash
# Inside the Cowork sandbox shell:
cd ~/Workspaces  # mounts to /sessions/<session>/mnt/Workspaces in the sandbox
git status       # works — read-only on the index, no lock needed
# Now attempt any write operation that would acquire .git/index.lock:
git add some-file.md
# Observe: warning: unable to unlink '.git/index.lock': Operation not permitted
ls -la .git/index.lock
# -rw------- 1 <sandbox-user> <sandbox-user> 0 ... .git/index.lock
# Lock file exists, owned by the sandbox user.
rm -f .git/index.lock
# rm: cannot remove '.git/index.lock': Operation not permitted
# Even though the file IS owned by the sandbox user.
```

Symptoms observed on 2026-05-20 in two consecutive sessions:
- First session (panel critique commit): blocked at the same step
- Second session (overnight bug-redesign work): blocked at the same step

The Cowork session can:
- Create files anywhere under mounted folders (including `.intent/`, `.git/objects/` if the path is writable)
- Read everything including `.git/HEAD`, `.git/config`, `.git/refs/`
- Execute `git status`, `git log`, `git diff`, `git show` — all read-only operations

The Cowork session cannot:
- Release `.git/index.lock` (the lockfile git creates on every write operation)
- Therefore cannot complete any `git add`, `git commit`, `git stash`, or any other index-mutating command

## Why this is an IDD-shaped problem

The IDD playbook (`Core/frameworks/intent/playbooks/idd-build-pattern.md`) describes a five-stage loop: Observe → Notice → Spec → Execute → Closure. The Execute stage produces artifacts (code, docs, critiques). Closure-DoD enforces the `upstream_control_path` / `catch_mechanism` / `pipeline_survival` triad — including that the artifact be committable so its provenance and refactor-run history survive.

Currently, every Cowork-driven IDD cycle that lands a tracked artifact terminates at "L0: commit needed by Brien" — a human-in-the-loop step that the rest of the cycle was designed to avoid. The L0 surface is not principled (it's not an external comm, money movement, or sign-off only Brien can give) — it's a filesystem-level capability gap.

If the hypothesis confirms, the IDD doctrine should be updated:
- The current pattern "Cowork writes, Brien commits" is the workaround, not the design
- The closure-DoD `pipeline_survival` is partial when commits cannot land autonomously inside the same session
- The L0 escalation list in `cowork-idd-with-panel-critique.md` quietly includes a non-principled gate ("commit") that the spawn prompt itself treats as already-handled (the prompt says "Brien decides push timing" but commits cannot even land before push)

## What to investigate (in order)

1. **Confirm or refute the reproducer.** Open a fresh Cowork session, mount Workspaces, attempt a `git add` of a small test file. Document exact behavior — including whether the lock is owned by the sandbox user, whether `chmod 644` on the lock changes anything, and whether the failure mode varies by mount type.

2. **Locate the filesystem layer that blocks unlink.** Cowork mounts folders into the sandbox via some host→VM bridge. Is the unlink-block at the bridge layer (e.g., FUSE-style denial of unlink), at the cgroup/AppArmor layer (filesystem policy), or at the host-OS-level (macOS quarantine flag on `.git/`)? The error message ("Operation not permitted") is too generic to pin without testing.
   - Try: `touch ~/Workspaces/.test-write && rm ~/Workspaces/.test-write` — does this work? (Probably yes — regular files in mounted folders are writable.)
   - Try: `touch ~/Workspaces/.git/.test-write && rm ~/Workspaces/.git/.test-write` — does this work? (Probably no — `.git/` may be specifically protected.)
   - Try: same on a different `.git/` (a worktree's `.git` file vs. a full `.git/` directory) — does behavior differ?

3. **Check whether Cowork has a "git" capability flag.** Some sandboxed agent harnesses ship a separate git-capability layer (a daemon or socket the agent can talk to that performs the git operations with elevated permissions). Look in the Cowork settings for a "git access" toggle, an MCP tool for git, or any configuration that exposes a different commit path. If one exists, the current behavior is just a missed setting.

4. **Evaluate whether `git commit-tree` + `git update-ref` bypass the lock.** The lockfile is on `.git/index`, not on the refs. If we build the tree directly and update HEAD via `update-ref`, we might avoid the index-lock path entirely.
   ```bash
   # Hypothetical bypass:
   tree=$(git write-tree)  # may still touch index
   commit=$(echo "msg" | git commit-tree $tree -p HEAD)  # uses refs, not index
   git update-ref HEAD $commit  # ref update, not index update
   ```
   Test whether this sidesteps the lock or hits the same `.git/` write block at a different file.

5. **If no autonomous-commit path exists**, then this is a real product-level limitation in Cowork. The IDD doctrine needs to update:
   - Either accept "commit" as a permanent L0 surface (and explicitly add it to the L0 list in the IDD spawn prompts)
   - Or treat Cowork's git-write capability as a product gap and surface it to Anthropic's Cowork team via the thumbs-down feedback channel

## Deliverables expected from this investigation

1. **Confirmation/refutation of reproducer** — one paragraph stating what was tested and what was observed
2. **Root cause** — which layer blocks `.git/index.lock` unlink (filesystem mount config, cgroup policy, sandbox AppArmor, or host-OS quarantine)
3. **Bypass evaluation** — does `commit-tree` + `update-ref` work; if so, document the safe-bypass recipe; if not, document why
4. **IDD-doctrine update proposal** — if no bypass, propose explicit language for the IDD spawn prompts that names "commit" as a permanent L0 surface OR proposes a product-level fix request
5. **Anti-pattern entry** — if the friction is real and unfixable in-session, land a new entry in `Core/frameworks/intent/learnings/process-drift-catalog.md` under the appropriate family (probably "Workflow Friction" or "Tool-capability Mismatch")

## Open questions for Brien before investigation lands

(These are honest L0 — only Brien can answer them.)

- Does Brien prefer a product-feedback escalation to Anthropic on Cowork's git-write capability, or just an updated doctrine that names this as expected?
- Should the IDD spawn prompts gain a "commit-channel" field where the session names how the commit will land (host shell · automated post-session hook · explicit defer to Brien)?
- Is there a non-trivial volume of IDD work that has accumulated as uncommitted-but-landed artifacts? If yes, that suggests the friction is already producing pipeline-survival debt.

## Closure-DoD for the investigation

upstream_control_path: this spawn prompt (`Core/frameworks/intent/spawn-prompts/cowork-sandbox-git-friction-investigation.md`); investigation findings should land at `Core/frameworks/intent/learnings/process-drift-catalog.md` if hypothesis confirms

catch_mechanism: the reproducer in this prompt is concrete and re-runnable; any future session can verify whether the friction persists by running the four reproducer commands; the bypass-evaluation step (commit-tree + update-ref) is the catch-net that either solves the friction or proves it requires upstream product change

pipeline_survival: if the investigation confirms the friction and finds no bypass, the anti-pattern entry in the drift catalog ensures every future IDD session reading the playbook sees "Cowork commits are L0 by structure, not by policy" and can plan accordingly; if a bypass is found, that recipe lives in the spawn-prompts directory as the new closure-of-commit path

---

*Prepared by Cowork Opus 4.7 during the bug-redesign overnight session, 2026-05-20. The friction was observed when attempting to commit two SPEC-001-valid critique markdowns and five HTML deliverables that Brien had explicitly approved for commit. The artifacts landed; the commits did not. This prompt is the IDD-correct response to that failure mode.*
