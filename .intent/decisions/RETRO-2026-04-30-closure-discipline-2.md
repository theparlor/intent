---
decision_id: RETRO-2026-04-30-closure-discipline-2
title: Use ANSI-C ($'...') bash quoting for hook regex with apostrophes; stdin-piped python for JSON parsing
date: 2026-04-30
status: accepted
source: retroactive-extraction
session_date: 2026-04-30
references:
  - Core/frameworks/intent/hooks/closure-discipline-stop-check.sh
  - Core/frameworks/intent/hooks/closure-discipline-signal-check.sh
---
# ANSI-C bash quoting + stdin-piped python for hook robustness

## Context
First-pass test runs of the closure-discipline hooks surfaced two distinct bugs:
1. Stop hook bash syntax error: regex inside `'...'` had embedded apostrophes (e.g., `[' ]?` to optionally match apostrophe-or-space) which prematurely terminated the single-quote scope.
2. PreTool hook silently failed to detect bad signal in test: heredoc-substitution pattern `python3 <<PYEOF ... json.loads('''$INPUT''') ...` was brittle when the substituted JSON contained quotes that could clash with python triple-quote delimiters.

## Decision
- Replace `'...'` regex strings containing apostrophes with `$'...'` ANSI-C-quoted strings using `\x27` (or just escape the apostrophe content out where possible). Pattern shown in `closure-discipline-stop-check.sh` line 112.
- Replace heredoc-substitution pattern with stdin-piped python (`printf '%s' "$INPUT" | python3 -c '...'`) for JSON parsing in hooks. Avoids bash-substitution quote interactions entirely.

## Alternatives Considered
- Drop the apostrophe-bearing patterns from the regex: rejected because legitimate completion-claim phrases use them (e.g., "we're done", "everything's working")
- Switch to Python-only hooks (no bash wrapper): worth considering for future hook iterations but breaks parallelism with autonomy-grant-stop-check.sh which uses bash; preserve consistency for now
- Use jq instead of inline python: rejected because jq isn't universally installed and adds an external-dep failure mode

## Consequences
Both patterns now codified in the closure-discipline hook scripts. Future Stop / PreToolUse hooks should follow the same conventions. Worth lifting into a `hooks/lib/common.sh` if the third hook of this shape gets built.

Test coverage: 4 cases now exercised (block-bad / allow-good × text + artifact). Pattern is verified, not just designed.
