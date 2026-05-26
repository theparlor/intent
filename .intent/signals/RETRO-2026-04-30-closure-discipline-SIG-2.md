---
signal_id: RETRO-2026-04-30-closure-discipline-SIG-2
title: Cowork sessions may not have hook enforcement — autonomy-grant only enforced in CC
severity: medium
detected: 2026-04-30
status: open
source: retroactive-extraction
trust_score: 0.5
autonomy: L2
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
