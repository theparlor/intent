export const meta = {
  name: 'formation-flight',
  description: 'TEMPLATE reference harness for coherent non-colliding parallel development. Decompose an intent into seams (frozen Contracts), fan out one sortie per seam each carrying a Mission Brief, run the two-stage coherence gate, loop until drift-clean. Adapt the seams + tasks per real run; do NOT run verbatim. Spec: SPEC-INTENT-FORMATION-FLIGHT-001.',
  phases: [
    { title: 'Fan out', detail: 'one sortie per seam, each with a Mission Brief; isolation+model per the governance matrix' },
    { title: 'Gate', detail: 'two-stage coherence gate (composed: coherence-gate.workflow.js)' },
    { title: 'Converge', detail: 'loop until drift-clean or max_passes' },
  ],
}

// =====================================================================
// args = {
//   intent: "INT-...",                     // the shared 'why' (ON-trigger key)
//   seams: [ {                             // one per frozen Contract; see mission-brief.schema.json
//     seam_id, interface_contract, task,
//     reference_frame: {glossary, canonical_terms, forbidden_synonyms},
//     invariants: [], non_goals: [], drift_markers: [],
//     trust_gate: "L2"|"L3"|"L4", lambda: 1.0,
//     isolation: "worktree"|"readonly"|"none", model: "sonnet"|"opus"|"haiku",
//     verification_rubric: { contract, verification_command }
//   }, ... ],
//   scope_token?: "internal",
//   intent_root?: "/Users/brien/Workspaces/Core/frameworks/intent",
//   max_passes?: 3
// }
// =====================================================================

const intent = (args && args.intent) || 'INT-UNKNOWN'
const seams = (args && args.seams) || []
const scopeToken = (args && args.scope_token) || 'internal'
const intentRoot = (args && args.intent_root) || '/Users/brien/Workspaces/Core/frameworks/intent'
const maxPasses = (args && args.max_passes) || 3
const GATE = intentRoot + '/formation/coherence-gate.workflow.js'

// ON-TRIGGER: formation machinery only applies to >=2 parallel sorties on one intent.
if (seams.length < 2) {
  log(`formation-flight: only ${seams.length} seam(s) — below the >=2 ON-trigger. Fly solo; no formation overhead needed.`)
  return { skipped: true, reason: 'solo path — formation not engaged', seams: seams.length }
}

// Compact Mission Report schema (canonical: formation/mission-report.schema.json; pinned by test_formation.py).
const MISSION_REPORT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['seam_id', 'brief_id', 'touched_paths', 'verification', 'vocabulary_terms', 'invariants_selfcheck', 'non_goals_selfcheck', 'contract_changed'],
  properties: {
    seam_id: { type: 'string' },
    brief_id: { type: 'string' },
    summary: { type: 'string' },
    outputs: { type: 'array', items: { type: 'object' } },
    touched_paths: { type: 'array', items: { type: 'string' } },
    verification: {
      type: 'object', additionalProperties: false, required: ['command', 'ran', 'passed'],
      properties: { command: { type: 'string' }, ran: { type: 'boolean' }, passed: { type: 'boolean' }, output: { type: 'string' } },
    },
    vocabulary_terms: { type: 'array', items: { type: 'string' } },
    invariants_selfcheck: { type: 'array', items: { type: 'object' } },
    non_goals_selfcheck: { type: 'array', items: { type: 'object' } },
    contract_changed: { type: 'boolean' },
    notes: { type: 'string' },
  },
}

// Build a Mission Brief from a seam (+ deterministic lineage; no Date/random in workflow scripts).
function buildBrief(seam, pass) {
  return {
    brief_id: `MB-${seam.seam_id}-p${pass}`,
    intent,
    seam_id: seam.seam_id,
    title: seam.title || seam.seam_id,
    interface_contract: seam.interface_contract,
    reference_frame: seam.reference_frame || { glossary: {} },
    invariants: seam.invariants || [],
    non_goals: seam.non_goals || [],
    drift_markers: seam.drift_markers || [],
    trust_gate: seam.trust_gate || 'L2',
    lambda: typeof seam.lambda === 'number' ? seam.lambda : 1.0,
    isolation: seam.isolation || 'none',
    model: seam.model,
    verification_rubric: seam.verification_rubric || { contract: seam.interface_contract, verification_command: '' },
    lineage: { trace_id: `formation-${intent}`, span_id: `${seam.seam_id}-p${pass}`, parent_id: `formation-${intent}` },
  }
}

