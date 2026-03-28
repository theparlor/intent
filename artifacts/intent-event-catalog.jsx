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
  decision: "#a855f7",
  danger: "#ef4444",
  // Emission sources
  cowork: "#f59e0b",
  cli: "#10b981",
  github: "#f1f5f9",
  scheduled: "#60a5fa",
  external: "#ec4899",
};

const tabs = [
  { id: "catalog", label: "Event Catalog" },
  { id: "sources", label: "Emission Sources" },
  { id: "schema", label: "Event Schema" },
  { id: "implementation", label: "Implementation Plan" },
];

// ─── Event Catalog ───
const events = [
  // Signal events
  {
    id: "signal.captured",
    category: "signal",
    name: "Signal Captured",
    description: "A new observation enters the system — from a conversation, agent trace, user research, or external source.",
    trigger: "A .intent/signals/ file is created",
    source: "cowork",
    sourceName: "Cowork Session",
    emission: "github-action",
    emissionDetail: "GitHub Action watches for new files in .intent/signals/. Also: Cowork session agent writes signal files during conversation (as we did today). Post-session extraction agent proposes signals from transcript.",
    frequency: "3-5 per session, ~10-20/week",
    schema: { event: "signal.captured", signal_id: "SIG-006", source: "cowork-session", confidence: "high", title: "..." },
    priority: "high",
    implementFirst: true,
  },
  {
    id: "signal.clustered",
    category: "signal",
    name: "Signals Clustered",
    description: "Multiple signals are recognized as pointing to the same opportunity area.",
    trigger: "Human or agent groups 3+ signals and links them to a shared theme",
    source: "cowork",
    sourceName: "Cowork Session",
    emission: "manual",
    emissionDetail: "Human updates signal files with a shared cluster_id in frontmatter. Could be semi-automated: agent proposes clusters based on content similarity.",
    frequency: "1-2/week",
    schema: { event: "signal.clustered", cluster_id: "CLU-001", signal_ids: ["SIG-001", "SIG-004"], theme: "..." },
    priority: "medium",
    implementFirst: false,
  },
  {
    id: "signal.resolved",
    category: "signal",
    name: "Signal Resolved",
    description: "A signal has been addressed — linked to an intent, dismissed as noise, or absorbed into a decision.",
    trigger: "Signal file's status field changes from 'new' to 'resolved' or 'dismissed'",
    source: "github",
    sourceName: "Git Commit",
    emission: "github-action",
    emissionDetail: "GitHub Action detects frontmatter status change in .intent/signals/ files via diff parsing.",
    frequency: "Matches signal capture rate",
    schema: { event: "signal.resolved", signal_id: "SIG-001", resolution: "linked_to_intent", intent_id: "INT-001" },
    priority: "medium",
    implementFirst: false,
  },
  // Intent events
  {
    id: "intent.created",
    category: "intent",
    name: "Intent Created",
    description: "A new desired outcome with a falsifiable hypothesis enters the system.",
    trigger: "A .intent/intents/ file is created with status: hypothesis",
    source: "cowork",
    sourceName: "Cowork Session",
    emission: "github-action",
    emissionDetail: "GitHub Action watches for new files in .intent/intents/. The intent file carries the hypothesis, success criteria, and linked signals.",
    frequency: "1-3/week",
    schema: { event: "intent.created", intent_id: "INT-003", hypothesis: "...", status: "hypothesis", signal_refs: ["SIG-001"] },
    priority: "high",
    implementFirst: true,
  },
  {
    id: "intent.status_changed",
    category: "intent",
    name: "Intent Status Changed",
    description: "An intent moves through its discovery lifecycle: hypothesis → exploring → validated → invalidated.",
    trigger: "Intent file's status field changes in YAML frontmatter",
    source: "github",
    sourceName: "Git Commit",
    emission: "github-action",
    emissionDetail: "GitHub Action diffs .intent/intents/ files, detects status field changes. This is the most important event — it gates what gets built.",
    frequency: "1-2/week per active intent",
    schema: { event: "intent.status_changed", intent_id: "INT-003", from: "hypothesis", to: "exploring", evidence: "..." },
    priority: "high",
    implementFirst: true,
  },
  // Spec events
  {
    id: "spec.authored",
    category: "spec",
    name: "Spec Authored",
    description: "A new spec is written — a declarative behavior description with contracts an agent can execute against.",
    trigger: "A spec/ file is created or a .intent/specs/ file is created",
    source: "cowork",
    sourceName: "Cowork Session",
    emission: "github-action",
    emissionDetail: "GitHub Action watches spec directories. The spec file links to its parent intent, declares dependencies, and lists contracts.",
    frequency: "2-5/week",
    schema: { event: "spec.authored", spec_id: "SPEC-012", intent_id: "INT-003", contracts: ["CON-031", "CON-032"], dependencies: [] },
    priority: "high",
    implementFirst: true,
  },
  {
    id: "spec.completed",
    category: "spec",
    name: "Spec Completed",
    description: "All contracts within a spec have passed their assertions.",
    trigger: "Last contract in the spec moves to status: passed",
    source: "cli",
    sourceName: "Claude Code CLI",
    emission: "github-action",
    emissionDetail: "GitHub Action checks if all contract files linked from a spec have status: passed. Derived event — not directly emitted, computed from contract statuses.",
    frequency: "Matches spec authoring rate, delayed",
    schema: { event: "spec.completed", spec_id: "SPEC-012", contracts_passed: 3, duration_hours: 4.2 },
    priority: "medium",
    implementFirst: false,
  },
  // Contract events
  {
    id: "contract.created",
    category: "contract",
    name: "Contract Created",
    description: "A verifiable interface agreement is defined — input schema, output behavior, invariants.",
    trigger: "A .intent/contracts/ file is created as part of spec decomposition",
    source: "cowork",
    sourceName: "Cowork Session",
    emission: "github-action",
    emissionDetail: "GitHub Action watches .intent/contracts/. Contracts are the atomic unit — their creation is the most granular meaningful event.",
    frequency: "3-8 per spec authored",
    schema: { event: "contract.created", contract_id: "CON-031", spec_id: "SPEC-012", assertions: 3 },
    priority: "medium",
    implementFirst: false,
  },
  {
    id: "contract.started",
    category: "contract",
    name: "Contract Execution Started",
    description: "An agent picks up a contract and begins implementing against its assertions.",
    trigger: "Entire.io session begins with a contract reference, or CLAUDE.md references the contract",
    source: "cli",
    sourceName: "Claude Code CLI",
    emission: "entire-hook",
    emissionDetail: "Entire.io session start event. The agent's prompt or CLAUDE.md should reference the contract ID. Entire captures this in session metadata. A post-session hook emits the event.",
    frequency: "Matches contract creation rate",
    schema: { event: "contract.started", contract_id: "CON-031", agent_session: "entire-uuid", timestamp: "..." },
    priority: "high",
    implementFirst: true,
  },
  {
    id: "contract.passed",
    category: "contract",
    name: "Contract Passed",
    description: "All assertions in the contract are verified — the agent's implementation satisfies the interface agreement.",
    trigger: "Agent commits code that passes contract assertions, or test suite passes",
    source: "cli",
    sourceName: "Claude Code CLI / CI",
    emission: "github-action",
    emissionDetail: "GitHub Action on push: runs contract assertions (test suite). If green, emits contract.passed. Contract file status updates to 'passed'. Also detectable from Entire.io session completion.",
    frequency: "Matches contract.started, with delay",
    schema: { event: "contract.passed", contract_id: "CON-031", commit: "abc123", duration_minutes: 12, agent_session: "entire-uuid" },
    priority: "high",
    implementFirst: true,
  },
  {
    id: "contract.failed",
    category: "contract",
    name: "Contract Failed",
    description: "Agent's implementation does not satisfy the contract assertions. Becomes a new signal.",
    trigger: "Test suite fails against contract assertions, or agent reports inability to satisfy",
    source: "cli",
    sourceName: "Claude Code CLI / CI",
    emission: "github-action",
    emissionDetail: "GitHub Action on push: contract assertions fail. Emit contract.failed AND auto-generate a signal (signal.captured with source: contract-failure). This closes the loop — failures feed back into notice.",
    frequency: "Hopefully rare, but important to capture",
    schema: { event: "contract.failed", contract_id: "CON-031", failure_reason: "...", auto_signal: "SIG-xxx" },
    priority: "high",
    implementFirst: true,
  },
  // Decision events
  {
    id: "decision.recorded",
    category: "decision",
    name: "Decision Recorded",
    description: "A significant architectural or strategic decision is captured with context and rationale.",
    trigger: "New entry appended to .intent/decisions.md or new file in .intent/decisions/",
    source: "cowork",
    sourceName: "Cowork Session / Observe Agent",
    emission: "github-action",
    emissionDetail: "GitHub Action detects changes to .intent/decisions.md (new H2 section added). Also: observe-cycle agent extracts decisions from Entire traces and writes them automatically.",
    frequency: "3-8/week",
    schema: { event: "decision.recorded", decision_id: "DEC-007", title: "...", source: "cowork-session" },
    priority: "medium",
    implementFirst: false,
  },
  // Capability events
  {
    id: "capability.permit_changed",
    category: "capability",
    name: "Capability Permit Changed",
    description: "A capability's governance level changes: play → build → operate (or reversed).",
    trigger: "Capability file's permit field changes in frontmatter",
    source: "github",
    sourceName: "Git Commit",
    emission: "github-action",
    emissionDetail: "GitHub Action diffs .intent/capabilities/ files, detects permit field changes. This is a governance event — it changes what agents are allowed to do.",
    frequency: "Rare but high-impact",
    schema: { event: "capability.permit_changed", capability_id: "CAP-003", from: "play", to: "build", decision_ref: "DEC-007" },
    priority: "low",
    implementFirst: false,
  },
  // System events
  {
    id: "pipeline.completed",
    category: "system",
    name: "Pipeline Completed",
    description: "A scheduled autonomous pipeline (nightly refresh, health check) completes its run.",
    trigger: "launchd-scheduled agent finishes and writes a log file",
    source: "scheduled",
    sourceName: "Scheduled Agent",
    emission: "log-watcher",
    emissionDetail: "The pipeline wrapper script already writes JSON logs. A lightweight watcher (or cron job) reads the log and emits a structured event. Alternatively, the wrapper script itself appends to .intent/events/.",
    frequency: "Daily per pipeline",
    schema: { event: "pipeline.completed", pipeline: "nightly-refresh", status: "success", duration_seconds: 340, coverage: "98.5%" },
    priority: "medium",
    implementFirst: false,
  },
  {
    id: "observe.cycle_completed",
    category: "system",
    name: "Observe Cycle Completed",
    description: "The observe-cycle agent has read Entire traces and written findings back to .intent/.",
    trigger: "Observe agent finishes and creates/updates signal, decision, or risk files",
    source: "scheduled",
    sourceName: "Observe Agent",
    emission: "self-emitting",
    emissionDetail: "The observe-cycle agent itself emits this event as its final action. It writes to .intent/events/ as part of its run. This is the cleanest emission pattern — the agent knows what it found.",
    frequency: "Daily or per-session",
    schema: { event: "observe.cycle_completed", signals_generated: 2, decisions_extracted: 1, risks_identified: 0, entire_sessions_read: 5 },
    priority: "medium",
    implementFirst: false,
  },
  // External events
  {
    id: "external.practitioner_response",
    category: "external",
    name: "Practitioner Response",
    description: "Someone outside the team responds to Intent content — a reply, a share, an inquiry.",
    trigger: "Email/Slack/social media response to manifesto or case study",
    source: "external",
    sourceName: "Zapier / Email",
    emission: "zapier",
    emissionDetail: "Zapier watches for: new email matching 'intent' subject, new GitHub issue on intent repo, social media mention. Zapier writes a signal file to .intent/signals/ via GitHub API or creates a draft for review.",
    frequency: "Depends on GTM phase. Target: 1-5/week after manifesto launch.",
    schema: { event: "external.practitioner_response", source: "email", from: "ari@example.com", summary: "..." },
    priority: "low",
    implementFirst: false,
  },
];

