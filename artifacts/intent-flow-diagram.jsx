import { useState } from "react";

const COLORS = {
  bg: "#0f172a",
  surface: "#1e293b",
  surfaceHover: "#334155",
  border: "#334155",
  text: "#f1f5f9",
  textMuted: "#94a3b8",
  textDim: "#64748b",
  notice: "#f59e0b",
  spec: "#3b82f6",
  execute: "#10b981",
  observe: "#a855f7",
  signal: "#f59e0b",
  intent: "#60a5fa",
  contract: "#10b981",
  capability: "#06b6d4",
  feature: "#8b5cf6",
  product: "#ec4899",
  danger: "#ef4444",
  // Personas
  architect: "#f59e0b",
  productLead: "#3b82f6",
  designQA: "#a855f7",
  agent: "#10b981",
};

// ─── Personas ───
const personas = [
  {
    id: "architect",
    name: "Practitioner-Architect",
    shortName: "Architect",
    color: COLORS.architect,
    icon: "△",
    description: "Senior IC who's collapsed their own workflow with AI but can't get the team's process to match.",
    primaryPhases: ["notice", "spec", "execute"],
    touchpoints: "Notices patterns in code, writes specs, drives agent execution. The hands-on builder who sees the gap between individual AI productivity and team process.",
  },
  {
    id: "productLead",
    name: "Product-Minded Leader",
    shortName: "Product Lead",
    color: COLORS.productLead,
    icon: "◇",
    description: "PM who reads Cagan, knows discovery was always the hard problem, sees AI as vindication.",
    primaryPhases: ["notice", "spec", "observe"],
    touchpoints: "Captures signals from users and stakeholders, shapes intents with hypotheses, reviews outcomes in the observe loop. The why-person.",
  },
  {
    id: "designQA",
    name: "Design-Quality Advocate",
    shortName: "Design/QA",
    color: COLORS.designQA,
    icon: "○",
    description: "Designer/QA frustrated that AI output is evaluated against ticket-level specs rather than UX-level intent.",
    primaryPhases: ["spec", "observe"],
    touchpoints: "Shapes specs to include experience contracts, reviews agent output against intent (not just code correctness). The quality guardian.",
  },
  {
    id: "agent",
    name: "AI Agent",
    shortName: "Agent",
    color: COLORS.agent,
    icon: "◆",
    description: "Bot that consumes specs, executes atomically, emits traces. Feedback is observable, not narrative.",
    primaryPhases: ["execute"],
    touchpoints: "Reads specs, executes until assertions pass, emits machine-readable traces. No opinions, just behavior.",
  },
];

