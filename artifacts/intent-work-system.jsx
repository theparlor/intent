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
      definition: "A coherent statement of purpose that directs discovery and shapes work.",
      properties: ["Title & narrative", "Related signals", "Three-dimension scope", "Lifecycle stage"],
      examples: ["Reduce time-to-production in the deploy pipeline", "Establish confidence in new user cohorts through frictionless onboarding", "Enable data-driven team operating model through observable intent execution"],
      key: "Every intent connects signals to work. It's not a solution — it's the question that shapes discovery.",
    },
    {
      id: "spec",
      name: "Spec Unit",
      color: COLORS.specUnit,
      replaces: "User Story / Task",
      icon: "◇",
      definition: "The smallest unit of work that realizes part of an intent. Fully specced, estimable, and executable.",
      properties: ["Parent intent", "Acceptance criteria", "Capability mapping", "Estimate", "Status"],
      examples: ["Implement webhook retry logic with exponential backoff for failed deployment events", "Design onboarding flow for first-time API consumers", "Create agent observe-cycle that compares spec-as-written to observed behavior"],
      key: "A spec unit lives in the middle ground between intent and execution. It's detailed enough to build, but loose enough to discover.",
    },
    {
      id: "contract",
      name: "Contract",
      color: COLORS.contract,
      replaces: "Definition of Done",
      icon: "◈",
      definition: "The interface agreement between work teams — what's promised, what's verified, what happens next.",
      properties: ["Input specification", "Output specification", "Quality gates", "SLO/SLA"],
      examples: ["Deployment service returns deployment event + webhook URL within 100ms, verified via contract tests", "Onboarding API returns user profile with email verification status within 30s", "Agent produces spec review + delta confidence score or rejects due to parsing error"],
      key: "Contracts are the language teams use to talk across intent boundaries. They're executable specifications of trust.",
    },
    {
      id: "capability",
      name: "Capability",
      color: COLORS.capability,
      replaces: "Feature / Component",
      icon: "◆",
      definition: "A stable, reusable system building block that spec units depend on.",
      properties: ["Owner / team", "Public interface", "SLO/SLA", "Supported spec units"],
      examples: ["Event Bus — handles pub/sub for deployment events, 99.9% uptime", "User Profile Service — manages profiles + verification status, <50ms API latency", "LLM Observe Engine — compares spec to runtime state, confidence threshold configurable"],
      key: "Capabilities are how you scale intent execution. They're the infrastructure of intelligent work.",
    },
    {
      id: "feature",
      name: "Feature",
      color: COLORS.feature,
      replaces: "Epic / Release Train",
      icon: "◇",
      definition: "A user-visible outcome that emerges from coordinated spec units and capabilities.",
      properties: ["User value proposition", "Launch checklist", "Governance review", "Observability instrumentation"],
      examples: ["Automated deployment retry with status transparency", "Zero-friction API onboarding for new partners", "Agent-driven spec validation with human-in-the-loop review"],
      key: "Features are where intent touches users. They're the feedback loop that drives the next signal.",
    },
    {
      id: "product",
      name: "Product",
      color: COLORS.product,
      replaces: "Product / Platform",
      icon: "◆",
      definition: "A coherent system of features + capabilities that solves a distinct user problem at scale.",
      properties: ["Market positioning", "Customer cohorts", "Revenue model", "Competitive landscape"],
      examples: ["Deploy Platform — handles CI/CD, observability, governance for infrastructure teams", "Developer Experience Platform — onboarding, API design, self-service capabilities", "Intent Execution Platform — spec authoring, agent orchestration, team coordination"],
      key: "Products are where multiple intents converge. They're the units of business value.",
    },
  ];

  return (
    <div style={{ padding: "24px", maxWidth: "1200px" }}>
      <div style={{ marginBottom: "32px" }}>
        <h2 style={{ fontSize: "24px", fontWeight: "600", marginBottom: "12px", color: COLORS.text }}>
          Work Ontology
        </h2>
        <p style={{ color: COLORS.textMuted, lineHeight: "1.6" }}>
          Intent work is organized around seven units that form a nested hierarchy. Each unit has a clear purpose, interface, and relationship to the others.
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "16px" }}>
        {units.map((unit) => (
          <div
            key={unit.id}
            onClick={() => setSelected(selected === unit.id ? null : unit.id)}
            style={{
              padding: "16px",
              borderRadius: "8px",
              border: `1px solid ${COLORS.border}`,
              background: selected === unit.id ? COLORS.surface : "transparent",
              cursor: "pointer",
              transition: "all 200ms",
              borderTop: `3px solid ${unit.color}`,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "12px" }}>
              <span style={{ fontSize: "20px" }}>{unit.icon}</span>
              <h3 style={{ fontSize: "16px", fontWeight: "600", color: unit.color }}>{unit.name}</h3>
            </div>
            <p style={{ fontSize: "12px", color: COLORS.textMuted, marginBottom: "8px" }}>Replaces: {unit.replaces}</p>
            <p style={{ color: COLORS.text, fontSize: "13px", lineHeight: "1.5", marginBottom: "12px" }}>{unit.definition}</p>

            {selected === unit.id && (
              <div style={{ marginTop: "12px", paddingTop: "12px", borderTop: `1px solid ${COLORS.border}` }}>
                <div style={{ marginBottom: "12px" }}>
                  <h4 style={{ fontSize: "12px", fontWeight: "600", color: COLORS.text, marginBottom: "4px" }}>Properties</h4>
                  <ul style={{ fontSize: "12px", color: COLORS.textMuted, marginLeft: "16px" }}>
                    {unit.properties.map((prop, i) => (
                      <li key={i} style={{ marginBottom: "2px" }}>
                        {prop}
                      </li>
                    ))}
                  </ul>
                </div>
                <div style={{ marginBottom: "12px" }}>
                  <h4 style={{ fontSize: "12px", fontWeight: "600", color: COLORS.text, marginBottom: "4px" }}>Examples</h4>
                  <ul style={{ fontSize: "12px", color: COLORS.textMuted, marginLeft: "16px" }}>
                    {unit.examples.map((ex, i) => (
                      <li key={i} style={{ marginBottom: "2px" }}>
                        {ex}
                      </li>
                    ))}
                  </ul>
                </div>
                <div style={{ padding: "8px", background: COLORS.bg, borderRadius: "4px", borderLeft: `2px solid ${unit.color}` }}>
                  <p style={{ fontSize: "12px", color: COLORS.text, fontWeight: "500" }}>{unit.key}</p>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Three Dimensions Tab ───
function DimensionsTab() {
  const dimensions = [
    {
      name: "Discovery",
      icon: "◈",
      color: COLORS.notice,
      description: "How do we learn?",
      elements: [
        { label: "Signal", color: COLORS.signal },
        { label: "Intent", color: COLORS.intent },
        { label: "Spec Unit", color: COLORS.specUnit },
      ],
      narrative: "Every piece of work starts with an observation. Signals feed intents. Intents are refined through spec units. Each cycle tightens our understanding of the problem and solution.",
    },
    {
      name: "Building",
      icon: "◆",
      color: COLORS.execute,
      description: "What do we create?",
      elements: [
        { label: "Capability", color: COLORS.capability },
        { label: "Feature", color: COLORS.feature },
        { label: "Product", color: COLORS.product },
      ],
      narrative: "Spec units coordinate into capabilities—reusable building blocks. Capabilities combine into features—user-visible outcomes. Features cluster into products—coherent solutions.",
    },
    {
      name: "Governance",
      icon: "◇",
      color: COLORS.operate,
      description: "How do we coordinate?",
      elements: [
        { label: "Contract", color: COLORS.contract },
        { label: "Play", color: COLORS.play },
        { label: "Operating Model", color: COLORS.operate },
      ],
      narrative: "Contracts are the language teams speak across boundaries. Plays are choreographed sequences of work. The operating model is how all three dimensions interlock.",
    },
  ];

  return (
    <div style={{ padding: "24px", maxWidth: "1200px" }}>
      <div style={{ marginBottom: "32px" }}>
        <h2 style={{ fontSize: "24px", fontWeight: "600", marginBottom: "12px", color: COLORS.text }}>Three Dimensions</h2>
        <p style={{ color: COLORS.textMuted, lineHeight: "1.6" }}>
          Intent organizes work along three orthogonal dimensions: Discovery (how we learn), Building (what we create), and Governance (how we coordinate).
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: "24px" }}>
        {dimensions.map((dim, idx) => (
          <div key={idx}>
            <div style={{ marginBottom: "16px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
                <span style={{ fontSize: "24px" }}>{dim.icon}</span>
                <h3 style={{ fontSize: "18px", fontWeight: "600", color: dim.color }}>{dim.name}</h3>
              </div>
              <p style={{ fontSize: "13px", color: COLORS.textMuted, fontStyle: "italic" }}>{dim.description}</p>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "8px", marginBottom: "16px" }}>
              {dim.elements.map((elem, i) => (
                <div
                  key={i}
                  style={{
                    padding: "12px",
                    background: COLORS.surface,
                    borderRadius: "6px",
                    borderLeft: `3px solid ${elem.color}`,
                    color: elem.color,
                    fontWeight: "500",
                    fontSize: "13px",
                  }}
                >
                  {elem.label}
                </div>
              ))}
            </div>

            <div
              style={{
                padding: "12px",
                background: COLORS.bg,
                borderRadius: "6px",
                borderLeft: `2px solid ${dim.color}`,
              }}
            >
              <p style={{ fontSize: "13px", color: COLORS.text, lineHeight: "1.5" }}>{dim.narrative}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Agent Flow Tab ───
function AgentFlowTab() {
  const phases = [
    {
      id: "notice",
      name: "Notice",
      color: COLORS.notice,
      description: "Observe signals and articulate intents.",
      agent: "Observer Agent",
      inputs: ["Logs, metrics, traces, user feedback"],
      outputs: ["Signal → Intent articulation"],
      example: "Scan deploy logs for patterns. If 3+ failed auth attempts in 1h, surface intent: 'Reduce pipeline auth friction'.",
    },
    {
      id: "spec",
      name: "Specify",
      color: COLORS.spec,
      description: "Refine intents into spec units.",
      agent: "Spec Agent",
      inputs: ["Intent + context"],
      outputs: ["Spec units → Acceptance criteria → Capability map"],
      example: "Given intent, generate spec unit: 'Add exponential backoff to webhook retry logic.' Estimate, assign to capability.",
    },
    {
      id: "execute",
      name: "Execute",
      color: COLORS.execute,
      description: "Implement spec units and build capabilities.",
      agent: "Build Agent",
      inputs: ["Spec units"],
      outputs: ["Code commits → Deployed features"],
      example: "Pull spec unit queue. Implement, test, merge. Update deployment manifest. Notify downstream capabilities.",
    },
    {
      id: "observe",
      name: "Observe",
      color: COLORS.observe,
      description: "Validate execution against spec and surface deltas.",
      agent: "Observer Agent",
      inputs: ["Spec + deployed code"],
      outputs: ["Drift signals → Next cycle intents"],
      example: "Compare spec (webhook <100ms) to observed (p99 150ms). Surface signal: 'Retry logic slower than specified'.",
    },
  ];

  return (
    <div style={{ padding: "24px", maxWidth: "1200px" }}>
      <div style={{ marginBottom: "32px" }}>
        <h2 style={{ fontSize: "24px", fontWeight: "600", marginBottom: "12px", color: COLORS.text }}>Agent Flow</h2>
        <p style={{ color: COLORS.textMuted, lineHeight: "1.6" }}>
          Intent execution is orchestrated by four complementary agents, each handling one phase of the notice→spec→execute→observe cycle.
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", gap: "16px" }}>
        {phases.map((phase) => (
          <div
            key={phase.id}
            style={{
              padding: "16px",
              background: COLORS.surface,
              borderRadius: "8px",
              borderTop: `3px solid ${phase.color}`,
            }}
          >
            <h3 style={{ fontSize: "16px", fontWeight: "600", color: phase.color, marginBottom: "4px" }}>{phase.name}</h3>
            <p style={{ fontSize: "12px", color: COLORS.textMuted, marginBottom: "12px" }}>{phase.agent}</p>
            <p style={{ fontSize: "13px", color: COLORS.text, marginBottom: "12px", lineHeight: "1.5" }}>{phase.description}</p>

            <div style={{ marginBottom: "12px" }}>
              <h4 style={{ fontSize: "11px", fontWeight: "600", color: COLORS.textMuted, marginBottom: "4px" }}>INPUTS</h4>
              <ul style={{ fontSize: "12px", color: COLORS.textMuted, marginLeft: "16px" }}>
                {phase.inputs.map((inp, i) => (
                  <li key={i}>{inp}</li>
                ))}
              </ul>
            </div>

            <div style={{ marginBottom: "12px" }}>
              <h4 style={{ fontSize: "11px", fontWeight: "600", color: COLORS.textMuted, marginBottom: "4px" }}>OUTPUTS</h4>
              <ul style={{ fontSize: "12px", color: COLORS.textMuted, marginLeft: "16px" }}>
                {phase.outputs.map((out, i) => (
                  <li key={i}>{out}</li>
                ))}
              </ul>
            </div>

            <div style={{ padding: "8px", background: COLORS.bg, borderRadius: "4px", borderLeft: `2px solid ${phase.color}` }}>
              <p style={{ fontSize: "12px", color: COLORS.text, fontStyle: "italic" }}>{phase.example}</p>
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: "32px", padding: "16px", background: COLORS.surface, borderRadius: "8px", borderLeft: `3px solid ${COLORS.spec}` }}>
        <h3 style={{ fontSize: "14px", fontWeight: "600", color: COLORS.text, marginBottom: "8px" }}>The Loop</h3>
        <p style={{ color: COLORS.textMuted, fontSize: "13px", lineHeight: "1.6" }}>
          These four phases form a continuous loop. Observe generates signals for Notice. Intents drive Spec. Specs guide Execute. Execution feeds Observe. The entire system is a learning machine—intent execution becomes better with each cycle.
        </p>
      </div>
    </div>
  );
}

// ─── Dashboard Tab ───
function DashboardTab() {
  const workUnits = [
    { label: "Signals", count: "24", color: COLORS.signal, trend: "+6" },
    { label: "Intents", count: "8", color: COLORS.intent, trend: "+2" },
    { label: "Spec Units", count: "47", color: COLORS.specUnit, trend: "+12" },
    { label: "Capabilities", count: "5", color: COLORS.capability, trend: "0" },
    { label: "Features", count: "3", color: COLORS.feature, trend: "+1" },
    { label: "Products", count: "1", color: COLORS.product, trend: "0" },
  ];

  const statuses = [
    { label: "Validated", count: "12", color: COLORS.validated },
    { label: "Exploring", count: "8", color: COLORS.exploring },
    { label: "Hypothesis", count: "5", color: COLORS.hypothesis },
    { label: "Invalidated", count: "2", color: COLORS.invalidated },
  ];

  return (
    <div style={{ padding: "24px", maxWidth: "1200px" }}>
      <div style={{ marginBottom: "32px" }}>
        <h2 style={{ fontSize: "24px", fontWeight: "600", marginBottom: "12px", color: COLORS.text }}>Dashboard</h2>
        <p style={{ color: COLORS.textMuted, lineHeight: "1.6" }}>
          Real-time view of work across all units and lifecycle stages.
        </p>
      </div>

      <div style={{ marginBottom: "32px" }}>
        <h3 style={{ fontSize: "16px", fontWeight: "600", color: COLORS.text, marginBottom: "16px" }}>Work Units</h3>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "12px" }}>
          {workUnits.map((unit, i) => (
            <div
              key={i}
              style={{
                padding: "16px",
                background: COLORS.surface,
                borderRadius: "8px",
                borderLeft: `3px solid ${unit.color}`,
              }}
            >
              <p style={{ fontSize: "12px", color: COLORS.textMuted, marginBottom: "8px" }}>{unit.label}</p>
              <div style={{ display: "flex", alignItems: "baseline", gap: "8px" }}>
                <span style={{ fontSize: "28px", fontWeight: "600", color: unit.color }}>{unit.count}</span>
                <span style={{ fontSize: "12px", color: COLORS.validated }}>{unit.trend}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 style={{ fontSize: "16px", fontWeight: "600", color: COLORS.text, marginBottom: "16px" }}>Status Breakdown</h3>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: "12px" }}>
          {statuses.map((status, i) => (
            <div
              key={i}
              style={{
                padding: "16px",
                background: COLORS.surface,
                borderRadius: "8px",
                borderTop: `3px solid ${status.color}`,
              }}
            >
              <p style={{ fontSize: "12px", color: COLORS.textMuted, marginBottom: "8px" }}>{status.label}</p>
              <p style={{ fontSize: "24px", fontWeight: "600", color: status.color }}>{status.count}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── Agile → Intent Tab ───
function VersusTab() {
  const comparison = [
    {
      aspect: "Basic Unit",
      agile: "User Story → Story Points",
      intent: "Spec Unit → Intent Intent",
      rationale: "Intent work links every spec to the problem it solves. Not just what to build, but why.",
    },
    {
      aspect: "Hierarchy",
      agile: "Theme → Epic → Story → Task",
      intent: "Product → Feature → Capability → Spec Unit → Intent → Signal",
      rationale: "Intent adds two critical layers below: the intent that drives each capability, and the signals that surface new intents. Tighter feedback.",
    },
    {
      aspect: "Execution",
      agile: "Team pulls stories, completes sprint",
      intent: "Agents orchestrate notice→spec→execute→observe. Humans author specs and make governance calls.",
      rationale: "Work is observable and continuous, not batched into sprints. Feedback loops close in hours, not weeks.",
    },
    {
      aspect: "Observability",
      agile: "Burndown chart, velocity metric",
      intent: "Spec vs. reality delta, intent lifecycle, agent reasoning",
      rationale: "You can see not just what's done, but whether what you did matches what you said you'd do. And why.",
    },
    {
      aspect: "Feedback",
      agile: "Retrospective at sprint end",
      intent: "Observe phase after every spec execution",
      rationale: "Don't wait for the sprint to end. Validate every spec in production immediately.",
    },
    {
      aspect: "Learning",
      agile: "Stories carry implicit context",
      intent: "Signal → Intent → Spec → Contract → Observe creates a complete reasoning trail",
      rationale: "You can see the entire decision history for any piece of work. Great for onboarding. Great for auditing.",
    },
  ];

  return (
    <div style={{ padding: "24px", maxWidth: "1200px" }}>
      <div style={{ marginBottom: "32px" }}>
        <h2 style={{ fontSize: "24px", fontWeight: "600", marginBottom: "12px", color: COLORS.text }}>Agile → Intent</h2>
        <p style={{ color: COLORS.textMuted, lineHeight: "1.6" }}>
          How Intent differs from traditional Agile. Not a replacement—an evolution that brings feedback loops closer and makes work observable.
        </p>
      </div>

      <div style={{ overflowX: "auto" }}>
        <div style={{ minWidth: "100%" }}>
          {comparison.map((row, i) => (
            <div
              key={i}
              style={{
                display: "grid",
                gridTemplateColumns: "150px 1fr 1fr 1fr",
                gap: "16px",
                padding: "16px",
                borderBottom: i < comparison.length - 1 ? `1px solid ${COLORS.border}` : "none",
                alignItems: "start",
              }}
            >
              <div style={{ fontWeight: "600", color: COLORS.text, fontSize: "13px" }}>{row.aspect}</div>
              <div style={{ fontSize: "12px", color: COLORS.textMuted }}>{row.agile}</div>
              <div style={{ fontSize: "12px", color: COLORS.spec }}>{row.intent}</div>
              <div style={{ fontSize: "12px", color: COLORS.textMuted, fontStyle: "italic" }}>{row.rationale}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── Main App ───
export default function App() {
  const [activeTab, setActiveTab] = useState("ontology");

  return (
    <div
      style={{
        minHeight: "100vh",
        background: COLORS.bg,
        color: COLORS.text,
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      }}
    >
      <div
        style={{
          display: "flex",
          borderBottom: `1px solid ${COLORS.border}`,
          background: COLORS.surface,
          position: "sticky",
          top: "0",
          zIndex: "10",
        }}
      >
        <div style={{ maxWidth: "1200px", width: "100%", margin: "0 auto", display: "flex" }}>
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                flex: 1,
                padding: "16px 0",
                background: activeTab === tab.id ? "transparent" : "transparent",
                border: "none",
                color: activeTab === tab.id ? COLORS.spec : COLORS.textMuted,
                borderBottom: activeTab === tab.id ? `2px solid ${COLORS.spec}` : "none",
                cursor: "pointer",
                fontSize: "13px",
                fontWeight: "500",
                transition: "all 200ms",
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {activeTab === "ontology" && <OntologyTab />}
      {activeTab === "dimensions" && <DimensionsTab />}
      {activeTab === "flow" && <AgentFlowTab />}
      {activeTab === "dashboard" && <DashboardTab />}
      {activeTab === "versus" && <VersusTab />}
    </div>
  );
}
