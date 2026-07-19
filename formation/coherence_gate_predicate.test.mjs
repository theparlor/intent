// coherence_gate_predicate.test.mjs — regression guard for SIG-2026-06-05.
// Run: node --test formation/coherence_gate_predicate.test.mjs
//
// The Workflow harness requires each workflow script to be self-contained
// (`export const meta` must be the first statement; no sibling imports), so the
// drift-clean predicate lives INLINE in coherence-gate.workflow.js. To test the
// REAL predicate rather than a shadow copy, this file reads the workflow source,
// extracts the block between the `coherence-gate:drift-predicate` sentinels, and
// executes that exact source against fixtures.
//
// The load-bearing assertion is "red baseline + zero delta => clean": if a
// future edit reverts the predicate to gate on absolute audit_chain color
// (`stageB.color === 'green'`), that test — and the no-.color source guard —
// go red. That is the whole point (reconsider_when: "gates on an ABSOLUTE
// health score/color rather than a delta").
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const src = readFileSync(join(here, 'coherence-gate.workflow.js'), 'utf8')

const START = '// >>> coherence-gate:drift-predicate:start'
const END = '// <<< coherence-gate:drift-predicate:end'
const s = src.indexOf(START)
const e = src.indexOf(END)
assert.ok(s !== -1 && e !== -1 && e > s, 'drift-predicate sentinels not found in coherence-gate.workflow.js')
const block = src.slice(s + START.length, e)

// Build an executable predicate from the REAL inline source. The block is pure
// in (args, stageB, stageAFindings) and defines driftClean/newTopology/hasBaseline.
const runPredicate = new Function(
  'args', 'stageB', 'stageAFindings',
  `${block}\nreturn { driftClean, newTopology, hasBaseline };`,
)

// baselineFindings === null  -> gate invoked with NO baseline (args has no key)
// baselineFindings === []    -> a real empty baseline (pre-fan-out found nothing)
function compute({ stageAFindings = [], stageB = null, baselineFindings = null } = {}) {
  const args = baselineFindings === null ? {} : { baseline_findings: baselineFindings }
  return runPredicate(args, stageB, stageAFindings)
}

const redBaseline = [
  { kind: 'orphan', id: 'sig-old-1' },
  { kind: 'unspecced_signal', id: 'sig-old-2' },
]
const stageBRedSameAsBaseline = { color: 'red', counts: { orphans: 1 }, findings: [...redBaseline] }

test('red baseline + clean formation (zero delta) => drift_clean TRUE', () => {
  // Anti-false-green guard: audit_chain color is RED, but no NEW findings => clean.
  const r = compute({ stageAFindings: [], stageB: stageBRedSameAsBaseline, baselineFindings: redBaseline })
  assert.equal(r.driftClean, true)
  assert.equal(r.newTopology.length, 0)
})

test('a NEW topology finding vs baseline => drift_clean FALSE', () => {
  const stageB = { color: 'red', counts: {}, findings: [...redBaseline, { kind: 'orphan', id: 'sig-NEW' }] }
  const r = compute({ stageAFindings: [], stageB, baselineFindings: redBaseline })
  assert.equal(r.driftClean, false)
  assert.equal(r.newTopology.length, 1)
  assert.equal(r.newTopology[0].id, 'sig-NEW')
})

test('no baseline => topology not gated (pre-existing debt ignored)', () => {
  const r = compute({ stageAFindings: [], stageB: { color: 'red', counts: {}, findings: redBaseline }, baselineFindings: null })
  assert.equal(r.hasBaseline, false)
  assert.equal(r.driftClean, true)
})

test('Stage-A findings => drift_clean FALSE even when topology is clean', () => {
  const r = compute({
    stageAFindings: [{ kind: 'non_goal_violated', detail: 'touched servers/models.py', severity: 'high' }],
    stageB: { color: 'green', counts: {}, findings: [] },
    baselineFindings: [],
  })
  assert.equal(r.driftClean, false)
})

test('green color + zero delta + no Stage-A findings => clean', () => {
  const r = compute({ stageAFindings: [], stageB: { color: 'green', counts: {}, findings: [] }, baselineFindings: [] })
  assert.equal(r.driftClean, true)
})

test('empty-baseline array is a real baseline: a NEW finding fails', () => {
  const r = compute({ stageAFindings: [], stageB: { color: 'amber', counts: {}, findings: [{ kind: 'orphan', id: 'x' }] }, baselineFindings: [] })
  assert.equal(r.hasBaseline, true)
  assert.equal(r.driftClean, false)
})

test('source guard: the predicate does NOT gate on absolute audit_chain color', () => {
  // Directly encodes reconsider_when: gating on ABSOLUTE color instead of delta.
  assert.ok(!/\.color\b/.test(block), 'drift predicate must not reference stageB.color — gate on the DELTA, not absolute color')
  assert.ok(/newTopology\.length === 0/.test(block), 'drift predicate must gate on the count of NEW findings vs baseline')
})
