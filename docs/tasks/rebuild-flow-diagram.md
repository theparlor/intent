# Task: Rebuild flow-diagram.html

> Handoff spec for Claude Code terminal. Read this file, execute, verify contracts.

## Context

`docs/flow-diagram.html` is currently a 1.5KB skeleton with a single paragraph. It needs a full rebuild as a rich, interactive visualization of the Intent loop.

## What to Build

A visually compelling page showing the **Notice → Spec → Execute → Observe** loop. This page lives in **Pillar 2 — The System** and serves as the visual explanation of how the loop works.

## Requirements

### Navigation (already in place per IA v2)
- Primary nav: 3 pillar links, "The System" active
- Sub-nav: Pillar 2 links, "Flow" active
- Standard footer with GitHub link and tagline

### CSS Strategy
- Link `styles.css` for shared foundation
- Page-specific `<style>` block for all custom visuals (Rich page)
- Use CSS custom properties from styles.css palette: `var(--bg)`, `var(--surface)`, `var(--border)`, `var(--text)`, `var(--text-muted)`, `var(--text-dim)`, `var(--accent-blue)`, `var(--accent-amber)`, `var(--accent-green)`, `var(--accent-purple)`

### Visual Components (build ALL of these)

#### 1. SVG Loop Diagram (centerpiece)
A circular or rounded-rectangle loop showing the four phases connected by directional arrows:
- **Notice** (amber `var(--accent-amber)`) — top or left
- **Spec** (blue `var(--accent-blue)`) — right or top-right
- **Execute** (green `var(--accent-green)`) — bottom or right
- **Observe** (purple `var(--accent-purple)`) — left or bottom-left

Each phase node should be a rounded box or circle with the phase name and a one-line description. Arrows connect them in a clockwise flow. The center of the loop should say "Intent" or show the Intent logo mark.

Use SVG, not canvas. CSS animations welcome (subtle pulse, flow arrows, etc.) but not required.

#### 2. Phase Detail Cards (below the loop)
Four cards in a 2×2 grid (or 4×1 on wide screens), one per phase:

**Notice** (amber accent)
- What: Capture signals from anywhere work happens
- Inputs: Error logs, conversations, user complaints, build failures, design reviews
- Output: Signal (atomic observation with metadata)
- Tool: `intent-signal "What you noticed"`

**Spec** (blue accent)
- What: Shape signals into agent-ready specifications
- Inputs: Signals, context, prior specs
- Output: Spec (verifiable contract with acceptance criteria)
- Tool: `intent-spec "What to build" --intent INT-003`

**Execute** (green accent)
- What: Agents implement against specs
- Inputs: Approved spec, tool access, context
- Output: Artifacts, code changes, deliverables
- Tool: Claude Code, GitHub Actions, Entire.io

**Observe** (purple accent)
- What: Measure outcomes and capture what happened
- Inputs: Execution results, metrics, user feedback
- Output: Events, learnings, new signals (loop restarts)
- Tool: `.intent/events/events.jsonl`, dashboards

#### 3. Loop Properties Section
A simple section below the cards explaining key properties:
- **Continuous** — No sprint boundaries. The loop runs whenever there's signal.
- **Multi-speed** — Some loops take minutes (a bug fix). Some take weeks (a strategy shift).
- **Observable** — Every transition emits an event. The loop is its own telemetry.
- **Agent-native** — Specs are contracts agents can execute. Not prose humans interpret.

#### 4. Connection to Work Ontology
A brief visual or text section showing how loop phases map to the work ontology:
- Notice produces **Signals**
- Signals promote to **Intents**
- Intents are shaped into **Specs** with **Contracts**
- Execution produces **Capabilities** → **Features** → **Products**

### Minimum File Size Target
The rebuilt page should be at least 8KB (meaningful content with SVG and CSS). The current 1.5KB skeleton is a known defect.

## Verification

After rebuilding, run these checks:

```bash
cd ~/Workspaces/Core/frameworks/intent/docs

# File size check (must be >8000 bytes)
SIZE=$(wc -c < flow-diagram.html)
echo "flow-diagram.html: ${SIZE}B"
[ "$SIZE" -gt 8000 ] && echo "PASS: size" || echo "FAIL: size below 8KB"

# Has SVG loop diagram
grep -q '<svg' flow-diagram.html && echo "PASS: has SVG" || echo "FAIL: missing SVG"

# Has all four phase names
for phase in Notice Spec Execute Observe; do
  grep -q "$phase" flow-diagram.html && echo "PASS: has $phase" || echo "FAIL: missing $phase"
done

# Has page-specific CSS (Rich page)
CSS_LINES=$(sed -n '/<style>/,/<\/style>/p' flow-diagram.html | wc -l)
echo "Inline CSS: ${CSS_LINES} lines"
[ "$CSS_LINES" -gt 20 ] && echo "PASS: rich CSS" || echo "FAIL: too little inline CSS"

# Has correct nav (IA v2)
grep -q 'The System' flow-diagram.html && echo "PASS: pillar nav" || echo "FAIL: missing pillar nav"
grep -q 'class="sub-nav"' flow-diagram.html && echo "PASS: sub-nav" || echo "FAIL: missing sub-nav"

# Standard footer
grep -q 'Built with the Intent methodology' flow-diagram.html && echo "PASS: footer" || echo "FAIL: missing footer"
```

Then run the full site contracts:
```bash
cd ~/Workspaces/Core/frameworks/intent/docs
# Run CON-SITE-001 through CON-SITE-010 from site-contracts.md
```

## After Verification

Commit and push:
```bash
cd ~/Workspaces/Core/frameworks/intent
git add docs/flow-diagram.html
git commit -m "Rebuild flow-diagram.html with SVG loop, phase cards, and loop properties

Rich interactive page replacing the 1.5KB skeleton. Features:
- SVG loop diagram with Notice/Spec/Execute/Observe phases
- Phase detail cards with inputs, outputs, and CLI tools
- Loop properties section (continuous, multi-speed, observable, agent-native)
- Work ontology connection
- IA v2 nav (Pillar 2 — The System)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push origin main
```