// ─── Flow Scenarios ───
const flows = [
  {
    id: "happy-path",
    name: "Happy Path",
    description: "Signal → Intent → Spec → Execution → Contract verification",
    color: "#10b981",
    steps: [
      { phase: "notice", persona: "architect", action: "Notices a code pattern", output: "Signal: 'Repeated error handling logic suggests abstraction opportunity'" },
      { phase: "spec", persona: "productLead", action: "Refines signal into hypothesis", output: "Intent: 'Reduce error handling boilerplate by 40% without changing API'" },
      { phase: "spec", persona: "designQA", action: "Adds UX contract", output: "Spec: Includes experience contract + assertions" },
      { phase: "execute", persona: "agent", action: "Runs against spec", output: "Code committed, traces emitted" },
      { phase: "observe", persona: "designQA", action: "Reviews traces vs. contract", output: "✓ Contract verified → Feature" },
    ],
  },
  {
    id: "failure-feedback",
    name: "Failure Feedback Loop",
    description: "Agent output fails contract → spec clarification → retry",
    color: "#ef4444",
    steps: [
      { phase: "execute", persona: "agent", action: "Executes spec", output: "Code generated, traces emitted" },
      { phase: "observe", persona: "designQA", action: "Reviews traces, contract fails", output: "Signal: 'Agent missed error condition Y'" },
      { phase: "spec", persona: "architect", action: "Clarifies spec with assertion", output: "Updated Spec: Added assertion for condition Y" },
      { phase: "execute", persona: "agent", action: "Re-executes against updated spec", output: "Code re-generated" },
      { phase: "observe", persona: "designQA", action: "Validates new output", output: "✓ Contract verified" },
    ],
  },
  {
    id: "governance",
    name: "Governance Escalation",
    description: "Spec proposes breaking change → escalation → intent refinement",
    color: "#f59e0b",
    steps: [
      { phase: "spec", persona: "architect", action: "Proposes API redesign", output: "Spec: Breaking change to handler interface" },
      { phase: "observe", persona: "productLead", action: "Reviews impact, requests intent alignment", output: "Signal: 'Need stakeholder alignment on timing'" },
      { phase: "notice", persona: "productLead", action: "Gathers stakeholder signals", output: "Intent refined: 'Phased deprecation over 2 releases'" },
      { phase: "spec", persona: "architect", action: "Revises spec for phasing", output: "Updated Spec: Deprecation + shim period" },
      { phase: "execute", persona: "agent", action: "Executes phased approach", output: "Multi-part capability" },
    ],
  },
  {
    id: "external-signal",
    name: "External Signal Injection",
    description: "User report → signal → intent loop → execution",
    color: "#a855f7",
    steps: [
      { phase: "notice", persona: "productLead", action: "Customer reports edge case", output: "Signal: 'Timeout under load with 10k concurrent connections'" },
      { phase: "spec", persona: "productLead", action: "Translates to performance intent", output: "Intent: 'Support 10k concurrent under <100ms p99'" },
      { phase: "spec", persona: "architect", action: "Specs performance contract", output: "Spec: Load test + assertion" },
      { phase: "execute", persona: "agent", action: "Implements + runs load test", output: "Optimization committed" },
      { phase: "observe", persona: "designQA", action: "Validates contract", output: "✓ Capability verified" },
    ],
  },
  {
    id: "autonomous-pipeline",
    name: "Autonomous Pipeline",
    description: "Agents execute in parallel based on spec DAG → traces feed new intents",
    color: "#06b6d4",
    steps: [
      { phase: "spec", persona: "architect", action: "Specs 3 independent capabilities", output: "Spec 1, 2, 3: Marked as parallel-safe" },
      { phase: "execute", persona: "agent", action: "Agents run specs 1, 2, 3 in parallel", output: "3 traces emitted simultaneously" },
      { phase: "observe", persona: "agent", action: "Trace analyzer detects coupling", output: "Signal: 'Specs 1 & 2 have undeclared dependency'" },
      { phase: "spec", persona: "architect", action: "Adds dependency constraint", output: "Updated Spec: Sequencing requirement" },
      { phase: "execute", persona: "agent", action: "Re-executes with ordering", output: "All specs pass" },
    ],
  },
];

// ─── Trigger Matrix ───
const triggerMatrix = [
  {
    source: "Code review",
    triggers: ["Signal (pattern noticed)"],
    example: "'This error handling is duplicated 7 times'",
  },
  {
    source: "Customer report",
    triggers: ["Signal (edge case)"],
    example: "'Crashes with null in handler'",
  },
  {
    source: "Metrics spike",
    triggers: ["Signal (observability)"],
    example: "'Latency p99 jumped 200ms'",
  },
  {
    source: "Discovery interview",
    triggers: ["Signal (user need)", "Intent (hypothesis)"],
    example: "'Users want to batch requests'",
  },
  {
    source: "Contract failure",
    triggers: ["Signal (spec gap)"],
    example: "'Agent output didn't handle error case'",
  },
  {
    source: "Trace anomaly",
    triggers: ["Signal (automation insight)"],
    example: "'Agent spent 5s on retry logic'",
  },
];

