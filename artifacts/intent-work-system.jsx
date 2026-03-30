import { useState } from "react";

const COLORS = {
  bg: "#0f172a",
  surface: "#1e293b",
  surfaceHover: "#334155",
  border: "#334155",
  text: "#f1f5f9",
  textMuted: "#94a3b8",
  // Intent loop phases
  notice: "#f59e0b",
  spec: "#3b82f6",
  execute: "#10b981",
  observe: "#a855f7",
  // Work units
  signal: "#f59e0b",
  intent: "#60a5fa",
  specUnit: "#3b82f6",
  contract: "#10b981",
  capability: "#06b6d4",
  feature: "#a855f7",
  product: "#ec4899",
  // Governance
  play: "#fbbf24",
  build: "#34d399",
  operate: "#60a5fa",
  // Status
  validated: "#10b981",
  exploring: "#f59e0b",
  hypothesis: "#94a3b8",
  invalidated: "#ef4444",
};

const tabs = [
  { id: "ontology", label: "Work Ontology" },
  { id: "dimensions", label: "Three Dimensions" },
  { id: "flow", label: "Agent Flow" },
  { id: "dashboard", label: "Dashboard" },
  { id: "versus", label: "Agile → Intent" },
];

// ─── Work Ontology Tab ───
function OntologyTab() {
  const [selected, setSelected] = useState(null);

  const units = [
    {
      id: "signal",
      name: "Signal",
      color: COLORS.signal,
      replaces: "Idea / Bug Report / Request",
      icon: "◈",
      definition: "An observed change, insight, or opportunity that enters the system.",
      properties: ["Source (Entire trace, user research, market, metrics, agent observation)", "Timestamp", "Confidence score", "Related intents"],
      examples: ["Entire.io trace shows 3 failed auth attempts in deploy pipeline", "User interview reveals confusion about onboarding flow", "Agent observe-cycle detects drift between spec and implementation"],
      key: "Signals are the raw material of discovery. They don't prescribe solutions — they surface reality. Every signal has a source you can trace back to.",
    },
    {
      id: "intent",
      name: "Intent",
      color: COLORS.intent,
      replaces: "Epic / Initiative / Theme",
      icon: "◆",
      definition: "A desired outcome with falsifiable success criteria and a discovery status.",
      properties: ["Hypothesis (falsifiable statement)", "Success criteria (observable outcomes)", "Discovery status (hypothesis → exploring → validated → invalidated)", "Constraints & boundaries", "Opportunity score (reach × impact × confidence)"],
      examples: ["\"Reduce time-to-first-value below 5 minutes for new users\"", "\"Enable agents to execute specs without human handoff\"", "\"Make deployment state visible across all repos in < 30 seconds\""],
      key: "Intents are NOT features. They're outcomes. Teresa Torres's opportunity solution trees live here. An intent stays open until validated or invalidated — it doesn't \"ship.\"",
    },
    {
      id: "spec",
      name: "Spec",
      color: COLORS.specUnit,
      replaces: "User Story / Requirement",
      icon: "◇",
      definition: "A declarative description of desired behavior with shape and boundaries. The unit agents receive and execute against.",
      properties: ["Intent (why this exists — links to parent Intent)", "Shape (boundaries, approach, what's in/out)", "Contracts (the verifiable outcomes)", "Architectural constraints (tech radar refs)", "Dependencies (other specs/contracts needed first)"],
      examples: ["spec/auth-flow-v2.md — reshapes login to reduce steps from 5 to 2", "spec/observe-cycle.md — agent reads Entire traces back into .intent/", "spec/catalog-coverage.md — pipeline achieves 95% asset coverage"],
      key: "Specs replace stories. But unlike stories (\"As a user, I want...\"), specs are declarative state descriptions that any agent can pick up. The spec IS the ticket.",
    },
    {
      id: "contract",
      name: "Contract",
      color: COLORS.contract,
      replaces: "Task / Subtask / Acceptance Criteria",
      icon: "▪",
      definition: "A verifiable interface agreement — input schema, output behavior, invariants. The true atomic unit.",
      properties: ["Input schema (what goes in)", "Output behavior (what comes out)", "Invariants (what must always hold)", "Test fixtures (how to verify)", "Isolation boundary (what this contract does NOT touch)"],
      examples: ["\"Given a library asset path, returns enriched metadata with ≥3 NER entities\"", "\"Given a git repo path, returns health score 0-100 with dimension breakdown\"", "\"Auth endpoint accepts JWT, returns user context in <200ms, never exposes PII\""],
      key: "This is the atom. Contracts are what agents actually execute against. A contract is \"done\" when its assertions pass — not when someone drags a card. Multiple agents can work on independent contracts in parallel.",
    },
    {
      id: "capability",
      name: "Capability",
      color: COLORS.capability,
      replaces: "Component / Service / Module",
      icon: "⬡",
      definition: "A reusable building block composed of contracts. Maps to the tech radar.",
      properties: ["Contracts that define its boundaries", "Tech radar status (adopt / trial / assess / hold)", "Permit level (play / build / operate)", "Dependencies (other capabilities)", "Owner (human or agent)"],
      examples: ["Library enrichment pipeline (NER + attribution + sidecar generation)", "Health check system (11 dimensions, JSON + digest output)", "Observe cycle agent (Entire trace → .intent/ writeback)"],
      key: "Capabilities are the portfolio view. They persist across intents and specs. When a new intent arrives, you check: \"Which capabilities exist? Which need to be built? Which need to be composed differently?\"",
    },
    {
      id: "feature",
      name: "Feature",
      color: COLORS.feature,
      replaces: "Feature / Story Map Column",
      icon: "⬢",
      definition: "A user-facing composition of capabilities delivering observable value.",
      properties: ["Capabilities composed", "User journey (Patton's story map row)", "Value metric (how you know it's working)", "Launch state (dark / beta / GA)"],
      examples: ["\"Repo health dashboard\" = health check + Entire traces + digest generation", "\"Autonomous nightly pipeline\" = enrichment + scheduling + error recovery + observation", "\"Intent-native repo setup\" = .intent/ scaffold + CLAUDE.md + Entire enable"],
      key: "Features are what users experience. They're Jeff Patton's walking skeleton — the thinnest slice of composed capabilities that delivers value. Features don't exist in a backlog; they emerge from composed capabilities.",
    },
    {
      id: "product",
      name: "Product",
      color: COLORS.product,
      replaces: "Program / Portfolio / Product Line",
      icon: "●",
      definition: "A composition of features delivering ongoing value to a defined audience.",
      properties: ["Features composed", "Audience (who it serves)", "Value proposition", "Health metrics (the dashboard view)", "Evolution stage (concept → validated → scaling)"],
      examples: ["Intent methodology product = manifesto + playbook + case studies + workshops", "Brien's autonomous workspace = library pipeline + health check + declutter + observe cycle", "MARS command center = SOW tracking + asset registry + kanban + stakeholder view"],
      key: "Products are living systems, not shipped artifacts. They evolve through the Notice → Spec → Execute → Observe loop continuously. The product IS the loop running.",
    },
  ];

  const compositionLevels = [
    { from: "signal", to: "intent", verb: "feeds", arrow: "→" },
    { from: "intent", to: "spec", verb: "shapes", arrow: "→" },
    { from: "spec", to: "contract", verb: "decomposes into", arrow: "→" },
    { from: "contract", to: "capability", verb: "composes into", arrow: "↑" },
    { from: "capability", to: "feature", verb: "composes into", arrow: "↑" },
    { from: "feature", to: "product", verb: "composes into", arrow: "↑" },
  ];

  return (
    <div>
      <p style={{ color: COLORS.textMuted, marginBottom: 24, lineHeight: 1.6, fontSize: 14 }}>
        The Intent work ontology replaces Jira's ticket hierarchy with <strong style={{ color: COLORS.text }}>declarative, composable units</strong> that agents can consume, execute against, and observe. The flow moves in two directions: <strong style={{ color: COLORS.signal }}>top-down</strong> from signals through discovery to contracts, and <strong style={{ color: COLORS.capability }}>bottom-up</strong> from contracts composing into capabilities, features, and products.
      </p>

      {/* Composition flow */}
      <div style={{ display: "flex", alignItems: "center", gap: 4, marginBottom: 28, flexWrap: "wrap", padding: "16px 12px", background: COLORS.surface, borderRadius: 8, border: `1px solid ${COLORS.border}` }}>
        <span style={{ color: COLORS.textMuted, fontSize: 11, marginRight: 8, textTransform: "uppercase", letterSpacing: 1 }}>Flow:</span>
        {units.map((u, i) => (
          <span key={u.id} style={{ display: "flex", alignItems: "center", gap: 4 }}>
            <span
              onClick={() => setSelected(selected === u.id ? null : u.id)}
              style={{
                color: COLORS.bg,
                background: u.color,
                padding: "3px 10px",
                borderRadius: 4,
                fontSize: 12,
                fontWeight: 600,
                cursor: "pointer",
                opacity: selected && selected !== u.id ? 0.4 : 1,
                transition: "opacity 0.2s",
              }}
            >
              {u.icon} {u.name}
            </span>
            {i < units.length - 1 && (
              <span style={{ color: COLORS.textMuted, fontSize: 14 }}>
                {i < 3 ? "→" : "↑"}
              </span>
            )}
          </span>
        ))}
      </div>

      {/* Unit cards */}
      <div style={{ display: "grid", gap: 12 }}>
        {units.map((u) => {
          const isExpanded = selected === u.id;
          return (
            <div
              key={u.id}
              onClick={() => setSelected(isExpanded ? null : u.id)}
              style={{
                background: isExpanded ? COLORS.surfaceHover : COLORS.surface,
                border: `1px solid ${isExpanded ? u.color + "60" : COLORS.border}`,
                borderRadius: 8,
                padding: isExpanded ? "20px" : "14px 20px",
                cursor: "pointer",
                transition: "all 0.2s",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ fontSize: 20, color: u.color }}>{u.icon}</span>
                  <div>
                    <span style={{ color: u.color, fontWeight: 700, fontSize: 16 }}>{u.name}</span>
                    <span style={{ color: COLORS.textMuted, fontSize: 12, marginLeft: 12 }}>
                      replaces: <span style={{ textDecoration: "line-through" }}>{u.replaces}</span>
                    </span>
                  </div>
                </div>
                <span style={{ color: COLORS.textMuted, fontSize: 18 }}>{isExpanded ? "−" : "+"}</span>
              </div>

              {!isExpanded && (
                <p style={{ color: COLORS.textMuted, fontSize: 13, margin: "8px 0 0 32px", lineHeight: 1.5 }}>
                  {u.definition}
                </p>
              )}

              {isExpanded && (
                <div style={{ marginTop: 16, marginLeft: 32 }}>
                  <p style={{ color: COLORS.text, fontSize: 14, lineHeight: 1.6, marginBottom: 16 }}>
                    {u.definition}
                  </p>

                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
                    <div>
                      <div style={{ color: u.color, fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>Properties</div>
                      {u.properties.map((p, i) => (
                        <div key={i} style={{ color: COLORS.text, fontSize: 13, marginBottom: 4, paddingLeft: 12, borderLeft: `2px solid ${u.color}30` }}>
                          {p}
                        </div>
                      ))}
                    </div>
                    <div>
                      <div style={{ color: u.color, fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>Examples</div>
                      {u.examples.map((e, i) => (
                        <div key={i} style={{ color: COLORS.textMuted, fontSize: 12, marginBottom: 6, fontStyle: "italic", paddingLeft: 12, borderLeft: `2px solid ${u.color}30` }}>
                          {e}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div style={{ background: u.color + "10", border: `1px solid ${u.color}30`, borderRadius: 6, padding: "12px 16px" }}>
                    <span style={{ color: u.color, fontSize: 11, fontWeight: 600 }}>KEY INSIGHT: </span>
                    <span style={{ color: COLORS.text, fontSize: 13, lineHeight: 1.6 }}>{u.key}</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── Three Dimensions Tab ───
function DimensionsTab() {
  const [activeDim, setActiveDim] = useState("right-thing");

  const dimensions = {
    "right-thing": {
      title: "Build the Right Things",
      subtitle: "Validate via Discovery",
      color: COLORS.notice,
      icon: "◈",
      description: "Discovery never stops. Signals flow in continuously, intents carry falsifiable hypotheses, and the observe cycle feeds learnings back. This replaces sprint planning's \"what should we build next?\" with a continuous validation engine.",
      layers: [
        {
          name: "Signal Capture",
          detail: "Entire.io traces, user interviews, agent observations, market signals, system metrics — all feed into a signal stream. No signal is a ticket. Signals are raw reality.",
          tools: "Entire.io, observe-cycle agent, user research notes",
        },
        {
          name: "Opportunity Mapping",
          detail: "Signals cluster into opportunities. Torres's opportunity solution trees organize them. Each opportunity maps to one or more intents. The question isn't \"should we build this feature?\" — it's \"is this outcome worth pursuing?\"",
          tools: "Opportunity tree in .intent/opportunities/, intent backlog",
        },
        {
          name: "Hypothesis Validation",
          detail: "Every intent carries a falsifiable hypothesis. Discovery moves it through: hypothesis → exploring → validated → invalidated. Only validated intents spawn specs. This is the filter that prevents building the wrong thing.",
          tools: "Intent discovery status, evidence log, assumption mapping",
        },
        {
          name: "Observe & Learn",
          detail: "After execution, the observe cycle reads Entire traces back into .intent/decisions.md and .intent/risks.md. What actually happened? Did the outcome match the hypothesis? This closes the loop and generates new signals.",
          tools: "Observe-cycle agent, Entire.io session replay, .intent/ writeback",
        },
      ],
    },
    "right-time": {
      title: "Build at the Right Time",
      subtitle: "Parallelize, Sequence & Prioritize",
      color: COLORS.spec,
      icon: "◆",
      description: "When agents can execute contracts in parallel, the bottleneck shifts from throughput to dependency management. The question isn't \"how many story points can we do?\" — it's \"what's the critical path through the dependency graph?\"",
      layers: [
        {
          name: "Dependency Graph",
          detail: "Every spec declares its dependencies: which contracts must exist, which capabilities it needs. The graph is the roadmap. Agents can parallelize across independent branches. Humans sequence across dependent ones.",
          tools: "Spec dependency declarations, contract interface graph",
        },
        {
          name: "Prioritization by Value",
          detail: "Intents carry opportunity scores (reach × impact × confidence ÷ effort). Specs inherit priority from their parent intent. Contracts inherit from their spec. No separate prioritization ceremony needed — priority flows through the hierarchy.",
          tools: "RICE / ICE scoring on intents, inherited priority cascade",
        },
        {
          name: "Agent Parallelism",
          detail: "Independent contracts execute simultaneously. Agent A works on auth contract. Agent B works on pipeline contract. Agent C works on UI contract. They don't coordinate via standups — they coordinate via contract interfaces.",
          tools: "Contract isolation boundaries, interface schemas, agent orchestrator",
        },
        {
          name: "Roadmap as Dependency Flow",
          detail: "The roadmap isn't a Gantt chart. It's the dependency graph viewed through time. \"Now\" = contracts with no unmet dependencies. \"Next\" = contracts whose dependencies are in progress. \"Later\" = contracts waiting on unvalidated intents.",
          tools: "Now / Next / Later view derived from dependency + discovery status",
        },
      ],
    },
    "right-way": {
      title: "Build the Right Way",
      subtitle: "Architectural Governance",
      color: COLORS.execute,
      icon: "◇",
      description: "The tech radar and permit system replace architecture review meetings. Agents consult CLAUDE.md and .intent/decisions.md before executing. Governance is embedded in context, not enforced by gatekeepers.",
      layers: [
        {
          name: "Tech Radar",
          detail: "Every technology has a ring: Adopt (default choice), Trial (approved for limited use), Assess (exploring, not production), Hold (actively migrating away). Agents read this from .intent/tech-radar.md before choosing implementations.",
          tools: ".intent/tech-radar.md, CLAUDE.md architectural constraints",
        },
        {
          name: "Permit Levels",
          detail: "Capabilities carry a permit: Play (experiment/spike — no production), Build (ship to production — with review), Operate (run in production with SLAs and monitoring). Permits gate what agents are allowed to do with a capability.",
          tools: "Capability permit status, .intent/decisions.md governance records",
        },
        {
          name: "Architectural Decision Records",
          detail: "Every significant decision lands in .intent/decisions.md with: what was decided, why, what was considered, what was rejected. Agents read these before proposing changes. Decisions accumulate institutional memory.",
          tools: ".intent/decisions.md, Entire.io trace → decision extraction",
        },
        {
          name: "Contract Boundaries",
          detail: "Contracts define isolation boundaries — what this component touches and what it explicitly does NOT touch. This replaces \"be careful with that module\" tribal knowledge with verifiable interface agreements.",
          tools: "Contract input/output schemas, invariants, isolation declarations",
        },
      ],
    },
  };

  const dim = dimensions[activeDim];

  return (
    <div>
      {/* Dimension selector */}
      <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
        {Object.entries(dimensions).map(([key, d]) => (
          <button
            key={key}
            onClick={() => setActiveDim(key)}
            style={{
              flex: 1,
              padding: "14px 16px",
              background: activeDim === key ? d.color + "15" : COLORS.surface,
              border: `1px solid ${activeDim === key ? d.color : COLORS.border}`,
              borderRadius: 8,
              cursor: "pointer",
              textAlign: "left",
              transition: "all 0.2s",
            }}
          >
            <div style={{ color: d.color, fontWeight: 700, fontSize: 14, marginBottom: 4 }}>
              {d.icon} {d.title}
            </div>
            <div style={{ color: COLORS.textMuted, fontSize: 12 }}>{d.subtitle}</div>
          </button>
        ))}
      </div>

      {/* Active dimension detail */}
      <p style={{ color: COLORS.textMuted, fontSize: 14, lineHeight: 1.6, marginBottom: 20 }}>
        {dim.description}
      </p>

      <div style={{ display: "grid", gap: 12 }}>
        {dim.layers.map((layer, i) => (
          <div
            key={i}
            style={{
              background: COLORS.surface,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 8,
              padding: "16px 20px",
              borderLeft: `3px solid ${dim.color}`,
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
              <div style={{ color: dim.color, fontWeight: 600, fontSize: 14 }}>
                {i + 1}. {layer.name}
              </div>
              <div style={{ color: COLORS.textMuted, fontSize: 11, background: COLORS.bg, padding: "2px 8px", borderRadius: 4 }}>
                {layer.tools}
              </div>
            </div>
            <p style={{ color: COLORS.text, fontSize: 13, lineHeight: 1.6, margin: 0 }}>
              {layer.detail}
            </p>
          </div>
        ))}
      </div>

      {/* Integration note */}
      <div style={{ marginTop: 20, background: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: 8, padding: 16 }}>
        <div style={{ color: COLORS.text, fontSize: 12, fontWeight: 600, marginBottom: 8 }}>HOW THEY INTERSECT</div>
        <p style={{ color: COLORS.textMuted, fontSize: 13, lineHeight: 1.6, margin: 0 }}>
          A validated <strong style={{ color: COLORS.notice }}>intent</strong> (right thing) spawns <strong style={{ color: COLORS.spec }}>specs with dependency declarations</strong> (right time) that reference <strong style={{ color: COLORS.execute }}>tech radar constraints and contract boundaries</strong> (right way). All three dimensions are encoded in the spec itself — not in separate systems or meetings.
        </p>
      </div>
    </div>
  );
}

// ─── Agent Flow Tab ───
function AgentFlowTab() {
  const phases = [
    {
      name: "Signal Intake",
      color: COLORS.signal,
      agent: "Observe-Cycle Agent",
      input: "Entire.io traces, metrics, user signals",
      output: ".intent/signals/ entries",
      description: "Agent reads Entire session metadata, extracts patterns (failures, drift, unexpected behaviors), writes structured signal files. Runs on schedule or trigger.",
      parallel: false,
    },
    {
      name: "Intent Shaping",
      color: COLORS.intent,
      agent: "Human (Brien) in Cowork",
      input: "Clustered signals, opportunity map",
      output: "Intent with hypothesis + success criteria",
      description: "This is the human-in-the-loop step. You shape signals into intents, write falsifiable hypotheses, define what success looks like. This is where Cagan's product discovery happens.",
      parallel: false,
    },
    {
      name: "Spec Authoring",
      color: COLORS.specUnit,
      agent: "Human + Claude (Cowork)",
      input: "Validated intent, architectural constraints",
      output: "Spec file with contracts + dependencies",
      description: "Collaborative spec writing. Human provides intent and shape. Claude helps decompose into contracts, identify dependencies, check against tech radar. The spec IS the work order.",
      parallel: false,
    },
    {
      name: "Contract Execution",
      color: COLORS.contract,
      agent: "Claude Code CLI Agent(s)",
      input: "Spec + contracts + CLAUDE.md context",
      output: "Implemented code, passing assertions",
      description: "This is where parallelism explodes. Independent contracts execute simultaneously across agents. Each agent reads CLAUDE.md for context, implements against the contract's assertions, commits with Entire.io tracing.",
      parallel: true,
    },
    {
      name: "Verification",
      color: COLORS.validated,
      agent: "Test Agent / CI",
      input: "Contract assertions, integration tests",
      output: "Green/red status per contract",
      description: "Contracts are self-verifying — their assertions ARE the tests. The verification agent runs them, reports status. Failed contracts get fed back as signals.",
      parallel: true,
    },
    {
      name: "Observation",
      color: COLORS.observe,
      agent: "Observe-Cycle Agent",
      input: "Entire.io traces from execution",
      output: "Updated .intent/decisions.md, .intent/risks.md, new signals",
      description: "The loop closes. The observe agent reads what actually happened during execution, extracts decisions and risks, writes them back to .intent/. Drift between spec and implementation becomes a new signal.",
      parallel: false,
    },
  ];

  return (
    <div>
      <p style={{ color: COLORS.textMuted, marginBottom: 24, lineHeight: 1.6, fontSize: 14 }}>
        Work flows through six phases. The key insight: <strong style={{ color: COLORS.contract }}>Contract Execution is the only phase that parallelizes across agents</strong>. Everything else is sequential or collaborative. This is by design — you want humans in the loop for shaping and discovery, agents for execution and observation.
      </p>

      <div style={{ position: "relative" }}>
        {phases.map((phase, i) => (
          <div key={i} style={{ display: "flex", gap: 16, marginBottom: i < phases.length - 1 ? 8 : 0 }}>
            {/* Timeline */}
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 24, flexShrink: 0 }}>
              <div style={{
                width: 16, height: 16, borderRadius: "50%",
                background: phase.color,
                border: `2px solid ${phase.color}`,
                flexShrink: 0,
              }} />
              {i < phases.length - 1 && (
                <div style={{
                  width: 2, flex: 1, minHeight: 20,
                  background: `linear-gradient(${phase.color}, ${phases[i + 1].color})`,
                }} />
              )}
            </div>

            {/* Content */}
            <div style={{
              flex: 1,
              background: COLORS.surface,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 8,
              padding: "14px 18px",
              marginBottom: 8,
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                <span style={{ color: phase.color, fontWeight: 700, fontSize: 14 }}>{phase.name}</span>
                <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                  {phase.parallel && (
                    <span style={{ fontSize: 10, color: COLORS.contract, background: COLORS.contract + "20", padding: "2px 8px", borderRadius: 4, fontWeight: 600 }}>
                      ⚡ PARALLELIZABLE
                    </span>
                  )}
                  <span style={{ fontSize: 11, color: COLORS.textMuted, background: COLORS.bg, padding: "2px 8px", borderRadius: 4 }}>
                    {phase.agent}
                  </span>
                </div>
              </div>
              <p style={{ color: COLORS.text, fontSize: 13, lineHeight: 1.6, margin: "0 0 10px 0" }}>
                {phase.description}
              </p>
              <div style={{ display: "flex", gap: 16, fontSize: 11 }}>
                <div>
                  <span style={{ color: COLORS.textMuted }}>IN: </span>
                  <span style={{ color: COLORS.text }}>{phase.input}</span>
                </div>
                <div>
                  <span style={{ color: COLORS.textMuted }}>OUT: </span>
                  <span style={{ color: COLORS.text }}>{phase.output}</span>
                </div>
              </div>
            </div>
          </div>
        ))}

        {/* Loop-back arrow */}
        <div style={{
          marginTop: 12,
          padding: "12px 16px",
          background: COLORS.observe + "10",
          border: `1px dashed ${COLORS.observe}40`,
          borderRadius: 8,
          textAlign: "center",
        }}>
          <span style={{ color: COLORS.observe, fontSize: 13 }}>
            ↩ Observation generates new <strong>Signals</strong> → loop restarts
          </span>
        </div>
      </div>

      {/* Parallelism callout */}
      <div style={{ marginTop: 20, background: COLORS.surface, border: `1px solid ${COLORS.contract}40`, borderRadius: 8, padding: 16 }}>
        <div style={{ color: COLORS.contract, fontSize: 12, fontWeight: 600, marginBottom: 8 }}>AGENT PARALLELISM MODEL</div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }}>
          {[
            { label: "Spec A → Contract 1", status: "Agent α executing", color: COLORS.contract },
            { label: "Spec A → Contract 2", status: "Agent β executing", color: COLORS.contract },
            { label: "Spec A → Contract 3", status: "Agent γ executing", color: COLORS.contract },
          ].map((c, i) => (
            <div key={i} style={{ background: COLORS.bg, borderRadius: 6, padding: "10px 12px", border: `1px solid ${COLORS.border}` }}>
              <div style={{ color: c.color, fontSize: 12, fontWeight: 600, marginBottom: 4 }}>{c.label}</div>
              <div style={{ color: COLORS.textMuted, fontSize: 11 }}>{c.status}</div>
              <div style={{ marginTop: 6, height: 4, borderRadius: 2, background: COLORS.border, overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${40 + i * 25}%`, background: c.color, borderRadius: 2 }} />
              </div>
            </div>
          ))}
        </div>
        <p style={{ color: COLORS.textMuted, fontSize: 12, marginTop: 10, marginBottom: 0 }}>
          Independent contracts from the same spec execute simultaneously. Agents don't coordinate via standups — they coordinate via <strong style={{ color: COLORS.text }}>contract interfaces</strong>. If Contract 2 depends on Contract 1's output schema, it waits. Otherwise, full parallelism.
        </p>
      </div>
    </div>
  );
}

// ─── Dashboard Tab ───
function DashboardTab() {
  const lookBack = [
    { label: "Signals captured (last 7d)", value: "12", trend: "+3", color: COLORS.signal },
    { label: "Intents validated", value: "2 / 5", trend: "40%", color: COLORS.intent },
    { label: "Specs completed", value: "4", trend: "+2", color: COLORS.specUnit },
    { label: "Contracts green", value: "18 / 21", trend: "86%", color: COLORS.contract },
    { label: "Decisions recorded", value: "6", trend: "+6", color: COLORS.observe },
  ];

  const nowNextLater = {
    now: [
      { name: "Health check scheduling", type: "spec", contracts: "3/3 green", intent: "Autonomous ops" },
      { name: "Observe cycle agent", type: "spec", contracts: "1/4 green", intent: "Self-observing repos" },
    ],
    next: [
      { name: "Digital declutter pipeline", type: "spec", contracts: "0/5 pending", intent: "Autonomous ops", blocked: "Awaiting health check pattern" },
      { name: "Intent manifesto draft", type: "spec", contracts: "0/3 pending", intent: "Thought leadership GTM" },
    ],
    later: [
      { name: "Workshop curriculum", type: "intent", status: "exploring", blocked: "Needs 3+ case studies validated" },
      { name: "Tooling product", type: "intent", status: "hypothesis", blocked: "Conditional on methodology adoption signal" },
    ],
  };

  const capabilities = [
    { name: "Library enrichment", permit: "operate", radar: "adopt", health: 98 },
    { name: "Health check", permit: "build", radar: "adopt", health: 85 },
    { name: "Observe cycle", permit: "play", radar: "trial", health: null },
    { name: "Digital declutter", permit: "play", radar: "assess", health: null },
    { name: "Intent scaffolding", permit: "build", radar: "adopt", health: 100 },
  ];

  const permitColor = { play: COLORS.play, build: COLORS.build, operate: COLORS.operate };
  const radarColor = { adopt: COLORS.validated, trial: COLORS.exploring, assess: COLORS.hypothesis, hold: COLORS.invalidated };

  return (
    <div>
      <p style={{ color: COLORS.textMuted, marginBottom: 20, lineHeight: 1.6, fontSize: 14 }}>
        This is what replaces the Jira board. A <strong style={{ color: COLORS.text }}>look-back / look-forward</strong> view showing work flowing through the Intent system. Numbers below are illustrative based on your current repos.
      </p>

      {/* Metrics strip */}
      <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
        {lookBack.map((m, i) => (
          <div key={i} style={{ flex: 1, background: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: 8, padding: "12px 14px" }}>
            <div style={{ color: m.color, fontSize: 22, fontWeight: 700 }}>{m.value}</div>
            <div style={{ color: COLORS.textMuted, fontSize: 11, marginTop: 4 }}>{m.label}</div>
            <div style={{ color: m.color, fontSize: 11, marginTop: 2, opacity: 0.7 }}>{m.trend}</div>
          </div>
        ))}
      </div>

      {/* Now / Next / Later */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12, marginBottom: 24 }}>
        {Object.entries(nowNextLater).map(([phase, items]) => (
          <div key={phase} style={{ background: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: 8, padding: 16 }}>
            <div style={{
              color: phase === "now" ? COLORS.contract : phase === "next" ? COLORS.specUnit : COLORS.textMuted,
              fontWeight: 700, fontSize: 13, textTransform: "uppercase", letterSpacing: 1, marginBottom: 12,
            }}>
              {phase === "now" ? "⚡ Now" : phase === "next" ? "→ Next" : "◌ Later"}
            </div>
            {items.map((item, i) => (
              <div key={i} style={{
                background: COLORS.bg,
                borderRadius: 6,
                padding: "10px 12px",
                marginBottom: i < items.length - 1 ? 8 : 0,
                borderLeft: `3px solid ${item.type === "spec" ? COLORS.specUnit : COLORS.intent}`,
              }}>
                <div style={{ color: COLORS.text, fontSize: 13, fontWeight: 600 }}>{item.name}</div>
                {item.contracts && (
                  <div style={{ color: COLORS.textMuted, fontSize: 11, marginTop: 4 }}>Contracts: {item.contracts}</div>
                )}
                {item.blocked && (
                  <div style={{ color: COLORS.exploring, fontSize: 11, marginTop: 4 }}>⏳ {item.blocked}</div>
                )}
                {item.status && (
                  <div style={{ color: radarColor[item.status === "exploring" ? "trial" : "assess"], fontSize: 11, marginTop: 4 }}>
                    Discovery: {item.status}
                  </div>
                )}
                <div style={{ color: COLORS.textMuted, fontSize: 10, marginTop: 4 }}>
                  ← {item.intent}
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* Capability Health */}
      <div style={{ background: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: 8, padding: 16 }}>
        <div style={{ color: COLORS.text, fontSize: 13, fontWeight: 700, marginBottom: 12 }}>CAPABILITY HEALTH + GOVERNANCE</div>
        <div style={{ display: "grid", gap: 8 }}>
          {capabilities.map((cap, i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, padding: "8px 12px", background: COLORS.bg, borderRadius: 6 }}>
              <div style={{ flex: 1, color: COLORS.text, fontSize: 13 }}>{cap.name}</div>
              <div style={{
                fontSize: 10, fontWeight: 600, padding: "2px 8px", borderRadius: 4,
                color: permitColor[cap.permit], background: permitColor[cap.permit] + "15",
              }}>
                {cap.permit.toUpperCase()}
              </div>
              <div style={{
                fontSize: 10, fontWeight: 600, padding: "2px 8px", borderRadius: 4,
                color: radarColor[cap.radar], background: radarColor[cap.radar] + "15",
              }}>
                {cap.radar}
              </div>
              <div style={{ width: 60, textAlign: "right" }}>
                {cap.health !== null ? (
                  <span style={{ color: cap.health > 90 ? COLORS.validated : COLORS.exploring, fontSize: 13, fontWeight: 600 }}>
                    {cap.health}%
                  </span>
                ) : (
                  <span style={{ color: COLORS.textMuted, fontSize: 11 }}>—</span>
                )}
              </div>
            </div>
          ))}
        </div>
        <p style={{ color: COLORS.textMuted, fontSize: 11, marginTop: 12, marginBottom: 0 }}>
          <strong style={{ color: COLORS.play }}>PLAY</strong> = experiment only &nbsp;|&nbsp;
          <strong style={{ color: COLORS.build }}>BUILD</strong> = ship to production &nbsp;|&nbsp;
          <strong style={{ color: COLORS.operate }}>OPERATE</strong> = running with SLAs
        </p>
      </div>
    </div>
  );
}

// ─── Agile vs Intent Tab ───
function VersusTab() {
  const comparisons = [
    {
      agile: { concept: "Sprint", description: "Fixed time box (2 weeks). Team commits to a set of work. Success = velocity." },
      intent: { concept: "The Loop", description: "Continuous Notice → Spec → Execute → Observe. No fixed cadence. Success = validated outcomes." },
      shift: "From time-boxed delivery commitments to continuous outcome validation.",
    },
    {
      agile: { concept: "Epic → Story → Task", description: "Hierarchy of human labor. Stories are \"units of work\" sized for humans. Points estimate effort." },
      intent: { concept: "Intent → Spec → Contract", description: "Hierarchy of desired state. Contracts are verifiable interface agreements sized for agents. No points — it's done when assertions pass." },
      shift: "From units of human labor to declarative state descriptions agents can execute.",
    },
    {
      agile: { concept: "Backlog", description: "Ordered list of stories. Groomed in refinement. Prioritized by PO. Lives in Jira." },
      intent: { concept: "Intent Backlog + Signal Stream", description: "Intents with discovery status + continuous signal intake. Prioritized by opportunity score. Lives in .intent/ files." },
      shift: "From a groomed list of features to a validated set of outcomes with evidence.",
    },
    {
      agile: { concept: "Acceptance Criteria", description: "\"Given/When/Then\" statements a human verifies by clicking through the app." },
      intent: { concept: "Contract Assertions", description: "Input/output schemas + invariants that agents verify automatically. Self-testing by design." },
      shift: "From human-verified behavior descriptions to machine-verifiable interface agreements.",
    },
    {
      agile: { concept: "Sprint Retro", description: "Team reflects on process every 2 weeks. Action items often forgotten by next retro." },
      intent: { concept: "Observe Cycle", description: "Agent reads Entire.io traces after every execution. Writes findings to .intent/decisions.md and .intent/risks.md. Nothing is forgotten." },
      shift: "From periodic human reflection to continuous automated observation.",
    },
    {
      agile: { concept: "Definition of Done", description: "Checklist: tests pass, PR reviewed, deployed to staging. Applies uniformly." },
      intent: { concept: "Contract Verification", description: "Each contract carries its own assertions. \"Done\" = all contract assertions pass + Entire trace captured. Different contracts can have different rigor levels." },
      shift: "From uniform checklist to per-contract verification appropriate to the boundary.",
    },
    {
      agile: { concept: "Sprint Planning", description: "Team estimates stories, commits to sprint scope. 2-4 hour ceremony." },
      intent: { concept: "Dependency Resolution", description: "Specs declare dependencies. The graph determines what's ready (Now), what's next (Next), what's waiting (Later). No ceremony — the graph IS the plan." },
      shift: "From estimation ceremonies to dependency graph traversal.",
    },
    {
      agile: { concept: "Jira Board", description: "Kanban/Scrum board showing cards moving through columns (To Do → In Progress → Done)." },
      intent: { concept: "Work Dashboard", description: "Look-back/look-forward view: signals → intents (discovery status) → specs (contract status) → capabilities (health + governance). The board shows system state, not card positions." },
      shift: "From card positions to system health. From \"where is the work?\" to \"is the system learning?\"",
    },
    {
      agile: { concept: "Standup", description: "Daily 15-minute sync. What did you do? What will you do? Any blockers?" },
      intent: { concept: "No Equivalent", description: "Agents don't need standups. Contract interfaces ARE the coordination mechanism. Humans review the dashboard and signal stream instead of asking each other for status." },
      shift: "From human sync ceremonies to observable system state.",
    },
  ];

  return (
    <div>
      <p style={{ color: COLORS.textMuted, marginBottom: 20, lineHeight: 1.6, fontSize: 14 }}>
        Every Agile ceremony and artifact has a structural replacement in the Intent system. The common pattern: <strong style={{ color: COLORS.text }}>ceremonies become continuous processes</strong>, <strong style={{ color: COLORS.text }}>human-verified artifacts become machine-verifiable contracts</strong>, and <strong style={{ color: COLORS.text }}>status-tracking becomes system observation</strong>.
      </p>

      <div style={{ display: "grid", gap: 10 }}>
        {comparisons.map((c, i) => (
          <div key={i} style={{ background: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: 8, overflow: "hidden" }}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 0 }}>
              {/* Agile side */}
              <div style={{ padding: "12px 16px", borderRight: `1px solid ${COLORS.border}`, opacity: 0.6 }}>
                <div style={{ color: COLORS.invalidated, fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 6 }}>
                  {c.agile.concept}
                </div>
                <p style={{ color: COLORS.textMuted, fontSize: 12, lineHeight: 1.5, margin: 0, textDecoration: "line-through", textDecorationColor: COLORS.invalidated + "40" }}>
                  {c.agile.description}
                </p>
              </div>
              {/* Intent side */}
              <div style={{ padding: "12px 16px" }}>
                <div style={{ color: COLORS.validated, fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 6 }}>
                  {c.intent.concept}
                </div>
                <p style={{ color: COLORS.text, fontSize: 12, lineHeight: 1.5, margin: 0 }}>
                  {c.intent.description}
                </p>
              </div>
            </div>
            {/* Shift line */}
            <div style={{ padding: "8px 16px", background: COLORS.bg, borderTop: `1px solid ${COLORS.border}` }}>
              <span style={{ color: COLORS.specUnit, fontSize: 11 }}>↳ </span>
              <span style={{ color: COLORS.textMuted, fontSize: 11 }}>{c.shift}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Main Component ───
export default function IntentWorkSystem() {
  const [activeTab, setActiveTab] = useState("ontology");

  return (
    <div style={{ background: COLORS.bg, color: COLORS.text, minHeight: "100vh", fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}>
      <div style={{ maxWidth: 900, margin: "0 auto", padding: "32px 24px" }}>
        {/* Header */}
        <div style={{ marginBottom: 32 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
            <div style={{
              width: 36, height: 36, borderRadius: 8,
              background: `linear-gradient(135deg, ${COLORS.specUnit}, ${COLORS.contract})`,
              display: "flex", alignItems: "center", justifyContent: "center",
              color: "white", fontWeight: 800, fontSize: 16,
            }}>
              I
            </div>
            <div>
              <h1 style={{ margin: 0, fontSize: 22, fontWeight: 700, color: COLORS.text }}>
                Intent Work System
              </h1>
              <p style={{ margin: 0, color: COLORS.textMuted, fontSize: 13 }}>
                The agent-native replacement for tickets, sprints, and boards
              </p>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div style={{ display: "flex", gap: 4, marginBottom: 28, borderBottom: `1px solid ${COLORS.border}`, paddingBottom: 0 }}>
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                padding: "10px 18px",
                background: "transparent",
                border: "none",
                borderBottom: `2px solid ${activeTab === tab.id ? COLORS.specUnit : "transparent"}`,
                color: activeTab === tab.id ? COLORS.text : COLORS.textMuted,
                fontSize: 13,
                fontWeight: activeTab === tab.id ? 600 : 400,
                cursor: "pointer",
                transition: "all 0.2s",
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab content */}
        {activeTab === "ontology" && <OntologyTab />}
        {activeTab === "dimensions" && <DimensionsTab />}
        {activeTab === "flow" && <AgentFlowTab />}
        {activeTab === "dashboard" && <DashboardTab />}
        {activeTab === "versus" && <VersusTab />}

        {/* Footer */}
        <div style={{ marginTop: 40, paddingTop: 16, borderTop: `1px solid ${COLORS.border}`, textAlign: "center" }}>
          <p style={{ color: COLORS.textMuted, fontSize: 11, margin: 0 }}>
            Intent Work System — replacing ceremonies with continuous processes, tickets with contracts, boards with observable system state
          </p>
        </div>
      </div>
    </div>
  );
}