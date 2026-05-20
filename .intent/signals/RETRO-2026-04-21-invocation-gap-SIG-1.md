---
signal_id: RETRO-2026-04-21-invocation-gap-SIG-1
title: frameworks/intent scripts invocation partially documented at CLAUDE.md — servers/ and observe/adapters/ undocumented
severity: low
detected: 2026-04-21
status: resolved
source: audit-sweep
session_topic: core-scripts-invocation-audit
trust_score: 0.75
autonomy: L2
related:
  - Core/products/org-design-tooling/.intent/signals/RETRO-2026-04-21-prefix-legibility-SIG-1.md
  - Core/products/org-design-tooling/journal/AUDIT-20260421-core-scripts-invocation.md
---
# frameworks/intent invocation documentation gap (partial)

## Observation

`Core/frameworks/intent/` contains 14 Python scripts and has a `CLAUDE.md` — but the invocation coverage is partial. The CLAUDE.md documents only the MCP tool (`tools/intent-mcp/server.py`) with: `Install: pip install mcp pydantic`.

Three other dep-bearing components are undocumented:

**1. `servers/` — requires `fastmcp>=2.0`**
Scripts: `servers/notice.py`, `servers/spec.py`, `servers/observe.py`, `servers/knowledge.py`, `servers/id_gen.py`, `servers/models.py`
Requirements at `servers/requirements.txt`: `fastmcp>=2.0`
CLAUDE.md: silent on this subdirectory.

**2. `observe/adapters/file-tail.py` — requires opentelemetry stack**
Requirements at `observe/adapters/requirements.txt`: `opentelemetry-api>=1.20.0`, `opentelemetry-sdk>=1.20.0`, `opentelemetry-exporter-otlp-proto-grpc>=1.20.0`
CLAUDE.md: silent on this subdirectory.

**3. Root `requirements.txt` — `fastmcp>=2.0`**
The root `requirements.txt` is identical to `servers/requirements.txt`. Relationship between the two is unclear. CLAUDE.md does not reference it.

**Architecture note:** There is no shared `.venv/` — each component has its own requirements file but no dedicated venv is present. The docs imply global install (`pip install mcp pydantic`) without isolation.

## Suggested resolution

Add an `## Invocation` section to `Core/frameworks/intent/CLAUDE.md` covering:
1. Four separate requirements files and what each covers (root, servers/, tools/intent-mcp/, observe/adapters/)
2. Recommended installation: one venv at `Core/frameworks/intent/.venv/` that satisfies all requirements, OR per-component venvs (document which strategy is intended)
3. How to start each server component and the file-tail adapter
4. Clarify whether root `requirements.txt` and `servers/requirements.txt` are intentionally duplicated or one should be removed

## Resolution (2026-04-22)

`## Invocation` section added to `Core/frameworks/intent/CLAUDE.md` covering all 4 components:

- **Root (`./`)** — `fastmcp>=2.0`, setup command documented, root/servers duplication flagged as unresolved
- **`servers/`** — `fastmcp>=2.0`, all 6 scripts listed (notice, spec, observe, knowledge, id_gen, models), per-component venv setup + invocation commands documented
- **`tools/intent-mcp/`** — `mcp>=1.0.0` + `pydantic>=2.0.0`, MCP config registration block added (was previously only a bare `pip install` line)
- **`observe/adapters/`** — full OTel stack (`opentelemetry-api/sdk/exporter-otlp-proto-grpc>=1.20.0`), `file-tail.py` invocation documented with collector dependency note

**Per-component venv status at time of repair:** No venvs exist in any of the 4 locations. All 4 need setup before first invocation. Per-component venv strategy adopted (not a shared root venv).

**Upstream still open:** root vs `servers/` requirements.txt duplication is unresolved — both contain `fastmcp>=2.0` with no clear rationale for two files. A follow-up signal or DDR should decide whether to collapse to one or explicitly justify the split.

## Resolution closure (2026-04-22)

`fastmcp>=2.0` duplication resolved via **Option 2 (consolidate to servers)**. Root `requirements.txt` now contains `-r servers/requirements.txt` (pointer). `servers/requirements.txt` unchanged as the canonical source. `CLAUDE.md` §Invocation §Root updated to reflect delegation. All conditions in this signal are now resolved — status moved to `resolved`.
