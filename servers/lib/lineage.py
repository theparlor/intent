"""
Lineage traversal — backward + forward chain following entity frontmatter.

Per substrate-exposure-architecture.md (Q4 / DEC-010 verb table):
    lineage(signal_id, depth=3) →
        backward chain (signal → causing events / parent_signal)
        forward chain  (signal → resulting intent → spec)
    Bounded by graph traversal depth (default 3).

Frontmatter fields recognized:
    Backward (parent direction):
        caused_by:        [ID, ID, ...]    — explicit upstream IDs
        parent_signal:    SIG-NNN          — parent signal pointer
        supersedes:       [ID, ID, ...]    — replaced predecessor IDs

    Forward (child direction):
        causes:           [ID, ID, ...]    — explicit downstream IDs
        related_intents:  [INT-NNN, ...]   — signal → intent
        related_signals:  [SIG-NNN, ...]   — generic related (treated as forward
                                              if not a known back-pointer)
        promotes_to:      INT-NNN          — promoted target

A node is "in scope" iff its resolved Classification matches the caller's
scope_token. Out-of-scope nodes truncate the chain at that point and emit a
single explicit marker `"lineage continues outside your scope"` so the caller
sees the boundary instead of silent drop-off.

Lineage assembly does NOT cross scope. This is the lineage-side mirror of
the classification enforcement that `get` / `list` / `query` apply.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .classification import ClassificationResolver, in_scope


# Recognized canonical ID prefixes (DEC-010 + WS-DDR convention)
ID_PATTERN = re.compile(
    r"\b(SIG|INT|SPEC|CON|DEC|WS-DDR)-[A-Z0-9-]+\b",
    re.IGNORECASE,
)

BACKWARD_FIELDS = ("caused_by", "parent_signal", "supersedes")
FORWARD_FIELDS = ("causes", "related_intents", "promotes_to")


@dataclass
class LineageNode:
    """A single node in the lineage graph."""
    entity_id: str
    title: str = ""
    path: Optional[str] = None
    in_scope: bool = True
    direction: str = ""  # "self" | "backward" | "forward"
    depth: int = 0


@dataclass
class LineageChain:
    """Result of a lineage traversal."""
    root: str
    backward: list[LineageNode] = field(default_factory=list)
    forward: list[LineageNode] = field(default_factory=list)
    truncated_backward: bool = False   # at least one out-of-scope node hit walking backward
    truncated_forward: bool = False    # at least one out-of-scope node hit walking forward
    max_depth: int = 3

    def to_dict(self) -> dict:
        return {
            "root": self.root,
            "backward": [
                {"id": n.entity_id, "title": n.title, "path": n.path,
                 "depth": n.depth, "in_scope": n.in_scope}
                for n in self.backward
            ],
            "forward": [
                {"id": n.entity_id, "title": n.title, "path": n.path,
                 "depth": n.depth, "in_scope": n.in_scope}
                for n in self.forward
            ],
            "truncated_backward": self.truncated_backward,
            "truncated_forward": self.truncated_forward,
            "max_depth": self.max_depth,
            "scope_marker": (
                "lineage continues outside your scope"
                if (self.truncated_backward or self.truncated_forward) else None
            ),
        }


# ─── Frontmatter parsing ───────────────────────────────────────

def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from a markdown file. Returns {} if absent or malformed."""
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end < 0:
        return {}
    block = content[3:end].strip()
    # Minimal YAML parse — use pyyaml for robustness
    try:
        import yaml
        data = yaml.safe_load(block) or {}
        if not isinstance(data, dict):
            return {}
        return data
    except Exception:
        return {}


def extract_title(content: str) -> str:
    """Pull the first `# Heading` line. Returns empty string if absent."""
    for line in content.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_refs(value) -> list[str]:
    """
    Normalize a frontmatter value into a list of canonical IDs.
    Accepts:
        - None     → []
        - str      → list of IDs found by ID_PATTERN
        - list     → flattened; each item parsed for IDs
    """
    if value is None:
        return []
    refs: list[str] = []
    if isinstance(value, str):
        refs.extend(m.group(0).upper() for m in ID_PATTERN.finditer(value))
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                refs.extend(m.group(0).upper() for m in ID_PATTERN.finditer(item))
    elif isinstance(value, dict):
        # Some frontmatter uses {ID: note} shape
        for k in value.keys():
            if isinstance(k, str):
                refs.extend(m.group(0).upper() for m in ID_PATTERN.finditer(k))
    # Dedupe preserving order
    seen = set()
    out = []
    for r in refs:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


# ─── Entity index ──────────────────────────────────────────────