const emissionMechanisms = [
  {
    id: "github-action",
    name: "GitHub Action",
    color: COLORS.github,
    icon: "⚙",
    description: "A GitHub Action workflow triggered on push to main. Watches for file changes in .intent/ directories, parses YAML frontmatter diffs, and appends structured events to .intent/events/events.jsonl.",
    covers: events.filter(e => e.emission === "github-action").map(e => e.id),
    effort: "Low — single workflow file, ~50 lines YAML + ~100 lines Node.js for frontmatter diffing",
    implementation: "Create .github/workflows/intent-events.yml. On push, diff .intent/ files. For new files: emit creation events. For modified files: parse frontmatter changes (status, permit). Append to .intent/events/events.jsonl and commit.",
  },
  {
    id: "entire-hook",
    name: "Entire.io Session Hook",
    color: COLORS.execute,
    icon: "◉",
    description: "A post-session hook that fires when an Entire.io-tracked Claude Code session completes. Reads the session metadata and emits contract.started/contract.passed events.",
    covers: events.filter(e => e.emission === "entire-hook").map(e => e.id),
    effort: "Medium — requires understanding Entire.io's hook/webhook system or a file watcher on .entire/metadata/",
    implementation: "Watch .entire/metadata/ for new session directories. When a session completes (full.jsonl written), read prompt.txt for contract references. Emit contract.started with session UUID. If the session's final state indicates success, emit contract.passed.",
  },
  {
    id: "self-emitting",
    name: "Self-Emitting Agent",
    color: COLORS.observe,
    icon: "↻",
    description: "Agents that emit their own events as part of their execution. The observe-cycle agent and pipeline agents write events as their final action.",
    covers: events.filter(e => e.emission === "self-emitting").map(e => e.id),
    effort: "Low — add 5-10 lines to existing agent command files (CLAUDE.md instructions)",
    implementation: "Add to .claude/commands/observe-cycle.md: 'As your final step, append an event to .intent/events/events.jsonl with: event type, signals generated, decisions extracted, risks identified, sessions read, timestamp.'",
  },
  {
    id: "log-watcher",
    name: "Log File Watcher",
    color: COLORS.scheduled,
    icon: "📋",
    description: "A lightweight watcher that reads existing pipeline log files (nightly-*.json, health-*.json) and converts them to Intent events.",
    covers: events.filter(e => e.emission === "log-watcher").map(e => e.id),
    effort: "Low — the pipeline already writes structured JSON logs. Just need a transformer.",
    implementation: "Add a post-run step to the wrapper scripts: after pipeline completes, read the JSON log, extract key fields (status, duration, coverage), format as an Intent event, append to .intent/events/events.jsonl.",
  },
  {
    id: "zapier",
    name: "Zapier / n8n Integration",
    color: COLORS.external,
    icon: "⚡",
    description: "External automation platform watching for signals from outside the development system — email responses, social mentions, GitHub stars.",
    covers: events.filter(e => e.emission === "zapier").map(e => e.id),
    effort: "Medium — requires Zapier account + GitHub API token. One zap per trigger source.",
    implementation: "Create Zapier zaps: (1) Gmail filter for 'intent' → create signal file via GitHub API. (2) GitHub webhook for new stars/issues → create signal. (3) Future: social listening triggers. Each creates a .intent/signals/ file with source: external.",
  },
  {
    id: "manual",
    name: "Manual / Conversation",
    color: COLORS.cowork,
    icon: "✍",
    description: "Events that are currently emitted by a human (Brien) or by Claude during a Cowork session. These are candidates for future automation.",
    covers: events.filter(e => e.emission === "manual").map(e => e.id),
    effort: "Zero — this is what we're already doing. The automation path is clear for each.",
    implementation: "Continue as-is. As patterns stabilize, migrate to GitHub Action (file watching) or dedicated agent (content analysis). The manual emission today IS the design research for the automated version tomorrow.",
  },
];

