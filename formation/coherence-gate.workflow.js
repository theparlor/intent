export const meta = {
  name: 'coherence-gate',
  description: 'Two-stage Formation Flight coherence gate: Stage A brief-conformance (per-sortie, in-orchestrator) + Stage B audit_chain (persisted-graph topology) -> drift-clean verdict. Wrapping audit_chain ALONE is a false-green gate (it sees topology, not output semantics); Stage A is the load-bearing check. Spec: SPEC-INTENT-COHERENCE-GATE-001. Runnable standalone OR composed via workflow({scriptPath}) from formation-flight.workflow.js.',
  phases: [
    { title: 'Stage A — brief conformance', detail: 'per sortie: run verification_command; diff output vs invariants/non_goals/glossary; contract-freeze; cross-sortie touched_paths overlap' },
    { title: 'Stage B — chain audit', detail: 'wrap audit_chain on merged scope; compute drift-clean predicate' },
  ],
}

// =====================================================================
// args = {
//   sorties: [ { brief: <Mission Brief>, report: <Mission Report> }, ... ],
//   scope_token?: "internal" | "public" | "engagement:<slug>",
//   intent_root?: "/Users/brien/Workspaces/Core/frameworks/intent",
//   prev_findings?: number   // count from the previous pass, for the "no NEW findings" half of drift-clean
// }
// returns { drift_clean, stageA: [findings], stageB: {color,counts,findings}, new_findings }
// =====================================================================

const sorties = (args && args.sorties) || []
const scopeToken = (args && args.scope_token) || 'internal'
const intentRoot = (args && args.intent_root) || '/Users/brien/Workspaces/Core/frameworks/intent'
// Stage B gates on the DELTA vs args.baseline_findings (pre-fan-out audit_chain), not absolute color.
// See the drift-clean predicate at the bottom.

if (!sorties.length) {
  // FAIL-CLOSED: a gate handed nothing must NOT report clean — that would be a false-green on
  // mis-invocation. (Surfaced by the 2026-06-05 exercise: top-level Workflow-tool `args` arrive
  // stringified, so `args.sorties` was empty and an earlier version early-returned drift_clean:true.
  // A gate fails closed, never open.)
  log('coherence-gate: NO sorties supplied — FAIL-CLOSED (likely a mis-invocation, e.g. stringified args).')
  return {
    drift_clean: false,
    stageA: [{ kind: 'no_sorties', detail: 'gate invoked with empty sorties — fail-closed to avoid false-green on mis-invocation', severity: 'high' }],
    stageB: null,
    new_findings: 1,
    error: 'empty_sorties',
  }
}

// Schema the Stage-A agents are forced to return.
const FINDINGS_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['findings'],
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['kind', 'detail', 'severity'],
        properties: {
          kind: { type: 'string', description: 'verification_failed | invariant_violated | non_goal_violated | vocabulary_drift | contract_breach' },
          detail: { type: 'string' },
          severity: { type: 'string', enum: ['low', 'medium', 'high'] },
        },
      },
    },
  },
}

const AUDIT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['color', 'counts', 'findings'],
  properties: {
    color: { type: 'string', enum: ['green', 'amber', 'red'] },
    counts: { type: 'object' },
    findings: { type: 'array', items: { type: 'object' } },
  },
}

function stageAPrompt(s) {
  const b = s.brief || {}
  const r = s.report || {}
  const vr = b.verification_rubric || {}
  return [
    'You are the coherence gate (Stage A) checking ONE sortie of a formation for brief-conformance.',
    'Return ONLY findings (problems). An empty findings array means the sortie conformed.',
    '',
    '## Mission Brief (the contract this sortie flew under)',
    JSON.stringify(b, null, 2),
    '',
    '## Mission Report (what the sortie says it did)',
    JSON.stringify(r, null, 2),
    '',
    '## Checks (emit a finding for each failure)',
    '1. VERIFICATION (kind=verification_failed, high): run this exact command with Bash and require exit 0:',
    '   `' + (vr.verification_command || '(none provided — emit a medium finding that the seam has no verification_command)') + '`',
    '   Trust the real exit code, not the report\'s self-claim. If it does not exit 0, that is a finding.',
    '2. INVARIANTS (kind=invariant_violated, high): for each brief.invariants entry, confirm it held.',
    '   Corroborate testable ones with the verification result and the actual files — do NOT trust',
    '   invariants_selfcheck alone.',
    '3. NON-GOALS (kind=non_goal_violated, high): for each brief.non_goals entry, confirm the report did',
    '   not touch it (cross-check report.touched_paths).',
    '4. VOCABULARY (kind=vocabulary_drift, medium): compare report.vocabulary_terms against',
    '   brief.reference_frame.canonical_terms (must be used) and forbidden_synonyms (must NOT appear).',
    '5. CONTRACT FREEZE (kind=contract_breach, high): if report.contract_changed is true, that is a breach —',
    '   a seam may not move its own interface_contract.',
    '',
    'Preserve contradictions as separate findings; never merge two problems into one (Voices conservation law).',
  ].join('\n')
}

