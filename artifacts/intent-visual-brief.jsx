import { useState } from "react";
import {
  ChevronRight,
  ChevronDown,
  Eye,
  FileText,
  Zap,
  BarChart3,
  AlertTriangle,
  Users,
  Layers,
  Target,
  ArrowRight,
  ArrowDown,
  Clock,
  XCircle,
  CheckCircle2,
  Lightbulb,
  Compass,
  Rocket,
  Wrench,
  MessageSquare,
  GitBranch,
  Brain,
  Activity,
  CircleDot,
} from "lucide-react";

/* ─── palette ─── */
const C = {
  bg: "#0f1117",
  surface: "#181b24",
  surfaceAlt: "#1e2230",
  border: "#2a2f3e",
  borderHover: "#3d4560",
  text: "#e4e6ed",
  textMuted: "#8b90a0",
  accent: "#3b82f6",
  accentDim: "#1e3a5f",
  notice: "#f59e0b",
  noticeDim: "#3d2e0a",
  spec: "#8b5cf6",
  specDim: "#2d1f5e",
  execute: "#10b981",
  executeDim: "#0a3d2e",
  observe: "#ef4444",
  observeDim: "#3d1414",
  warn: "#f97316",
};

/* ─── section nav ─── */
const sections = [
  { id: "problem", label: "The Problem", icon: AlertTriangle },
  { id: "loop", label: "The Loop", icon: Activity },
  { id: "stack", label: "The Stack", icon: Layers },
  { id: "audience", label: "Audience", icon: Users },
  { id: "gtm", label: "Go-to-Market", icon: Rocket },
  { id: "hypotheses", label: "Hypotheses", icon: Target },
  { id: "landscape", label: "Landscape", icon: Compass },
];

/* ─── reusable card ─── */
function Card({ children, style, onClick, hover }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background: C.surface,
        border: `1px solid ${hovered && hover ? C.borderHover : C.border}`,
        borderRadius: 8,
        padding: 20,
        transition: "all 0.2s ease",
        cursor: onClick ? "pointer" : "default",
        transform: hovered && hover ? "translateY(-2px)" : "none",
        ...style,
      }}
    >
      {children}
    </div>
  );
}

/* ─── badge ─── */
function Badge({ children, color }) {
  return (
    <span
      style={{
        display: "inline-block",
        fontSize: 11,
        fontWeight: 600,
        textTransform: "uppercase",
        letterSpacing: "0.05em",
        padding: "3px 8px",
        borderRadius: 4,
        color: color,
        background: color + "18",
        border: `1px solid ${color}40`,
      }}
    >
      {children}
    </span>
  );
}

/* ═══════════════════════════════════════════
   SECTION: THE PROBLEM
   ═══════════════════════════════════════════ */
