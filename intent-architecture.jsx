import { useState } from "react";

const PHASES = [
  { id: "notice", label: "Notice", color: "#22D3EE", icon: "◉" },
  { id: "spec", label: "Spec", color: "#A78BFA", icon: "◈" },
  { id: "execute", label: "Execute", color: "#F59E0B", icon: "◆" },
  { id: "observe", label: "Observe", color: "#34D399", icon: "◎" },
];

const SERVERS = [
  {
    id: "notice",
    name: "intent-notice",
    phase: "notice",
    port: 8001,
    description: "Signal lifecycle: capture → enrich → cluster → promote to intent",
    tools: [
      { name: "create_signal", desc: "Capture with trust scoring + autonomy level" },
      { name: "score_trust", desc: "Rescore trust factors, detect boundary crossings" },
      { name: "cluster_signals", desc: "Group by emergent theme" },
      { name: "promote_to_intent", desc: "Cluster → INT-NNN problem worth solving" },
      { name: "add_reference", desc: "Track amplification (7-day half-life)" },
      { name: "dismiss_signal", desc: "Remove from active pipeline" },
      { name: "list_signals", desc: "Query with status/trust/cluster filters" },
      { name: "get_events", desc: "Notice-phase event stream" },
    ],
    schemas: ["Signal (SIG-NNN)", "Intent (INT-NNN)"],
    storage: ".intent/signals/, .intent/intents/",
    events: ["signal.created", "signal.updated", "signal.dismissed", "signal.clustered", "signal.promoted", "intent.proposed"],
  },
  {
    id: "spec",
    name: "intent-spec",
    phase: "spec",
    port: 8002,
    description: "Shape intents into agent-executable specs with verifiable contracts",
    tools: [
      { name: "create_spec", desc: "Spec from intent with completeness scoring" },
      { name: "create_contract", desc: "Verifiable assertion (4 types × 3 severities)" },
      { name: "verify_contract", desc: "Record verification result, emit event" },
      { name: "assess_agent_readiness", desc: "Check spec meets L3/L4 threshold" },
      { name: "list_specs", desc: "Query by status/product/agent-ready" },
    ],
    schemas: ["Spec (SPEC-NNN)", "Contract (CON-NNN)"],
    storage: "spec/SPEC-NNN-*.md, spec/contracts/",
    events: ["spec.created", "spec.approved", "spec.executing", "spec.completed", "contract.verified", "contract.failed"],
  },
  {
    id: "observe",
    name: "intent-observe",
    phase: "observe",
    port: 8003,
    description: "Event ingestion, delta detection, loop closure via suggested signals",
    tools: [
      { name: "ingest_event", desc: "Accept any of 15 OTel-compatible event types" },
      { name: "detect_spec_delta", desc: "Compare specified vs actual" },
      { name: "detect_trust_drift", desc: "Find signals with shifting trust" },
      { name: "system_health", desc: "Pipeline health across all 4 phases" },
      { name: "suggest_signals_from_events", desc: "CLOSES THE LOOP: observe → notice" },
    ],
    schemas: ["Event (JSONL)"],
    storage: ".intent/events/events.jsonl",
    events: ["system.status", "(consumes all 15 types)"],
  },
  {
    id: "knowledge",
    name: "intent-knowledge",
    phase: "knowledge",
    port: 8004,
    description: "Knowledge Engine: compile raw → knowledge, query, lint gaps/contradictions (DDR-005, 2026-04-06)",
    tools: [
      { name: "ingest", desc: "Compile raw/ sources → knowledge/ artifacts (personas, journeys, DDRs)" },
      { name: "query", desc: "Query KB for personas, journeys, DDRs during spec authoring" },
      { name: "lint", desc: "Detect gaps, contradictions, staleness — surfaces as signals to Notice" },
      { name: "enrich", desc: "On-demand retroactive enrichment (suggested-first via lint)" },
      { name: "redact", desc: "Apply confidentiality projection at tool level (DDR-016)" },
    ],
    schemas: ["Knowledge artifact (PER/JRN/DDR/THM/DOM/RAT)"],
    storage: "raw/ (immutable), knowledge/ (compiled)",
    events: ["knowledge.compiled", "knowledge.queried", "lint.gap_detected", "lint.contradiction_detected", "lint.staleness_detected"],
  },
];

