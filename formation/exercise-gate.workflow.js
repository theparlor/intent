export const meta = {
  name: 'exercise-formation-gate',
  description: 'EXERCISE harness: run the REAL coherence gate over a CLEAN sortie + a SEEDED-DRIFT sortie to prove Stage A catches semantic collision (vocabulary drift, non-goal violation, failed verification, contract breach) that Stage B (audit_chain) structurally cannot see. Self-contained (sorties inlined) so it does NOT depend on top-level Workflow args-passing, which stringifies objects.',
  phases: [{ title: 'Gate', detail: 'invoke the real two-stage coherence gate on a clean + a drifted sortie' }],
}

const GATE = '/Users/brien/Workspaces/Core/frameworks/intent/formation/coherence-gate.workflow.js'
const INTENT_ROOT = '/Users/brien/Workspaces/Core/frameworks/intent'

// Inlined fixtures (mirror formation/example-*-drift.json + the clean example).
const sorties = [
  {
    brief: {
      brief_id: 'MB-seam-schema-p1', intent: 'INT-FORMATION-FLIGHT', seam_id: 'seam-schema',
      title: 'Author the Mission Brief JSON Schema', interface_contract: 'CON-FORMATION-SCHEMA',
      reference_frame: {
        glossary: { 'Mission Brief': 'the typed coherence contract handed to a sortie', sortie: 'one agent flying one seam' },
        canonical_terms: ['Mission Brief', 'sortie', 'seam'],
        forbidden_synonyms: { 'Mission Brief': ['Brief Envelope', 'Dispatch Brief'] },
      },
      invariants: ['JSON Schema is the single source of truth'],
      non_goals: ['do not modify the coherence gate', 'do not edit servers/models.py'],
      drift_markers: [], trust_gate: 'L3', lambda: 1.5, isolation: 'worktree', model: 'opus',
      verification_rubric: { contract: 'CON-FORMATION-SCHEMA', verification_command: 'true' },
      lineage: { trace_id: 'formation-INT-FORMATION-FLIGHT', span_id: 'seam-schema-p1', parent_id: 'formation-INT-FORMATION-FLIGHT' },
    },
    report: {
      seam_id: 'seam-schema', brief_id: 'MB-seam-schema-p1', summary: 'Authored the Mission Brief JSON Schema.',
      outputs: [{ path: 'formation/mission-brief.schema.json' }],
      touched_paths: ['formation/mission-brief.schema.json'],
      verification: { command: 'true', ran: true, passed: true, output: 'ok' },
      vocabulary_terms: ['Mission Brief', 'sortie', 'seam'],
      invariants_selfcheck: [{ invariant: 'JSON Schema is the single source of truth', held: true }],
      non_goals_selfcheck: [{ non_goal: 'do not modify the coherence gate', respected: true }, { non_goal: 'do not edit servers/models.py', respected: true }],
      contract_changed: false,
    },
  },
  {
    brief: {
      brief_id: 'MB-seam-gate-p1', intent: 'INT-FORMATION-FLIGHT', seam_id: 'seam-gate',
      title: 'author the coherence gate', interface_contract: 'CON-FORMATION-GATE',
      reference_frame: {
        glossary: { 'Mission Brief': 'the typed coherence contract handed to a sortie' },
        canonical_terms: ['Mission Brief'],
        forbidden_synonyms: { 'Mission Brief': ['Brief Envelope', 'Dispatch Brief', 'Flight Brief'] },
      },
      invariants: ['the gate is template-only, never a new hook under hooks/'],
      non_goals: ['do not edit servers/models.py', 'do not add a hook under hooks/'],
      drift_markers: ['any absolute-green gating'], trust_gate: 'L3', lambda: 1.5, isolation: 'worktree', model: 'opus',
      verification_rubric: { contract: 'CON-FORMATION-GATE', verification_command: 'false' },
      lineage: { trace_id: 'formation-INT-FORMATION-FLIGHT', span_id: 'seam-gate-p1', parent_id: 'formation-INT-FORMATION-FLIGHT' },
    },
    report: {
      seam_id: 'seam-gate', brief_id: 'MB-seam-gate-p1', summary: 'built the gate but drifted on every axis.',
      outputs: [{ path: 'formation/coherence-gate.workflow.js' }, { path: 'servers/models.py' }],
      touched_paths: ['formation/coherence-gate.workflow.js', 'servers/models.py', 'hooks/new-gate-hook.sh'],
      verification: { command: 'false', ran: true, passed: false, output: 'exit 1' },
      vocabulary_terms: ['Brief Envelope', 'gate'],
      invariants_selfcheck: [{ invariant: 'the gate is template-only, never a new hook under hooks/', held: true, note: 'self-claims held' }],
      non_goals_selfcheck: [{ non_goal: 'do not edit servers/models.py', respected: true, note: 'self-claims respected' }, { non_goal: 'do not add a hook under hooks/', respected: true }],
      contract_changed: true,
      notes: 'seeded drift fixture',
    },
  },
]

phase('Gate')
const verdict = await workflow({ scriptPath: GATE }, { sorties, scope_token: 'internal', intent_root: INTENT_ROOT })

log(`EXERCISE verdict: drift_clean=${verdict.drift_clean} · StageA findings=${(verdict.stageA || []).length}`)
for (const f of (verdict.stageA || [])) log(`  Stage A finding: [${f.severity}] ${f.seam_id} · ${f.kind} · ${f.detail}`)
log(`Stage B audit_chain.color=${verdict.stageB && verdict.stageB.color} — this is the WHOLE-REPO topology, identical regardless of sortie, so audit_chain ALONE cannot tell the clean sortie from the drifted one (false-green).`)

return verdict
