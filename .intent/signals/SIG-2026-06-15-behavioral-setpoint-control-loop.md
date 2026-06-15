---
id: SIG-2026-06-15-behavioral-setpoint-control-loop
type: signal
status: captured
severity: medium
created: 2026-06-15
target: "Intent Observe plane — a model-agnostic behavioral-telemetry + closed-loop setpoint-enforcement primitive (drift sensor -> conditional re-injection with hysteresis), with adherence telemetry feeding Observe."
discovered_during: "Intake triage of theparlor/intake#11 — analysis of the Poorna-Repos opus-fable-mode toolkit (governor-block.md / reinject.sh / leak_test.py)."
requested_by: brien (via intake#11)
lineage: theparlor/intake#11
reference_prior_art: "https://github.com/Poorna-Repos/opus-fable-mode (MIT) — JSONL parsing + UserPromptSubmit hook wiring. Reference only; do NOT extend."
---
# Behavioral setpoint as an Intent Observe-plane control loop

## The idea (lift the method, discard the target)
The opus-fable-mode repo chases Claude Fable 5's specific working-style signature (model nostalgia, ~one-release shelf life). The durable artifact underneath is a **model-agnostic behavioral-telemetry + closed-loop setpoint-enforcement module** that maps almost 1:1 onto Intent's Observe plane + DDRs + the flight-dynamics/coefficient model + the existing live drift monitor.

Mapping:
- `governor-block.md` (8-rule CLAUDE.md directive) ≈ a behavioral Contract/Spec (typed artifact / setpoint).
- `reinject.sh` (every-turn re-print hook) ≈ salience-maintenance actuator (thermostat).
- `leak_test.py` (offline JSONL parser → words p25/p50/p75, tool:text ratio, caveat %, self-opener %) ≈ Observe-plane sensor (thermometer). Intent already has a *live in-session* version via the drift-logging FastMCP tool + color-signal monitor.

## Beatable pieces, ranked (per intake#11)
1. **Close the control loop (highest value + Intent fit).** Their diagram labels setpoint/thermostat/measurement, but the thermostat is NOT wired to the thermometer — `reinject.sh` fires unconditionally every turn regardless of drift reading. Wire sensor→actuator: in-session drift detection → conditional re-injection with hysteresis. Cheaper on tokens, self-documenting (each re-injection = a drift Signal/DDR). Needs a live in-session signal (hook reading running JSONL, or in-context heuristic).
2. **Harden the sensor into a real instrument.** Concrete bugs in leak_test.py: (a) `--cap` truncation samples first-N in alphabetical filename order = project-alphabetical sampling bias → reservoir/random sampling; (b) the "terse body + long tail" thesis is never measured — quartiles miss the tail → add p90/p99 + skew + bimodality indicator; (c) "words" = whitespace-split of concatenated blocks, so code fences inflate prose counts → segment code vs prose; (d) verdict fires "✓ converging" on noise with only an n<30 INSUFF gate, no significance test → bootstrap CIs / permutation test on pre/post delta; (e) no confound control though README admits "same project ≠ same task" → task-stratified within-strata comparison to separate model-delta from task-selection.
3. **Generalize the setpoint** from "Fable mode" to any declared behavioral Contract (persona/Voice as setpoint) so it survives the next model release — a Contract on agent behavior with adherence telemetry feeding Observe.
4. **Validation harness / A-B battery.** Governed vs ungoverned on a fixed task battery, effect sizes with error bars — turns behavioral claims into measurements. Couples to #2.

## Recommended scope for a future Claude Code session
Take **#1 + #2 fused**, built as an Intent Observe-plane primitive (drift sensor → DDR-emitting conditional re-injection), model-agnostic, with the Fable signature as just one example contract in the test battery.

Do NOT: chase Fable's specific texture as an end goal; try to close the capability-tier gap (that's orchestration / multi-LLM A-B-C — Vantage — not a prompt).

## Confidence (per intake#11)
Implementation critique HIGH (source read directly). Behavioral deltas are the author's single-corpus measurements — directional only, not reproduced. Product framing (Fable suspended 2026-06-12) checks out.

## Next
Idea captured for review-in-arrears. Promotion to a build is a Brien call — if greenlit, scope is #1+#2 fused above. This is propose-only; nothing built.
