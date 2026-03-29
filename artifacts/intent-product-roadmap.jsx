import { useState } from "react";

const PRODUCTS = [
  {
    id: "notice",
    name: "Notice",
    personas: "△◇",
    verb: "capture",
    color: "#f59e0b",
    maturity: "Operational",
    description: "Captures observations — patterns, friction, insights, hunches — from wherever practitioners work, and lands them as structured signals.",
    assets: [
      { name: "Signal schema & template", status: "done" },
      { name: "CLI capture tool", status: "done" },
      { name: "MCP server (Claude Code, Cowork, Cursor)", status: "done" },
      { name: "GitHub Action (event emission)", status: "done" },
      { name: "Quickstart guide", status: "done" },
      { name: "Signal capture architecture", status: "done" },
      { name: "11 founding signals", status: "done" },
      { name: "Slack integration", status: "specced" },
      { name: "GitHub native capture", status: "specced" },
      { name: "ChatGPT / Copilot / Codex plugins", status: "specced" },
      { name: "Signal clustering", status: "not-started" },
      { name: "Signal-to-intent promotion", status: "not-started" },
    ],
    enhance: [
      "Signal deduplication across capture surfaces",
      "Confidence scoring enrichment (frequency, diversity, recency)",
      "Signal review workflow — weekly digest of unclustered signals",
    ],
    build: [
      "Slack bot — reaction-based capture (:signal: emoji → PR)",
      "GitHub issue/PR label capture",
      "Signal-to-intent promotion — 3+ clustered signals suggest an intent",
    ],
    learn: [
      "Do practitioners capture in flow or batch later?",
      "What's the signal-to-noise ratio?",
      "Which capture surfaces generate highest-quality signals?",
    ],
    cli: { cmd: "intent-signal", example: 'intent-signal "What you noticed"' },
  },
  {
    id: "spec",
    name: "Spec",
    personas: "△◇○",
    verb: "shape",
    color: "#3b82f6",
    maturity: "Conceptual",
    description: "Transforms clustered signals into actionable specifications that AI agents can execute against. The shaping layer between noticing and building.",
    assets: [
      { name: "Work ontology (7 levels)", status: "done" },
      { name: "Cross-functional shaping workflow", status: "done" },
      { name: "Intent template", status: "done" },
      { name: "Spec template", status: "done" },
      { name: "Contract template", status: "done" },
      { name: "CLI tools (intent-intent, intent-spec)", status: "done" },
      { name: "Spec validation tooling", status: "not-started" },
      { name: "Spec-to-agent handoff format", status: "not-started" },
    ],
    enhance: [
      "Define 'spec completeness' criteria — agent-ready vs. human-ready",
      "Codify shaping flow into checklist, not just diagram",
    ],
    build: [
      "MCP tools: intent_create_spec, intent_validate_spec",
      "Spec validation CLI — check completeness against criteria",
    ],
    learn: [
      "What's the minimum spec an agent can execute against?",
      "Is the 7-level ontology right, or do teams need fewer levels?",
      "Does cross-functional shaping happen, or does the architect spec solo?",
    ],
    cli: { cmd: "intent-intent / intent-spec", example: 'intent-spec "What to build" --intent INT-001' },
  },
  {
    id: "execute",
    name: "Execute",
    personas: "△◉",
    verb: "build",
    color: "#10b981",
    maturity: "Defined",
    description: "Where AI agents implement against specs. Intent is deliberately thin here — agents bring their own capabilities. Execute ensures specs flow to agents and events flow back.",
    assets: [
      { name: "Event schema for execution events", status: "done" },
      { name: "Agent trace capture", status: "not-started" },
      { name: "Spec-to-agent handoff", status: "not-started" },
      { name: "Contract verification (pre/post)", status: "not-started" },
      { name: "Execution observability", status: "not-started" },
    ],
    enhance: [
      "Refine execution event schema — minimum needed from agents",
    ],
    build: [
      "Agent trace adapter — emit execution events to events.jsonl",
      "Contract verification tool — check implementation against spec",
      "Entire.io integration — bridge agent reasoning into event stream",
    ],
    learn: [
      "How much execution observability do teams want?",
      "Do agents need to read specs natively, or is human translating?",
      "Right boundary between Intent and tools like Entire.io?",
    ],
    cli: { cmd: "—", example: "Planned: intent-exec" },
  },
  {
    id: "observe",
    name: "Observe",
    personas: "◇○",
    verb: "learn",
    color: "#8b5cf6",
    maturity: "Schema-Ready",
    description: "Makes the event stream visible — dashboards, digests, pattern detection, feedback loops. The learning layer that closes the loop back to Notice.",
    assets: [
      { name: "Event schema (OTel-compatible)", status: "done" },
      { name: "Event log format (JSONL)", status: "done" },
      { name: "15 cataloged event types", status: "done" },
      { name: "GitHub Action event emission", status: "done" },
      { name: "Dashboard", status: "not-started" },
      { name: "Signal clustering view", status: "not-started" },
      { name: "Weekly digest / report", status: "not-started" },
      { name: "Metrics framework", status: "not-started" },
    ],
    enhance: [
      "Validate event schema against real data",
      "JSONL → queryable format (even a summary script)",
    ],
    build: [
      "Intent dashboard — signal volume, intent lifecycle, spec rates",
      "Weekly digest generator — summarize event stream",
      "Spec-to-outcome trace — full chain from signal to shipped",
    ],
    learn: [
      "What do leaders want to see? Volume? Throughput? Cycle time?",
      "Is JSONL sufficient, or need a database at team scale?",
      "Does Observe generate new signals (closing the loop)?",
    ],
    cli: { cmd: "intent-status", example: "intent-status roadmap" },
  },
];

