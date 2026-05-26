---
title: Dex Horthy's Context Engineering & 12 Factor Agents — Analysis and Intent Framework Mapping
type: reference
depth_score: 2
depth_signals:
  file_size_kb: 3.3
  content_chars: 2955
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.68
source: Dex Horthy (@dexhorthy), HumanLayer founder, multiple repos and articles
analyzed: 2026-04-12
relevance: high — directly applicable to persona loading, Cowork plugin design, and MCP server architecture
---
# Dex Horthy — Context Engineering & 12 Factor Agents Analysis

Dexter Horthy is founder of HumanLayer (YC F24), former NASA JPL and Replicated. He coined "context engineering" in April 2025, adopted by Anthropic, LangChain, and Martin Fowler.

## Key Numbers
- 12 Factor Agents repo: 19.2K GitHub stars
- HumanLayer: 10.4K stars
- slopfiles (Claude Code plugin): active development

## Three Ideas That Map to Brien's Work

### 1. The 40% Context Rule
LLM performance degrades sharply past ~40% of the context window. "Frequent intentional compaction" — deliberately condensing conversation history into structured artifacts.

**Intent mapping:** When persona registries + corpus are loaded into a Cowork session, they eat context window. The Knowledge Engine's compilation model (compile once, query compiled artifacts) is the architectural answer to this constraint. But the persona loading mechanism needs to be context-budget-aware — don't load the full 180KB Nick Tune corpus when a 5KB compiled summary would serve.

### 2. Harness Engineering (6 Configuration Surfaces)
Dex's taxonomy of agent configuration: CLAUDE.md, MCP servers, skills, sub-agents, hooks, back-pressure. Sub-agents act as "context firewalls" — each gets a clean context instead of competing for the parent's window.

**Intent mapping:** Maps 1:1 to Cowork plugin architecture. Brien's CLAUDE.md files ARE harness configuration. The MCP servers (notice, spec, observe, knowledge) ARE tool surfaces. The persona skills ARE agent configuration. The insight that sub-agents are context firewalls explains why sequential dispatch works better than parallel — each task gets clean context.

### 3. The <important if> Pattern (slopfiles)
Claude Code plugin that rewrites CLAUDE.md using conditional XML blocks — instructions that only activate in specific contexts. Keeps instruction files lean while handling diverse scenarios.

**Intent mapping:** Immediately usable for Brien's engagement CLAUDE.md files. A Subaru engagement CLAUDE.md could have conditional blocks that activate only when working on specific workstreams, keeping the file lean for other contexts.

## Adoption Recommendations
- Evaluate slopfiles plugin for direct installation
- Apply 40% rule to persona loading — build a "context budget" checker
- Design Cowork plugin with explicit harness engineering taxonomy
- Test sub-agent context firewall pattern against current dispatch approach

## Key Repos
- github.com/dexhorthy/12-factor-agents (19.2K stars)
- github.com/humanlayer/advanced-context-engineering-for-coding-agents
- github.com/dexhorthy/slopfiles
- github.com/humanlayer/humanlayer (10.4K stars)

## Cross-References
- Rohit's Principle 4 (Context Engineering) cites the same 40% finding
- HumanLayer directly implements Rohit's Principle 3 (approval workflows)
- Intent signals: SIG-031 through SIG-034
