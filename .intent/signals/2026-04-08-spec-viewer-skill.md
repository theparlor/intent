---
title: "Spec Viewer — reusable skill for rendering markdown specs as styled HTML"
severity: low
detected: 2026-04-08
status: active
source: feedback — Brien needs specs to read visually, not as raw markdown
---

## Observation

Design specs and technical documents written in markdown are hard to read and review in their raw form. Brien is a visual thinker — the document needs to communicate with the same intentionality as the product it describes.

We rendered the persona browser + product dashboard spec as styled HTML using the intent-site design system (dark slate palette, table of contents, syntax-highlighted YAML, section color coding). Brien confirmed this is the right approach.

## Opportunity

Build a reusable skill that renders any spec markdown as styled HTML:
- **Input:** A markdown file path
- **Output:** An HTML file in the same directory, using the intent-site design system
- **Features:** Table of contents, syntax highlighting, section numbering, status badges, responsive layout
- **Trigger:** Any time a spec is written, offer to render it

## Parallel

Typora selected as local markdown editor for WYSIWYG editing. The spec-viewer skill complements Typora for reading/sharing specs that need to look polished without a dedicated tool.

## Triage, 2026-07-08

Disposition: still pending. Searched for any spec-viewer skill or markdown-to-styled-HTML renderer; none exists as a reusable skill (only the one-off intent-site rendering this signal describes, done manually, not as a repeatable tool). Needed control: build the reusable skill this signal specified (input: markdown path, output: styled HTML with table of contents, syntax highlighting, section numbering, status badges).
