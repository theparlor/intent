---
id: ARB-XXX
atom: ATOM-XXX     # atom under review
date: YYYY-MM-DD
reviewers: []      # persona identifiers or human names
verdict: ""        # approved | approved-with-concerns | blocked | needs-info
concerns: []       # list of concern strings
conditions: []     # conditions for approval (if approved-with-concerns)
---
# ARB Review: [atom title]

## Review Summary
One paragraph verdict. Does this atom pass the ARB?

## Persona Assessments

### triangle Practitioner-Architect
**Assessment:** [pass | flag | block]
- Fits existing patterns: [yes/no — explain]
- Integration points identified: [list]
- Blast radius: [low | medium | high]

### diamond Product Leader
**Assessment:** [pass | flag | block]
- Signal-driven: [which signals/clusters drove this]
- Adoption impact: [who uses this, how often]
- Investment justified: [yes/no — explain]

### circle Design-Quality Advocate
**Assessment:** [pass | flag | block]
- Tech debt risk: [low | medium | high]
- Test strategy: [how to verify]
- Simpler alternative considered: [yes/no]

### filled-circle AI Agent
**Assessment:** [pass | flag | block]
- Acceptance criteria binary: [yes/no]
- Contracts explicit: [yes/no]
- Context files listed: [yes/no]

### lightning Claude Code Lens
**Assessment:** [pass | flag | block]
- Session estimate: [S/M/L]
- Stack compatible: [yes/no — which tools]
- SIG-014 risk: [low | medium | high]
- Dependencies met: [yes/no]

## Conditions (if approved-with-concerns)
- [Condition 1]
- [Condition 2]

## Decision
**Verdict:** [approved | approved-with-concerns | blocked | needs-info]
**Next step:** [what happens next — e.g., "proceed to spec", "address concerns first"]
