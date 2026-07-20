---
title: Intent Templates
type: reference
maturity: active
confidentiality: shareable
created: 2026-07-20
purpose: The template set for Intent work artifacts, and the one convention every template follows.
---
# Intent Templates

> **In plain terms:** These are the fill-in scaffolds for every Intent work artifact: signal, intent, spec, contract, decision, atom, cluster, arb-review, digest, event, product, team. Copy one, fill it in, and the shape carries the discipline for you.

## The one convention: human face on top, machine record below

Every template opens with a plain-language lede block, a blockquote labeled "In plain terms" (or, for a contract, "What this protects"). Write that block so a person who was not in the working session understands what happened, what is being asked, or what was decided, in words they already knew, without reading the structured detail below. The structured sections under it are the precise version the agents and tools execute against. Keep both. Never make the human read the machine layer to understand.

This follows the narration primer at /Users/brien/Workspaces/Core/templates/decision-framing/NARRATION-PRIMER.md. The three shapes (telling the story of a change, framing a decision still open, recording a decision made) and the full droppable prompt live there.

## Rules that keep every template shareable

- No undefined term of art. A codename (a product name, or a SIG, INT, SPEC, CON, DEC, or DDR id) appears only with a plain gloss and a bare-absolute path to the real document. A named thing with no link is a dead end.
- No em-dashes, en-dashes, arrow glyphs, or ellipsis characters, ever. Use periods, commas, colons, parentheses, or the words "to" and "vs". Peers read the glyphs as an AI tell and it blocks sharing.
- The four persona symbols (triangle for Practitioner-Architect, diamond for Product Leader, circle for Design-Quality Advocate, filled circle for AI Agent) are Intent domain notation, not decoration. They stay.

## Two spec templates, on purpose

- /Users/brien/Workspaces/Core/frameworks/intent/spec/SPEC_TEMPLATE.md is the authoring guide: the full walkthrough with the fat-marker-sketch framing. Start here when you are learning to write a spec.
- /Users/brien/Workspaces/Core/frameworks/intent/.intent/templates/spec.md is the terse operational scaffold with the complete frontmatter the tools expect. Copy this one when you are producing a real spec.

Each links the other, so there is no ambiguity about which to use.

## The test before you save one

Could someone who never saw Intent read the filled-in artifact once, understand it, click through to the evidence, and act, without a single clarifying question. If not, the human layer is not done yet.
