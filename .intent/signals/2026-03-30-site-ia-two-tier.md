---
id: SIG-020
title: Intent site needs two-tier information architecture
type: friction
source: conversation
source_context: QA audit review revealed flat nav hiding depth differences
date: 2026-03-30
status: active
cluster: product
autonomy_level: L1
tags: [site, navigation, information-architecture, ux]
---

# SIG-020: Intent site needs two-tier information architecture

## Observation

During QA audit of all 15 site pages, Brien identified that the current flat nav treats all pages as equal depth, but the content naturally splits into two tiers:

**Primary (storytelling surface):** Pitch, Methodology, Concept Brief, Work System, Roadmap
- These answer "what and why" — a visitor moves left to right building understanding

**Technical depth (engineering surface):** Flow Diagram, Schemas, ARB, Dogfood, Signals
- These answer "how and with what" — someone here is already bought in, wants the machinery

**Reference (not in nav):** Decisions, Visual Brief, Native Repos, Event Catalog
- Supporting material, linked from context but not primary navigation targets

## Specific Issues Identified

- Flow Diagram and Work System are stub pages with no real content
- Signals page (a rich 48KB interactive dashboard) has no nav link — undiscoverable
- ARB page was missing site nav entirely (fixed)
- Technical pages need a sub-navigation that groups them as a connected documentation surface

## Implication

The flat nav needs to become a two-tier structure. Primary pages get the main horizontal nav. Technical/depth pages get a secondary nav — possibly a left sidebar or a grouped sub-menu under a "Docs" or "Technical" umbrella.

## Blocks

- Work System page redesign
- Flow Diagram content
- Any new page additions

## Relates To

- SIG-019 (vocabulary refinement affects page content)
