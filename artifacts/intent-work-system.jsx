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