function sortiePrompt(brief, corrective) {
  return [
    'You are ONE sortie in a formation. Fly ONLY your seam, behind your FROZEN interface_contract.',
    'Your Mission Brief is the contract you fly under — honor its invariants, stay out of its non_goals,',
    'use the reference_frame vocabulary verbatim, and DO NOT change your interface_contract.',
    '',
    '## Mission Brief',
    JSON.stringify(brief, null, 2),
    '',
    corrective ? '## CORRECTIVE PASS — fix exactly these findings from the last gate:\n' + corrective + '\n' : '',
    '## Your task',
    brief._task || '(no task text supplied)',
    '',
    '## On completion, return a Mission Report (the schema). Be honest:',
    '- Actually RUN your verification_rubric.verification_command and report the real result.',
    '- List EVERY path you touched (the gate intersects these across sorties for collisions).',
    '- Report the vocabulary terms you used for the brief concepts (the gate diffs vs the glossary).',
    '- Self-check each invariant and non_goal. contract_changed=true ONLY if you altered the interface.',
  ].join('\n')
}

// Pre-formation baseline so the gate measures DELTA (new debt), not absolute topology. Gating on
// absolute audit_chain color would fire on the repo's pre-existing chain debt — zero-violation-start.
phase('Gate')
const BASELINE_AUDIT_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['color', 'counts', 'findings'],
  properties: { color: { type: 'string' }, counts: { type: 'object' }, findings: { type: 'array', items: { type: 'object' } } },
}
const baseline = await agent([
  'Return the CURRENT Intent audit_chain result as {color, counts, findings} (the pre-formation baseline).',
  'Run with Bash from the servers dir and parse the JSON it prints:',
  `  cd ${intentRoot}/servers && ./.venv/bin/python -c "import knowledge; print(knowledge.audit_chain('${scopeToken}'))"`,
].join('\n'), { label: 'baseline:audit_chain', phase: 'Gate', schema: BASELINE_AUDIT_SCHEMA })
const baselineFindings = (baseline && baseline.findings) || []
log(`baseline audit_chain: color=${baseline && baseline.color}, ${baselineFindings.length} pre-existing finding(s) — gate measures delta from here`)

let activeSeams = seams
let lastVerdict = null

for (let pass = 1; pass <= maxPasses; pass++) {
  phase('Fan out')
  log(`pass ${pass}/${maxPasses}: dispatching ${activeSeams.length} sortie(s) for intent ${intent}`)

  const sorties = await parallel(activeSeams.map((seam) => () => {
    const brief = buildBrief(seam, pass)
    brief._task = seam.task
    const corrective = seam._corrective || ''
    const opts = { label: `sortie:${seam.seam_id}`, phase: 'Fan out', schema: MISSION_REPORT_SCHEMA }
    if (seam.model) opts.model = seam.model
    if (seam.isolation === 'worktree') opts.isolation = 'worktree' // physical separation minima
    return agent(sortiePrompt(brief, corrective), opts).then((report) => ({ brief, report }))
  }))

  const valid = sorties.filter((s) => s && s.report)

  phase('Gate')
  const verdict = await workflow({ scriptPath: GATE }, {
    sorties: valid,
    scope_token: scopeToken,
    intent_root: intentRoot,
    baseline_findings: baselineFindings,
  })
  lastVerdict = verdict

  phase('Converge')
  if (verdict.drift_clean) {
    log(`formation converged on pass ${pass}: drift-clean.`)
    return { converged: true, passes: pass, verdict }
  }

  // Corrective pass: re-dispatch only the seams that drew findings, told what to fix.
  const bySeam = {}
  for (const f of verdict.stageA || []) {
    if (!f.seam_id) continue
    ;(bySeam[f.seam_id] = bySeam[f.seam_id] || []).push(`- [${f.severity}] ${f.kind}: ${f.detail}`)
  }
  activeSeams = seams
    .filter((s) => bySeam[s.seam_id])
    .map((s) => ({ ...s, _corrective: bySeam[s.seam_id].join('\n') }))

  log(`pass ${pass} not drift-clean: ${verdict.stageA.length} Stage-A finding(s) + audit_chain=${verdict.stageB && verdict.stageB.color}; ${activeSeams.length} seam(s) need a corrective pass.`)
  if (!activeSeams.length) {
    // findings were cross-cutting (e.g. audit_chain amber) with no per-seam owner — stop, surface.
    log('no per-seam corrective target; surfacing verdict for human review.')
    return { converged: false, passes: pass, verdict, reason: 'non-seam findings need human review' }
  }
}

log(`formation did NOT converge within ${maxPasses} passes — surfacing last verdict (this is a "where it cannot stand up" signal).`)
return { converged: false, passes: maxPasses, verdict: lastVerdict }