function stageBPrompt() {
  return [
    'You are the coherence gate (Stage B): the persisted-graph topology read for a formation.',
    'Call the Intent `audit_chain` verb and return its parsed result {color, counts, findings}.',
    '',
    'Preferred: if an intent-knowledge MCP tool exposing audit_chain is connected, call it with',
    `scope_token="${scopeToken}".`,
    'Fallback (works without the MCP server): run with Bash from the servers dir and parse the JSON it prints:',
    '  ```',
    `  cd ${intentRoot}/servers && ./.venv/bin/python -c "import knowledge; print(knowledge.audit_chain('${scopeToken}'))"`,
    '  ```',
    'Return EXACTLY the parsed object: {color, counts, findings}. Do not editorialize.',
    'NOTE: audit_chain sees graph TOPOLOGY only (orphans, unspecced signals, uncontracted specs, unverified',
    'contracts). It cannot see vocabulary/non-goal/contract-breach drift — that is Stage A\'s job.',
  ].join('\n')
}

// ---- Stage A: cross-sortie mid-air collision is plain code (no agent needed) ----
phase('Stage A — brief conformance')
const touched = {}
for (const s of sorties) {
  const seam = (s.brief && s.brief.seam_id) || 'unknown-seam'
  for (const p of ((s.report && s.report.touched_paths) || [])) {
    ;(touched[p] = touched[p] || []).push(seam)
  }
}
const overlapFindings = Object.entries(touched)
  .map(([p, seams]) => [p, [...new Set(seams)]])
  .filter(([, seams]) => seams.length > 1)
  .map(([p, seams]) => ({
    kind: 'mid_air_collision',
    detail: `path ${p} mutated by multiple seams: ${seams.join(', ')}`,
    severity: 'high',
    seam_id: seams.join('+'),
  }))

// ---- Stage A: per-sortie brief-conformance, one agent each, in parallel ----
const perSortie = await parallel(sorties.map((s) => () =>
  agent(stageAPrompt(s), {
    label: `stageA:${(s.brief && s.brief.seam_id) || '?'}`,
    phase: 'Stage A — brief conformance',
    schema: FINDINGS_SCHEMA,
  }).then((res) => ((res && res.findings) || []).map((f) => ({
    ...f,
    seam_id: (s.brief && s.brief.seam_id) || null,
    brief_id: (s.brief && s.brief.brief_id) || null,
  })))
))

const stageAFindings = [...overlapFindings, ...perSortie.filter(Boolean).flat()]

// ---- Stage B: audit_chain topology read on the merged scope ----
phase('Stage B — chain audit')
const stageB = await agent(stageBPrompt(), {
  label: 'stageB:audit_chain',
  phase: 'Stage B — chain audit',
  schema: AUDIT_SCHEMA,
})

// ---- drift-clean stop predicate (DELTA, not absolute) ----
// audit_chain reports whole-repo topology health, which may be amber/red for PRE-EXISTING debt that
// has nothing to do with this formation. Gating on absolute green would fire against existing state —
// violating the zero-violation-start principle (memory: feedback_invariant_zero_violation_start). So
// Stage B gates on the DELTA: did THIS formation introduce NEW topology findings vs the pre-fan-out
// baseline? Absolute color is reported but informational. (Surfaced by exercising the gate, 2026-06-05.)
// The drift-clean predicate is a pure function of (stageAFindings, stageB, args).
// The block between the sentinels below is extracted and executed verbatim by
// coherence_gate_predicate.test.mjs — it is the SINGLE source of truth, tested
// directly (the Workflow harness forbids importing a sibling module, so the
// predicate must live inline; the test reads it here rather than a shadow copy).
// A regression that gates on absolute stageB.color instead of the DELTA fails
// those tests. Keep this block pure: reference only stageAFindings, stageB, args.
// >>> coherence-gate:drift-predicate:start
const fid = (f) => `${f && f.kind}:${f && f.id}`
const hasBaseline = !!(args && args.baseline_findings)
const baselineIds = new Set(((args && args.baseline_findings) || []).map(fid))
const afterFindings = (stageB && stageB.findings) || []
const newTopology = afterFindings.filter((f) => !baselineIds.has(fid(f)))
const topologyClean = hasBaseline ? newTopology.length === 0 : true // no baseline => don't gate on pre-existing debt
const driftClean = stageAFindings.length === 0 && topologyClean
// <<< coherence-gate:drift-predicate:end

log(`coherence-gate verdict: drift_clean=${driftClean} · StageA=${stageAFindings.length} · audit_chain.color=${stageB && stageB.color} (informational) · NEW topology=${hasBaseline ? newTopology.length : 'n/a (no baseline)'}`)

return { drift_clean: driftClean, stageA: stageAFindings, stageB, new_findings: stageAFindings.length, new_topology: newTopology }
