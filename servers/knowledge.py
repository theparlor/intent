"""
Intent Knowledge Server — The Knowledge Engine + Substrate Exposure
====================================================================
Compiles raw sources into structured knowledge artifacts (personas,
journeys, DDRs, themes, domain models, design rationale). Provides
ingest, query, and lint operations against a compiled knowledge base.

Per DEC-010 (2026-05-26), the server's scope is extended to cover
cross-surface substrate exposure with five additional read verbs:
    query, get, list, lineage, freshness

Every substrate-exposure verb takes a `scope_token` argument and runs
each response through a binary classification check (per DEC-011 and
substrate-exposure-architecture.md §Phase 1) before returning content.

This is a SEPARABLE product from Intent's methodology loop.
It can be used independently of intent-notice/spec/observe.

Schema:   knowledge-engine/AGENTS.md
Spec:     knowledge-engine/spec/operations.md
Contracts: knowledge-engine/spec/contracts.md

Deploy: fastmcp.cloud or `fastmcp run servers/knowledge.py`
Port: 8004
"""

from fastmcp import FastMCP
from models import (
    KnowledgeArtifactType, make_event,
)
import json
import os
import re
import sys
import glob
from datetime import datetime
from pathlib import Path

# Make the `lib/` sibling package importable when knowledge.py is run
# directly via `python servers/knowledge.py` (the FastMCP convention).
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from lib.classification import (  # noqa: E402
    Classification, ClassificationResolver, ScopeTokenError,
    in_scope, validate_scope_token,
)
from lib.lineage import (  # noqa: E402
    EntityIndex, parse_frontmatter, extract_title, trace_lineage,
)
from lib.library_index_client import (  # noqa: E402
    LibraryIndexClient, repo_keyword_fallback,
)

mcp = FastMCP(
    "intent-knowledge",
    instructions="""You are the Knowledge Engine for the Intent system.
    Your domain is compiled domain knowledge — the persistent, compounding
    understanding that feeds the Spec phase of the Intent loop.

    You manage a compiled knowledge base with six artifact types:
    - Personas (PER): who the users are
    - Journeys (JRN): how they move through experiences
    - Decisions (DDR): what was decided and why
    - Themes (THM): cross-cutting insights from evidence
    - Domain Models (DOM): bounded contexts, glossaries, entities
    - Design Rationale (RAT): why-level reasoning with framework grounding

    Three operations:
    - Ingest: compile raw sources into knowledge artifacts
    - Query: answer questions from compiled knowledge with citations
    - Lint: scan for contradictions, orphans, staleness, coverage gaps

    Schema: knowledge-engine/AGENTS.md
    Every artifact uses YAML frontmatter with: id, type, confidence, origin,
    created, updated. Cross-references use [[wikilinks]].
    Confidence 0.0-1.0. Origin: human | agent | synthetic.
    Agent-originated artifacts start at confidence ≤ 0.5.
    """,
)

# ─── File-backed helpers ─────────────────────────────────────

def _find_intent_root() -> str:
    """Walk up from cwd to find .intent/ directory."""
    d = os.getcwd()
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, ".intent")):
            return d
        d = os.path.dirname(d)
    return os.getcwd()

ROOT = _find_intent_root()
KNOWLEDGE_DIR = os.path.join(ROOT, "knowledge")
RAW_DIR = os.path.join(ROOT, "raw")
INDEX_FILE = os.path.join(KNOWLEDGE_DIR, "_index.md")
LOG_FILE = os.path.join(KNOWLEDGE_DIR, "log.md")
EVENTS_FILE = os.path.join(ROOT, ".intent", "events", "events.jsonl")


def _list_artifacts() -> list[str]:
    """List all knowledge artifact files (excluding navigation files)."""
    skip = {"_index.md", "log.md", "traceability.md"}
    artifacts = []
    for dirpath, _, filenames in os.walk(KNOWLEDGE_DIR):
        for f in filenames:
            if f.endswith(".md") and f not in skip:
                artifacts.append(os.path.join(dirpath, f))
    return sorted(artifacts)


