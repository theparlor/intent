---
signal_id: RETRO-2026-04-30-closure-discipline-SIG-2
title: Cowork sessions may not have hook enforcement — autonomy-grant only enforced in CC
severity: medium
detected: 2026-04-30
status: resolved
source: retroactive-extraction
trust_score: 0.5
autonomy: L2
upstream_control_path: "/Users/brien/Workspaces/CLAUDE.md, non-negotiable #5 ('No closure claims without the hook fabric') + 'Cowork -> Code handoff protocol' section"
catch_mechanism: "CLAUDE.md is checked into the Workspaces repo root and read by any harness that loads a folder-root CLAUDE.md, including Cowork; it explicitly states Cowork output is DRAFT-only and requires a .context/cowork-inbox/HANDOFF.md entry, which a Code session then verifies/commits/signals"
verification_command: "grep -n 'hook fabric' -A2 /Users/brien/Workspaces/CLAUDE.md"
---
# Cowork sessions may not have hook enforcement — only enforced in CC

## Observation
The autonomy-grant Stop hook is registered in `~/.claude/settings.json` which applies to Claude Code (CC) sessions. Cowork (claude.ai chat-style) sessions may not have access to this settings.json layer. If true, behavioral discipline applied via hooks is asymmetric across surfaces — CC sessions enforce, Cowork sessions don't.

## Context
The session this extraction is documenting was a CC session (via the `claude` CLI, with full hook stack active). But the Tamagotchi reference in the prior-art research and the broader "behavioral discipline at AI surface" framing both apply equally to Cowork. If hooks only fire in CC, half the surface area is unprotected.

## Implication
Need to verify:
1. Does Cowork honor `~/.claude/settings.json` hooks? (Likely no based on architecture differences)
2. If no, is there a Cowork-equivalent hook surface? (Anthropic's published Cowork docs would say)
3. If no equivalent, can the policy text loaded by SessionStart hooks be propagated via project knowledge / system prompts to Cowork?

Worst-case scenario: behavioral discipline only applies in CC. Cowork sessions inherit zero hook enforcement, run on memory + system prompt only. Brien's published methodology could specify "hook-enforced" vs "hook-unenforced" surfaces explicitly.

Recommended action: open a follow-up signal/spec asking the question to Anthropic via support channel, OR test by deliberately drifting in a Cowork session and observing whether anything blocks. Either way, the asymmetry needs documenting in the autonomy-grant + closure-discipline specs.

## Triage, 2026-07-08

Disposition: control exists now, verified live. The worst-case scenario this signal flagged is confirmed as fact (not hypothesis) and explicitly documented: `/Users/brien/Workspaces/CLAUDE.md` non-negotiable #5 states that running without this repo's Claude Code hooks (Cowork, chat, any third-party harness) makes the output a DRAFT by definition, because governance enforcement (closure-discipline, autonomy-grant, signal capture) did not run. The asymmetry is not just documented but operationalized: the same file's "Cowork -> Code handoff protocol" section requires a Cowork session to append a dated row to `.context/cowork-inbox/HANDOFF.md` rather than claim closure, which a subsequent Claude Code session (with the hook fabric) verifies, versions, signals, and commits. This answers all three of this signal's investigation questions: Cowork does not honor hooks (no), there is no Cowork-equivalent hook surface (no), and yes, the policy propagates via project-checked-in CLAUDE.md rather than a session-layer mechanism.