export default function IntentFlowDiagram() {
  const [activeFlow, setActiveFlow] = useState(flows[0].id);
  const [activeTab, setActiveTab] = useState("flows");

  const currentFlow = flows.find((f) => f.id === activeFlow);

  return (
    <div
      style={{
        background: COLORS.bg,
        color: COLORS.text,
        padding: "40px 24px",
        fontFamily:
          "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        minHeight: "100vh",
      }}
    >
      <div style={{ maxWidth: "1200px", margin: "0 auto" }}>
        {/* Header */}
        <div style={{ marginBottom: "40px" }}>
          <h1
            style={{
              fontSize: "32px",
              fontWeight: 700,
              marginBottom: "8px",
            }}
          >
            Intent Flow Diagram
          </h1>
          <p style={{ color: COLORS.textMuted, fontSize: "14px" }}>
            Five concrete flows showing persona paths through the notice → spec →
            execute → observe loop
          </p>
        </div>

        {/* Tabs */}
        <div
          style={{
            display: "flex",
            gap: "8px",
            marginBottom: "32px",
            borderBottom: `1px solid ${COLORS.border}`,
            paddingBottom: "16px",
          }}
        >
          {[
            { id: "flows", label: "Flow Paths" },
            { id: "triggers", label: "Trigger Matrix" },
            { id: "personas", label: "Persona Map" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                background: "none",
                border: "none",
                color:
                  activeTab === tab.id ? COLORS.text : COLORS.textMuted,
                fontSize: "14px",
                fontWeight: activeTab === tab.id ? 600 : 400,
                cursor: "pointer",
                paddingBottom: "8px",
                borderBottom:
                  activeTab === tab.id
                    ? `2px solid ${COLORS.spec}`
                    : "none",
                transition: "all 0.2s",
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Flows Tab */}
        {activeTab === "flows" && (
          <div>
            {/* Flow Selector */}
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
                gap: "12px",
                marginBottom: "32px",
              }}
            >
              {flows.map((flow) => (
                <button
                  key={flow.id}
                  onClick={() => setActiveFlow(flow.id)}
                  style={{
                    background:
                      activeFlow === flow.id
                        ? COLORS.surface
                        : "transparent",
                    border: `1px solid ${activeFlow === flow.id ? flow.color : COLORS.border}`,
                    color: COLORS.text,
                    padding: "16px",
                    borderRadius: "8px",
                    cursor: "pointer",
                    fontSize: "13px",
                    fontWeight: activeFlow === flow.id ? 600 : 400,
                    transition: "all 0.2s",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "8px",
                      marginBottom: "4px",
                    }}
                  >
                    <div
                      style={{
                        width: "8px",
                        height: "8px",
                        borderRadius: "2px",
                        background: flow.color,
                      }}
                    />
                    <span style={{ fontWeight: 600 }}>{flow.name}</span>
                  </div>
                  <p style={{ color: COLORS.textMuted, fontSize: "11px" }}>
                    {flow.description}
                  </p>
                </button>
              ))}
            </div>

            {/* Flow Steps */}
            {currentFlow && (
              <div
                style={{
                  background: COLORS.surface,
                  border: `1px solid ${COLORS.border}`,
                  borderRadius: "12px",
                  padding: "32px",
                }}
              >
                <h2
                  style={{
                    fontSize: "18px",
                    fontWeight: 600,
                    marginBottom: "24px",
                    color: currentFlow.color,
                  }}
                >
                  {currentFlow.name}
                </h2>

                <div style={{ display: "flex", flexDirection: "column" }}>
                  {currentFlow.steps.map((step, idx) => (
                    <div key={idx}>
                      <div
                        style={{
                          display: "grid",
                          gridTemplateColumns: "120px 1fr",
                          gap: "24px",
                          marginBottom: "16px",
                          paddingLeft: "8px",
                        }}
                      >
                        <div>
                          <div
                            style={{
                              display: "inline-block",
                              background: COLORS.bg,
                              border: `2px solid ${(() => {
                                switch (step.phase) {
                                  case "notice":
                                    return COLORS.notice;
                                  case "spec":
                                    return COLORS.spec;
                                  case "execute":
                                    return COLORS.execute;
                                  case "observe":
                                    return COLORS.observe;
                                  default:
                                    return COLORS.border;
                                }
                              })()}`,
                              color: (() => {
                                switch (step.phase) {
                                  case "notice":
                                    return COLORS.notice;
                                  case "spec":
                                    return COLORS.spec;
                                  case "execute":
                                    return COLORS.execute;
                                  case "observe":
                                    return COLORS.observe;
                                  default:
                                    return COLORS.border;
                                }
                              })(),
                              padding: "6px 12px",
                              borderRadius: "4px",
                              fontSize: "11px",
                              fontWeight: 600,
                              textTransform: "uppercase",
                            }}
                          >
                            {step.phase}
                          </div>
                        </div>
                        <div>
                          <div
                            style={{
                              fontSize: "13px",
                              marginBottom: "8px",
                            }}
                          >
                            <strong>{step.persona}:</strong> {step.action}
                          </div>
                          <div
                            style={{
                              background: COLORS.bg,
                              padding: "12px",
                              borderRadius: "6px",
                              fontSize: "12px",
                              color: COLORS.textMuted,
                              fontFamily: "'Monaco', monospace",
                            }}
                          >
                            → {step.output}
                          </div>
                        </div>
                      </div>
                      {idx < currentFlow.steps.length - 1 && (
                        <div
                          style={{
                            height: "24px",
                            display: "flex",
                            alignItems: "center",
                            paddingLeft: "8px",
                            marginBottom: "8px",
                          }}
                        >
                          <div
                            style={{
                              width: "2px",
                              height: "100%",
                              background: COLORS.border,
                            }}
                          />
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Trigger Matrix Tab */}
        {activeTab === "triggers" && (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
              gap: "16px",
            }}
          >
            {triggerMatrix.map((row, idx) => (
              <div
                key={idx}
                style={{
                  background: COLORS.surface,
                  border: `1px solid ${COLORS.border}`,
                  borderRadius: "8px",
                  padding: "16px",
                }}
              >
                <h3 style={{ fontSize: "13px", fontWeight: 600, marginBottom: "8px" }}>
                  {row.source}
                </h3>
                <div style={{ marginBottom: "12px" }}>
                  {row.triggers.map((t, tIdx) => (
                    <div
                      key={tIdx}
                      style={{
                        display: "inline-block",
                        background: COLORS.bg,
                        padding: "4px 8px",
                        borderRadius: "4px",
                        fontSize: "11px",
                        marginRight: "6px",
                        marginBottom: "4px",
                        color: COLORS.intent,
                        border: `1px solid ${COLORS.intent}`,
                      }}
                    >
                      {t}
                    </div>
                  ))}
                </div>
                <div
                  style={{
                    fontSize: "12px",
                    color: COLORS.textMuted,
                    fontStyle: "italic",
                  }}
                >
                  "{row.example}"
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Personas Tab */}
        {activeTab === "personas" && (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
              gap: "16px",
            }}
          >
            {personas.map((p) => (
              <div
                key={p.id}
                style={{
                  background: COLORS.surface,
                  border: `1px solid ${COLORS.border}`,
                  borderRadius: "8px",
                  padding: "16px",
                }}
              >
                <div style={{ marginBottom: "12px" }}>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "12px",
                      marginBottom: "8px",
                    }}
                  >
                    <div
                      style={{
                        width: "32px",
                        height: "32px",
                        borderRadius: "4px",
                        background: p.color,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: "16px",
                        color: COLORS.bg,
                        fontWeight: 700,
                      }}
                    >
                      {p.icon}
                    </div>
                    <div>
                      <h3
                        style={{
                          fontSize: "14px",
                          fontWeight: 600,
                          color: COLORS.text,
                        }}
                      >
                        {p.name}
                      </h3>
                      <p style={{ fontSize: "11px", color: COLORS.textMuted }}>
                        {p.shortName}
                      </p>
                    </div>
                  </div>
                  <p style={{ fontSize: "12px", color: COLORS.textMuted }}>
                    {p.description}
                  </p>
                </div>

                <div style={{ marginBottom: "12px" }}>
                  <p style={{ fontSize: "11px", fontWeight: 600, marginBottom: "6px" }}>
                    Primary Phases:
                  </p>
                  <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
                    {p.primaryPhases.map((phase) => (
                      <div
                        key={phase}
                        style={{
                          display: "inline-block",
                          background: COLORS.bg,
                          padding: "4px 8px",
                          borderRadius: "4px",
                          fontSize: "10px",
                          fontWeight: 500,
                          textTransform: "capitalize",
                          color: (() => {
                            switch (phase) {
                              case "notice":
                                return COLORS.notice;
                              case "spec":
                                return COLORS.spec;
                              case "execute":
                                return COLORS.execute;
                              case "observe":
                                return COLORS.observe;
                              default:
                                return COLORS.textMuted;
                            }
                          })(),
                        }}
                      >
                        {phase}
                      </div>
                    ))}
                  </div>
                </div>

                <p style={{ fontSize: "12px", color: COLORS.textMuted, lineHeight: "1.5" }}>
                  {p.touchpoints}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
