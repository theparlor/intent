#!/usr/bin/env python3
"""
Intent Signal Capture MCP Server

An MCP server that lets practitioners capture signals from any MCP-compatible
surface (Claude Code, Cowork, Cursor) directly into .intent/signals/.

Install: pip install mcp pydantic
Run: python server.py (stdio transport for local use)
"""

import os
import re
import json
import glob
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("intent_mcp")

# --- Configuration ---

def find_intent_root(start_path: str = None) -> Optional[Path]:
    """Walk up from start_path to find a directory containing .intent/"""
    current = Path(start_path or os.getcwd()).resolve()
    for _ in range(20):  # max depth
        if (current / ".intent").is_dir():
            return current
        if current.parent == current:
            break
        current = current.parent
    return None


def get_signals_dir(repo_root: Path) -> Path:
    """Get or create the signals directory."""
    signals_dir = repo_root / ".intent" / "signals"
    signals_dir.mkdir(parents=True, exist_ok=True)
    return signals_dir


def get_events_dir(repo_root: Path) -> Path:
    """Get or create the events directory."""
    events_dir = repo_root / ".intent" / "events"
    events_dir.mkdir(parents=True, exist_ok=True)
    return events_dir


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:60].rstrip('-')


def next_signal_id(signals_dir: Path) -> str:
    """Generate the next SIG-XXX ID based on existing signals."""
    existing = list(signals_dir.glob("*.md"))
    max_id = 0
    for f in existing:
        content = f.read_text()
        match = re.search(r'id:\s*SIG-(\d+)', content)
        if match:
            max_id = max(max_id, int(match.group(1)))
    return f"SIG-{max_id + 1:03d}"


# --- Tool Input Models ---

class CaptureSignalInput(BaseModel):
    """Input for capturing a new signal."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    title: str = Field(
        ...,
        description="One-line summary of what was noticed. Be specific: 'OTel traces show 40% contract failure rate' not 'things are broken'.",
        min_length=5,
        max_length=200
    )
    body: Optional[str] = Field(
        default=None,
        description="Optional longer description of the signal — context, evidence, why it might matter."
    )
    confidence: Optional[float] = Field(
        default=None,
        description="How confident are you this signal matters? 0.0 to 1.0. Leave blank if unsure — can be scored later.",
        ge=0.0,
        le=1.0
    )
    source: str = Field(
        default="mcp",
        description="Where this signal was captured from. Auto-set to 'mcp' but can be overridden (e.g., 'slack', 'conversation', 'pr-review')."
    )
    related_intents: Optional[list[str]] = Field(
        default_factory=list,
        description="Optional list of related intent areas (e.g., 'positioning', 'tech-architecture')."
    )
    author: Optional[str] = Field(
        default=None,
        description="Who noticed this signal. Defaults to system user if not provided."
    )
    repo_path: Optional[str] = Field(
        default=None,
        description="Path to the repo root. If not provided, searches upward from current directory for .intent/ directory."
    )


class ListSignalsInput(BaseModel):
    """Input for listing signals."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    limit: int = Field(
        default=10,
        description="Maximum number of signals to return (most recent first).",
        ge=1,
        le=50
    )
    repo_path: Optional[str] = Field(
        default=None,
        description="Path to the repo root. If not provided, searches upward from current directory."
    )