// DoR / DoD Gate Enforcement Layer (added 2026-04-14 per SIG-045/046)
// Hard gates: work cannot start without DoR met, cannot close without DoD verified
const GATES = [
  {
    id: "dor",
    label: "Definition of Ready",
    role: "Entry gate",
    color: "#EC4899",
    blocks: "dispatch to builder",
    rule: "DoR failure → blocked from starting (blocked_if_unmet: true)",
    template: "knowledge-engine/templates/dor.md",
  },
  {
    id: "dod",
    label: "Definition of Done",
    role: "Exit gate",
    color: "#EC4899",
    blocks: "declaration of complete",
    rule: "DoD failure → remediation list, not quiet deferral",
    template: "knowledge-engine/templates/dod.md",
  },
];

// Work types that use DoR/DoD (6 canonical types per dor-dod-library.md)
const GATE_WORK_TYPES = [
  "Skill Build",
  "Spec Authoring",
  "Engagement Kickoff",
  "Engagement Closure",
  "Persona Enrichment Pass",
  "Critique Panel",
];

// Coherence Engineering stack — CE sits ABOVE Intent per DEFINITION.md §7
// Each layer contains the ones below it
const CE_STACK = [
  {
    tier: 4,
    label: "Coherence Engineering",
    scope: "team / system",
    desc: "Multiple human + agent producers compose into coherent outputs. 5 axioms · 4 altitudes · 7 coexistence constraints.",
    color: "#A855F7",
    current: true,
  },
  {
    tier: 3,
    label: "Harness Engineering",
    scope: "individual workflow",
    desc: "Scaffolding that makes execution reliable",
    color: "#64748B",
  },
  {
    tier: 2,
    label: "Context Engineering",
    scope: "individual session",
    desc: "What the model sees when it thinks",
    color: "#64748B",
  },
  {
    tier: 1,
    label: "Prompt Engineering",
    scope: "individual utterance",
    desc: "What you say to the model",
    color: "#64748B",
  },
];

// The Intent → CE relationship per DEFINITION.md §7
const CE_CHAIN = [
  { label: "Coherence Engineering", desc: "Discipline — what is coherent, why, toward what vision", color: "#A855F7" },
  { label: "Intent", desc: "Framework — Notice · Spec · Execute · Observe for individual work", color: "#A78BFA" },
  { label: "Scope Resolvers", desc: "Per-artifact-type lookup tables — where does this belong", color: "#22D3EE" },
  { label: "Write-through Hooks / Gates", desc: "Enforcement at creation time (DoR / DoD)", color: "#EC4899" },
];

const AGENTS = [
  { id: "capture", name: "signal-capture", model: "Haiku", server: "notice", color: "#22D3EE", desc: "Captures raw signals" },
  { id: "enricher", name: "signal-enricher", model: "Sonnet", server: "notice", color: "#22D3EE", desc: "Clusters + promotes" },
  { id: "writer", name: "spec-writer", model: "Sonnet", server: "spec", color: "#A78BFA", desc: "Specs + contracts" },
  { id: "verifier", name: "contract-verifier", model: "Sonnet", server: "spec", color: "#F59E0B", desc: "Checks contracts" },
  { id: "observer", name: "observer", model: "Sonnet", server: "observe", color: "#34D399", desc: "Detects + closes loop" },
  { id: "coordinator", name: "coordinator", model: "Sonnet", server: "all", color: "#F472B6", desc: "Orchestrates all" },
];

const AUTONOMY = [
  { level: "L0", range: "< 0.2", behavior: "Human drives. Agent records only.", color: "#EF4444" },
  { level: "L1", range: "0.2–0.4", behavior: "Agent suggests. Human decides.", color: "#F97316" },
  { level: "L2", range: "0.4–0.6", behavior: "Agent proposes, awaits approval.", color: "#EAB308" },
  { level: "L3", range: "0.6–0.85", behavior: "Agent executes. Human monitors.", color: "#22C55E" },
  { level: "L4", range: "≥ 0.85", behavior: "Full autonomy. Circuit breakers only.", color: "#06B6D4" },
];