class EntityIndex:
    """
    Build an in-memory index mapping canonical entity IDs → filesystem path.
    Walks `.intent/{signals,intents,specs,decisions}/` and
    `spec/decision-log.md` to catalog known IDs.
    """

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root).resolve()
        self._by_id: dict[str, str] = {}
        self._title_cache: dict[str, str] = {}

    def _scan_file_for_id(self, path: Path) -> Optional[str]:
        """Read frontmatter `id:` from a markdown file."""
        try:
            with open(path) as f:
                content = f.read(4096)  # only need frontmatter
        except OSError:
            return None
        fm = parse_frontmatter(content)
        eid = fm.get("id")
        if isinstance(eid, str):
            return eid.upper().strip()
        return None

    def build(self) -> None:
        """Scan every .intent/ tree under the repo for entity files."""
        # Walk all .intent/ directories — multi-product substrate (one repo
        # may host many products each with their own .intent/).
        intent_dirs: list[Path] = []
        for path in self.repo_root.rglob(".intent"):
            if path.is_dir():
                intent_dirs.append(path)

        entity_subdirs = ("signals", "intents", "specs", "decisions", "contracts")
        for intent_dir in intent_dirs:
            for sub in entity_subdirs:
                target = intent_dir / sub
                if not target.is_dir():
                    continue
                for path in target.rglob("*.md"):
                    if path.name in ("README.md", "INDEX.md", "_index.md"):
                        continue
                    eid = self._scan_file_for_id(path)
                    if eid and eid not in self._by_id:
                        self._by_id[eid] = str(path)

        # Also scan the legacy knowledge/decisions tree
        kd = self.repo_root / "knowledge" / "decisions"
        if kd.is_dir():
            for path in kd.rglob("*.md"):
                if path.name in ("README.md", "INDEX.md", "_index.md"):
                    continue
                eid = self._scan_file_for_id(path)
                if eid and eid not in self._by_id:
                    self._by_id[eid] = str(path)

        # Scan decision-log.md for inline DEC-NNN entries
        dec_log = self.repo_root / "spec" / "decision-log.md"
        if dec_log.is_file():
            try:
                with open(dec_log) as f:
                    text = f.read()
            except OSError:
                text = ""
            # Each DEC-NNN: line in the file is a decision atom.
            for match in re.finditer(r"^### (DEC-\d+):", text, re.MULTILINE):
                did = match.group(1).upper()
                if did not in self._by_id:
                    self._by_id[did] = str(dec_log)

    def path_for(self, entity_id: str) -> Optional[str]:
        return self._by_id.get(entity_id.upper())

    def known_ids(self) -> set[str]:
        return set(self._by_id.keys())


# ─── Lineage traversal ─────────────────────────────────────────

def _load_entity(path: str) -> tuple[dict, str]:
    """Read frontmatter dict + title for an entity file."""
    try:
        with open(path) as f:
            content = f.read()
    except OSError:
        return {}, ""
    return parse_frontmatter(content), extract_title(content)


def trace_lineage(
    root_id: str,
    index: EntityIndex,
    resolver: ClassificationResolver,
    scope_token: str,
    depth: int = 3,
) -> LineageChain:
    """
    Build a bounded lineage chain for `root_id`.

    Walks backward through BACKWARD_FIELDS and forward through FORWARD_FIELDS
    up to `depth` hops. Out-of-scope nodes truncate the chain at that node
    (the boundary node is included with in_scope=False; its children are not
    walked) so the caller sees an explicit marker.

    Cycle protection: visited-set dedupe per direction.
    """
    chain = LineageChain(root=root_id.upper(), max_depth=depth)
    root_path = index.path_for(root_id)
    if not root_path:
        return chain  # unknown root — empty chain

    # Walk backward
    visited_back: set[str] = {root_id.upper()}
    _walk(
        node_id=root_id.upper(),
        index=index,
        resolver=resolver,
        scope_token=scope_token,
        fields=BACKWARD_FIELDS,
        out_list=chain.backward,
        visited=visited_back,
        depth=depth,
        cur_depth=1,
        direction="backward",
        truncation_flag=chain,
        flag_attr="truncated_backward",
    )

    # Walk forward
    visited_fwd: set[str] = {root_id.upper()}
    _walk(
        node_id=root_id.upper(),
        index=index,
        resolver=resolver,
        scope_token=scope_token,
        fields=FORWARD_FIELDS,
        out_list=chain.forward,
        visited=visited_fwd,
        depth=depth,
        cur_depth=1,
        direction="forward",
        truncation_flag=chain,
        flag_attr="truncated_forward",
    )

    return chain


def _walk(
    node_id: str,
    index: EntityIndex,
    resolver: ClassificationResolver,
    scope_token: str,
    fields: tuple[str, ...],
    out_list: list[LineageNode],
    visited: set[str],
    depth: int,
    cur_depth: int,
    direction: str,
    truncation_flag: LineageChain,
    flag_attr: str,
) -> None:
    if cur_depth > depth:
        return
    node_path = index.path_for(node_id)
    if not node_path:
        return
    fm, _ = _load_entity(node_path)
    refs: list[str] = []
    for field in fields:
        refs.extend(extract_refs(fm.get(field)))
    for ref in refs:
        if ref in visited:
            continue
        visited.add(ref)
        ref_path = index.path_for(ref)
        if not ref_path:
            # Reference to an entity we don't have a file for — record with no path
            out_list.append(LineageNode(
                entity_id=ref, title="", path=None,
                in_scope=True, direction=direction, depth=cur_depth,
            ))
            continue
        # Check scope on the referenced entity
        cls = resolver.resolve(ref_path)
        node_in_scope = in_scope(scope_token, cls)
        if not node_in_scope:
            # Boundary node: record it with in_scope=False, do NOT recurse
            out_list.append(LineageNode(
                entity_id=ref, title="", path=None,
                in_scope=False, direction=direction, depth=cur_depth,
            ))
            setattr(truncation_flag, flag_attr, True)
            continue
        # In scope — record + recurse
        _fm, title = _load_entity(ref_path)
        out_list.append(LineageNode(
            entity_id=ref, title=title, path=ref_path,
            in_scope=True, direction=direction, depth=cur_depth,
        ))
        _walk(
            node_id=ref,
            index=index,
            resolver=resolver,
            scope_token=scope_token,
            fields=fields,
            out_list=out_list,
            visited=visited,
            depth=depth,
            cur_depth=cur_depth + 1,
            direction=direction,
            truncation_flag=truncation_flag,
            flag_attr=flag_attr,
        )
