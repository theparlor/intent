---
id: SIG-035
timestamp: 2026-04-13T01:30:00Z
source: research-synthesis
confidence: 0.9
trust: 0.85
autonomy_level: L3
status: symptom-repaired, upstream-pending
status_corrected: 2026-04-16
correction_rationale: "Flagged by SIG-F-001 audit. Recommendation called for updating overwatch SKILL.md to add incestuous-amplification detection as an explicit check category; grep of overwatch SKILL.md finds zero hits for 'incestuous' or 'amplification'. Per signal-stream.md closure policy, 'resolved' requires the upstream control's file path + ID. Follow-up: install the overwatch check or explicitly defer with rationale + reassess_by."
cluster: governance
author: agent
related_intents: []
referenced_by:
  - SIG-032
parent_signal: SIG-032
---
# Overwatch must detect incestuous amplification — Boyd's organizational survival mechanism

Boyd identified that the IG&C feedback from Orient back to Observe creates a dangerous self-reinforcing loop: orientation filters observation to confirm itself. Richards calls this "incestuous amplification" — the organization only sees data that confirms existing beliefs. Opposing views are marginalized. The data environment becomes a closed loop.

**In Intent terms:** If the knowledge base only surfaces signals that confirm existing personas, DDRs, and themes, the system stops noticing gaps. The lint operation catches structural issues (orphan pages, missing links). But lint doesn't catch confirmation bias — it doesn't ask "what are we NOT seeing?"

Boyd's prescription: "even attempting to assess your organization's status from inside will increase the confusion and disorder within it. You need outside reference points."

**Overwatch is that external reference point.** But the current overwatch skill spec doesn't explicitly codify this failure mode. It should include:

1. **Disconfirmation check:** For each active persona/DDR/theme, explicitly search for evidence that contradicts or limits it. Not just "is it stale?" but "is it wrong?"
2. **Signal diversity audit:** Are signals clustering in one domain while another goes dark? Absence of signals from a domain IS a signal.
3. **Source freshness vs. conclusion freshness:** A conclusion can be stale even if its sources are current — if the sources have been reinterpreted by the field but our compiled interpretation hasn't updated.

**Action:** Update overwatch SKILL.md to add incestuous amplification detection as an explicit check category. This is L3 — the skill spec is a file we own, the change is additive, and the risk is low (adding a check that may surface false positives is better than missing confirmation bias).

**Grounded in:** Richards (2020), Boyd's "diseases of orientation," RAT-003.