const PRIORITIES = {
  now: [
    "Validate Notice end-to-end on real repos",
    "Enable GitHub Pages — make the site live",
    "Use CLI tools on real work: first intents and specs",
  ],
  next: [
    "Intent dashboard v1 — visualize the event stream",
    "Slack signal capture — reaction-based bot",
    "Spec validation — completeness checking",
  ],
  later: [
    "AI tool plugins (ChatGPT, Copilot, Codex)",
    "Agent trace integration (Entire.io bridge)",
    "Signal intelligence (clustering, promotion)",
  ],
};

function StatusDot({ status }) {
  const colors = { done: "#10b981", specced: "#f59e0b", "not-started": "#334155" };
  return (
    <span
      style={{
        width: 8, height: 8, borderRadius: "50%",
        background: colors[status] || "#334155",
        display: "inline-block", marginRight: 8, flexShrink: 0,
      }}
    />
  );
}

function InvestGroup({ label, color, items }) {
  if (!items.length) return null;
  return (
    <div style={{ marginBottom: 16 }}>
      <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.8, color, marginBottom: 6 }}>
        {label}
      </div>
      {items.map((item, i) => (
        <div key={i} style={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 6, padding: "8px 12px", marginBottom: 4, fontSize: 13, color: "#94a3b8", lineHeight: 1.5 }}>
          {item}
        </div>
      ))}
    </div>
  );
}

function ProductCard({ product, isExpanded, onToggle }) {
  const doneCount = product.assets.filter(a => a.status === "done").length;
  const totalCount = product.assets.length;

  return (
    <div
      style={{
        background: "#1e293b", border: `1px solid ${isExpanded ? product.color : "#334155"}`,
        borderRadius: 12, marginBottom: 12, overflow: "hidden",
        transition: "border-color 0.2s",
      }}
    >
      <div
        onClick={onToggle}
        style={{
          padding: "16px 20px", cursor: "pointer", display: "flex",
          alignItems: "center", gap: 12,
        }}
      >
        <span style={{ fontSize: 20 }}>{product.personas}</span>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 700, fontSize: 18, color: product.color }}>{product.name}</div>
          <div style={{ fontSize: 12, color: "#64748b" }}>{product.verb} · {doneCount}/{totalCount} assets ready</div>
        </div>
        <span
          style={{
            fontSize: 11, padding: "3px 10px", borderRadius: 12, fontWeight: 600,
            textTransform: "uppercase", letterSpacing: 0.5,
            background: `${product.color}22`, color: product.color,
          }}
        >
          {product.maturity}
        </span>
        <span style={{ color: "#64748b", fontSize: 18, transform: isExpanded ? "rotate(180deg)" : "rotate(0)", transition: "transform 0.2s" }}>▾</span>
      </div>

      {isExpanded && (
        <div style={{ padding: "0 20px 20px", borderTop: "1px solid #334155" }}>
          <p style={{ color: "#94a3b8", fontSize: 13, lineHeight: 1.6, margin: "16px 0" }}>{product.description}</p>

          {/* Progress bar */}
          <div style={{ background: "#0f172a", borderRadius: 4, height: 6, marginBottom: 16, overflow: "hidden" }}>
            <div style={{ background: product.color, height: "100%", width: `${(doneCount / totalCount) * 100}%`, borderRadius: 4, transition: "width 0.3s" }} />
          </div>

          {/* Assets */}
          <div style={{ marginBottom: 20 }}>
            {product.assets.map((asset, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", padding: "6px 0", fontSize: 13 }}>
                <StatusDot status={asset.status} />
                <span style={{ color: asset.status === "done" ? "#f1f5f9" : "#64748b" }}>{asset.name}</span>
                {asset.status === "specced" && <span style={{ marginLeft: 8, fontSize: 10, color: "#f59e0b", background: "rgba(245,158,11,0.1)", padding: "1px 6px", borderRadius: 8 }}>specced</span>}
              </div>
            ))}
          </div>

          {/* Investments */}
          <InvestGroup label="Enhance" color="#f59e0b" items={product.enhance} />
          <InvestGroup label="Build" color="#10b981" items={product.build} />
          <InvestGroup label="Learn" color="#8b5cf6" items={product.learn} />

          {/* CLI */}
          <div style={{ background: "#0f172a", borderRadius: 8, padding: "10px 14px", marginTop: 8 }}>
            <span style={{ fontSize: 11, color: "#64748b" }}>CLI: </span>
            <code style={{ fontSize: 12, color: "#10b981", fontFamily: "'SF Mono', 'Fira Code', monospace" }}>{product.cli.example}</code>
          </div>
        </div>
      )}
    </div>
  );
}

