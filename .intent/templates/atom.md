---
id: ATOM-XXX
title: ""
product: ""        # notice | spec | execute | observe | cross-cutting
priority: ""       # now | next | later
size: ""           # S (1 session) | M (2-3 sessions) | L (4+ sessions)
status: draft      # draft → arb-reviewed → specced → executing → complete
parent_intent: ""  # INT-XXX if derived from an intent
parent_cluster: "" # CLU-XXX if derived from a cluster
dependencies: []   # ATOM-XXX IDs that must complete first
files: []          # file paths this atom will modify or create
assignee: ""       # human or agent identifier
arb_verdict: ""    # approved | approved-with-concerns | blocked | needs-info
arb_date:
---
# Atom: [title]

## Description
What specifically needs to be built or changed? Write this so that
Claude Code can execute against it without asking clarifying questions.
Include the exact files to modify, the pattern to follow, and the
behavior to implement.

## Acceptance Criteria
Binary pass/fail assertions. Each one should be testable:
- [ ] Given [precondition], when [action], then [expected result]
- [ ] Given [precondition], when [action], then [expected result]

## Dependencies
What must exist before this atom can start?
- [ATOM-XXX or file path or external prerequisite]

## Files to Modify
- `path/to/file` — what changes
- `path/to/new/file` — what gets created

## ARB Review

### Practitioner-Architect (triangle)
[Does this fit existing patterns? Integration points?]

### Product Leader (diamond)
[Is this solving a validated problem? Signal-driven?]

### Quality Advocate (circle)
[Tech debt risk? Simpler alternative? Test strategy?]

### AI Agent (filled circle)
[Are contracts binary? Scope contained? Context clear?]

### Claude Code Lens (lightning)
[Single session? Stack compatible? SIG-014 risk?]

## Concerns
[Any flags from the ARB review. Empty if none.]
