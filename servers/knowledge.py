"""
Intent Knowledge Server — The Knowledge Engine
================================================
Compiles raw sources into structured knowledge artifacts (personas,
journeys, DDRs, themes, domain models, design rationale). Provides
ingest, query, and lint operations against a compiled knowledge base.

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
import glob
from datetime import datetime

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