class GetSignalInput(BaseModel):
    """Input for getting a specific signal."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    signal_id: str = Field(
        ...,
        description="Signal ID (e.g., 'SIG-001') or filename slug."
    )
    repo_path: Optional[str] = Field(
        default=None,
        description="Path to the repo root. If not provided, searches upward from current directory."
    )


# --- Tools ---

@mcp.tool(
    name="intent_capture_signal",
    annotations={
        "title": "Capture a Signal",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def capture_signal(params: CaptureSignalInput) -> str:
    """
    Capture an observation as a structured signal in .intent/signals/.

    Use this when you or the practitioner notice something worth recording —
    a pattern in code, an insight from conversation, a problem that keeps
    recurring, or evidence that supports or contradicts a hypothesis.

    The signal is saved as a markdown file with YAML frontmatter and
    optionally emits a signal.created event to the event log.
    """
    # Find repo root
    repo_root = find_intent_root(params.repo_path)
    if not repo_root:
        return "Error: No .intent/ directory found. Run from within an Intent-native repo, or pass repo_path explicitly."

    signals_dir = get_signals_dir(repo_root)
    events_dir = get_events_dir(repo_root)

    # Generate metadata
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    timestamp = now.isoformat()
    signal_id = next_signal_id(signals_dir)
    slug = slugify(params.title)
    filename = f"{date_str}-{slug}.md"
    author = params.author or os.environ.get("USER", "unknown")

    # Build frontmatter
    frontmatter_lines = [
        "---",
        f"id: {signal_id}",
        f"timestamp: {timestamp}",
        f"source: {params.source}",
        f"author: {author}",
    ]
    if params.confidence is not None:
        frontmatter_lines.append(f"confidence: {params.confidence}")
    if params.related_intents:
        frontmatter_lines.append(f"related_intents: [{', '.join(params.related_intents)}]")
    frontmatter_lines.append("---")

    # Build body
    body = f"# {params.title}\n"
    if params.body:
        body += f"\n{params.body}\n"

    # Write signal file
    signal_path = signals_dir / filename
    signal_content = "\n".join(frontmatter_lines) + "\n" + body
    signal_path.write_text(signal_content)

    # Write event to events.jsonl
    event = {
        "version": "0.1.0",
        "event": "signal.created",
        "timestamp": timestamp,
        "trace_id": None,
        "span_id": signal_id,
        "parent_id": None,
        "source": f"mcp-{params.source}",
        "data": {
            "signal_id": signal_id,
            "title": params.title,
            "confidence": params.confidence,
            "author": author,
            "file": str(signal_path.relative_to(repo_root))
        }
    }
    events_file = events_dir / "events.jsonl"
    with open(events_file, "a") as f:
        f.write(json.dumps(event) + "\n")

    return (
        f"Signal captured: {signal_id}\n"
        f"File: {signal_path.relative_to(repo_root)}\n"
        f"Event: signal.created written to .intent/events/events.jsonl\n\n"
        f"To commit: git add {signal_path.relative_to(repo_root)} .intent/events/events.jsonl && git commit -m 'signal: {params.title[:50]}'"
    )


@mcp.tool(
    name="intent_list_signals",
    annotations={
        "title": "List Recent Signals",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def list_signals(params: ListSignalsInput) -> str:
    """
    List recent signals from .intent/signals/, most recent first.

    Use this to review what's been noticed recently, check for patterns
    across signals, or find a signal to link to an intent.
    """
    repo_root = find_intent_root(params.repo_path)
    if not repo_root:
        return "Error: No .intent/ directory found."

    signals_dir = get_signals_dir(repo_root)
    files = sorted(signals_dir.glob("*.md"), reverse=True)[:params.limit]

    if not files:
        return "No signals found in .intent/signals/."

    results = []
    for f in files:
        content = f.read_text()

        # Extract frontmatter fields
        sig_id = "unknown"
        confidence = "unscored"
        source = "unknown"

        id_match = re.search(r'id:\s*(SIG-\d+)', content)
        if id_match:
            sig_id = id_match.group(1)

        conf_match = re.search(r'confidence:\s*([\d.]+)', content)
        if conf_match:
            confidence = conf_match.group(1)

        source_match = re.search(r'source:\s*(\S+)', content)
        if source_match:
            source = source_match.group(1)

        # Extract title (first # heading)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else f.stem

        results.append(f"  {sig_id} | {confidence} | {source} | {title}")

    header = f"  {'ID':<8} | {'Conf':<8} | {'Source':<12} | Title"
    separator = "  " + "-" * 60
    return f"Signals ({len(results)} of {len(files)} shown):\n\n{header}\n{separator}\n" + "\n".join(results)


@mcp.tool(
    name="intent_get_signal",
    annotations={
        "title": "Get Signal Details",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_signal(params: GetSignalInput) -> str:
    """
    Get the full content of a specific signal by ID or filename.

    Use this to read the details of a signal before linking it to an
    intent or when reviewing signal quality.
    """
    repo_root = find_intent_root(params.repo_path)
    if not repo_root:
        return "Error: No .intent/ directory found."

    signals_dir = get_signals_dir(repo_root)

    # Search by ID or slug
    for f in signals_dir.glob("*.md"):
        content = f.read_text()
        if params.signal_id.upper() in content or params.signal_id.lower() in f.name:
            return f"File: {f.relative_to(repo_root)}\n\n{content}"

    return f"Signal '{params.signal_id}' not found in .intent/signals/."


# --- Entry point ---

if __name__ == "__main__":
    mcp.run(transport="stdio")
