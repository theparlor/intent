---
title: Team OS — Aakash Gupta Substack Note
type: corpus-entry
depth_score: 2
depth_signals:
  file_size_kb: 2.3
  content_chars: 1842
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 1.09
source_url: "https://substack.com/@aakashgupta/note/c-240536298"
date_published: 2026-04-09
date_captured: 2026-05-08
format: substack-note
subject: Hannah Stulberg's Team OS at DoorDash
analysis_file: reference/aakash-gupta-team-os-analysis.md
signal: SIG-038
---
# Team OS — Aakash Gupta Substack Note (Apr 9, 2026)

## Source Summary

Aakash profiles Hannah Stulberg (DoorDash PM, ex-Google APM, 1,500+ hours in Claude Code) who built a "Team OS" — a shared GitHub repo serving ~20 people across PM, design, analytics, engineering, and strategy. The system eliminates the PM as context bottleneck by making all team knowledge agent-accessible.

## 7-Part Architecture (as described by Aakash)

1. Root CLAUDE.md (under 500 tokens): doc index, team roster, Slack IDs, GitHub handles
2. Nested CLAUDE.md files in every major folder: navigation indexes only, ~3% context per query
3. Folder ownership by function: PM owns product, data scientist owns analytics, strategy owns customer calls
4. Analytics layer: metric definitions, SQL queries, dashboard links — loaded progressively by depth
5. Shared skills: customer call summaries, PR creation, weekly synthesis
6. Verified playbooks: recurring analyses (funnel drop-off, churn investigation)
7. Launch gate: no feature ships until metrics, queries, schemas, dashboards, and playbooks are checked into the repo

## Key Quote

"Build the system that makes you unnecessary to the system."

## Related Resources

- Example repo: https://github.com/in-the-weeds-hannah-stulberg/team-os-example-repo
- Hannah's Substack: https://hannahstulberg.substack.com/
- Podcast episode: https://www.youtube.com/watch?v=0UArKLQ6bXA
- Maven workshop (May 10, 2026): https://maven.com/hannah-stulberg/how-to-build-your-teamos

## Intent Relevance

Maps to L3 (Team OS) in SPEC-productivity-os-layers.md. Validates the term, the knowledge-as-shared-repo pattern, and the market. Does NOT include Intent's loop, trust model, signal capture, observability, or compilation. See full analysis at reference/aakash-gupta-team-os-analysis.md.