export default function IntentRoadmap() {
  const [expanded, setExpanded] = useState("notice");
  const [view, setView] = useState("products"); // products | priorities

  return (
    <div style={{ background: "#0f172a", minHeight: "100vh", color: "#f1f5f9", fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}>
      <div style={{ maxWidth: 700, margin: "0 auto", padding: "32px 20px" }}>
        {/* Header */}
        <div style={{ marginBottom: 32 }}>
          <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 4 }}>
            <span style={{ color: "#3b82f6" }}>I</span>ntent Product Roadmap
          </h1>
          <p style={{ color: "#64748b", fontSize: 14 }}>Four products, one value stream. Click a product to explore.</p>
        </div>

        {/* Loop visualization */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 6, marginBottom: 32, flexWrap: "wrap" }}>
          {PRODUCTS.map((p, i) => (
            <div key={p.id} style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <div
                onClick={() => { setExpanded(p.id); setView("products"); }}
                style={{
                  background: expanded === p.id ? `${p.color}15` : "#1e293b",
                  border: `2px solid ${expanded === p.id ? p.color : "#334155"}`,
                  borderRadius: 10, padding: "10px 18px", textAlign: "center",
                  cursor: "pointer", transition: "all 0.2s", minWidth: 100,
                }}
              >
                <div style={{ fontWeight: 700, fontSize: 13, color: p.color }}>{p.name.toUpperCase()}</div>
                <div style={{ fontSize: 10, color: "#64748b" }}>{p.maturity}</div>
              </div>
              {i < PRODUCTS.length - 1 && <span style={{ color: "#334155", fontSize: 16 }}>→</span>}
            </div>
          ))}
        </div>

        {/* View toggle */}
        <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
          {[
            { key: "products", label: "Products" },
            { key: "priorities", label: "Priorities" },
          ].map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setView(key)}
              style={{
                background: view === key ? "#334155" : "transparent",
                border: "1px solid #334155", borderRadius: 6,
                color: view === key ? "#f1f5f9" : "#64748b",
                padding: "6px 14px", fontSize: 12, fontWeight: 600,
                cursor: "pointer", transition: "all 0.2s",
              }}
            >
              {label}
            </button>
          ))}
        </div>

        {/* Products view */}
        {view === "products" && (
          <div>
            {PRODUCTS.map((p) => (
              <ProductCard
                key={p.id}
                product={p}
                isExpanded={expanded === p.id}
                onToggle={() => setExpanded(expanded === p.id ? null : p.id)}
              />
            ))}
          </div>
        )}

        {/* Priorities view */}
        {view === "priorities" && (
          <div>
            {[
              { key: "now", label: "Now", color: "#f59e0b", desc: "This week" },
              { key: "next", label: "Next", color: "#3b82f6", desc: "This month" },
              { key: "later", label: "Later", color: "#64748b", desc: "After validation" },
            ].map(({ key, label, color, desc }) => (
              <div key={key} style={{ marginBottom: 24 }}>
                <div style={{ display: "flex", alignItems: "baseline", gap: 8, marginBottom: 10 }}>
                  <h3 style={{ fontSize: 16, fontWeight: 700, color }}>{label}</h3>
                  <span style={{ fontSize: 11, color: "#475569" }}>{desc}</span>
                </div>
                {PRIORITIES[key].map((item, i) => (
                  <div key={i} style={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 6, padding: "10px 14px", marginBottom: 6, fontSize: 13, color: "#94a3b8", display: "flex", alignItems: "center", gap: 10 }}>
                    <span style={{ color: "#475569", fontWeight: 700, fontSize: 12, minWidth: 18 }}>{i + 1}</span>
                    {item}
                  </div>
                ))}
              </div>
            ))}
          </div>
        )}

        {/* Footer */}
        <div style={{ marginTop: 40, paddingTop: 20, borderTop: "1px solid #1e293b", fontSize: 11, color: "#475569" }}>
          Intent by The Parlor · Source: spec/product-roadmap.md
        </div>
      </div>
    </div>
  );
}
