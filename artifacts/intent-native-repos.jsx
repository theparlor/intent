import { useState } from "react";

const COLORS = {
  bg: "#0f172a",
  surface: "#1e293b",
  surfaceHover: "#334155",
  border: "#334155",
  borderActive: "#60a5fa",
  text: "#f1f5f9",
  textMuted: "#94a3b8",
  textDim: "#64748b",
  notice: "#f59e0b",
  spec: "#3b82f6",
  execute: "#10b981",
  observe: "#a855f7",
  entire: "#ec4899",
  accent: "#60a5fa",
  warn: "#f59e0b",
  success: "#10b981",
};

const tabs = [
  { id: "template", label: "Repo Template", icon: "\ud83d\udcd0" },
  { id: "tiers", label: "Adoption Tiers", icon: "\ud83e\udea4" },
  { id: "loop", label: "Entire \u2192 Spec Loop", icon: "\ud83d\udd04" },
  { id: "apply", label: "Your Repos Now", icon: "\ud83d\uddfa\ufe0f" },
];

function RepoTemplate() {
  const [expanded, setExpanded] = useState(null);

  const layers = [
    {
      id: "intent-layer",
      name: ".intent/",
      desc: "The loop metadata \u2014 what makes this repo Intent-native",
      color: COLORS.spec,
      files: [
        {
          name: "INTENT.md",
          purpose: "The repo's intent declaration \u2014 why this repo exists, what outcome it serves, what phase of the loop it's primarily in",
          required: true,
          example: `---\nname: MARS Command Center\npurpose: Web-based operational dashboard for Subaru retailer network\nloop-phase: execute\nowner: Brien\nspec-source: spec/\nobserve-via: entire\n---\n\n# Intent\nDeliver a real-time operational view of the MARS retailer network.\nThis is a consulting engagement deliverable for Subaru/SOA.\n\n# Current Shape\nStatic HTML + JS dashboard. No backend. Content managed via markdown + YAML.\n\n# Active Contracts\n- Dashboard loads in <2s on retail network hardware\n- All data visible without authentication\n- Visual language matches Subaru brand system`,
        },
        {
          name: "decisions.md",
          purpose: "Running decision log \u2014 extracted from Entire.io traces and manual observations. The institutional memory of WHY things are the way they are.",
          required: true,
          example: `# Decision Log\n\n## 2026-03-28 \u2014 Static HTML over React\n**Context:** Agent considered React for dashboard components\n**Decision:** Stay with vanilla HTML + JS\n**Why:** Retail network hardware runs older browsers. No build step means no deployment complexity.\n**Source:** entire session 02e2bcc3 (commit a1b2c3d)\n**Risk if reversed:** Build tooling dependency, browser compat issues\n\n## 2026-03-27 \u2014 No authentication layer\n**Context:** SOW scope question\n**Decision:** Dashboard is read-only, no auth needed\n**Why:** Adds complexity without value \u2014 data is not sensitive\n**Source:** Brien manual decision, SOW section 3.2`,
        },
        {
          name: "risks.md",
          purpose: "Active risk register \u2014 surfaced from Entire traces, spec reviews, and observe cycles. Each risk links back to the decision or session that identified it.",
          required: false,
          example: `# Risk Register\n\n| ID | Risk | Severity | Source | Mitigation | Status |\n|----|------|----------|--------|------------|--------|\n| R1 | Browser compat on kiosk hardware | High | Entire session 4631a39f | Test on actual hardware monthly | Open |\n| R2 | mars-nav.js growing beyond maintainability | Medium | Health check 2026-03-28 | Refactor to module pattern if >500 LOC | Monitoring |\n| R3 | No offline fallback | Low | Spec review | Static files cached by browser natively | Accepted |`,
        },
      ],
    },
    {
      id: "claude-layer",
      name: ".claude/",
      desc: "Agent operating context \u2014 how Claude Code works in this repo",
      color: COLORS.execute,
      files: [
        {
          name: "CLAUDE.md (root)",
          purpose: "Project-level context. Tells Claude Code WHO it is in this repo, WHAT the repo does, and HOW to work here. References INTENT.md for strategic context.",
          required: true,
        },
        {
          name: "commands/*.md",
          purpose: "Headless prompts for autonomous ops. Each file is both a slash command and a prompt for claude -p invocation.",
          required: false,
        },
        {
          name: "settings.json",
          purpose: "Tool permissions, model preferences, project-specific config.",
          required: false,
        },
      ],
    },
    {
      id: "entire-layer",
      name: ".entire/",
      desc: "Observability layer \u2014 agent reasoning captured alongside commits",
      color: COLORS.entire,
      files: [
        {
          name: "settings.json",
          purpose: "Entire.io configuration (created by `entire enable`)",
          required: true,
        },
        {
          name: "metadata/*/",
          purpose: "Session captures \u2014 prompt.txt + full.jsonl per agent session. This is the raw material that feeds back into .intent/decisions.md",
          required: true,
        },
      ],
    },
    {
      id: "spec-layer",
      name: "spec/ (or docs/spec/)",
      desc: "Spec artifacts \u2014 Intent, Shape, Contract for each unit of work",
      color: COLORS.spec,
      files: [
        {
          name: "*.md",
          purpose: "Each spec follows the three-part structure: Intent (why), Shape (what good looks like), Contract (how we know it's done)",
          required: true,
        },
      ],
    },
  ];

  return (
    <div>
      <p style={{ color: COLORS.textMuted, marginBottom: 24, lineHeight: 1.6 }}>
        Not every repo needs the full <code style={{ color: COLORS.notice }}>notice/ spec/ execute/ observe/</code> directory
        structure \u2014 that's for the Intent methodology repo itself, which IS the product. For working codebases,
        the pattern is lighter: three dotfile directories and a spec convention.
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {layers.map((layer) => (
          <div key={layer.id}>
            <button
              onClick={() => setExpanded(expanded === layer.id ? null : layer.id)}
              style={{
                width: "100%",
                background: expanded === layer.id ? COLORS.surfaceHover : COLORS.surface,
                border: `1px solid ${expanded === layer.id ? layer.color : COLORS.border}`,
                borderRadius: 8,
                padding: "14px 18px",
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                transition: "all 0.2s",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                <code style={{ color: layer.color, fontSize: 16, fontWeight: 600 }}>{layer.name}</code>
                <span style={{ color: COLORS.textMuted, fontSize: 13 }}>{layer.desc}</span>
              </div>
              <span style={{ color: COLORS.textDim, fontSize: 18, transform: expanded === layer.id ? "rotate(90deg)" : "none", transition: "transform 0.2s" }}>\u203a</span>
            </button>
            {expanded === layer.id && (
              <div style={{ marginTop: 4, marginLeft: 16, borderLeft: `2px solid ${layer.color}30`, paddingLeft: 16 }}>
                {layer.files.map((file, i) => (
                  <div key={i} style={{ background: COLORS.surface, borderRadius: 6, padding: 14, marginBottom: 8 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                      <code style={{ color: layer.color, fontSize: 13 }}>{file.name}</code>
                      {file.required && (
                        <span style={{ background: `${layer.color}20`, color: layer.color, fontSize: 10, padding: "2px 6px", borderRadius: 4 }}>required</span>
                      )}
                      {!file.required && (
                        <span style={{ background: `${COLORS.textDim}20`, color: COLORS.textDim, fontSize: 10, padding: "2px 6px", borderRadius: 4 }}>optional</span>
                      )}
                    </div>
                    <p style={{ color: COLORS.textMuted, fontSize: 13, lineHeight: 1.5, margin: 0 }}>{file.purpose}</p>
                    {file.example && (
                      <details style={{ marginTop: 8 }}>
                        <summary style={{ color: COLORS.textDim, fontSize: 12, cursor: "pointer" }}>Example content</summary>
                        <pre style={{ background: COLORS.bg, borderRadius: 4, padding: 10, marginTop: 6, fontSize: 11, color: COLORS.textMuted, overflowX: "auto", whiteSpace: "pre-wrap" }}>
                          {file.example}
                        </pre>
                      </details>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
      <div style={{ marginTop: 24, background: `${COLORS.spec}10`, border: `1px solid ${COLORS.spec}30`, borderRadius: 8, padding: 16 }}>
        <p style={{ color: COLORS.spec, fontWeight: 600, fontSize: 14, margin: "0 0 8px 0" }}>The minimum viable Intent repo</p>
        <p style={{ color: COLORS.textMuted, fontSize: 13, lineHeight: 1.6, margin: 0 }}>
          <code style={{ color: COLORS.spec }}>.intent/INTENT.md</code> + <code style={{ color: COLORS.spec }}>.intent/decisions.md</code> + <code style={{ color: COLORS.execute }}>.claude/CLAUDE.md</code> + <code style={{ color: COLORS.entire }}>.entire/</code> enabled.
          That's four files and one <code>entire enable</code>. Everything else scales up from there.
        </p>
      </div>
    </div>
  );
}

function AdoptionTiers() {
  const tiers = [
    {
      name: "Tier 0: Observable",
      tagline: '"At least I can see what happened"',
      color: COLORS.observe,
      what: "Just Entire.io enabled. No other structural changes.",
      gets: "Agent reasoning traces alongside every commit. You can retroactively understand decisions even without a formal decision log.",
      effort: "30 seconds \u2014 `entire enable`",
      repos: "Everything. No reason not to.",
    },
    {
      name: "Tier 1: Intentional",
      tagline: '"The repo knows why it exists"',
      color: COLORS.spec,
      what: ".intent/INTENT.md + .intent/decisions.md + CLAUDE.md",
      gets: "Strategic context is captured. Any agent (or human) landing in this repo knows the purpose, active shape, and key decisions. Decisions.md becomes the institutional memory.",
      effort: "15-30 minutes to write the initial INTENT.md and seed decisions.md from memory",
      repos: "Any repo you'll return to more than twice.",
    },
    {
      name: "Tier 2: Autonomous",
      tagline: '"The repo runs itself"',
      color: COLORS.execute,
      what: "Tier 1 + .claude/commands/*.md + ops/*.sh + launchd plist + structured logs",
      gets: "The full autonomous ops stack. Agent does work on a schedule, logs everything, Entire captures the reasoning, and the feedback loop from observe \u2192 notice \u2192 spec is closable.",
      effort: "1-2 hours to spec the commands and build the wrapper.",
      repos: "Repos with recurring operational work.",
    },
    {
      name: "Tier 3: Self-Observing",
      tagline: '"The repo closes its own loop"',
      color: COLORS.entire,
      what: "Tier 2 + an automated observe phase that reads Entire traces, extracts decisions/risks/challenges, and writes them back into .intent/decisions.md and .intent/risks.md",
      gets: "The fully closed Intent loop. Execute \u2192 Entire captures \u2192 Observe agent reads traces \u2192 Extracts signal \u2192 Writes to decisions.md \u2192 Next spec reads decisions.md \u2192 Better spec \u2192 Better execution.",
      effort: "A new .claude/commands/observe-cycle.md that runs after nightly ops.",
      repos: "High-value repos where decision drift is a real risk.",
    },
  ];

  return (
    <div>
      <p style={{ color: COLORS.textMuted, marginBottom: 24, lineHeight: 1.6 }}>
        Not every repo needs the full treatment. Think of these as maturity levels \u2014 you can adopt incrementally
        and each tier delivers value on its own.
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        {tiers.map((tier, i) => (
          <div key={i} style={{ background: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: 8, overflow: "hidden" }}>
            <div style={{ background: `${tier.color}15`, padding: "12px 18px", borderBottom: `1px solid ${tier.color}30` }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <span style={{ color: tier.color, fontWeight: 700, fontSize: 15 }}>{tier.name}</span>
              </div>
              <p style={{ color: COLORS.textMuted, fontSize: 13, fontStyle: "italic", margin: "4px 0 0 0" }}>{tier.tagline}</p>
            </div>
            <div style={{ padding: 16 }}>
              <div style={{ display: "grid", gridTemplateColumns: "80px 1fr", gap: "8px 12px", fontSize: 13 }}>
                <span style={{ color: COLORS.textDim, fontWeight: 600 }}>Add</span>
                <span style={{ color: COLORS.text }}>{tier.what}</span>
                <span style={{ color: COLORS.textDim, fontWeight: 600 }}>Gets you</span>
                <span style={{ color: COLORS.textMuted, lineHeight: 1.5 }}>{tier.gets}</span>
                <span style={{ color: COLORS.textDim, fontWeight: 600 }}>Effort</span>
                <span style={{ color: COLORS.success }}>{tier.effort}</span>
                <span style={{ color: COLORS.textDim, fontWeight: 600 }}>Apply to</span>
                <span style={{ color: COLORS.textMuted }}>{tier.repos}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function EntireSpecLoop() {
  const [step, setStep] = useState(0);

  const steps = [
    {
      phase: "Execute",
      color: COLORS.execute,
      title: "Agent builds against spec",
      detail: "Claude Code runs \u2014 implements a feature, runs the pipeline, makes autonomous decisions within spec boundaries. Some decisions are straightforward. Some involve trade-offs, workarounds, or discovered risks.",
      artifact: "Git commits + code changes",
    },
    {
      phase: "Capture",
      color: COLORS.entire,
      title: "Entire.io records the full session",
      detail: "Every agent session is captured as first-class versioned data: the prompt, the full reasoning transcript (full.jsonl), linked to the commit SHA. This happens automatically \u2014 zero effort.",
      artifact: ".entire/metadata/{session-id}/full.jsonl + prompt.txt",
    },
    {
      phase: "Extract",
      color: COLORS.observe,
      title: "Observe agent reads traces, extracts signal",
      detail: "A scheduled observe-cycle command reads recent Entire sessions and looks for: decisions made (trade-offs, alternatives considered), challenges encountered (errors, ambiguities, workarounds), and risks discovered (edge cases, performance concerns, fragile assumptions).",
      artifact: "Structured observations with session links",
    },
    {
      phase: "Write Back",
      color: COLORS.observe,
      title: "Observations flow into .intent/",
      detail: "The observe agent appends new entries to decisions.md (with session source links), updates risks.md with newly discovered risks, and optionally writes a notice if something significant was found \u2014 a signal that a new spec cycle may be warranted.",
      artifact: ".intent/decisions.md, .intent/risks.md updated",
    },
    {
      phase: "Inform",
      color: COLORS.spec,
      title: "Next spec reads the accumulated context",
      detail: "When you (or an agent) write the next spec for this repo, decisions.md and risks.md are right there. The spec is informed by what actually happened during execution \u2014 not just what was planned. This is the Cagan insight operationalized: learning from delivery, not just planning it.",
      artifact: "Better spec \u2192 better execution \u2192 tighter loop",
    },
  ];

  return (
    <div>
      <p style={{ color: COLORS.textMuted, marginBottom: 20, lineHeight: 1.6 }}>
        Entire captures everything, but right now that data sits in <code style={{ color: COLORS.entire }}>.entire/metadata/</code> as raw transcripts.
        The observe-cycle agent is what turns raw traces into actionable institutional knowledge.
      </p>
      <div style={{ display: "flex", gap: 4, marginBottom: 20 }}>
        {steps.map((s, i) => (
          <button
            key={i}
            onClick={() => setStep(i)}
            style={{
              flex: 1,
              background: step === i ? `${s.color}20` : COLORS.surface,
              border: `1px solid ${step === i ? s.color : COLORS.border}`,
              borderRadius: 6,
              padding: "8px 4px",
              cursor: "pointer",
              transition: "all 0.2s",
            }}
          >
            <div style={{ color: s.color, fontSize: 11, fontWeight: 700 }}>{s.phase}</div>
            <div style={{ color: step === i ? COLORS.text : COLORS.textDim, fontSize: 10, marginTop: 2 }}>{i + 1}/5</div>
          </button>
        ))}
      </div>
      <div style={{ background: COLORS.surface, border: `1px solid ${steps[step].color}40`, borderRadius: 8, padding: 20 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
          <span style={{ background: `${steps[step].color}20`, color: steps[step].color, padding: "4px 10px", borderRadius: 4, fontSize: 12, fontWeight: 600 }}>
            {steps[step].phase}
          </span>
          <span style={{ color: COLORS.text, fontWeight: 600, fontSize: 15 }}>{steps[step].title}</span>
        </div>
        <p style={{ color: COLORS.textMuted, lineHeight: 1.7, fontSize: 14, margin: "0 0 16px 0" }}>
          {steps[step].detail}
        </p>
        <div style={{ background: COLORS.bg, borderRadius: 6, padding: "10px 14px" }}>
          <span style={{ color: COLORS.textDim, fontSize: 11 }}>Artifact: </span>
          <code style={{ color: steps[step].color, fontSize: 12 }}>{steps[step].artifact}</code>
        </div>
      </div>

      <div style={{ marginTop: 24, background: `${COLORS.entire}10`, border: `1px solid ${COLORS.entire}30`, borderRadius: 8, padding: 16 }}>
        <p style={{ color: COLORS.entire, fontWeight: 600, fontSize: 14, margin: "0 0 8px 0" }}>The observe-cycle command</p>
        <p style={{ color: COLORS.textMuted, fontSize: 13, lineHeight: 1.6, margin: "0 0 12px 0" }}>
          This would be a new <code style={{ color: COLORS.entire }}>.claude/commands/observe-cycle.md</code> \u2014 a prompt that tells Claude Code to:
        </p>
        <div style={{ fontSize: 13, color: COLORS.textMuted, lineHeight: 1.8 }}>
          <div>1. Read recent Entire session transcripts (<code style={{ color: COLORS.entire }}>entire explain --commit</code> for last N commits)</div>
          <div>2. Extract decisions (alternatives considered, trade-offs made)</div>
          <div>3. Extract challenges (errors hit, workarounds applied, ambiguities resolved)</div>
          <div>4. Extract risks (edge cases found, fragile assumptions, TODO-as-debt)</div>
          <div>5. Append structured entries to <code style={{ color: COLORS.spec }}>.intent/decisions.md</code> and <code style={{ color: COLORS.spec }}>.intent/risks.md</code></div>
          <div>6. If anything is significant, write a notice entry flagging it for spec attention</div>
        </div>
      </div>
    </div>
  );
}

function YourReposNow() {
  return (
    <div>
      <p style={{ color: COLORS.textMuted, marginBottom: 24, lineHeight: 1.6 }}>
        Intent-native adoption is incremental. Start at Tier 0 (Entire.io enabled), then layer on
        .intent/ files and autonomous ops as the repo matures.
      </p>
      <div style={{ marginTop: 16, background: `${COLORS.success}10`, border: `1px solid ${COLORS.success}30`, borderRadius: 8, padding: 16 }}>
        <p style={{ color: COLORS.success, fontWeight: 600, fontSize: 14, margin: "0 0 8px 0" }}>Getting started</p>
        <p style={{ color: COLORS.textMuted, fontSize: 13, lineHeight: 1.6, margin: 0 }}>
          Run <code style={{ color: COLORS.entire }}>entire enable</code> in your repo (Tier 0), then add
          <code style={{ color: COLORS.spec }}> .intent/INTENT.md</code> and <code style={{ color: COLORS.spec }}>.intent/decisions.md</code> (Tier 1).
          The repo template tab shows exactly what goes in each file.
        </p>
      </div>
    </div>
  );
}

export default function IntentNativeRepos() {
  const [activeTab, setActiveTab] = useState("template");

  return (
    <div style={{ background: COLORS.bg, minHeight: "100vh", color: COLORS.text, fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}>
      <div style={{ maxWidth: 780, margin: "0 auto", padding: "32px 20px" }}>
        <div style={{ marginBottom: 32 }}>
          <h1 style={{ fontSize: 24, fontWeight: 700, margin: "0 0 8px 0", color: COLORS.text }}>
            Intent-Native Repos
          </h1>
          <p style={{ color: COLORS.textMuted, fontSize: 14, margin: 0, lineHeight: 1.6 }}>
            What every repo needs to follow the Intent pattern \u2014 and how Entire.io closes the loop from execution back into the spec layer.
          </p>
        </div>

        <div style={{ display: "flex", gap: 4, marginBottom: 24, borderBottom: `1px solid ${COLORS.border}`, paddingBottom: 4 }}>
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                background: activeTab === tab.id ? COLORS.surfaceHover : "transparent",
                border: "none",
                borderRadius: "6px 6px 0 0",
                padding: "10px 16px",
                cursor: "pointer",
                color: activeTab === tab.id ? COLORS.text : COLORS.textDim,
                fontWeight: activeTab === tab.id ? 600 : 400,
                fontSize: 13,
                transition: "all 0.2s",
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <span style={{ fontSize: 14 }}>{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>

        {activeTab === "template" && <RepoTemplate />}
        {activeTab === "tiers" && <AdoptionTiers />}
        {activeTab === "loop" && <EntireSpecLoop />}
        {activeTab === "apply" && <YourReposNow />}
      </div>
    </div>
  );
}