function EventCatalogTab() {
  const [expanded, setExpanded] = useState(null);
  const [filter, setFilter] = useState("all");

  const categories = [
    { id: "all", label: "All Events", count: events.length },
    { id: "signal", label: "Signal", color: COLORS.signal, count: events.filter(e => e.category === "signal").length },
    { id: "intent", label: "Intent", color: COLORS.intent, count: events.filter(e => e.category === "intent").length },
    { id: "spec", label: "Spec", color: COLORS.spec, count: events.filter(e => e.category === "spec").length },
    { id: "contract", label: "Contract", color: COLORS.contract, count: events.filter(e => e.category === "contract").length },
    { id: "decision", label: "Decision", color: COLORS.decision, count: events.filter(e => e.category === "decision").length },
    { id: "system", label: "System", color: COLORS.scheduled, count: events.filter(e => e.category === "system").length },
    { id: "external", label: "External", color: COLORS.external, count: events.filter(e => e.category === "external").length },
  ];

  const categoryColor = {
    signal: COLORS.signal, intent: COLORS.intent, spec: COLORS.spec,
    contract: COLORS.contract, decision: COLORS.decision, system: COLORS.scheduled,
    capability: COLORS.capability, external: COLORS.external,
  };

  const filtered = filter === "all" ? events : events.filter(e => e.category === filter);

  return (
    <div>
      <p style={{ color: COLORS.textMuted, fontSize: 14, lineHeight: 1.6, marginBottom: 20 }}>
        Every meaningful state change in the Intent work system. Each event has a <strong style={{ color: COLORS.text }}>trigger</strong> (what causes it), a <strong style={{ color: COLORS.text }}>source</strong> (where it originates), and an <strong style={{ color: COLORS.text }}>emission mechanism</strong> (how it gets captured). Events marked with ★ should be implemented first.
      </p>

      {/* Filter bar */}
      <div style={{ display: "flex", gap: 6, marginBottom: 20, flexWrap: "wrap" }}>
        {categories.map(c => (
          <button key={c.id} onClick={() => setFilter(c.id)} style={{
            padding: "6px 12px", borderRadius: 6, border: `1px solid ${filter === c.id ? (c.color || COLORS.text) : COLORS.border}`,
            background: filter === c.id ? (c.color || COLORS.text) + "15" : "transparent",
            color: filter === c.id ? (c.color || COLORS.text) : COLORS.textMuted,
            fontSize: 12, fontWeight: 500, cursor: "pointer", transition: "all 0.2s",
          }}>
            {c.label} ({c.count})
          </button>
        ))}
      </div>

      {/* Event cards */}
      <div style={{ display: "grid", gap: 8 }}>
        {filtered.map(evt => {
          const isExpanded = expanded === evt.id;
          const color = categoryColor[evt.category] || COLORS.textMuted;
          return (
            <div key={evt.id} onClick={() => setExpanded(isExpanded ? null : evt.id)} style={{
              background: COLORS.surface, border: `1px solid ${isExpanded ? color + "60" : COLORS.border}`,
              borderRadius: 8, padding: isExpanded ? "18px 20px" : "14px 20px", cursor: "pointer", transition: "all 0.2s",
              borderLeft: `3px solid ${color}`,
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  {evt.implementFirst && <span style={{ color: COLORS.signal, fontSize: 14 }}>★</span>}
                  <code style={{ color, fontSize: 12, fontFamily: "'SF Mono', monospace", fontWeight: 600 }}>{evt.id}</code>
                  <span style={{ color: COLORS.text, fontSize: 14, fontWeight: 500 }}>{evt.name}</span>
                </div>
                <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                  <span style={{ fontSize: 10, color: COLORS.textDim, background: COLORS.bg, padding: "2px 8px", borderRadius: 4 }}>
                    {evt.emission}
                  </span>
                  <span style={{ color: COLORS.textMuted, fontSize: 16 }}>{isExpanded ? "−" : "+"}</span>
                </div>
              </div>

              {!isExpanded && (
                <p style={{ color: COLORS.textMuted, fontSize: 12, marginTop: 6, marginLeft: 24 }}>{evt.description}</p>
              )}

              {isExpanded && (
                <div style={{ marginTop: 14 }}>
                  <p style={{ color: COLORS.text, fontSize: 13, lineHeight: 1.6, marginBottom: 14 }}>{evt.description}</p>
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 14 }}>
                    <div style={{ padding: "10px 14px", background: COLORS.bg, borderRadius: 6 }}>
                      <div style={{ color: color, fontSize: 10, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 4 }}>Trigger</div>
                      <div style={{ color: COLORS.text, fontSize: 13 }}>{evt.trigger}</div>
                    </div>
                    <div style={{ padding: "10px 14px", background: COLORS.bg, borderRadius: 6 }}>
                      <div style={{ color: color, fontSize: 10, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 4 }}>Source</div>
                      <div style={{ color: COLORS.text, fontSize: 13 }}>{evt.sourceName}</div>
                    </div>
                  </div>
                  <div style={{ padding: "10px 14px", background: COLORS.bg, borderRadius: 6, marginBottom: 14 }}>
                    <div style={{ color: color, fontSize: 10, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 4 }}>Emission Mechanism</div>
                    <div style={{ color: COLORS.text, fontSize: 13, lineHeight: 1.5 }}>{evt.emissionDetail}</div>
                  </div>
                  <div style={{ padding: "10px 14px", background: COLORS.bg, borderRadius: 6, marginBottom: 10 }}>
                    <div style={{ color: color, fontSize: 10, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 4 }}>Example Event</div>
                    <pre style={{ color: COLORS.textMuted, fontSize: 11, fontFamily: "'SF Mono', monospace", whiteSpace: "pre-wrap", margin: 0 }}>
                      {JSON.stringify(evt.schema, null, 2)}
                    </pre>
                  </div>
                  <div style={{ color: COLORS.textDim, fontSize: 11 }}>Expected frequency: {evt.frequency}</div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── Emission Sources Tab ───
function EmissionSourcesTab() {
  const [expanded, setExpanded] = useState(null);

  return (
    <div>
      <p style={{ color: COLORS.textMuted, fontSize: 14, lineHeight: 1.6, marginBottom: 20 }}>
        Six emission mechanisms cover all events in the catalog. The key insight: <strong style={{ color: COLORS.text }}>GitHub Actions alone covers 9 of 15 events</strong> because most meaningful state changes are file changes in .intent/ — and every file change is a git commit.
      </p>

      <div style={{ display: "grid", gap: 12 }}>
        {emissionMechanisms.map(mech => {
          const isExpanded = expanded === mech.id;
          return (
            <div key={mech.id} onClick={() => setExpanded(isExpanded ? null : mech.id)} style={{
              background: COLORS.surface, border: `1px solid ${isExpanded ? mech.color + "60" : COLORS.border}`,
              borderRadius: 8, padding: "18px 20px", cursor: "pointer", transition: "all 0.2s",
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <span style={{ fontSize: 18 }}>{mech.icon}</span>
                  <span style={{ color: mech.color, fontWeight: 600, fontSize: 15 }}>{mech.name}</span>
                  <span style={{ color: COLORS.textDim, fontSize: 12 }}>({mech.covers.length} events)</span>
                </div>
                <span style={{ color: COLORS.textMuted, fontSize: 16 }}>{isExpanded ? "−" : "+"}</span>
              </div>
              <p style={{ color: COLORS.textMuted, fontSize: 13, marginTop: 8 }}>{mech.description}</p>

              {isExpanded && (
                <div style={{ marginTop: 14 }}>
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 14 }}>
                    <div style={{ padding: "10px 14px", background: COLORS.bg, borderRadius: 6 }}>
                      <div style={{ color: mech.color, fontSize: 10, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 6 }}>Events Covered</div>
                      <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                        {mech.covers.map(id => (
                          <code key={id} style={{ color: COLORS.text, fontSize: 11, background: COLORS.surface, padding: "2px 6px", borderRadius: 3, fontFamily: "'SF Mono', monospace" }}>{id}</code>
                        ))}
                      </div>
                    </div>
                    <div style={{ padding: "10px 14px", background: COLORS.bg, borderRadius: 6 }}>
                      <div style={{ color: mech.color, fontSize: 10, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 6 }}>Effort</div>
                      <div style={{ color: COLORS.text, fontSize: 13 }}>{mech.effort}</div>
                    </div>
                  </div>
                  <div style={{ padding: "10px 14px", background: COLORS.bg, borderRadius: 6 }}>
                    <div style={{ color: mech.color, fontSize: 10, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 6 }}>Implementation</div>
                    <div style={{ color: COLORS.text, fontSize: 13, lineHeight: 1.6 }}>{mech.implementation}</div>
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

// ─── Schema Tab ───
function SchemaTab() {
  const baseSchema = {
    version: "1",
    event: "signal.captured",
    timestamp: "2026-03-28T19:42:00Z",
    trace_id: "INT-003",
    span_id: "SIG-006",
    parent_id: null,
    source: { type: "cowork", session_id: "dreamy-keen-faraday", agent: "claude-opus" },
    data: { signal_id: "SIG-006", confidence: "high", title: "..." },
  };

  const fields = [
    { name: "version", type: "string", desc: "Schema version. Always '1' for now. Allows future evolution.", required: true },
    { name: "event", type: "string", desc: "Event type from the catalog (e.g., signal.captured, contract.passed). Dot-namespaced.", required: true },
    { name: "timestamp", type: "ISO 8601", desc: "When the event occurred. UTC.", required: true },
    { name: "trace_id", type: "string", desc: "The Intent ID this event belongs to. This is the OTel trace ID equivalent — it threads through from intent to spec to contract.", required: true },
    { name: "span_id", type: "string", desc: "The specific work unit this event describes (SIG-xxx, SPEC-xxx, CON-xxx). OTel span ID equivalent.", required: true },
    { name: "parent_id", type: "string | null", desc: "The parent work unit. For a signal: null. For a spec: the intent ID. For a contract: the spec ID. This builds the tree.", required: false },
    { name: "source.type", type: "enum", desc: "Where the event originated: cowork, cli, github, scheduled, external.", required: true },
    { name: "source.session_id", type: "string", desc: "Cowork session ID, Entire.io session UUID, or GitHub Action run ID. For traceability.", required: false },
    { name: "source.agent", type: "string", desc: "Which agent or human emitted: claude-opus, claude-code, brien, observe-cycle, etc.", required: false },
    { name: "data", type: "object", desc: "Event-specific payload. Schema varies by event type. Contains the meaningful details.", required: true },
  ];

  return (
    <div>
      <p style={{ color: COLORS.textMuted, fontSize: 14, lineHeight: 1.6, marginBottom: 20 }}>
        Every event shares this base schema. It's designed to be <strong style={{ color: COLORS.text }}>OTel-compatible</strong>: trace_id, span_id, and parent_id form the hierarchy. If we ever migrate to actual OpenTelemetry, these fields map 1:1.
      </p>

      <div style={{ background: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: 8, padding: 20, marginBottom: 24 }}>
        <div style={{ color: COLORS.spec, fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 12 }}>Example Event (events.jsonl)</div>
        <pre style={{ color: COLORS.textMuted, fontSize: 12, fontFamily: "'SF Mono', monospace", lineHeight: 1.6, margin: 0, whiteSpace: "pre-wrap" }}>
{JSON.stringify(baseSchema, null, 2)}
        </pre>
      </div>

      <div style={{ display: "grid", gap: 6 }}>
        {fields.map(f => (
          <div key={f.name} style={{ display: "grid", gridTemplateColumns: "160px 80px 1fr", gap: 12, padding: "10px 14px", background: COLORS.surface, borderRadius: 6, alignItems: "center" }}>
            <code style={{ color: COLORS.spec, fontSize: 12, fontFamily: "'SF Mono', monospace", fontWeight: 600 }}>{f.name}</code>
            <span style={{ color: COLORS.textDim, fontSize: 11 }}>{f.type}{f.required && <span style={{ color: COLORS.danger, marginLeft: 4 }}>*</span>}</span>
            <span style={{ color: COLORS.textMuted, fontSize: 12 }}>{f.desc}</span>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 24, background: COLORS.surface, border: `1px solid ${COLORS.spec}40`, borderRadius: 8, padding: 16 }}>
        <div style={{ color: COLORS.spec, fontSize: 12, fontWeight: 600, marginBottom: 8 }}>OTEL MAPPING</div>
        <p style={{ color: COLORS.textMuted, fontSize: 13, lineHeight: 1.6, margin: 0 }}>
          <code style={{ color: COLORS.text }}>trace_id</code> = OTel Trace ID (the Intent that everything flows from) &nbsp;|&nbsp;
          <code style={{ color: COLORS.text }}>span_id</code> = OTel Span ID (the specific work unit) &nbsp;|&nbsp;
          <code style={{ color: COLORS.text }}>parent_id</code> = OTel Parent Span ID (builds the tree: intent → spec → contract)
        </p>
      </div>

      <div style={{ marginTop: 16, background: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: 8, padding: 16 }}>
        <div style={{ color: COLORS.text, fontSize: 12, fontWeight: 600, marginBottom: 8 }}>STORAGE</div>
        <p style={{ color: COLORS.textMuted, fontSize: 13, lineHeight: 1.6, margin: 0 }}>
          Events are stored as append-only JSONL (one JSON object per line) in <code style={{ color: COLORS.text }}>.intent/events/events.jsonl</code>. Git-tracked, diffable, and readable by any JSON parser. The dashboard reads this file. When the file exceeds ~10MB, rotate to <code style={{ color: COLORS.text }}>events-2026-Q1.jsonl</code>.
        </p>
      </div>
    </div>
  );
}

// ─── Implementation Tab ───
function ImplementationTab() {
  const phases = [
    {
      name: "Phase 0: Manual (Now)",
      color: COLORS.cowork,
      status: "active",
      items: [
        "Cowork sessions generate signal files manually (what we did today)",
        "Human updates YAML frontmatter to change intent/contract status",
        "Pipeline logs already written as structured JSON",
        "Entire.io already captures agent execution traces",
      ],
      output: "Signals exist. Decisions exist. Events are implicit in git history but not structured.",
    },
    {
      name: "Phase 1: GitHub Action (Next)",
      color: COLORS.github,
      status: "ready",
      items: [
        "Create .github/workflows/intent-events.yml",
        "On push: diff .intent/ files → detect new files and frontmatter changes",
        "Emit events to .intent/events/events.jsonl",
        "Covers 9 of 15 events in the catalog",
        "Add event count to signals.html and decisions.html pages",
      ],
      output: "Structured event stream. File-based. Git-tracked. Dashboard-ready.",
    },
    {
      name: "Phase 2: Agent Self-Emission",
      color: COLORS.observe,
      status: "planned",
      items: [
        "Add event emission instructions to observe-cycle.md command",
        "Add post-run event to nightly-refresh-wrapper.sh",
        "Add post-run event to health-check-wrapper.sh",
        "Each writes one JSONL line to .intent/events/events.jsonl",
      ],
      output: "Autonomous agents contribute to the event stream without human intervention.",
    },
    {
      name: "Phase 3: Entire.io Integration",
      color: COLORS.execute,
      status: "planned",
      items: [
        "File watcher on .entire/metadata/ for new sessions",
        "Extract contract references from session prompts",
        "Emit contract.started / contract.passed events",
        "Link Entire session UUIDs to Intent trace IDs",
      ],
      output: "Agent execution events flow into Intent event stream. Full traceability from intent to code.",
    },
    {
      name: "Phase 4: External Signals",
      color: COLORS.external,
      status: "future",
      items: [
        "Zapier: Gmail → new signal file for practitioner responses",
        "Zapier: GitHub stars/issues → market signals",
        "Zapier: Social mentions → awareness signals",
        "Each creates a .intent/signals/ file via GitHub API",
      ],
      output: "External world feeds into the notice layer automatically.",
    },
    {
      name: "Phase 5: OTel Upgrade (If Needed)",
      color: COLORS.spec,
      status: "future",
      items: [
        "Replace JSONL with OpenTelemetry SDK spans",
        "Ship to Grafana Tempo or Jaeger",
        "Dashboard reads from trace backend instead of JSONL",
        "Schema is already trace-shaped — minimal refactoring",
      ],
      output: "Enterprise-grade observability. Only needed if team size or event volume demands it.",
    },
  ];

  return (
    <div>
      <p style={{ color: COLORS.textMuted, fontSize: 14, lineHeight: 1.6, marginBottom: 24 }}>
        Six phases, each additive. The key constraint: <strong style={{ color: COLORS.text }}>Phase 1 alone covers 60% of meaningful events</strong> with a single GitHub Action. Each subsequent phase adds a new emission source without changing the event schema.
      </p>

      <div style={{ position: "relative" }}>
        {phases.map((phase, i) => (
          <div key={i} style={{ display: "flex", gap: 16, marginBottom: 8 }}>
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 24, flexShrink: 0 }}>
              <div style={{
                width: phase.status === "active" ? 18 : 14,
                height: phase.status === "active" ? 18 : 14,
                borderRadius: "50%",
                background: phase.status === "active" ? phase.color : phase.status === "ready" ? phase.color + "80" : COLORS.border,
                border: phase.status === "active" ? `2px solid ${phase.color}` : "none",
                flexShrink: 0,
              }} />
              {i < phases.length - 1 && (
                <div style={{ width: 2, flex: 1, minHeight: 20, background: COLORS.border }} />
              )}
            </div>
            <div style={{
              flex: 1, background: COLORS.surface, border: `1px solid ${phase.status === "active" ? phase.color + "40" : COLORS.border}`,
              borderRadius: 8, padding: "16px 20px", marginBottom: 8,
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
                <span style={{ color: phase.color, fontWeight: 600, fontSize: 14 }}>{phase.name}</span>
                <span style={{
                  fontSize: 10, fontWeight: 600, padding: "2px 8px", borderRadius: 4,
                  color: phase.status === "active" ? COLORS.execute : phase.status === "ready" ? COLORS.signal : COLORS.textDim,
                  background: (phase.status === "active" ? COLORS.execute : phase.status === "ready" ? COLORS.signal : COLORS.textDim) + "15",
                }}>
                  {phase.status === "active" ? "ACTIVE" : phase.status === "ready" ? "READY" : "PLANNED"}
                </span>
              </div>
              {phase.items.map((item, j) => (
                <div key={j} style={{ color: COLORS.textMuted, fontSize: 13, marginBottom: 4, paddingLeft: 12, borderLeft: `2px solid ${phase.color}20` }}>
                  {item}
                </div>
              ))}
              <div style={{ marginTop: 10, padding: "8px 12px", background: COLORS.bg, borderRadius: 4 }}>
                <span style={{ color: phase.color, fontSize: 11, fontWeight: 600 }}>OUTPUT: </span>
                <span style={{ color: COLORS.text, fontSize: 12 }}>{phase.output}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Main ───
export default function IntentEventCatalog() {
  const [activeTab, setActiveTab] = useState("catalog");

  return (
    <div style={{ background: COLORS.bg, color: COLORS.text, minHeight: "100vh", fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}>
      <div style={{ maxWidth: 900, margin: "0 auto", padding: "32px 24px" }}>
        <div style={{ marginBottom: 32 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
            <div style={{
              width: 36, height: 36, borderRadius: 8,
              background: `linear-gradient(135deg, ${COLORS.signal}, ${COLORS.contract})`,
              display: "flex", alignItems: "center", justifyContent: "center",
              color: "white", fontWeight: 800, fontSize: 16,
            }}>⚡</div>
            <div>
              <h1 style={{ margin: 0, fontSize: 22, fontWeight: 700 }}>Intent Event Catalog</h1>
              <p style={{ margin: 0, color: COLORS.textMuted, fontSize: 13 }}>What emits the events — sources, triggers, schemas, and implementation</p>
            </div>
          </div>
        </div>

        <div style={{ display: "flex", gap: 4, marginBottom: 28, borderBottom: `1px solid ${COLORS.border}` }}>
          {tabs.map(tab => (
            <button key={tab.id} onClick={() => setActiveTab(tab.id)} style={{
              padding: "10px 18px", background: "transparent", border: "none",
              borderBottom: `2px solid ${activeTab === tab.id ? COLORS.spec : "transparent"}`,
              color: activeTab === tab.id ? COLORS.text : COLORS.textMuted,
              fontSize: 13, fontWeight: activeTab === tab.id ? 600 : 400, cursor: "pointer", transition: "all 0.2s",
            }}>{tab.label}</button>
          ))}
        </div>

        {activeTab === "catalog" && <EventCatalogTab />}
        {activeTab === "sources" && <EmissionSourcesTab />}
        {activeTab === "schema" && <SchemaTab />}
        {activeTab === "implementation" && <ImplementationTab />}

        <div style={{ marginTop: 40, paddingTop: 16, borderTop: `1px solid ${COLORS.border}`, textAlign: "center" }}>
          <p style={{ color: COLORS.textMuted, fontSize: 11 }}>Intent Event Catalog — what emits, what's captured, and how the system becomes observable</p>
        </div>
      </div>
    </div>
  );
}