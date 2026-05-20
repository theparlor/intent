---
id: SIG-043
title: Prompt caching and structured formatting (XML/markdown) are the frictionless enablers for L1-L2 productivity — this space must be addressed
timestamp: 2026-04-12T22:00:00Z
source: cowork-session
author: brien
confidence: 0.85
trust: 0.7
autonomy_level: L2
status: active
cluster: productivity-os-layers
referenced_by:
  - "Dex Horthy, context engineering / 40% rule"
  - "SPEC-productivity-os-layers (L1 Personal OS, L2 Independent Builders)"
  - "Hermes/Obsidian three-tier memory analysis"
  - "Rohit production agent principles, Principle 4 (context engineering)"
---

# SIG-043: Prompt Caching + Structured Formatting as L1-L2 Enablers

## What was noticed

The Productivity Stack Model identifies L1 (Solo Builder) and L2 (Independent Builders) as the foundation layers where individual practitioners interact with AI. At these layers, the two most impactful technical concerns are:

1. **Prompt layer (L1)**: How instructions are structured, cached, and reused
2. **Context layer (L2)**: How knowledge is formatted, compressed, and loaded

Prompt caching (where providers like Anthropic cache the static prefix of a prompt so repeated calls with the same system prompt/context pay reduced token costs) and structured formatting (XML blocks for conditional activation, markdown for compiled knowledge artifacts) are the mechanical enablers that make L1-L2 productivity frictionless.

## Why this matters

Without prompt caching:
- Every Cowork dispatch task pays full token cost for the same CLAUDE.md, persona registry, and context files
- The 22-task parallel sweeps we run are paying 22x for identical prompt prefixes
- The economic argument for compilation (compile once, query compiled artifacts) breaks down if the compiled artifacts aren't cached at the provider level

Without structured formatting discipline:
- XML conditional blocks (Dex Horthy's slopfiles `<important if>` pattern) keep instruction files lean — only the relevant blocks activate per context
- Markdown as the compilation target means knowledge artifacts are model-agnostic AND cache-friendly (stable text that doesn't change between calls)
- The 40% context rule is easier to maintain when the format is predictable and cacheable

## The space to be addressed

This doesn't have to be an Intent product. It needs to be handled by SOMEONE in the L1-L2 stack — whether that's:
- Anthropic's prompt caching feature (already exists, needs to be leveraged deliberately)
- Dex Horthy's slopfiles pattern (conditional XML blocks for CLAUDE.md optimization)
- The Hermes/Obsidian hot memory promotion trigger (format-aware context management)
- OpenRouter/LiteLLM proxy configurations that optimize cache hit rates across providers
- A best-practices guide for how to structure CLAUDE.md, persona files, and knowledge artifacts for maximum cache reuse

## Specific actions to investigate

1. **Audit current cache efficiency**: Are Brien's CLAUDE.md files and persona registries structured to maximize prompt cache hits? The static prefix (system prompt + CLAUDE.md + persona context) should be identical across dispatch tasks targeting the same persona.

2. **XML block discipline**: Adopt the `<important if>` pattern from slopfiles for engagement-specific CLAUDE.md files. Subaru context only activates when working on Subaru, keeping the cached prefix lean for other contexts.

3. **Markdown compilation standard**: Define a standard for how compiled knowledge artifacts (personas, domain models) are formatted so they're both human-readable AND cache-optimal. Short, structured, predictable frontmatter + body format.

4. **Provider-specific caching**: Map which providers offer prompt caching (Anthropic yes, OpenAI yes, DeepSeek unknown, GLM-5.1 local = no caching needed). The multi-model gateway should route cache-sensitive work to providers that support caching.

5. **Cost impact modeling**: With CodeBurn installed, measure the actual token spend on repeated context loading. Calculate the savings if prompt caching were fully leveraged. This data drives the ROI case for investing in formatting discipline.

## Connection to Productivity OS Layers

In the Productivity Stack visualization:
- **L1 Prompt row**: CLAUDE.md + slopfiles is the product. Prompt caching is the infrastructure that makes it economically sustainable at scale.
- **L2 Context row**: Shared context artifacts are the product. Structured formatting (XML/markdown) is what makes them loadable, cacheable, and model-agnostic.

These two cells are the foundation that everything above builds on. If L1-L2 are expensive and friction-heavy, the value proposition of L3-L6 weakens because every higher layer multiplies the L1-L2 cost.

## Who might address this

- **Anthropic**: Prompt caching already exists. Better documentation and tooling for structuring cacheable prompts would help.
- **Dex Horthy / HumanLayer**: slopfiles is the leading open-source approach to structured prompt management.
- **The Parlor / Intent**: Could publish a best-practices guide for L1-L2 formatting discipline as part of the Intent methodology. This would be the "Getting Started" content for the 401 level in the enterprise guide maturity ladder.
- **Community tools**: MacWhisper-style "just works" tools that handle formatting automatically.