export default function IntentArchitecture() {
  const [view, setView] = useState("loop");
  const [selectedServer, setSelectedServer] = useState(null);

  const server = SERVERS.find((s) => s.id === selectedServer);
  const phaseColor = (id) => {
    if (id === "knowledge") return "#F472B6";
    return PHASES.find((p) => p.id === id)?.color || "#64748B";
  };

  return (
    <div style={{
      fontFamily: "'IBM Plex Mono', 'JetBrains Mono', monospace",
      background: "#050810",
      color: "#CBD5E1",
      minHeight: "100vh",
      padding: "20px",
    }}>
      <div style={{ maxWidth: 960, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ marginBottom: 28 }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
            <h1 style={{ fontSize: 24, fontWeight: 700, color: "#F8FAFC", margin: 0, letterSpacing: "-0.03em" }}>
              Intent
            </h1>
            <span style={{ fontSize: 13, color: "#475569" }}>Multi-Agent MCP Architecture</span>
          </div>
          <p style={{ color: "#475569", fontSize: 12, marginTop: 4 }}>
            Four MCP servers · Six Claude Code subagents · Four-phase loop · DoR/DoD gates · Coherence Engineering above
          </p>
        </div>

        {/* View Toggle */}
        <div style={{ display: "flex", gap: 6, marginBottom: 20, flexWrap: "wrap" }}>
          {[
            { id: "ce", label: "CE Stack" },
            { id: "loop", label: "The Loop" },
            { id: "servers", label: "MCP Servers" },
            { id: "gates", label: "DoR / DoD" },
            { id: "agents", label: "Subagents" },
            { id: "trust", label: "Trust & Autonomy" },
          ].map((v) => (
            <button
              key={v.id}
              onClick={() => { setView(v.id); setSelectedServer(null); }}
              style={{
                padding: "5px 12px",
                borderRadius: 5,
                border: `1px solid ${view === v.id ? "#A78BFA" : "#1E293B"}`,
                background: view === v.id ? "#A78BFA15" : "#0F172A",
                color: view === v.id ? "#C4B5FD" : "#64748B",
                cursor: "pointer",
                fontSize: 11,
                fontFamily: "inherit",
              }}
            >{v.label}</button>
          ))}
        </div>

        {/* ─── CE Stack View (above Intent) ─── */}
        {view === "ce" && (
          <div>
            {/* Discipline progression */}
            <div style={{
              background: "#0C1220", border: "1px solid #1E293B", borderRadius: 10,
              padding: 20, marginBottom: 16,
            }}>
              <div style={{ color: "#A855F7", fontSize: 10, textTransform: "uppercase", marginBottom: 4, letterSpacing: "0.08em", fontWeight: 700 }}>
                Discipline Progression (each contains the ones below)
              </div>
              <div style={{ color: "#475569", fontSize: 11, marginBottom: 16 }}>
                From DEFINITION.md §1 — Coherence Engineering sits above Intent
              </div>
              <div style={{ display: "grid", gap: 6 }}>
                {CE_STACK.map((tier) => (
                  <div key={tier.tier} style={{
                    display: "grid", gridTemplateColumns: "36px 220px 1fr", gap: 12,
                    alignItems: "center",
                    padding: "10px 14px",
                    background: tier.current ? `${tier.color}10` : "#0F1729",
                    border: `1px solid ${tier.color}${tier.current ? "60" : "20"}`,
                    borderLeft: `3px solid ${tier.color}`,
                    borderRadius: 6,
                  }}>
                    <span style={{ color: tier.color, fontWeight: 700, fontSize: 13 }}>T{tier.tier}</span>
                    <div>
                      <div style={{ color: tier.current ? tier.color : "#94A3B8", fontSize: 13, fontWeight: 600 }}>
                        {tier.label}{tier.current && " ←"}
                      </div>
                      <div style={{ color: "#475569", fontSize: 10 }}>{tier.scope}</div>
                    </div>
                    <span style={{ color: "#64748B", fontSize: 11, lineHeight: 1.5 }}>{tier.desc}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* CE → Intent → Resolvers → Gates chain */}
            <div style={{
              background: "#0C1220", border: "1px solid #1E293B", borderRadius: 10,
              padding: 20, marginBottom: 16,
            }}>
              <div style={{ color: "#A855F7", fontSize: 10, textTransform: "uppercase", marginBottom: 4, letterSpacing: "0.08em", fontWeight: 700 }}>
                CE → Intent → Resolvers → Gates
              </div>
              <div style={{ color: "#475569", fontSize: 11, marginBottom: 16 }}>
                Intent is not at the top of the stack. CE is. Intent is how CE is made operational.
              </div>
              <div style={{ display: "grid", gap: 4 }}>
                {CE_CHAIN.map((row, i) => (
                  <div key={row.label}>
                    <div style={{
                      padding: "10px 14px",
                      background: "#0F1729",
                      border: `1px solid ${row.color}30`,
                      borderLeft: `3px solid ${row.color}`,
                      borderRadius: 6,
                      display: "grid", gridTemplateColumns: "240px 1fr", gap: 12, alignItems: "center",
                    }}>
                      <span style={{ color: row.color, fontSize: 13, fontWeight: 600 }}>{row.label}</span>
                      <span style={{ color: "#94A3B8", fontSize: 11 }}>{row.desc}</span>
                    </div>
                    {i < CE_CHAIN.length - 1 && (
                      <div style={{ textAlign: "center", color: "#334155", fontSize: 12, padding: "2px 0" }}>↓</div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Five axioms summary */}
            <div style={{
              background: "#0C1220", border: "1px solid #1E293B", borderRadius: 10, padding: 16,
            }}>
              <div style={{ color: "#A855F7", fontSize: 10, textTransform: "uppercase", marginBottom: 8, letterSpacing: "0.08em", fontWeight: 700 }}>
                Five Axioms (evaluation gate)
              </div>
              <div style={{ color: "#94A3B8", fontSize: 11, lineHeight: 1.7 }}>
                <strong style={{ color: "#F8FAFC" }}>Non-duplicative</strong> (DRY) ·{" "}
                <strong style={{ color: "#F8FAFC" }}>Non-competitive</strong> (bounded context) ·{" "}
                <strong style={{ color: "#F8FAFC" }}>Chainable</strong> (Unix pipes) ·{" "}
                <strong style={{ color: "#F8FAFC" }}>Composable</strong> (atomic + recomposable) ·{" "}
                <strong style={{ color: "#F8FAFC" }}>Intentionally portable</strong> (12-factor).
                Plus <em>vision alignment</em> as sixth anchor.
              </div>
            </div>
          </div>
        )}

        {/* ─── DoR / DoD Gates View ─── */}
        {view === "gates" && (
          <div>
            <div style={{
              background: "#0C1220", border: "1px solid #1E293B", borderRadius: 10,
              padding: 20, marginBottom: 16,
            }}>
              <div style={{ color: "#EC4899", fontSize: 10, textTransform: "uppercase", marginBottom: 4, letterSpacing: "0.08em", fontWeight: 700 }}>
                Hard Gates — Added 2026-04-14 (SIG-045 / SIG-046)
              </div>
              <div style={{ color: "#475569", fontSize: 11, marginBottom: 16 }}>
                Not checklists — hard gates. DoR failure = blocked from starting. DoD failure = blocked from closing.
              </div>
              <div style={{ display: "grid", gap: 10 }}>
                {GATES.map((g) => (
                  <div key={g.id} style={{
                    padding: "14px 18px",
                    background: "#0F1729",
                    border: `1px solid ${g.color}40`,
                    borderLeft: `3px solid ${g.color}`,
                    borderRadius: 6,
                  }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
                      <span style={{ color: g.color, fontSize: 14, fontWeight: 700 }}>{g.label}</span>
                      <span style={{ color: "#64748B", fontSize: 10, textTransform: "uppercase" }}>{g.role}</span>
                    </div>
                    <div style={{ color: "#94A3B8", fontSize: 12, marginTop: 6 }}>{g.rule}</div>
                    <div style={{ color: "#475569", fontSize: 10, marginTop: 6 }}>
                      Blocks: <code style={{ color: "#CBD5E1" }}>{g.blocks}</code>
                      <span style={{ marginLeft: 12 }}>
                        Template: <code style={{ color: "#CBD5E1" }}>{g.template}</code>
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 6 work types */}
            <div style={{
              background: "#0C1220", border: "1px solid #1E293B", borderRadius: 10, padding: 16,
            }}>
              <div style={{ color: "#EC4899", fontSize: 10, textTransform: "uppercase", marginBottom: 8, letterSpacing: "0.08em", fontWeight: 700 }}>
                6 Canonical Work Types (use DoR / DoD)
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 6 }}>
                {GATE_WORK_TYPES.map((t) => (
                  <div key={t} style={{
                    padding: "8px 12px",
                    background: "#0F1729",
                    border: "1px solid #1E293B",
                    borderRadius: 5,
                    color: "#94A3B8",
                    fontSize: 11,
                  }}>{t}</div>
                ))}
              </div>
            </div>

            {/* Enforcement */}
            <div style={{
              background: "#0C1220", border: "1px solid #1E293B", borderRadius: 10,
              padding: 16, marginTop: 16,
            }}>
              <div style={{ color: "#EC4899", fontSize: 10, textTransform: "uppercase", marginBottom: 8, letterSpacing: "0.08em", fontWeight: 700 }}>
                Enforcement (5-Layer Build-Intake)
              </div>
              <div style={{ color: "#94A3B8", fontSize: 11, lineHeight: 1.6 }}>
                Layer 1: PreToolUse hook (<code style={{ color: "#CBD5E1" }}>~/.claude/hooks/skill-intake-gate-check.sh</code>) ·{" "}
                Layer 2: SessionStart reminder (<code style={{ color: "#CBD5E1" }}>build-intake-mandatory</code>) ·{" "}
                Layer 3: Trigger breadth · Layer 4: Visible banner · Layer 5: Overwatch audit.
                Bypass is logged to <code style={{ color: "#CBD5E1" }}>~/.claude/audit/build-intake-bypasses.log</code>.
              </div>
            </div>
          </div>
        )}

        {/* ─── The Loop View ─── */}
        {view === "loop" && (
          <div style={{ background: "#0C1220", border: "1px solid #1E293B", borderRadius: 10, padding: 24 }}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              {PHASES.map((phase, i) => (
                <div
                  key={phase.id}
                  onClick={() => {
                    const srv = SERVERS.find((s) => s.phase === phase.id);
                    if (srv) { setView("servers"); setSelectedServer(srv.id); }
                  }}
                  style={{
                    padding: 20,
                    background: "#0F1729",
                    border: `1px solid ${phase.color}30`,
                    borderRadius: 8,
                    cursor: "pointer",
                    position: "relative",
                    transition: "border-color 0.2s",
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.borderColor = phase.color}
                  onMouseLeave={(e) => e.currentTarget.style.borderColor = `${phase.color}30`}
                >
                  {/* Arrow to next */}
                  {i < 3 && (
                    <div style={{
                      position: "absolute",
                      right: i % 2 === 0 ? -12 : "auto",
                      bottom: i < 2 ? "auto" : -12,
                      left: i % 2 === 1 ? -12 : "auto",
                      top: i < 2 ? "50%" : "auto",
                      color: "#334155",
                      fontSize: 14,
                    }}>
                      {i === 0 ? "→" : i === 1 ? "↓" : "←"}
                    </div>
                  )}

                  <div style={{ fontSize: 20, marginBottom: 4 }}>
                    <span style={{ color: phase.color }}>{phase.icon}</span>
                    <span style={{ color: "#F8FAFC", fontSize: 16, fontWeight: 600, marginLeft: 8 }}>
                      {phase.label}
                    </span>
                  </div>
                  <div style={{ color: "#64748B", fontSize: 11, lineHeight: 1.5 }}>
                    {phase.id === "notice" && "Capture signals from every surface. Trust-score them. Cluster. Promote to intents."}
                    {phase.id === "spec" && "Shape intents into agent-ready specs with verifiable contracts. Clear specs = agent autonomy."}
                    {phase.id === "execute" && "Agents implement against specs at trust-gated autonomy. Atoms coordinate execution."}
                    {phase.id === "observe" && "Events emitted by every action. Compare actual vs spec. Feed deltas back as signals."}
                  </div>
                  <div style={{ marginTop: 10, fontSize: 10, color: phase.color, opacity: 0.7 }}>
                    {phase.id === "notice" && "MCP: intent-notice · SIG-NNN, INT-NNN"}
                    {phase.id === "spec" && "MCP: intent-spec · SPEC-NNN, CON-NNN"}
                    {phase.id === "execute" && "Claude Code subagents · ATOM-NNN"}
                    {phase.id === "observe" && "MCP: intent-observe · events.jsonl"}
                  </div>
                </div>
              ))}
            </div>

            {/* Loop closure arrow */}
            <div style={{
              textAlign: "center", marginTop: 12, color: "#34D399",
              fontSize: 11, opacity: 0.8,
            }}>
              ↻ observe → notice · suggest_signals_from_events closes the loop
            </div>
          </div>
        )}

        {/* ─── Servers View ─── */}
        {view === "servers" && (
          <div>
            <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
              {SERVERS.map((s) => (
                <button
                  key={s.id}
                  onClick={() => setSelectedServer(s.id === selectedServer ? null : s.id)}
                  style={{
                    flex: 1,
                    padding: "12px 14px",
                    borderRadius: 8,
                    border: `1px solid ${selectedServer === s.id ? phaseColor(s.phase) : "#1E293B"}`,
                    background: selectedServer === s.id ? `${phaseColor(s.phase)}12` : "#0C1220",
                    cursor: "pointer",
                    textAlign: "left",
                    fontFamily: "inherit",
                  }}
                >
                  <div style={{ color: phaseColor(s.phase), fontSize: 13, fontWeight: 600 }}>{s.name}</div>
                  <div style={{ color: "#475569", fontSize: 10, marginTop: 2 }}>
                    :{s.port} · {s.tools.length} tools
                  </div>
                </button>
              ))}
            </div>

            {server && (
              <div style={{
                background: "#0C1220",
                border: `1px solid ${phaseColor(server.phase)}30`,
                borderRadius: 10,
                padding: 20,
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
                  <div>
                    <h3 style={{ margin: 0, color: "#F8FAFC", fontSize: 16 }}>{server.name}</h3>
                    <p style={{ color: "#94A3B8", fontSize: 12, margin: "4px 0 0" }}>{server.description}</p>
                  </div>
                  <div style={{
                    padding: "4px 10px", borderRadius: 5, alignSelf: "flex-start",
                    background: `${phaseColor(server.phase)}20`, color: phaseColor(server.phase),
                    fontSize: 11,
                  }}>
                    {server.phase} · :{server.port}
                  </div>
                </div>

                {/* Tools */}
                <div style={{ marginBottom: 16 }}>
                  <div style={{ color: "#475569", fontSize: 10, marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.05em" }}>
                    Tools
                  </div>
                  <div style={{ display: "grid", gap: 6 }}>
                    {server.tools.map((t) => (
                      <div key={t.name} style={{
                        display: "flex", gap: 8, alignItems: "baseline",
                        padding: "6px 10px", background: "#0F1729", borderRadius: 5,
                      }}>
                        <code style={{ color: phaseColor(server.phase), fontSize: 12, flexShrink: 0 }}>{t.name}</code>
                        <span style={{ color: "#475569", fontSize: 10 }}>{t.desc}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Schemas + Events */}
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }}>
                  <div style={{ padding: 10, background: "#0F1729", borderRadius: 6 }}>
                    <div style={{ color: "#475569", fontSize: 9, textTransform: "uppercase", marginBottom: 4 }}>Schemas</div>
                    {server.schemas.map((s) => (
                      <div key={s} style={{ color: "#94A3B8", fontSize: 11 }}>{s}</div>
                    ))}
                  </div>
                  <div style={{ padding: 10, background: "#0F1729", borderRadius: 6 }}>
                    <div style={{ color: "#475569", fontSize: 9, textTransform: "uppercase", marginBottom: 4 }}>Storage</div>
                    <div style={{ color: "#94A3B8", fontSize: 10, wordBreak: "break-all" }}>{server.storage}</div>
                  </div>
                  <div style={{ padding: 10, background: "#0F1729", borderRadius: 6 }}>
                    <div style={{ color: "#475569", fontSize: 9, textTransform: "uppercase", marginBottom: 4 }}>Events</div>
                    {server.events.map((e) => (
                      <div key={e} style={{ color: "#94A3B8", fontSize: 10 }}>{e}</div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ─── Agents View ─── */}
        {view === "agents" && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
            {AGENTS.map((a) => (
              <div key={a.id} style={{
                padding: 14,
                background: "#0C1220",
                border: `1px solid ${a.color}25`,
                borderRadius: 8,
                borderLeft: `3px solid ${a.color}`,
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <code style={{ color: a.color, fontSize: 13 }}>@{a.name}</code>
                  <span style={{
                    padding: "2px 8px", borderRadius: 4, fontSize: 10,
                    background: a.model === "Haiku" ? "#10B98120" : a.model === "Opus" ? "#EC489920" : "#6366F120",
                    color: a.model === "Haiku" ? "#10B981" : a.model === "Opus" ? "#EC4899" : "#818CF8",
                  }}>{a.model}</span>
                </div>
                <div style={{ color: "#64748B", fontSize: 11, marginTop: 6 }}>{a.desc}</div>
                <div style={{ color: "#334155", fontSize: 10, marginTop: 4 }}>
                  → {a.server === "all" ? "all servers" : `intent-${a.server}`}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* ─── Trust View ─── */}
        {view === "trust" && (
          <div>
            <div style={{
              background: "#0C1220", border: "1px solid #1E293B", borderRadius: 10,
              padding: 20, marginBottom: 16,
            }}>
              <div style={{ color: "#64748B", fontSize: 10, textTransform: "uppercase", marginBottom: 12, letterSpacing: "0.05em" }}>
                Trust Formula
              </div>
              <code style={{ color: "#C4B5FD", fontSize: 12, lineHeight: 1.6 }}>
                trust = clarity × <span style={{color:"#22D3EE"}}>0.30</span> + (1/blast_radius) × <span style={{color:"#22D3EE"}}>0.20</span> + reversibility × <span style={{color:"#22D3EE"}}>0.20</span> + testability × <span style={{color:"#22D3EE"}}>0.20</span> + precedent × <span style={{color:"#22D3EE"}}>0.10</span>
              </code>
            </div>

            <div style={{ display: "grid", gap: 6 }}>
              {AUTONOMY.map((a) => (
                <div key={a.level} style={{
                  display: "grid", gridTemplateColumns: "50px 80px 1fr", gap: 12,
                  alignItems: "center",
                  padding: "10px 14px",
                  background: "#0C1220",
                  border: `1px solid ${a.color}20`,
                  borderLeft: `3px solid ${a.color}`,
                  borderRadius: 6,
                }}>
                  <span style={{ color: a.color, fontWeight: 700, fontSize: 14 }}>{a.level}</span>
                  <span style={{ color: "#64748B", fontSize: 11 }}>{a.range}</span>
                  <span style={{ color: "#94A3B8", fontSize: 12 }}>{a.behavior}</span>
                </div>
              ))}
            </div>

            <div style={{
              background: "#0C1220", border: "1px solid #1E293B", borderRadius: 10,
              padding: 16, marginTop: 16,
            }}>
              <div style={{ color: "#64748B", fontSize: 10, textTransform: "uppercase", marginBottom: 8, letterSpacing: "0.05em" }}>
                Amplification (Signal PageRank)
              </div>
              <div style={{ color: "#94A3B8", fontSize: 11, lineHeight: 1.6 }}>
                Signals gain weight through reference. Weight by type: spec/intent = 0.20, signal = 0.15, conversation = 0.10, commit = 0.05.
                References decay with 7-day half-life. When effective_trust crosses an autonomy boundary → flagged for review.
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div style={{
          marginTop: 24, padding: "12px 16px",
          background: "#0C1220", border: "1px solid #1E293B", borderRadius: 8,
          display: "flex", justifyContent: "space-between", alignItems: "center",
        }}>
          <span style={{ color: "#334155", fontSize: 10 }}>
            github.com/theparlor/intent
          </span>
          <span style={{ color: "#334155", fontSize: 10 }}>
            FastMCP Cloud · Cloudflare Workers · Railway — all free tier
          </span>
        </div>
      </div>
    </div>
  );
}
