---
id: SIG-024
title: Cowork sandbox cannot reliably sync to GitHub — needs Claude Code CLI path
type: friction
source: conversation
source_context: Signal content lost/corrupted during multiple push attempts through GitHub MCP API
date: 2026-03-30
status: active
cluster: infrastructure
autonomy_level: L1
tags: [sync, github, sandbox, claude-code, tooling, friction]
---

# SIG-024: Cowork sandbox cannot reliably sync to GitHub — needs Claude Code CLI path

## Observation

Multiple failures during this session pushing content to GitHub from Cowork:

1. **signals.html corruption** — 48KB file pushed as wrong 25KB version (agent substituted different content)
2. **signals.html literal string** — Earlier push wrote `$(cat /path/to/file)` as literal text instead of expanding it
3. **Large file truncation** — 48KB file too large to pass inline through MCP tool parameters (truncated at 46.9KB)
4. **Signal ID collision** — No visibility into what's already on the live site when creating signals locally

The root cause: Cowork operates in a sandboxed environment. It can read/write local files and call the GitHub MCP API, but:
- Can't `git clone && git push` (no git credentials in sandbox)
- MCP API has content size limits and no diffing
- No bidirectional sync — local state and repo state drift apart
- Agent intermediaries introduce content substitution risk

## What Works

- GitHub MCP API for small file updates (<30KB)
- Agent-delegated pushes for medium files (with verification)
- Reading files from GitHub (get_file_contents works reliably)

## What Breaks

- Large file pushes (>40KB) — content truncation
- Multi-file atomic commits — each file is a separate commit
- Bidirectional sync — no pull mechanism
- Content verification — have to re-read after push to confirm

## Implication

For reliable repo operations (especially pushing signal files, updating the site, and keeping local + remote in sync), the workflow should route through Claude Code via terminal with full git access. Cowork is the architect surface; Claude Code is the builder surface. The handoff needs to be clean.

## Relates To

- SIG-014 on site (always-on requirement — processing can't die with laptop)
- SIG-018 (cloud MCP hosting — servers need their own GitHub access)
- Brien's workflow preferences (Cowork = architect, Claude Code = builder)