function ProblemSection() {
  const [expanded, setExpanded] = useState(null);

  const cascade = [
    {
      id: "assumption",
      icon: Zap,
      color: C.accent,
      title: "The Detonated Assumption",
      subtitle: "AI collapses implementation from weeks to hours",
      detail:
        "Agile was built on the premise that delivery is slow and uncertain. When a well-specified feature can be implemented in hours by an AI agent, that premise collapses — and every ceremony built on it becomes overhead.",
    },
    {
      id: "ceremony",
      icon: Clock,
      color: C.notice,
      title: "The Ceremony Tax",
      subtitle: "Sprint cycles impose artificial boundaries on hours-long work",
      detail:
        "Planning meetings estimate work that doesn't need estimating. Standups report on work already done. Retros examine a process that was never the bottleneck. The cadence designed for 2-week cycles now wraps around 2-hour cycles.",
    },
    {
      id: "spec",
      icon: FileText,
      color: C.spec,
      title: "The Specification Gap",
      subtitle: 'Tickets designed for "enough to start a conversation" fail AI agents',
      detail:
        "Jira tickets were coordination artifacts between humans who fill gaps with hallway conversations. AI agents can't do that. They need Intent (why), Shape (what good looks like), and Contract (boundaries). Most teams feed agents ticket-quality specs and get ticket-quality output.",
    },
    {
      id: "silo",
      icon: XCircle,
      color: C.observe,
      title: "The Silo Persistence",
      subtitle: "Sequential handoffs in a world where agents don't respect role boundaries",
      detail:
        "Product → Design → Engineering → QA was already problematic. With AI generating code, tests, and design tokens simultaneously, sequential handoffs become absurd. But the team's operating model still forces them.",
    },
    {
      id: "void",
      icon: Eye,
      color: C.textMuted,
      title: "The Observability Void",
      subtitle: "Agent reasoning trapped in sessions that close and vanish",
      detail:
        "When humans wrote the code, you could read the PR to understand reasoning. When an agent writes 80%, the reasoning dies with the prompt window. Teams lose the ability to understand why decisions were made.",
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 32 }}>
        <h2
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: C.text,
            margin: 0,
            lineHeight: 1.2,
          }}
        >
          The bottleneck moved upstream.
          <br />
          <span style={{ color: C.textMuted, fontWeight: 400 }}>
            The operating model didn't follow.
          </span>
        </h2>
      </div>

      {/* cascade flow */}
      <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
        {cascade.map((item, i) => {
          const Icon = item.icon;
          const isExpanded = expanded === item.id;
          return (
            <div key={item.id}>
              <Card
                hover
                onClick={() =>
                  setExpanded(isExpanded ? null : item.id)
                }
                style={{
                  borderLeft: `3px solid ${item.color}`,
                  paddingLeft: 20,
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "flex-start",
                    gap: 14,
                  }}
                >
                  <div
                    style={{
                      marginTop: 2,
                      width: 36,
                      height: 36,
                      borderRadius: 8,
                      background: item.color + "15",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      flexShrink: 0,
                    }}
                  >
                    <Icon size={18} color={item.color} />
                  </div>
                  <div style={{ flex: 1 }}>
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                      }}
                    >
                      <div
                        style={{
                          fontSize: 15,
                          fontWeight: 600,
                          color: C.text,
                        }}
                      >
                        {item.title}
                      </div>
                      {isExpanded ? (
                        <ChevronDown size={16} color={C.textMuted} />
                      ) : (
                        <ChevronRight size={16} color={C.textMuted} />
                      )}
                    </div>
                    <div
                      style={{
                        fontSize: 13,
                        color: C.textMuted,
                        marginTop: 2,
                      }}
                    >
                      {item.subtitle}
                    </div>
                    {isExpanded && (
                      <div
                        style={{
                          fontSize: 14,
                          color: C.text,
                          marginTop: 12,
                          lineHeight: 1.6,
                          opacity: 0.85,
                          borderTop: `1px solid ${C.border}`,
                          paddingTop: 12,
                        }}
                      >
                        {item.detail}
                      </div>
                    )}
                  </div>
                </div>
              </Card>
              {i < cascade.length - 1 && (
                <div
                  style={{
                    display: "flex",
                    justifyContent: "center",
                    padding: "4px 0",
                  }}
                >
                  <ArrowDown size={16} color={C.border} />
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* root cause callout */}
      <div
        style={{
          marginTop: 28,
          padding: "16px 20px",
          background: C.warn + "0a",
          border: `1px solid ${C.warn}30`,
          borderRadius: 8,
        }}
      >
        <div
          style={{
            fontSize: 12,
            fontWeight: 700,
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            color: C.warn,
            marginBottom: 6,
          }}
        >
          Root cause
        </div>
        <div style={{ fontSize: 14, color: C.text, lineHeight: 1.6 }}>
          The industry bolts AI onto the existing Agile model — "AI-augmented
          Scrum" — rather than questioning whether the model itself still fits.
          Motor on a horse-drawn carriage.
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   SECTION: THE LOOP
   ═══════════════════════════════════════════ */
function LoopSection() {
  const [active, setActive] = useState("notice");

  const phases = [
    {
      id: "notice",
      label: "Notice",
      color: C.notice,
      dim: C.noticeDim,
      icon: Eye,
      replaces: "Backlog grooming",
      becomes: "Living signal stream",
      who: "Anyone on the team",
      desc: "Continuous discovery. The team is always sensing: user feedback, system signals, market shifts, agent-surfaced patterns. Anyone can raise a signal. No grooming meetings — a living stream of things worth paying attention to.",
    },
    {
      id: "spec",
      label: "Spec",
      color: C.spec,
      dim: C.specDim,
      icon: FileText,
      replaces: "Sprint planning + ticket writing",
      becomes: "Collaborative shaping",
      who: "Product + Design + Engineering + Quality",
      desc: "When a signal warrants action, the full team shapes it into a three-part specification: Intent (why), Shape (what good looks like), Contract (boundaries and acceptance criteria). This is the team's highest-leverage activity.",
    },
    {
      id: "execute",
      label: "Execute",
      color: C.execute,
      dim: C.executeDim,
      icon: Zap,
      replaces: "Sprint execution",
      becomes: "Agent-augmented implementation",
      who: "Humans + AI agents",
      desc: "With a well-shaped spec, execution involves any combination of human and AI work. The spec is source of truth. Agents implement, test, and validate against the contract. Humans steer and handle judgment calls. Observability captures agent reasoning.",
    },
    {
      id: "observe",
      label: "Observe",
      color: C.observe,
      dim: C.observeDim,
      icon: BarChart3,
      replaces: "Sprint review + retrospective",
      becomes: "Continuous verification",
      who: "The team + the system",
      desc: "Watch the outcome through real signals, not ceremonies. Did user behavior change? Did the metric move? Did agent reasoning reveal a misunderstanding in the spec? Observations feed directly back into Notice.",
    },
  ];

  const activePhase = phases.find((p) => p.id === active);

  return (
    <div>
      <div style={{ marginBottom: 32 }}>
        <h2
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: C.text,
            margin: 0,
            lineHeight: 1.2,
          }}
        >
          The Core Loop
          <br />
          <span style={{ color: C.textMuted, fontWeight: 400 }}>
            No sprint boundaries. Continuous flow.
          </span>
        </h2>
      </div>

      {/* loop visual */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: 0,
          alignItems: "center",
          marginBottom: 32,
          flexWrap: "wrap",
        }}
      >
        {phases.map((phase, i) => {
          const Icon = phase.icon;
          const isActive = active === phase.id;
          return (
            <div
              key={phase.id}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 0,
              }}
            >
              <div
                onClick={() => setActive(phase.id)}
                style={{
                  cursor: "pointer",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 8,
                  padding: "16px 20px",
                  borderRadius: 10,
                  border: `2px solid ${isActive ? phase.color : "transparent"}`,
                  background: isActive ? phase.dim : "transparent",
                  transition: "all 0.2s ease",
                  minWidth: 100,
                }}
              >
                <div
                  style={{
                    width: 48,
                    height: 48,
                    borderRadius: 12,
                    background: phase.color + (isActive ? "30" : "15"),
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <Icon size={22} color={phase.color} />
                </div>
                <div
                  style={{
                    fontSize: 14,
                    fontWeight: 700,
                    color: isActive ? phase.color : C.textMuted,
                    textTransform: "uppercase",
                    letterSpacing: "0.06em",
                  }}
                >
                  {phase.label}
                </div>
              </div>
              {i < phases.length - 1 && (
                <ArrowRight
                  size={18}
                  color={C.border}
                  style={{ margin: "0 4px", flexShrink: 0 }}
                />
              )}
            </div>
          );
        })}
        {/* return arrow indicator */}
        <div
          style={{
            width: "100%",
            display: "flex",
            justifyContent: "center",
            marginTop: 4,
          }}
        >
          <div
            style={{
              fontSize: 11,
              color: C.textMuted,
              fontStyle: "italic",
              display: "flex",
              alignItems: "center",
              gap: 6,
            }}
          >
            <span style={{ color: C.observe }}>Observe</span>
            <span>feeds back into</span>
            <span style={{ color: C.notice }}>Notice</span>
            <span style={{ fontSize: 16, color: C.border }}>↩</span>
          </div>
        </div>
      </div>

      {/* detail panel */}
      {activePhase && (
        <Card
          style={{
            borderTop: `3px solid ${activePhase.color}`,
          }}
        >
          <div style={{ marginBottom: 16 }}>
            <div
              style={{
                fontSize: 18,
                fontWeight: 700,
                color: activePhase.color,
              }}
            >
              {activePhase.label}
            </div>
          </div>

          <div style={{ fontSize: 14, color: C.text, lineHeight: 1.65, marginBottom: 20 }}>
            {activePhase.desc}
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: 12,
            }}
          >
            <div
              style={{
                padding: 12,
                background: C.surfaceAlt,
                borderRadius: 6,
              }}
            >
              <div
                style={{
                  fontSize: 10,
                  fontWeight: 700,
                  textTransform: "uppercase",
                  color: C.observe,
                  marginBottom: 4,
                  letterSpacing: "0.08em",
                }}
              >
                Replaces
              </div>
              <div style={{ fontSize: 13, color: C.textMuted }}>
                {activePhase.replaces}
              </div>
            </div>
            <div
              style={{
                padding: 12,
                background: C.surfaceAlt,
                borderRadius: 6,
              }}
            >
              <div
                style={{
                  fontSize: 10,
                  fontWeight: 700,
                  textTransform: "uppercase",
                  color: C.execute,
                  marginBottom: 4,
                  letterSpacing: "0.08em",
                }}
              >
                Becomes
              </div>
              <div style={{ fontSize: 13, color: C.text }}>
                {activePhase.becomes}
              </div>
            </div>
            <div
              style={{
                padding: 12,
                background: C.surfaceAlt,
                borderRadius: 6,
              }}
            >
              <div
                style={{
                  fontSize: 10,
                  fontWeight: 700,
                  textTransform: "uppercase",
                  color: C.accent,
                  marginBottom: 4,
                  letterSpacing: "0.08em",
                }}
              >
                Who
              </div>
              <div style={{ fontSize: 13, color: C.text }}>
                {activePhase.who}
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* spec anatomy */}
      <div style={{ marginTop: 28 }}>
        <div
          style={{
            fontSize: 12,
            fontWeight: 700,
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            color: C.spec,
            marginBottom: 12,
          }}
        >
          The Spec Artifact — three parts
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
          {[
            {
              title: "Intent",
              q: "Why are we doing this?",
              desc: "Outcome sought, problem being solved, who benefits",
            },
            {
              title: "Shape",
              q: "What does good look like?",
              desc: "Constraints, boundaries, key interactions, design principles",
            },
            {
              title: "Contract",
              q: "How do we know it's done?",
              desc: "Acceptance criteria, what must not break, validation rules",
            },
          ].map((part) => (
            <Card key={part.title} style={{ background: C.specDim + "60" }}>
              <div
                style={{ fontSize: 16, fontWeight: 700, color: C.spec }}
              >
                {part.title}
              </div>
              <div
                style={{
                  fontSize: 13,
                  color: C.text,
                  fontStyle: "italic",
                  marginTop: 4,
                }}
              >
                {part.q}
              </div>
              <div
                style={{
                  fontSize: 12,
                  color: C.textMuted,
                  marginTop: 8,
                  lineHeight: 1.5,
                }}
              >
                {part.desc}
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   SECTION: THE STACK
   ═══════════════════════════════════════════ */
function StackSection() {
  return (
    <div>
      <div style={{ marginBottom: 32 }}>
        <h2
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: C.text,
            margin: 0,
            lineHeight: 1.2,
          }}
        >
          The Missing Layer
          <br />
          <span style={{ color: C.textMuted, fontWeight: 400 }}>
            Everyone's solving the bottom. Nobody's solving the top.
          </span>
        </h2>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 3 }}>
        {/* top layer — Intent */}
        <div
          style={{
            background: `linear-gradient(135deg, ${C.accent}20, ${C.spec}15)`,
            border: `2px solid ${C.accent}60`,
            borderRadius: "10px 10px 4px 4px",
            padding: 24,
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "flex-start",
            }}
          >
            <div>
              <Badge color={C.accent}>INTENT</Badge>
              <div
                style={{
                  fontSize: 18,
                  fontWeight: 700,
                  color: C.text,
                  marginTop: 8,
                }}
              >
                Team Operating Model
              </div>
              <div
                style={{
                  fontSize: 14,
                  color: C.textMuted,
                  marginTop: 4,
                  lineHeight: 1.5,
                }}
              >
                How the team flows, decides, and learns together.
                <br />
                Product + Design + Engineering + Quality as one unit.
              </div>
            </div>
            <div
              style={{
                background: C.accent + "25",
                borderRadius: 8,
                padding: "8px 14px",
                fontSize: 12,
                fontWeight: 600,
                color: C.accent,
                whiteSpace: "nowrap",
              }}
            >
              THIS CONCEPT
            </div>
          </div>
        </div>

        {/* middle layer — SDD */}
        <div
          style={{
            background: C.surface,
            border: `1px solid ${C.border}`,
            borderRadius: 4,
            padding: 20,
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "flex-start",
            }}
          >
            <div>
              <Badge color={C.spec}>Spec-Driven Development</Badge>
              <div
                style={{
                  fontSize: 16,
                  fontWeight: 600,
                  color: C.text,
                  marginTop: 8,
                }}
              >
                How specs become code via AI agents
              </div>
              <div
                style={{
                  fontSize: 13,
                  color: C.textMuted,
                  marginTop: 4,
                }}
              >
                The engineering execution layer
              </div>
            </div>
            <div
              style={{
                display: "flex",
                gap: 8,
                flexWrap: "wrap",
                justifyContent: "flex-end",
              }}
            >
              {["GitHub Spec Kit", "Kiro", "Tessl"].map((t) => (
                <span
                  key={t}
                  style={{
                    fontSize: 11,
                    color: C.textMuted,
                    padding: "3px 8px",
                    background: C.surfaceAlt,
                    borderRadius: 4,
                  }}
                >
                  {t}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* bottom layer — assistants */}
        <div
          style={{
            background: C.surface,
            border: `1px solid ${C.border}`,
            borderRadius: "4px 4px 10px 10px",
            padding: 20,
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "flex-start",
            }}
          >
            <div>
              <Badge color={C.execute}>AI Coding Assistants</Badge>
              <div
                style={{
                  fontSize: 16,
                  fontWeight: 600,
                  color: C.text,
                  marginTop: 8,
                }}
              >
                How individual developers get AI help
              </div>
              <div
                style={{
                  fontSize: 13,
                  color: C.textMuted,
                  marginTop: 4,
                }}
              >
                The individual productivity layer
              </div>
            </div>
            <div
              style={{
                display: "flex",
                gap: 8,
                flexWrap: "wrap",
                justifyContent: "flex-end",
              }}
            >
              {["Copilot", "Claude Code", "Cursor"].map((t) => (
                <span
                  key={t}
                  style={{
                    fontSize: 11,
                    color: C.textMuted,
                    padding: "3px 8px",
                    background: C.surfaceAlt,
                    borderRadius: 4,
                  }}
                >
                  {t}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* intersection diagram */}
      <div style={{ marginTop: 32 }}>
        <div
          style={{
            fontSize: 12,
            fontWeight: 700,
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            color: C.textMuted,
            marginBottom: 14,
          }}
        >
          Intent occupies the intersection of
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
          {[
            {
              label: "Product Thinking",
              sub: "the why",
              names: "Cagan, Torres, Patton",
              color: C.notice,
            },
            {
              label: "Spec-Driven Dev",
              sub: "the how",
              names: "Spec Kit, Kiro, Tessl",
              color: C.spec,
            },
            {
              label: "Agent Observability",
              sub: "the memory",
              names: "Entire.io",
              color: C.execute,
            },
          ].map((item) => (
            <Card key={item.label}>
              <div
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: item.color,
                  marginBottom: 10,
                }}
              />
              <div
                style={{
                  fontSize: 15,
                  fontWeight: 600,
                  color: C.text,
                }}
              >
                {item.label}
              </div>
              <div
                style={{
                  fontSize: 12,
                  color: item.color,
                  fontStyle: "italic",
                  marginTop: 2,
                }}
              >
                {item.sub}
              </div>
              <div
                style={{
                  fontSize: 11,
                  color: C.textMuted,
                  marginTop: 8,
                }}
              >
                {item.names}
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   SECTION: AUDIENCE
   ═══════════════════════════════════════════ */
function AudienceSection() {
  const [selectedPersona, setSelectedPersona] = useState(0);

  const personas = [
    {
      role: "Practitioner-Architect",
      color: C.accent,
      icon: GitBranch,
      title: "Senior IC / Tech Lead",
      signal: "Has already collapsed their own workflow with AI",
      pain: "Can't get their team's process to match their personal velocity",
      motivation:
        "They're the early adopter who drags the team forward. They see the mismatch every day — they ship in hours, but the team plans in weeks.",
      reads: "Claude Code docs, Hacker News, Shape Up",
    },
    {
      role: "Product-Minded Leader",
      color: C.notice,
      icon: Brain,
      title: "PM / Product Lead",
      signal: "Reads Cagan, follows Torres on continuous discovery",
      pain: "Knows the bottleneck was always discovery — not delivery",
      motivation:
        "Sees AI as vindication of what they've argued for years: the team should spend 80% of its energy understanding the problem. Now delivery speed proves them right.",
      reads: "SVPG, Empowered, Continuous Discovery Habits",
    },
    {
      role: "Design-Quality Advocate",
      color: C.spec,
      icon: Target,
      title: "Designer / QA Lead",
      signal: "Frustrated that AI output is evaluated against ticket-level specs",
      pain: "Wants specs to encode why this matters to the user, not just what to build",
      motivation:
        "The spec should carry user-experience-level intent. When specs are shallow, AI produces technically correct but experientially wrong output.",
      reads: "Jobs to Be Done, Intercom on Product, Nielsen Norman",
    },
  ];

  const p = personas[selectedPersona];
  const Icon = p.icon;

  return (
    <div>
      <div style={{ marginBottom: 32 }}>
        <h2
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: C.text,
            margin: 0,
            lineHeight: 1.2,
          }}
        >
          Small cross-functional teams
          <br />
          <span style={{ color: C.textMuted, fontWeight: 400 }}>
            3–5 people. Product + Design + Engineering + Quality.
          </span>
        </h2>
      </div>

      {/* team traits */}
      <Card style={{ marginBottom: 24 }}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 16,
          }}
        >
          {[
            {
              trait: "Already felt the pull",
              desc: "At least one member heavily using AI agents — the rest feel the process is out of sync",
            },
            {
              trait: "Value flow over ceremony",
              desc: "Would rather ship a well-understood feature in a day than plan it for two weeks",
            },
            {
              trait: "Want collective ownership",
              desc: "Everyone contributes to the shape, with AI agents as participants — not tools one role uses",
            },
            {
              trait: "Demand higher signal",
              desc: "Specs that connect the why to the work so deeply that any participant can decide locally",
            },
          ].map((item) => (
            <div
              key={item.trait}
              style={{
                padding: 14,
                background: C.surfaceAlt,
                borderRadius: 6,
              }}
            >
              <div
                style={{
                  fontSize: 14,
                  fontWeight: 600,
                  color: C.text,
                  marginBottom: 4,
                }}
              >
                {item.trait}
              </div>
              <div
                style={{
                  fontSize: 12,
                  color: C.textMuted,
                  lineHeight: 1.5,
                }}
              >
                {item.desc}
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* persona tabs */}
      <div style={{ display: "flex", gap: 6, marginBottom: 3 }}>
        {personas.map((per, i) => (
          <button
            key={per.role}
            onClick={() => setSelectedPersona(i)}
            style={{
              flex: 1,
              padding: "10px 12px",
              background:
                selectedPersona === i ? per.color + "20" : C.surface,
              border: `1px solid ${
                selectedPersona === i ? per.color + "60" : C.border
              }`,
              borderBottom:
                selectedPersona === i
                  ? `2px solid ${per.color}`
                  : "1px solid transparent",
              borderRadius: "8px 8px 0 0",
              cursor: "pointer",
              color:
                selectedPersona === i ? per.color : C.textMuted,
              fontSize: 13,
              fontWeight: 600,
            }}
          >
            {per.role}
          </button>
        ))}
      </div>

      {/* persona detail */}
      <Card
        style={{
          borderRadius: "0 0 8px 8px",
          borderTop: `2px solid ${p.color}`,
        }}
      >
        <div
          style={{
            display: "flex",
            gap: 16,
            alignItems: "flex-start",
          }}
        >
          <div
            style={{
              width: 48,
              height: 48,
              borderRadius: 10,
              background: p.color + "20",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              flexShrink: 0,
            }}
          >
            <Icon size={22} color={p.color} />
          </div>
          <div style={{ flex: 1 }}>
            <div
              style={{
                fontSize: 17,
                fontWeight: 700,
                color: C.text,
              }}
            >
              {p.title}
            </div>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: 12,
                marginTop: 14,
              }}
            >
              <div>
                <div
                  style={{
                    fontSize: 10,
                    fontWeight: 700,
                    textTransform: "uppercase",
                    color: C.execute,
                    marginBottom: 3,
                    letterSpacing: "0.06em",
                  }}
                >
                  Buying signal
                </div>
                <div
                  style={{
                    fontSize: 13,
                    color: C.text,
                    lineHeight: 1.5,
                  }}
                >
                  {p.signal}
                </div>
              </div>
              <div>
                <div
                  style={{
                    fontSize: 10,
                    fontWeight: 700,
                    textTransform: "uppercase",
                    color: C.observe,
                    marginBottom: 3,
                    letterSpacing: "0.06em",
                  }}
                >
                  Core pain
                </div>
                <div
                  style={{
                    fontSize: 13,
                    color: C.text,
                    lineHeight: 1.5,
                  }}
                >
                  {p.pain}
                </div>
              </div>
            </div>
            <div style={{ marginTop: 14 }}>
              <div
                style={{
                  fontSize: 13,
                  color: C.textMuted,
                  lineHeight: 1.6,
                }}
              >
                {p.motivation}
              </div>
            </div>
            <div
              style={{
                marginTop: 12,
                fontSize: 11,
                color: C.textMuted,
              }}
            >
              <span style={{ fontWeight: 600 }}>Reads: </span>
              {p.reads}
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}

/* ═══════════════════════════════════════════
   SECTION: GO-TO-MARKET
   ═══════════════════════════════════════════ */
function GTMSection() {
  const phases = [
    {
      num: 1,
      title: "Thought Leadership",
      timeline: "Months 1–6",
      color: C.notice,
      product: "Brien's expertise, packaged",
      items: [
        "Intent Manifesto — sharp, opinionated, shareable",
        "Case studies — Brien's workflow + Ari's team",
        "Content engine — blog, podcasts, talks",
        "Practitioner community — curated experiments",
      ],
      metric: "500+ practitioners engaged · 10+ teams experimenting",
      icon: MessageSquare,
    },
    {
      num: 2,
      title: "Methodology Product",
      timeline: "Months 6–12",
      color: C.spec,
      product: "Teachable, adoptable artifacts",
      items: [
        "Intent Playbook — practical guide + templates",
        "Assessment tool — ceremony-to-flow spectrum",
        "Paid workshops and coaching",
      ],
      metric: "5+ paying clients · NPS from practitioners",
      icon: Wrench,
    },
    {
      num: 3,
      title: "Tooling Product",
      timeline: "Months 12–24 (conditional)",
      color: C.execute,
      product: "Software if methodology validates",
      items: [
        "Intent Hub — lightweight loop support layer",
        "Agent Context Bridge — connect why to work",
      ],
      metric: "Paying teams · Measurable spec quality improvement",
      icon: Layers,
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 32 }}>
        <h2
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: C.text,
            margin: 0,
            lineHeight: 1.2,
          }}
        >
          Staged Evolution
          <br />
          <span style={{ color: C.textMuted, fontWeight: 400 }}>
            Thought leadership → methodology → tooling
          </span>
        </h2>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 3 }}>
        {phases.map((phase, i) => {
          const Icon = phase.icon;
          return (
            <div key={phase.num}>
              <Card>
                <div
                  style={{
                    display: "flex",
                    gap: 16,
                    alignItems: "flex-start",
                  }}
                >
                  <div
                    style={{
                      width: 44,
                      height: 44,
                      borderRadius: 10,
                      background: phase.color + "18",
                      border: `1px solid ${phase.color}40`,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      flexShrink: 0,
                    }}
                  >
                    <Icon size={20} color={phase.color} />
                  </div>
                  <div style={{ flex: 1 }}>
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        marginBottom: 4,
                      }}
                    >
                      <div
                        style={{
                          fontSize: 16,
                          fontWeight: 700,
                          color: C.text,
                        }}
                      >
                        Phase {phase.num}: {phase.title}
                      </div>
                      <span
                        style={{
                          fontSize: 12,
                          color: phase.color,
                          fontWeight: 600,
                        }}
                      >
                        {phase.timeline}
                      </span>
                    </div>
                    <div
                      style={{
                        fontSize: 13,
                        color: C.textMuted,
                        fontStyle: "italic",
                        marginBottom: 12,
                      }}
                    >
                      {phase.product}
                    </div>
                    <div
                      style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: 6,
                      }}
                    >
                      {phase.items.map((item) => (
                        <div
                          key={item}
                          style={{
                            display: "flex",
                            gap: 8,
                            alignItems: "flex-start",
                          }}
                        >
                          <CircleDot
                            size={10}
                            color={phase.color}
                            style={{ marginTop: 4, flexShrink: 0 }}
                          />
                          <span
                            style={{
                              fontSize: 13,
                              color: C.text,
                              lineHeight: 1.4,
                            }}
                          >
                            {item}
                          </span>
                        </div>
                      ))}
                    </div>
                    <div
                      style={{
                        marginTop: 14,
                        padding: "8px 12px",
                        background: C.surfaceAlt,
                        borderRadius: 6,
                        fontSize: 12,
                        color: C.textMuted,
                      }}
                    >
                      <span
                        style={{
                          fontWeight: 700,
                          color: phase.color,
                          marginRight: 6,
                        }}
                      >
                        Signal:
                      </span>
                      {phase.metric}
                    </div>
                  </div>
                </div>
              </Card>
              {i < phases.length - 1 && (
                <div
                  style={{
                    display: "flex",
                    justifyContent: "center",
                    padding: "4px 0",
                  }}
                >
                  <ArrowDown size={16} color={C.border} />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   SECTION: HYPOTHESES
   ═══════════════════════════════════════════ */
function HypothesesSection() {
  const [expanded, setExpanded] = useState(null);

  const hypotheses = [
    {
      id: "H1",
      title: "The Problem Is Real and Felt",
      claim: "Small product teams using AI agents are experiencing the ceremony/process mismatch and actively looking for alternatives.",
      test: "Find 20 teams who self-identify with this problem within 60 days of publishing the manifesto.",
      null_h: "The Ceremony Tax is real, but teams won't change because Agile is culturally entrenched.",
      risk: "medium",
    },
    {
      id: "H2",
      title: "The Specification Gap Is the Core Pain",
      claim: 'The biggest frustration isn\'t "AI can\'t code well enough" — it\'s "we can\'t specify well enough."',
      test: "In interviews with 10 teams, does spec quality rank as a top-3 pain point?",
      null_h: "Teams blame AI capability, not their own spec quality. The spec gap is invisible to them.",
      risk: "low",
    },
    {
      id: "H3",
      title: "Cross-Functional Shaping Is the Unlock",
      claim: "Teams involving product, design, and quality in specs produce measurably better AI-augmented outcomes.",
      test: "Compare spec quality and outcome satisfaction across team types.",
      null_h: "Engineering-only specs are sufficient; cross-functional shaping adds overhead without outcome improvement.",
      risk: "high",
    },
    {
      id: "H4",
      title: "Methodology Before Tooling",
      claim: "Teams will adopt the loop using existing tools before needing purpose-built software.",
      test: "Can 5 teams sustain the Intent loop 3+ months using only markdown specs and Git?",
      null_h: "Without tooling, the methodology is too manual and teams regress to old habits.",
      risk: "medium",
    },
    {
      id: "H5",
      title: "Thought Leadership Creates Demand",
      claim: "Publishing the manifesto and case studies generates inbound interest for workshops and advisory.",
      test: "3+ inbound consulting inquiries within 90 days of manifesto publication.",
      null_h: "Manifesto gets attention but doesn't convert to paid engagements — free content satisfies the need.",
      risk: "high",
    },
  ];

  const riskColor = { low: C.execute, medium: C.notice, high: C.observe };

  return (
    <div>
      <div style={{ marginBottom: 32 }}>
        <h2
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: C.text,
            margin: 0,
            lineHeight: 1.2,
          }}
        >
          What Must Be True
          <br />
          <span style={{ color: C.textMuted, fontWeight: 400 }}>
            Falsifiable hypotheses with null alternatives
          </span>
        </h2>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        {hypotheses.map((h) => {
          const isOpen = expanded === h.id;
          return (
            <Card
              key={h.id}
              hover
              onClick={() => setExpanded(isOpen ? null : h.id)}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                  <span
                    style={{
                      fontSize: 13,
                      fontWeight: 800,
                      color: C.accent,
                      fontFamily: "monospace",
                    }}
                  >
                    {h.id}
                  </span>
                  <span
                    style={{
                      fontSize: 15,
                      fontWeight: 600,
                      color: C.text,
                    }}
                  >
                    {h.title}
                  </span>
                </div>
                <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                  <Badge color={riskColor[h.risk]}>{h.risk} risk</Badge>
                  {isOpen ? (
                    <ChevronDown size={16} color={C.textMuted} />
                  ) : (
                    <ChevronRight size={16} color={C.textMuted} />
                  )}
                </div>
              </div>

              {isOpen && (
                <div style={{ marginTop: 16 }}>
                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns: "1fr 1fr",
                      gap: 10,
                    }}
                  >
                    <div
                      style={{
                        padding: 14,
                        background: C.execute + "0c",
                        border: `1px solid ${C.execute}25`,
                        borderRadius: 6,
                      }}
                    >
                      <div
                        style={{
                          fontSize: 10,
                          fontWeight: 700,
                          textTransform: "uppercase",
                          color: C.execute,
                          marginBottom: 6,
                          letterSpacing: "0.06em",
                        }}
                      >
                        Claim
                      </div>
                      <div
                        style={{
                          fontSize: 13,
                          color: C.text,
                          lineHeight: 1.5,
                        }}
                      >
                        {h.claim}
                      </div>
                    </div>
                    <div
                      style={{
                        padding: 14,
                        background: C.observe + "0c",
                        border: `1px solid ${C.observe}25`,
                        borderRadius: 6,
                      }}
                    >
                      <div
                        style={{
                          fontSize: 10,
                          fontWeight: 700,
                          textTransform: "uppercase",
                          color: C.observe,
                          marginBottom: 6,
                          letterSpacing: "0.06em",
                        }}
                      >
                        Null hypothesis
                      </div>
                      <div
                        style={{
                          fontSize: 13,
                          color: C.text,
                          lineHeight: 1.5,
                        }}
                      >
                        {h.null_h}
                      </div>
                    </div>
                  </div>
                  <div
                    style={{
                      marginTop: 10,
                      padding: 14,
                      background: C.accent + "0c",
                      border: `1px solid ${C.accent}25`,
                      borderRadius: 6,
                    }}
                  >
                    <div
                      style={{
                        fontSize: 10,
                        fontWeight: 700,
                        textTransform: "uppercase",
                        color: C.accent,
                        marginBottom: 6,
                        letterSpacing: "0.06em",
                      }}
                    >
                      Validation test
                    </div>
                    <div
                      style={{
                        fontSize: 13,
                        color: C.text,
                        lineHeight: 1.5,
                      }}
                    >
                      {h.test}
                    </div>
                  </div>
                </div>
              )}
            </Card>
          );
        })}
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   SECTION: COMPETITIVE LANDSCAPE
   ═══════════════════════════════════════════ */
function LandscapeSection() {
  const competitors = [
    {
      name: "AI-Augmented Scrum",
      examples: "Monday.ai, Jira AI, Linear",
      approach: "Bolt AI onto existing ceremonies",
      solves: "Efficiency within current model",
      misses: "Doesn't question whether ceremonies are the right container",
      quadrant: { x: 20, y: 70 },
    },
    {
      name: "Spec-Driven Dev Tools",
      examples: "GitHub Spec Kit, Kiro, Tessl",
      approach: "Specs as source of truth for AI agents",
      solves: "Engineering execution quality",
      misses: "Doesn't address how the spec gets shaped (upstream) or outcomes observed (downstream)",
      quadrant: { x: 75, y: 30 },
    },
    {
      name: "Cagan's Product Model",
      examples: "SVPG, Empowered, Transformed",
      approach: "Empowered teams, discovery over delivery",
      solves: "Team philosophy and structure",
      misses: "Designed for weeks-long delivery cycles, not hours",
      quadrant: { x: 30, y: 30 },
    },
    {
      name: "Intent",
      examples: "This concept",
      approach: "Team operating model for AI-augmented product teams",
      solves: "How the full team flows when AI changes the tempo",
      misses: "Unproven — needs validation",
      quadrant: { x: 72, y: 72 },
    },
  ];

  const [hoveredComp, setHoveredComp] = useState(null);

  return (
    <div>
      <div style={{ marginBottom: 32 }}>
        <h2
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: C.text,
            margin: 0,
            lineHeight: 1.2,
          }}
        >
          Competitive Landscape
          <br />
          <span style={{ color: C.textMuted, fontWeight: 400 }}>
            Where Intent sits relative to existing approaches
          </span>
        </h2>
      </div>

      {/* 2x2 map */}
      <Card style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ position: "relative", width: "100%", height: 360 }}>
          {/* axis labels */}
          <div
            style={{
              position: "absolute",
              top: 8,
              left: "50%",
              transform: "translateX(-50%)",
              fontSize: 11,
              color: C.textMuted,
              fontWeight: 600,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
            }}
          >
            Team Operating Model Scope
          </div>
          <div
            style={{
              position: "absolute",
              top: 8,
              left: 14,
              fontSize: 10,
              color: C.textMuted,
            }}
          >
            Narrow
          </div>
          <div
            style={{
              position: "absolute",
              top: 8,
              right: 14,
              fontSize: 10,
              color: C.textMuted,
            }}
          >
            Broad
          </div>
          <div
            style={{
              position: "absolute",
              left: 10,
              top: "50%",
              transform: "translateY(-50%) rotate(-90deg)",
              fontSize: 11,
              color: C.textMuted,
              fontWeight: 600,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              whiteSpace: "nowrap",
            }}
          >
            AI-Native
          </div>
          <div
            style={{
              position: "absolute",
              bottom: 8,
              left: 28,
              fontSize: 10,
              color: C.textMuted,
            }}
          >
            Low
          </div>
          <div
            style={{
              position: "absolute",
              top: 28,
              left: 28,
              fontSize: 10,
              color: C.textMuted,
            }}
          >
            High
          </div>

          {/* grid lines */}
          <div
            style={{
              position: "absolute",
              left: 40,
              right: 16,
              top: "50%",
              height: 1,
              background: C.border,
            }}
          />
          <div
            style={{
              position: "absolute",
              top: 28,
              bottom: 16,
              left: "50%",
              width: 1,
              background: C.border,
            }}
          />

          {/* quadrant labels */}
          {[
            { label: "Process\nOptimization", x: "28%", y: "72%" },
            { label: "Philosophy\nFrameworks", x: "28%", y: "35%" },
            { label: "Engineering\nTooling", x: "70%", y: "35%" },
            { label: "Operating\nModel", x: "70%", y: "72%" },
          ].map((q) => (
            <div
              key={q.label}
              style={{
                position: "absolute",
                left: q.x,
                top: q.y,
                transform: "translate(-50%, -50%)",
                fontSize: 10,
                color: C.border,
                textAlign: "center",
                whiteSpace: "pre-line",
                lineHeight: 1.3,
                fontWeight: 600,
              }}
            >
              {q.label}
            </div>
          ))}

          {/* competitor dots */}
          {competitors.map((comp, i) => {
            const isIntent = comp.name === "Intent";
            const isHovered = hoveredComp === i;
            const dotColor = isIntent ? C.accent : C.textMuted;
            // map x: 0-100 → 50px-calc(100%-30px), y: 0-100 → bottom to top
            const left = `calc(50px + ${comp.quadrant.x}% * 0.7)`;
            const top = `calc(340px - ${comp.quadrant.y}% * 3px)`;
            return (
              <div
                key={comp.name}
                onMouseEnter={() => setHoveredComp(i)}
                onMouseLeave={() => setHoveredComp(null)}
                style={{
                  position: "absolute",
                  left: `${40 + comp.quadrant.x * 0.55}%`,
                  top: `${90 - comp.quadrant.y * 0.75}%`,
                  transform: "translate(-50%, -50%)",
                  cursor: "pointer",
                  zIndex: isHovered ? 10 : 1,
                }}
              >
                <div
                  style={{
                    width: isIntent ? 16 : 12,
                    height: isIntent ? 16 : 12,
                    borderRadius: "50%",
                    background: dotColor,
                    border: isIntent
                      ? `2px solid ${C.accent}`
                      : `2px solid ${C.textMuted}60`,
                    boxShadow: isIntent
                      ? `0 0 12px ${C.accent}40`
                      : "none",
                    transition: "all 0.2s",
                    transform: isHovered ? "scale(1.4)" : "scale(1)",
                  }}
                />
                <div
                  style={{
                    position: "absolute",
                    top: isIntent ? -8 : 18,
                    left: "50%",
                    transform: "translateX(-50%)",
                    fontSize: 11,
                    fontWeight: isIntent ? 700 : 500,
                    color: isIntent ? C.accent : C.textMuted,
                    whiteSpace: "nowrap",
                  }}
                >
                  {comp.name}
                </div>
              </div>
            );
          })}
        </div>
      </Card>

      {/* detail cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 8,
          marginTop: 16,
        }}
      >
        {competitors.map((comp, i) => {
          const isIntent = comp.name === "Intent";
          return (
            <Card
              key={comp.name}
              hover
              style={{
                borderLeft: isIntent
                  ? `3px solid ${C.accent}`
                  : `1px solid ${C.border}`,
                background: hoveredComp === i ? C.surfaceAlt : C.surface,
              }}
              onClick={() =>
                setHoveredComp(hoveredComp === i ? null : i)
              }
            >
              <div
                style={{
                  fontSize: 14,
                  fontWeight: 700,
                  color: isIntent ? C.accent : C.text,
                  marginBottom: 2,
                }}
              >
                {comp.name}
              </div>
              <div
                style={{
                  fontSize: 11,
                  color: C.textMuted,
                  marginBottom: 10,
                }}
              >
                {comp.examples}
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                <div>
                  <span
                    style={{
                      fontSize: 10,
                      fontWeight: 700,
                      color: C.execute,
                      textTransform: "uppercase",
                    }}
                  >
                    Solves:{" "}
                  </span>
                  <span style={{ fontSize: 12, color: C.text }}>
                    {comp.solves}
                  </span>
                </div>
                <div>
                  <span
                    style={{
                      fontSize: 10,
                      fontWeight: 700,
                      color: C.observe,
                      textTransform: "uppercase",
                    }}
                  >
                    Misses:{" "}
                  </span>
                  <span style={{ fontSize: 12, color: C.textMuted }}>
                    {comp.misses}
                  </span>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   MAIN APP
   ═══════════════════════════════════════════ */
export default function IntentBrief() {
  const [activeSection, setActiveSection] = useState("problem");

  const renderSection = () => {
    switch (activeSection) {
      case "problem":
        return <ProblemSection />;
      case "loop":
        return <LoopSection />;
      case "stack":
        return <StackSection />;
      case "audience":
        return <AudienceSection />;
      case "gtm":
        return <GTMSection />;
      case "hypotheses":
        return <HypothesesSection />;
      case "landscape":
        return <LandscapeSection />;
      default:
        return null;
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: C.bg,
        color: C.text,
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      }}
    >
      {/* header */}
      <div
        style={{
          padding: "24px 28px 20px",
          borderBottom: `1px solid ${C.border}`,
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-end",
          }}
        >
          <div>
            <div
              style={{
                fontSize: 11,
                fontWeight: 700,
                textTransform: "uppercase",
                letterSpacing: "0.1em",
                color: C.accent,
                marginBottom: 6,
              }}
            >
              Lab / Pipeline / Ideas
            </div>
            <h1
              style={{
                fontSize: 32,
                fontWeight: 800,
                color: C.text,
                margin: 0,
                letterSpacing: "-0.02em",
              }}
            >
              Intent
            </h1>
            <div
              style={{
                fontSize: 15,
                color: C.textMuted,
                marginTop: 4,
              }}
            >
              A team operating model for AI-augmented product teams
            </div>
          </div>
          <div style={{ display: "flex", gap: 8 }}>
            <Badge color={C.notice}>IDEA STAGE</Badge>
            <Badge color={C.textMuted}>2026-03-28</Badge>
          </div>
        </div>
      </div>

      {/* body */}
      <div style={{ display: "flex" }}>
        {/* sidebar nav */}
        <div
          style={{
            width: 200,
            padding: "16px 12px",
            borderRight: `1px solid ${C.border}`,
            position: "sticky",
            top: 0,
            height: "calc(100vh - 90px)",
            flexShrink: 0,
          }}
        >
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 2,
            }}
          >
            {sections.map((s) => {
              const Icon = s.icon;
              const isActive = activeSection === s.id;
              return (
                <button
                  key={s.id}
                  onClick={() => setActiveSection(s.id)}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 10,
                    padding: "9px 12px",
                    background: isActive ? C.accent + "15" : "transparent",
                    border: "none",
                    borderRadius: 6,
                    cursor: "pointer",
                    textAlign: "left",
                    borderLeft: isActive
                      ? `2px solid ${C.accent}`
                      : "2px solid transparent",
                  }}
                >
                  <Icon
                    size={15}
                    color={isActive ? C.accent : C.textMuted}
                  />
                  <span
                    style={{
                      fontSize: 13,
                      fontWeight: isActive ? 600 : 400,
                      color: isActive ? C.text : C.textMuted,
                    }}
                  >
                    {s.label}
                  </span>
                </button>
              );
            })}
          </div>

          {/* analogy */}
          <div
            style={{
              marginTop: 28,
              padding: 14,
              background: C.surfaceAlt,
              borderRadius: 8,
              borderLeft: `2px solid ${C.accent}40`,
            }}
          >
            <div
              style={{
                fontSize: 10,
                fontWeight: 700,
                textTransform: "uppercase",
                color: C.accent,
                marginBottom: 6,
                letterSpacing: "0.08em",
              }}
            >
              The Analogy
            </div>
            <div
              style={{
                fontSize: 12,
                color: C.textMuted,
                lineHeight: 1.55,
              }}
            >
              Agile was the OS for teams with human labor as the primary
              resource. Intent is the OS for teams with AI agents as
              co-participants. The bottleneck moved from "hands building" to
              "minds deciding what to build."
            </div>
          </div>
        </div>

        {/* main content */}
        <div
          style={{
            flex: 1,
            padding: "28px 32px 60px",
            maxWidth: 780,
          }}
        >
          {renderSection()}
        </div>
      </div>
    </div>
  );
}