def _read_file(path: str) -> str:
    """Read a file, return empty string if not found."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return ""


def _get_frontmatter_field(content: str, field: str) -> str:
    """Extract a YAML frontmatter field value."""
    match = re.search(rf"^{field}:\s*(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else ""


def _emit_event(event_type: str, ref: str, data: dict):
    """Append event to events.jsonl."""
    os.makedirs(os.path.dirname(EVENTS_FILE), exist_ok=True)
    event = make_event(event_type, "knowledge-engine", ref, data, source="mcp")
    with open(EVENTS_FILE, "a") as f:
        f.write(event + "\n")


def _append_log(entry: str):
    """Append to knowledge log.md."""
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")


def _count_by_type() -> dict[str, int]:
    """Count artifacts by subdirectory type."""
    counts = {}
    for subdir in ["personas", "journeys", "decisions", "themes", "domain-models", "design-rationale"]:
        path = os.path.join(KNOWLEDGE_DIR, subdir)
        if os.path.isdir(path):
            counts[subdir] = len([f for f in os.listdir(path) if f.endswith(".md")])
        else:
            counts[subdir] = 0
    return counts


# ─── MCP Tools ───────────────────────────────────────────────

@mcp.tool()
def knowledge_status() -> str:
    """Get the current state of the compiled knowledge base: artifact counts, average confidence, last ingest, coverage summary."""
    artifacts = _list_artifacts()
    counts = _count_by_type()
    total = len(artifacts)

    # Average confidence
    conf_sum = 0.0
    conf_count = 0
    for path in artifacts:
        content = _read_file(path)
        conf = _get_frontmatter_field(content, "confidence")
        try:
            val = float(conf)
            conf_sum += val
            conf_count += 1
        except (ValueError, TypeError):
            pass

    avg_conf = round(conf_sum / conf_count, 2) if conf_count > 0 else 0.0

    # Last ingest from log
    log_content = _read_file(LOG_FILE)
    last_ingest = "none"
    for line in reversed(log_content.split("\n")):
        if line.startswith("[INGEST]"):
            last_ingest = line
            break

    # Raw source count
    raw_count = 0
    for dirpath, _, filenames in os.walk(RAW_DIR):
        raw_count += sum(1 for f in filenames if f.endswith(".md"))

    result = [
        "# Knowledge Base Status",
        "",
        f"Total artifacts: {total}",
        f"Average confidence: {avg_conf}",
        f"Raw sources: {raw_count}",
        f"Last ingest: {last_ingest}",
        "",
        "## By Type",
    ]
    for subdir, count in counts.items():
        result.append(f"- {subdir}: {count}")

    return "\n".join(result)


@mcp.tool()
def knowledge_ingest(source_path: str) -> str:
    """
    Ingest a raw source file into the compiled knowledge base.

    Reads the source, reads the current index, and returns instructions
    for the LLM to compile the source into knowledge artifacts.

    Args:
        source_path: Path to the source file in raw/ (relative to repo root)
    """
    full_path = os.path.join(ROOT, source_path) if not os.path.isabs(source_path) else source_path

    if not os.path.exists(full_path):
        return f"Error: Source file not found: {source_path}"

    if not full_path.endswith(".md"):
        return f"Warning: Non-markdown source ({source_path}). Only .md supported in v1."

    source_content = _read_file(full_path)
    index_content = _read_file(INDEX_FILE)

    # Check if already ingested
    already_ingested = False
    for artifact_path in _list_artifacts():
        content = _read_file(artifact_path)
        if source_path in content:
            already_ingested = True
            break

    existing_artifacts = []
    for artifact_path in _list_artifacts():
        content = _read_file(artifact_path)
        art_id = _get_frontmatter_field(content, "id")
        art_type = _get_frontmatter_field(content, "type")
        title = ""
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:]
                break
        existing_artifacts.append(f"- {art_id} ({art_type}): {title}")

    result = [
        "# Ingest Request",
        "",
        f"## Source: {source_path}",
        "",
        "### Source Content (first 2000 chars)",
        source_content[:2000],
        "",
        "### Current Knowledge Base State",
        f"Existing artifacts: {len(existing_artifacts)}",
        "",
        "\n".join(existing_artifacts) if existing_artifacts else "(empty knowledge base)",
        "",
    ]

    if already_ingested:
        result.append("⚠ This source appears in existing artifacts. UPDATE existing artifacts, do not create duplicates.")
        result.append("")

    result.extend([
        "### Instructions",
        "",
        "Follow knowledge-engine/AGENTS.md §4.1 (Ingest) and knowledge-engine/spec/operations.md:",
        "",
        "1. Read the full source file",
        "2. For each persona, journey, theme, decision, or domain model mentioned:",
        "   - If artifact exists → update with new evidence, adjust confidence",
        "   - If artifact doesn't exist → create with template from knowledge-engine/templates/",
        "3. Add [[wikilinks]] for cross-references",
        "4. Update knowledge/_index.md with new/modified artifacts",
        "5. Append to knowledge/log.md: [INGEST] date source → created: [list], updated: [list]",
        "",
        "Confidence scoring:",
        "- Single source mention: 0.3",
        "- Corroborated by 2+ sources: 0.5",
        "- Agent-originated: ≤ 0.5 unless corroborated",
    ])

    _emit_event("knowledge.ingested", source_path, {"source": source_path, "status": "requested"})
    _append_log(f"[INGEST] {datetime.utcnow().strftime('%Y-%m-%d')} {source_path} → requested (awaiting agent compilation)")

    return "\n".join(result)


@mcp.tool()
def knowledge_query(question: str) -> str:
    """
    Query the compiled knowledge base. Returns the current index and
    relevant artifact summaries for the LLM to synthesize an answer.

    Args:
        question: The question to answer from compiled knowledge
    """
    index_content = _read_file(INDEX_FILE)

    # Simple keyword matching to find relevant artifacts
    keywords = [w.lower() for w in question.split() if len(w) > 3]
    relevant = []
    for artifact_path in _list_artifacts():
        content = _read_file(artifact_path)
        content_lower = content.lower()
        score = sum(1 for kw in keywords if kw in content_lower)
        if score > 0:
            art_id = _get_frontmatter_field(content, "id")
            title = ""
            for line in content.split("\n"):
                if line.startswith("# "):
                    title = line[2:]
                    break
            relevant.append((score, art_id, title, artifact_path, content[:500]))

    relevant.sort(key=lambda x: -x[0])

    result = [
        "# Query Request",
        "",
        f"**Question:** {question}",
        "",
        "## Current Knowledge Base Index",
        index_content[:3000],
        "",
        f"## Most Relevant Artifacts ({len(relevant)} found)",
        "",
    ]

    for score, art_id, title, path, preview in relevant[:10]:
        rel_path = os.path.relpath(path, ROOT)
        result.extend([
            f"### {art_id}: {title} (relevance: {score})",
            f"Path: {rel_path}",
            preview,
            "",
        ])

    result.extend([
        "## Instructions",
        "",
        "1. Read the relevant artifacts listed above (full content if needed)",
        "2. Synthesize an answer with [[citations]] to specific artifacts",
        "3. If the answer reveals a significant new insight, offer to file as a new THM or RAT artifact",
        "4. If a gap is found, note it for the next lint pass",
    ])

    _emit_event("knowledge.queried", "query", {"question": question, "relevant_count": len(relevant)})
    _append_log(f'[QUERY] {datetime.utcnow().strftime("%Y-%m-%d")} "{question}" → {len(relevant)} artifacts matched')

    return "\n".join(result)


@mcp.tool()
def knowledge_lint() -> str:
    """
    Scan the compiled knowledge base for contradictions, orphans,
    stale claims, missing cross-references, coverage gaps, and
    provenance drift. Returns findings as actionable items.
    """
    artifacts = _list_artifacts()
    findings = []

    # Check 1: Orphans (no inbound references)
    for path in artifacts:
        basename = os.path.splitext(os.path.basename(path))[0]
        refs = 0
        for other_path in artifacts:
            if other_path == path:
                continue
            content = _read_file(other_path)
            if basename in content:
                refs += 1
        if refs == 0:
            rel = os.path.relpath(path, ROOT)
            findings.append(f"ORPHAN: {rel} — no inbound references from other artifacts")

    # Check 2: Missing confidence
    for path in artifacts:
        content = _read_file(path)
        conf = _get_frontmatter_field(content, "confidence")
        if not conf:
            rel = os.path.relpath(path, ROOT)
            findings.append(f"MISSING_FIELD: {rel} — no confidence score")

    # Check 3: Provenance drift (agent artifacts with high confidence)
    for path in artifacts:
        content = _read_file(path)
        origin = _get_frontmatter_field(content, "origin")
        conf = _get_frontmatter_field(content, "confidence")
        if origin in ("agent", "synthetic"):
            try:
                if float(conf) > 0.5:
                    rel = os.path.relpath(path, ROOT)
                    findings.append(f"PROVENANCE: {rel} — origin={origin} but confidence={conf} (>0.5 needs human review)")
            except (ValueError, TypeError):
                pass

    # Check 4: Coverage gaps
    personas_dir = os.path.join(KNOWLEDGE_DIR, "personas")
    journeys_dir = os.path.join(KNOWLEDGE_DIR, "journeys")
    decisions_dir = os.path.join(KNOWLEDGE_DIR, "decisions")

    if os.path.isdir(personas_dir):
        for f in os.listdir(personas_dir):
            if not f.endswith(".md"):
                continue
            content = _read_file(os.path.join(personas_dir, f))
            per_id = _get_frontmatter_field(content, "id")
            # Check if any journey references this persona
            has_journey = False
            if os.path.isdir(journeys_dir):
                for jf in os.listdir(journeys_dir):
                    if not jf.endswith(".md"):
                        continue
                    jcontent = _read_file(os.path.join(journeys_dir, jf))
                    if per_id and per_id in jcontent:
                        has_journey = True
                        break
            if not has_journey and per_id:
                findings.append(f"COVERAGE_GAP: {per_id} has no journey map")

    if os.path.isdir(decisions_dir):
        for f in os.listdir(decisions_dir):
            if not f.endswith(".md"):
                continue
            content = _read_file(os.path.join(decisions_dir, f))
            ddr_id = _get_frontmatter_field(content, "id")
            specs = _get_frontmatter_field(content, "related_specs")
            if not specs or specs == "[]":
                findings.append(f"COVERAGE_GAP: {ddr_id} has no linked spec")

    # Check 5: Index drift
    actual_count = len(artifacts)
    index_content = _read_file(INDEX_FILE)
    match = re.search(r"artifact_count:\s*(\d+)", index_content)
    claimed = int(match.group(1)) if match else 0
    if actual_count != claimed:
        findings.append(f"INDEX_DRIFT: _index.md claims {claimed} artifacts but {actual_count} exist")

    # Format output
    result = [
        "# Knowledge Lint Report",
        f"Scanned: {len(artifacts)} artifacts",
        f"Findings: {len(findings)}",
        "",
    ]

    if findings:
        by_type: dict[str, list[str]] = {}
        for f in findings:
            ftype = f.split(":")[0]
            by_type.setdefault(ftype, []).append(f)

        for ftype, items in sorted(by_type.items()):
            result.append(f"## {ftype} ({len(items)})")
            for item in items:
                result.append(f"- {item}")
            result.append("")
    else:
        result.append("No findings. Knowledge base is clean.")

    result.extend([
        "",
        "---",
        "To create signals from findings: each finding can be captured as a signal",
        "with `source: knowledge-lint` for processing through the Intent loop.",
    ])

    _emit_event("knowledge.linted", "lint", {"findings": len(findings), "artifacts_scanned": len(artifacts)})
    _append_log(f"[LINT] {datetime.utcnow().strftime('%Y-%m-%d')} findings: {len(findings)}")

    return "\n".join(result)


# ─── Dossier types and mappings ──────────────────────────────

DOSSIER_TYPES = {
    "person":   {"prefix": "DSR-PER", "dir": "people",      "skill": "individual-research"},
    "company":  {"prefix": "DSR-COM", "dir": "companies",    "skill": "company-dossier"},
    "product":  {"prefix": "DSR-PRD", "dir": "products",     "skill": "product-analysis"},
    "service":  {"prefix": "DSR-SVC", "dir": "services",     "skill": None},
    "industry": {"prefix": "DSR-IND", "dir": "industries",   "skill": "industry-scan"},
    "context":  {"prefix": "DSR-CTX", "dir": "contexts",     "skill": None},
}


@mcp.tool()
def knowledge_dossier(entity_type: str, name: str) -> str:
    """
    Generate an entity dossier — a structured profile of a person, company,
    product, service, industry, or context. Returns research instructions
    and the template for the LLM to compile.

    Args:
        entity_type: One of: person, company, product, service, industry, context
        name: The name of the entity to research
    """
    if entity_type not in DOSSIER_TYPES:
        return f"Error: Unknown dossier type '{entity_type}'. Valid: {', '.join(DOSSIER_TYPES.keys())}"

    dtype = DOSSIER_TYPES[entity_type]
    dossier_dir = os.path.join(KNOWLEDGE_DIR, "dossiers", dtype["dir"])
    os.makedirs(dossier_dir, exist_ok=True)

    # Get next ID
    max_id = 0
    if os.path.isdir(dossier_dir):
        for f in os.listdir(dossier_dir):
            if f.endswith(".md"):
                content = _read_file(os.path.join(dossier_dir, f))
                fid = _get_frontmatter_field(content, "id")
                try:
                    num = int(fid.split("-")[-1])
                    if num > max_id:
                        max_id = num
                except (ValueError, IndexError):
                    pass
    next_id = max_id + 1
    dossier_id = f"{dtype['prefix']}-{next_id:03d}"

    slug = name.lower().replace(" ", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)

    # Read the template
    template_path = os.path.join(ROOT, "knowledge-engine", "templates", f"dossier-{entity_type}.md")
    template = _read_file(template_path)

    # Check for existing dossier
    existing = None
    for f in os.listdir(dossier_dir) if os.path.isdir(dossier_dir) else []:
        if f.endswith(".md"):
            content = _read_file(os.path.join(dossier_dir, f))
            if name.lower() in content.lower():
                existing = f
                break

    result = [
        "# Dossier Request",
        "",
        f"**Entity:** {name}",
        f"**Type:** {entity_type}",
        f"**ID:** {dossier_id}",
        f"**Output:** knowledge/dossiers/{dtype['dir']}/{dossier_id}-{slug}.md",
        "",
    ]

    if existing:
        result.append(f"⚠ Existing dossier found: {existing}. UPDATE it instead of creating a duplicate.")
        result.append("")

    if dtype["skill"]:
        result.extend([
            f"## Skills Engine Integration",
            "",
            f"Run the `{dtype['skill']}` skill from Core/products/skills-engine/ first:",
            f"  This produces a research output that feeds the dossier template.",
            "",
        ])

    result.extend([
        "## Template",
        "",
        template,
        "",
        "## Instructions",
        "",
        "1. Research the entity using available sources (web search, existing raw/ material, Skills Engine output)",
        "2. Apply depth guarantees (5 checks: adjacent, temporal, contrarian, network, implication)",
        "3. Fill the template with compiled findings",
        "4. Set confidence based on evidence strength",
        "5. Set origin to 'agent' (will need human review for confidence > 0.5)",
        "6. Update knowledge/_index.md and knowledge/log.md",
        "",
        "## Post-Dossier Generation",
        "",
        "After creating the dossier, consider:",
        "- Person dossiers → generate a hero persona (PER-NNN) from the dossier",
        "- Company dossiers → generate domain models (DOM) and themes (THM)",
        "- Industry dossiers → generate themes (THM) and design rationale (RAT)",
        "- Context dossiers → use as engagement scoping for all subsequent work",
    ])

    _emit_event("knowledge.ingested", dossier_id, {
        "type": "dossier", "subtype": entity_type, "name": name, "status": "requested"
    })
    _append_log(f"[DOSSIER] {datetime.utcnow().strftime('%Y-%m-%d')} {entity_type}: {name} → {dossier_id} requested")

    return "\n".join(result)


# ═══════════════════════════════════════════════════════════════════════
# SUBSTRATE EXPOSURE VERBS (DEC-010, 2026-05-26)
# ═══════════════════════════════════════════════════════════════════════
#
# Five new read verbs that expose the .intent/ substrate to chat surfaces
# via the MCP transport. Every verb takes a `scope_token` argument and
# enforces binary classification before returning content (DEC-011 +
# substrate-exposure-architecture.md §Phase 1).
#
# scope_token semantics:
#   "public"               → matches tier=public only
#   "internal"             → matches tier in {public, internal}
#   "engagement:<slug>"    → matches tier in {public, internal,
#                            confidential:<slug-exact>}
#
# Out-of-scope behavior per verb:
#   query     → omit hit from results
#   get       → return error response with reason
#   list      → omit from list
#   lineage   → truncate with explicit boundary marker
#   freshness → return error response with reason

# Recognized canonical-ID prefix patterns.
_CANONICAL_ID_PATTERN = re.compile(
    r"^(SIG|INT|SPEC|CON|DEC|WS-DDR)-[A-Z0-9-]+$",
    re.IGNORECASE,
)

# Type → subdirectory-name(s) under any .intent/ directory the substrate
# exposes. The verbs walk all .intent/ trees under ROOT (multi-product
# substrate), not just the top-level one. `spec/decision-log.md` and
# `knowledge/decisions/` are scanned as extra roots for decision types.
_TYPE_INTENT_SUBDIRS = {
    "signal":   ["signals"],
    "intent":   ["intents"],
    "spec":     ["specs"],
    "decision": ["decisions"],
    "ddr":      ["decisions"],
    "contract": ["contracts"],
}
_TYPE_EXTRA_ROOTS = {
    "spec":     ["spec"],
    "decision": ["knowledge/decisions"],
    "ddr":      ["knowledge/decisions"],
}


def _discover_intent_dirs(root: Path) -> list[Path]:
    """Find every `.intent/` directory under `root`. Multi-product substrate."""
    out: list[Path] = []
    for path in root.rglob(".intent"):
        if path.is_dir():
            out.append(path)
    return out


def _paths_for_type(type_key: str) -> list[str]:
    """Collect every entity-file path for the given type across the substrate."""
    repo_root = Path(ROOT)
    paths: list[str] = []
    intent_subdirs = _TYPE_INTENT_SUBDIRS.get(type_key, [])
    extra_roots = _TYPE_EXTRA_ROOTS.get(type_key, [])

    seen: set[str] = set()
    for intent_dir in _discover_intent_dirs(repo_root):
        for sub in intent_subdirs:
            target = intent_dir / sub
            if not target.is_dir():
                continue
            for f in target.rglob("*.md"):
                if f.name in ("README.md", "INDEX.md", "_index.md"):
                    continue
                if str(f) not in seen:
                    seen.add(str(f))
                    paths.append(str(f))
    for sub in extra_roots:
        target = repo_root / sub
        if not target.is_dir():
            continue
        for f in target.rglob("*.md"):
            if f.name in ("README.md", "INDEX.md", "_index.md"):
                continue
            if str(f) not in seen:
                seen.add(str(f))
                paths.append(str(f))
    return paths


def _make_resolver() -> ClassificationResolver:
    """Per-request classification resolver. Bounded by repo ROOT."""
    return ClassificationResolver(repo_root=Path(ROOT))


def _make_index() -> EntityIndex:
    """Build a fresh entity index keyed by canonical ID."""
    idx = EntityIndex(Path(ROOT))
    idx.build()
    return idx


def _get_entity_path(entity_id: str, index: EntityIndex) -> str | None:
    """Look up the on-disk path for a canonical entity ID."""
    return index.path_for(entity_id)


def _entity_summary(path: str) -> dict:
    """Build a shaped summary (title + id + timestamp + status) from a file."""
    try:
        with open(path) as f:
            content = f.read()
    except OSError:
        return {"path": path, "error": "unreadable"}
    fm = parse_frontmatter(content)
    title = extract_title(content) or fm.get("title", "")
    return {
        "id": (fm.get("id") or "").upper() if fm.get("id") else "",
        "title": title,
        "timestamp": fm.get("timestamp") or fm.get("created") or fm.get("declared_at") or "",
        "status": fm.get("status") or fm.get("maturity") or "",
        "path": os.path.relpath(path, ROOT),
    }


@mcp.tool()
def query(text: str, scope_token: str = "internal", k: int = 10) -> str:
    """
    Top-K relevance-ranked substrate chunks for a text query (substrate exposure).

    Composes with library-index (BM25 + vector) when available; falls back to
    repo-only keyword scoring when not. Every returned hit is run through the
    classification check — out-of-scope hits are omitted from results.

    Args:
        text:         The query string.
        scope_token:  "public" | "internal" | "engagement:<slug>". Default "internal".
        k:            Top-K results. Default 10, max 25.

    Returns:
        JSON: {hits: [...], total_in_scope: N, fallback: bool, library_index_status: str}
    """
    try:
        scope_token = validate_scope_token(scope_token)
    except ScopeTokenError as exc:
        return json.dumps({"error": str(exc), "verb": "query"})

    k = max(1, min(int(k), 25))
    resolver = _make_resolver()

    # Try library-index; fall back to repo keyword walker if it raises.
    # INTENT_KNOWLEDGE_CATALOG override exists so tests can point at a
    # synthetic catalog (or force the fallback path by pointing at a
    # missing file).
    catalog_override = os.environ.get("INTENT_KNOWLEDGE_CATALOG")
    catalog_path = Path(catalog_override) if catalog_override else None
    client = LibraryIndexClient(repo_root=Path(ROOT), catalog_path=catalog_path)
    fallback = False
    li_status = "wired (CATALOG.json depth-sorted; see investigation-2026-05-26)"
    try:
        raw_hits = client.query(text, k=k)
    except NotImplementedError:
        fallback = True
        li_status = "fallback — CATALOG.json unavailable, using repo keyword walker"
        raw_hits = repo_keyword_fallback(Path(ROOT), text, k=k)
    except Exception as exc:  # defensive: never fail the verb
        fallback = True
        li_status = f"fallback — client error: {exc}"
        raw_hits = repo_keyword_fallback(Path(ROOT), text, k=k)

    hits = []
    omitted = 0
    for hit in raw_hits:
        cls = resolver.resolve(hit.path)
        if not in_scope(scope_token, cls):
            omitted += 1
            continue
        hits.append({
            "path": os.path.relpath(hit.path, ROOT) if os.path.isabs(hit.path) else hit.path,
            "chunk": hit.chunk[:800],   # bound chunk length defensively
            "score": hit.score,
            "entity_id": hit.entity_id,
            "tier": cls.tier,
        })
        if len(hits) >= k:
            break

    _emit_event("knowledge.queried", "query", {
        "text": text[:200], "k": k, "hits": len(hits),
        "omitted_oos": omitted, "scope": scope_token, "fallback": fallback,
    })

    return json.dumps({
        "verb": "query",
        "scope_token": scope_token,
        "k": k,
        "hits": hits,
        "total_in_scope": len(hits),
        "omitted_out_of_scope": omitted,
        "fallback_used": fallback,
        "library_index_status": li_status,
    }, indent=2)


@mcp.tool()
def get(entity_id: str, scope_token: str = "internal") -> str:
    """
    Return the full body of one canonical entity (substrate exposure).

    Recognized IDs: SIG-NNN, INT-NNN, SPEC-NNN, CON-NNN, DEC-NNN, WS-DDR-NNN.
    Out-of-scope entities return a 404-equivalent error with reason.

    Args:
        entity_id:    Canonical entity ID.
        scope_token:  "public" | "internal" | "engagement:<slug>". Default "internal".

    Returns:
        JSON: {entity: {id, title, frontmatter, body, path}} or {error, reason}.
    """
    try:
        scope_token = validate_scope_token(scope_token)
    except ScopeTokenError as exc:
        return json.dumps({"error": str(exc), "verb": "get"})

    entity_id = (entity_id or "").upper().strip()
    if not _CANONICAL_ID_PATTERN.match(entity_id):
        return json.dumps({
            "error": "invalid_id",
            "reason": f"{entity_id!r} is not a canonical ID (SIG/INT/SPEC/CON/DEC/WS-DDR-NNN)",
            "verb": "get",
        })

    index = _make_index()
    path = _get_entity_path(entity_id, index)
    if not path:
        return json.dumps({
            "error": "not_found",
            "reason": f"no entity file for {entity_id}",
            "verb": "get",
        })

    resolver = _make_resolver()
    cls = resolver.resolve(path)
    if not in_scope(scope_token, cls):
        return json.dumps({
            "error": "out_of_scope",
            "reason": "entity classification does not match scope_token",
            "scope_token": scope_token,
            "tier": cls.tier,
            "verb": "get",
        })

    try:
        with open(path) as f:
            content = f.read()
    except OSError as exc:
        return json.dumps({
            "error": "read_failed", "reason": str(exc), "verb": "get",
        })

    fm = parse_frontmatter(content)
    title = extract_title(content) or fm.get("title", "")
    body_start = 0
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end >= 0:
            body_start = end + 4

    _emit_event("knowledge.queried", entity_id, {
        "verb": "get", "scope": scope_token, "tier": cls.tier,
    })

    return json.dumps({
        "verb": "get",
        "entity": {
            "id": entity_id,
            "title": title,
            "tier": cls.tier,
            "frontmatter": fm,
            "body": content[body_start:].lstrip(),
            "path": os.path.relpath(path, ROOT),
        },
    }, indent=2, default=str)


@mcp.tool()
def list_entities(
    type: str = "signal",
    filter: str = "",
    scope_token: str = "internal",
    limit: int = 20,
) -> str:
    """
    List entities of a given type as shaped summaries (substrate exposure).

    Returns title + id + timestamp + status only — never full bodies.
    Out-of-scope entries are omitted from the list. Optional substring filter
    applied to title/id.

    Args:
        type:         signal | intent | spec | decision | contract.
        filter:       Substring filter (case-insensitive) on title or id. Optional.
        scope_token:  "public" | "internal" | "engagement:<slug>". Default "internal".
        limit:        Default 20, max 50.

    Returns:
        JSON: {entities: [...], total_in_scope: N, omitted_out_of_scope: N}.
    """
    try:
        scope_token = validate_scope_token(scope_token)
    except ScopeTokenError as exc:
        return json.dumps({"error": str(exc), "verb": "list"})

    limit = max(1, min(int(limit), 50))
    type_key = (type or "").lower().strip()
    if type_key not in _TYPE_INTENT_SUBDIRS:
        return json.dumps({
            "error": "invalid_type",
            "reason": f"type must be one of: {sorted(_TYPE_INTENT_SUBDIRS.keys())}",
            "verb": "list",
        })

    filt = (filter or "").lower().strip()
    resolver = _make_resolver()
    paths = _paths_for_type(type_key)

    entities = []
    omitted = 0
    for path in sorted(paths):
        cls = resolver.resolve(path)
        if not in_scope(scope_token, cls):
            omitted += 1
            continue
        summary = _entity_summary(path)
        if filt:
            hay = (summary.get("title", "") + " " + summary.get("id", "")).lower()
            if filt not in hay:
                continue
        summary["tier"] = cls.tier
        entities.append(summary)
        if len(entities) >= limit:
            break

    _emit_event("knowledge.queried", "list", {
        "verb": "list", "type": type_key, "scope": scope_token,
        "returned": len(entities), "omitted_oos": omitted,
    })

    return json.dumps({
        "verb": "list",
        "type": type_key,
        "scope_token": scope_token,
        "limit": limit,
        "entities": entities,
        "total_in_scope": len(entities),
        "omitted_out_of_scope": omitted,
    }, indent=2, default=str)


@mcp.tool()
def lineage(signal_id: str, scope_token: str = "internal", depth: int = 3) -> str:
    """
    Backward + forward lineage chain for an entity (substrate exposure).

    Walks BACKWARD via caused_by / parent_signal / supersedes, and FORWARD
    via causes / related_intents / promotes_to. Truncates at scope boundaries
    with an explicit "lineage continues outside your scope" marker.

    Args:
        signal_id:    Canonical entity ID (typically SIG-NNN but any works).
        scope_token:  "public" | "internal" | "engagement:<slug>". Default "internal".
        depth:        Traversal depth per direction. Default 3, max 5.

    Returns:
        JSON: {root, backward: [...], forward: [...], truncated_*: bool, scope_marker?}.
    """
    try:
        scope_token = validate_scope_token(scope_token)
    except ScopeTokenError as exc:
        return json.dumps({"error": str(exc), "verb": "lineage"})

    entity_id = (signal_id or "").upper().strip()
    if not _CANONICAL_ID_PATTERN.match(entity_id):
        return json.dumps({
            "error": "invalid_id",
            "reason": f"{entity_id!r} is not a canonical ID",
            "verb": "lineage",
        })

    depth = max(1, min(int(depth), 5))
    index = _make_index()
    root_path = index.path_for(entity_id)
    if not root_path:
        return json.dumps({
            "error": "not_found",
            "reason": f"no entity file for {entity_id}",
            "verb": "lineage",
        })

    resolver = _make_resolver()
    root_cls = resolver.resolve(root_path)
    if not in_scope(scope_token, root_cls):
        return json.dumps({
            "error": "out_of_scope",
            "reason": "root entity is out of scope",
            "scope_token": scope_token,
            "tier": root_cls.tier,
            "verb": "lineage",
        })

    chain = trace_lineage(
        root_id=entity_id,
        index=index,
        resolver=resolver,
        scope_token=scope_token,
        depth=depth,
    )

    _emit_event("knowledge.queried", entity_id, {
        "verb": "lineage", "scope": scope_token, "depth": depth,
        "backward_count": len(chain.backward),
        "forward_count": len(chain.forward),
        "truncated": chain.truncated_backward or chain.truncated_forward,
    })

    return json.dumps({
        "verb": "lineage",
        "scope_token": scope_token,
        **chain.to_dict(),
    }, indent=2, default=str)


@mcp.tool()
def freshness(path: str, scope_token: str = "internal") -> str:
    """
    Last-modified state for a substrate path (substrate exposure).

    Returns mtime + size + classification + (when available) the most recent
    `knowledge.ingested` or `signal.created` event for the path. Out-of-scope
    paths return a 404-equivalent error.

    Args:
        path:         Filesystem path (absolute, or relative to repo root).
        scope_token:  "public" | "internal" | "engagement:<slug>". Default "internal".

    Returns:
        JSON: {path, mtime, size, tier, last_event?} or {error, reason}.
    """
    try:
        scope_token = validate_scope_token(scope_token)
    except ScopeTokenError as exc:
        return json.dumps({"error": str(exc), "verb": "freshness"})

    if not path:
        return json.dumps({
            "error": "invalid_path", "reason": "path is required", "verb": "freshness",
        })

    raw = path
    if not os.path.isabs(raw):
        full = os.path.join(ROOT, raw)
    else:
        full = raw
    full = os.path.abspath(full)

    # Refuse paths that escape ROOT — guards against path traversal.
    if not full.startswith(os.path.abspath(ROOT) + os.sep) and full != os.path.abspath(ROOT):
        return json.dumps({
            "error": "outside_repo",
            "reason": "path resolves outside the substrate repo",
            "verb": "freshness",
        })

    if not os.path.exists(full):
        return json.dumps({
            "error": "not_found", "reason": f"no file at {raw}", "verb": "freshness",
        })

    resolver = _make_resolver()
    cls = resolver.resolve(full)
    if not in_scope(scope_token, cls):
        return json.dumps({
            "error": "out_of_scope",
            "reason": "path classification does not match scope_token",
            "scope_token": scope_token,
            "tier": cls.tier,
            "verb": "freshness",
        })

    stat = os.stat(full)
    mtime_iso = datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z"

    # Best-effort: scan events.jsonl for the last event referencing this path
    last_event = None
    if os.path.exists(EVENTS_FILE):
        rel = os.path.relpath(full, ROOT)
        try:
            with open(EVENTS_FILE) as f:
                # Walk backward for most recent first
                lines = f.readlines()
            for line in reversed(lines):
                line = line.strip()
                if not line:
                    continue
                if rel in line:
                    try:
                        ev = json.loads(line)
                        last_event = {
                            "event": ev.get("event"),
                            "timestamp": ev.get("timestamp"),
                            "ref": ev.get("ref"),
                        }
                        break
                    except json.JSONDecodeError:
                        continue
        except OSError:
            pass

    _emit_event("knowledge.queried", "freshness", {
        "verb": "freshness", "scope": scope_token,
        "path": os.path.relpath(full, ROOT),
    })

    return json.dumps({
        "verb": "freshness",
        "scope_token": scope_token,
        "path": os.path.relpath(full, ROOT),
        "mtime": mtime_iso,
        "size_bytes": stat.st_size,
        "tier": cls.tier,
        "classification_source": cls.source_path,
        "last_event": last_event,
    }, indent=2)


# ─── Entry point ─────────────────────────────────────────────

if __name__ == "__main__":
    import logging

    from port_resolver import resolve_port

    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )
    host, port = resolve_port(
        "intent-knowledge", 8004, port_env="INTENT_KNOWLEDGE_PORT"
    )
    logging.getLogger("intent.knowledge").info(
        "listening on http://%s:%d/mcp", host, port
    )
    mcp.run(transport="streamable-http", host=host, port=port)
