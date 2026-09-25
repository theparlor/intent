#!/usr/bin/env python3
# cross-engagement-write-guard.sh
#
# PreToolUse hook (matcher: Write|Edit|MultiEdit|NotebookEdit|Bash). Two rules, one for each
# way a session leaks one engagement's work into another:
#
#   1. REPO WRITE, advisory. The session's folder belongs to engagement S and a write lands in
#      engagement T's tree. Warn once per session per T, naming the fix. Never blocks: a
#      granted session worktree of T is a legitimate workaround for one sitting.
#   2. MEMORY WRITE, blocking. A write into the Claude project memory of engagement E
#      (~/.claude/projects/<encoded path of E>/memory/) names people or products that appear in
#      ANOTHER engagement's glossary.md and not in E's own. Engagement names alone ("Subaru",
#      "Johnson Controls") are allowed.
#
# Why this exists:
# - The Claude desktop app opens a session as a worktree of the repo it was launched from,
#   not the repo the task belongs to, and it refuses change_directory for those worktrees.
# - 2026-09-24: a session opened in the JohnsonControls folder did a full day of Subaru work.
#   The files landed correctly in the Subaru repo through a granted folder, but the session
#   wrote three feedback memories naming Subaru client people and a Subaru product into the
#   JohnsonControls project memory, which every later JCI session auto-loads. That breaks
#   the federation rule in AGENTS.md: inherit down, promote up, never leak sideways.
#   Brien noticed the mismatch before any check did.
#   Signal: Work/Consulting/Engagements/JohnsonControls/.intent/signals/
#           SIG-0026-session-opened-in-jci-folder-did-another-engagements-work-2026-09-24.md
# - Rule 2 blocks because a memory leak compounds silently: it loads into every later session
#   of the wrong engagement. Rule 1 only warns because the files themselves can land
#   correctly through a granted folder, and the fix (a handoff, then a new session from the
#   right folder) is a step at the end of the sitting.
#
# Engagement of a path: `Work/Consulting/Engagements/<Name>` or `Work/Advising/Engagements/<Name>`
# under ~/Workspaces (also inside a root-repo desktop worktree). An app worktree
# `<Name>/.claude/worktrees/...` is <Name>; a kit sibling `<Name>-wt-<task>` is <Name>. The
# session engagement comes from the hook input's cwd. A memory dir's engagement comes from its
# encoded project folder name, so the memory of a JCI app worktree session (keyed by the JCI
# primary checkout) resolves to JCI. The reference for rule 2 is the MEMORY DIR's engagement:
# moving a lesson with Subaru names INTO Subaru's memory from a JCI session is the repair,
# not a leak.
#
# Terms, read from every engagement's glossary.md at call time (no client name lives here):
# - Sections are read by heading. A heading about vocabulary, methods, process, quality,
#   documents, finance, policy, measurement and the like is skipped: its terms are shared
#   practice, not identity. People sections (people, roster, stakeholders, names, contacts, or
#   a "Name" column) yield person names, including names inside the row's other cells; org,
#   team, client, vendor, product, program, platform, system and tool sections yield names of
#   teams and products. Anything else yields only terms that carry a non-dictionary word.
# - STRONG terms block on their own: a full person name, a surname of five letters or more,
#   and a team, org or product name that carries a non-dictionary word.
#   WEAK terms: a first name, a short surname, a team name built only of dictionary words
#   ("North Star"), a lone word from a neutral section. One weak hit is an advisory; two or
#   more distinct weak hits block, because a memory that names two of another engagement's
#   people or teams is about that engagement.
# - Never flagged: any form of any engagement's name (folder name, its CamelCase parts, the
#   aliases in the central glossary's engagement table, alias sections, and a glossary row
#   that defines the client itself); a term the memory's own engagement glossary uses anywhere
#   in its text; the central glossary's disambiguated headings; public tool names; the
#   operator's own name (git user.name); dictionary words (/usr/share/dict/words, with plural
#   and tense endings) and all-caps acronyms. Matching is case-sensitive and whole-word, and a
#   line wrap inside a name still matches.
# - The hook is only as good as the glossaries: a person or product missing from its
#   engagement's glossary is invisible here. Adding it there is the fix.
#
# Scope and mechanics:
# - Write/Edit/MultiEdit/NotebookEdit: the file path; memory content is `content`,
#   `new_string`, every `edits[].new_string`, or `new_source`.
# - Bash: targets of clear writes only: output redirections (> >> &>), tee, cp/mv/install/
#   rsync/ln/ditto (the destination; a cp or mv source file's text is scanned for rule 2),
#   touch, mkdir, rm, rmdir, truncate, sed -i and perl -i, git write verbs (commit, add, push,
#   ...) at `git -C` or the effective cwd, and `.agents/bin/session start|land|finish`. A `cd`
#   earlier in the command is honored. Heredoc bodies are stripped before finding targets;
#   for rule 2 the whole command text, heredocs included, is the content.
# - Once-per-session state: ~/.claude/state/cross-engagement-write-guard-warned.json, keyed by
#   session id and target engagement, pruned after 7 days.
# - Output: rule 1, and a single weak rule 2 hit, go out as hookSpecificOutput.additionalContext
#   (the only non-blocking path to the model), rule 1 also as a systemMessage line for Brien;
#   exit 0. A rule 2 block is exit 2 + stderr (PreToolUse convention). The log records counts
#   and engagement names, never the flagged terms.
# - Bypass: CROSS_ENGAGEMENT_WRITE_GUARD_BYPASSED=1 in the environment, or as an inline prefix
#   on a Bash command. Logged.
# - Fails open: an internal error is logged and the call is allowed. A write that touches no
#   engagement and no memory dir costs two path regexes and no file reads.
# - `--selftest` builds a temp Workspaces with fixture engagements (Alpha, Beta, Gamma) and runs
#   the decision table plus end-to-end stdin payloads through this file. It also replays the
#   real 2026-09-24 case when that material is on this machine: the Subaru-side copy of the
#   target-state lesson (filed in Subaru's project memory by the repair), written from a
#   JohnsonControls app worktree into JCI memory, must block; the three repaired JCI memories
#   must stay writable.

import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

BYPASS = "CROSS_ENGAGEMENT_WRITE_GUARD_BYPASSED"
FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
KINDS = ("Consulting", "Advising")
SIGNAL = ("Work/Consulting/Engagements/JohnsonControls/.intent/signals/"
          "SIG-0026-session-opened-in-jci-folder-did-another-engagements-work-2026-09-24.md")
DICT_PATH = "/usr/share/dict/words"
WARN_TTL = 7 * 86400
MAX_SOURCE_BYTES = 200_000

HOME = WORKSPACES = PROJECTS = STATE_FILE = ""


def _configure(home: str) -> None:
    """Point every path at one home. The selftest reconfigures to a fixture home."""
    global HOME, WORKSPACES, PROJECTS, STATE_FILE
    HOME = os.path.normpath(home)
    WORKSPACES = HOME + "/Workspaces"
    PROJECTS = HOME + "/.claude/projects"
    STATE_FILE = HOME + "/.claude/state/cross-engagement-write-guard-warned.json"


_configure(str(Path.home()))


def _log(msg: str) -> None:
    try:
        d = Path(HOME) / ".claude" / "logs"
        d.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with (d / "cross-engagement-write-guard.log").open("a") as fh:
            fh.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


# ---------------------------------------------------------------- engagement resolution

_NAME = r"[A-Za-z0-9][A-Za-z0-9_]*"


def _encode(path: str) -> str:
    """Claude Code's project folder name for a path: every non-alphanumeric becomes '-'."""
    return re.sub(r"[^A-Za-z0-9]", "-", path)


def _abs(path: str, cwd=None) -> str:
    p = os.path.expanduser(str(path))
    p = re.sub(r"^\$\{?HOME\}?(?=/|$)", lambda _m: HOME, p)
    if not os.path.isabs(p):
        p = os.path.join(os.path.expanduser(cwd) if cwd else os.getcwd(), p)
    return os.path.normpath(p)


def _roots():
    ws = os.path.normpath(WORKSPACES)
    real = os.path.realpath(ws)
    return [ws] if real == ws else [ws, real]


def engagement_of(path: str, cwd=None):
    """(kind, name) of the engagement tree a path is in, or None."""
    if not path:
        return None
    p = _abs(path, cwd)
    for cand in dict.fromkeys((p, os.path.realpath(p))):
        for root in _roots():
            m = re.match(re.escape(root) + r"(?:/\.claude/worktrees/[^/]+)?/Work/(Consulting|Advising)"
                         r"/Engagements/([^/]+)(?:/|$)", cand)
            if not m:
                continue
            name = m.group(2).split("-wt-", 1)[0]
            if re.fullmatch(_NAME, name):
                return m.group(1), name
    return None


def memory_dir_of(path: str, cwd=None):
    """(memory_dir, (kind, name) or None) when path is inside ~/.claude/projects/<P>/memory/."""
    if not path:
        return None
    p = _abs(path, cwd)
    proj = os.path.normpath(PROJECTS)
    if not p.startswith(proj + "/"):
        return None
    parts = p[len(proj) + 1:].split("/")
    if len(parts) < 3 or parts[1] != "memory":
        return None
    folder = parts[0]
    eng = None
    for root in _roots():
        enc = _encode(root)
        if folder == enc or folder.startswith(enc + "-"):
            m = re.search(r"-Work-(Consulting|Advising)-Engagements-([A-Za-z0-9]+)", folder[len(enc):])
            if m:
                eng = (m.group(1), m.group(2))
                break
    return os.path.join(proj, folder, "memory"), eng


def primary_of(eng) -> str:
    return f"{WORKSPACES}/Work/{eng[0]}/Engagements/{eng[1]}"


# ---------------------------------------------------------------- glossary terms

VOCAB = re.compile(r"vocab|method|process|quality|defect|decision|style|document|gantt|swim|"
                   r"financ|polic|artifact|provenance|regulat|measure|commercial|contract|conflict|"
                   r"question|reference|practice|channel|positioning|column|\bt&e\b|rule|cadence|"
                   r"footprint|ceremon|metric", re.I)
PEOPLE = re.compile(r"people|person|stakeholder|roster|\bnames?\b|\bwho\b|contacts?", re.I)
ENTITY = re.compile(r"\borg|team|client|vendor|partner|product|platform|program|initiative|"
                    r"system|tool|squad|compan|brand|department|division|customer", re.I)
ALIAS = re.compile(r"alias|name forms", re.I)
CLIENT_ROW = re.compile(r"\b(?:end client|the client\b|client entity|the company|parent company|"
                        r"staffing firm|engagement name)", re.I)
TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9.&'+-]*")
CAPNAME = re.compile(r"\b[A-Z][a-z]+(?: [A-Z][A-Za-z'-]+){1,2}\b")
TLD = re.compile(r"\.(?:com|ai|net|org|io)$", re.I)
# Sentence words that can open a capitalized run in a roster cell ("Not Winston ...").
LEADING = {"A", "An", "And", "The", "Not", "Left", "With", "For", "Both", "Also", "Per", "Via",
           "Former", "Ex", "Was", "Is", "Reports", "Replaced", "Backup", "See", "Plus", "Or"}
CALENDAR = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
            "january", "february", "march", "april", "may", "june", "july", "august",
            "september", "october", "november", "december"}
# Public product and vendor names: never client-confidential, used across every engagement.
PUBLIC = {"jira", "confluence", "rovo", "atlassian", "miro", "slack", "teams", "sharepoint",
          "onedrive", "outlook", "excel", "powerpoint", "word", "microsoft", "google", "gmail",
          "drive", "zoom", "webex", "granola", "harvest", "github", "gitlab", "claude",
          "anthropic", "openai", "chatgpt", "copilot", "servicenow", "salesforce", "workday",
          "azure", "aws", "gcp", "linkedin", "notion", "figma", "lucid", "lucidchart", "visio",
          "tableau", "powerbi", "smartsheet", "asana", "trello", "loom", "screenpipe", "cowork",
          "dynamics", "oracle", "sap", "adobe", "apple", "mac", "macos", "windows", "intune",
          "crowdstrike", "zscaler", "planview", "agiletest", "xray"}
# Fallback when the system word list is missing: enough to keep common words from counting.
BUILTIN_WORDS = set("""a about above after again all also an and any are as at back base be been
before being big board business by can capacity change client day delivery design do done down
each engagement even every first for from full get good great group has have he her here high his
how if in into is it its just last lead let light like line long made make many may me more most
much must my new next no north not now of off on once one only or other our out over own part
people plan platform point portfolio product program project quality real report retail right
road room same see service services she should show so solution solutions some south star state
still such system systems take team than that the their them then there these they this those
three through time to today too two under up us use value very want was way we well were what
when where which while who why will with work would year you your""".split())

_DICT = None


def _dict() -> set:
    global _DICT
    if _DICT is None:
        words = set(BUILTIN_WORDS)
        try:
            with open(DICT_PATH, encoding="utf-8", errors="replace") as fh:
                words.update(w.strip() for w in fh if w[:1].islower())
        except Exception:
            pass
        _DICT = words
    return _DICT


def _is_word(lw: str) -> bool:
    d = _dict()
    if lw in d or lw in CALENDAR:
        return True
    for suf, rep in (("ies", "y"), ("es", ""), ("s", ""), ("ed", ""), ("ed", "e"),
                     ("ing", ""), ("ing", "e"), ("ers", ""), ("er", ""), ("ly", "")):
        if lw.endswith(suf) and len(lw) - len(suf) >= 3:
            b = lw[:-len(suf)] + rep
            if b in d or (len(b) >= 4 and b[-1] == b[-2] and b[:-1] in d):
                return True
    return False


def _norm_token(t: str) -> str:
    t = t.strip(".'&+-")
    t = re.sub(r"'s$", "", t)
    return TLD.sub("", t)


def _generic(t: str) -> bool:
    """A token that says nothing about identity: a word, an acronym, a number, a public tool."""
    t = _norm_token(t)
    if not t or any(ch.isdigit() for ch in t) or t.isupper() or t.lower() in PUBLIC:
        return True
    parts = [p for p in t.split("-") if p]
    return all(len(p) < 3 or _is_word(p.lower()) for p in parts)


def _cells(line: str):
    s = line.strip()
    if not s.startswith("|"):
        return None
    return [c.strip() for c in s.strip("|").split("|")]


def _clean(t: str) -> str:
    return re.sub(r"\s+", " ", t.replace("**", "").replace("__", "").replace("`", "")).strip()


def _alternatives(cell: str):
    """A first cell's name forms: split on ' / ', ';' and ',', parentheticals dropped, quoted
    nicknames kept (a 'Jane Roe ("Janie")' cell gives both)."""
    nick = re.findall(r"[\"“]([^\"”]{2,40})[\"”]", cell)
    base = re.sub(r"\([^)]*\)", "", cell)
    base = re.sub(r"[\"“][^\"”]*[\"”]", "", base)
    out = [a.strip(" .:-*") for a in re.split(r"\s+/\s+|;|,", base)]
    return [a for a in out + nick if a]


def _pattern(term: str):
    words = term.split()
    return re.compile(r"(?<![A-Za-z0-9])" + r"\s+".join(re.escape(w) for w in words) + r"(?![A-Za-z0-9])")


def _read(path: str) -> str:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except Exception:
        return ""


def _engagements():
    """{name: (kind, glossary path or None)} for every engagement primary folder."""
    out = {}
    for kind in KINDS:
        base = f"{WORKSPACES}/Work/{kind}/Engagements"
        try:
            names = sorted(os.listdir(base))
        except Exception:
            continue
        for n in names:
            if "-wt-" in n or not re.fullmatch(_NAME, n) or not os.path.isdir(os.path.join(base, n)):
                continue
            g = os.path.join(base, n, "glossary.md")
            out.setdefault(n, (kind, g if os.path.isfile(g) else None))
    return out


def _central_glossary() -> str:
    for p in (f"{WORKSPACES}/memory/glossary.md", f"{PROJECTS}/{_encode(WORKSPACES)}/memory/glossary.md"):
        if os.path.isfile(p):
            return _read(p)
    return ""


def _operator_tokens() -> set:
    try:
        r = subprocess.run(["git", "config", "--global", "user.name"], capture_output=True,
                           text=True, timeout=3, env=dict(os.environ, HOME=HOME))
        return set(TOKEN.findall(r.stdout.strip())) if r.returncode == 0 else set()
    except Exception:
        return set()


def build_index():
    """(terms, allowed_tokens, glossary_texts).
    terms: list of (term, engagement, weight, why). allowed_tokens: every engagement name form,
    central-glossary heading, and operator name token. glossary_texts: {engagement: text}."""
    engs = _engagements()
    allowed = set(_operator_tokens())
    for n in engs:
        allowed.add(n)
        allowed.update(p for p in re.findall(r"[A-Z][a-z0-9]+|[A-Z]+(?![a-z])", n) if len(p) >= 3)
    central = _central_glossary()
    allowed.update(h.strip() for h in re.findall(r"^###\s+(.+?)\s*$", central, re.M))
    in_table = False
    for line in central.splitlines():
        if re.match(r"\*\*Active engagement glossaries", line):
            in_table = True
            continue
        if in_table:
            c = _cells(line)
            if c is None:
                if line.strip():
                    in_table = False
                continue
            allowed.update(_norm_token(t) for t in TOKEN.findall(_clean(c[0])))

    texts, raw = {}, []
    for name, (_kind, path) in engs.items():
        text = _read(path) if path else ""
        texts[name] = text
        h2 = h3 = ""
        header = None
        for line in text.splitlines():
            if line.startswith("## "):
                h2, h3, header = line, "", None
                continue
            if line.startswith("###"):
                h3, header = line, None
                continue
            c = _cells(line)
            if c is None:
                header = None
                continue
            if header is None:
                header = c
                continue
            if all(re.fullmatch(r":?-{2,}:?", x or "-") for x in c):
                continue
            heads = h2 + " " + h3
            first = _clean(c[0])
            if ALIAS.search(heads) or (len(c) > 1 and CLIENT_ROW.search(c[1])):
                for a in _alternatives(first):
                    allowed.update(_norm_token(t) for t in TOKEN.findall(a))
                continue
            if VOCAB.search(heads):
                continue
            col = header[0].replace("*", "").strip().lower() if header else ""
            people = bool(PEOPLE.search(heads)) or col in ("name", "person", "who")
            entity = people or bool(ENTITY.search(heads))
            raw.append((name, first, c[1:], people, entity))

    def distinct(t):
        return not _generic(t) and _norm_token(t) not in allowed

    terms = {}

    def add(term, eng, weight, why):
        term = term.strip()
        if term and term not in terms:
            terms[term] = (term, eng, weight, why)

    for name, first, rest, people, entity in raw:
        for a in _alternatives(first):
            toks = TOKEN.findall(a)
            if not toks or len(toks) > 5 or not a[:1].isupper():
                continue
            d = [t for t in toks if distinct(t)]
            titled = all(t[:1].isupper() for t in toks)
            if people and 2 <= len(toks) <= 3 and titled and d:
                add(a, name, "strong", "a person")
                last, given = _norm_token(toks[-1]), _norm_token(toks[0])
                if distinct(last):
                    add(last, name, "strong" if len(last) >= 5 else "weak", "a person's surname")
                if distinct(given):
                    add(given, name, "weak", "a person's first name")
            elif len(toks) == 1:
                if d:
                    t = _norm_token(toks[0])
                    if people:
                        add(t, name, "weak", "a person, first name only")
                    elif entity:
                        add(t, name, "strong", "a team, org or product")
                    else:
                        add(t, name, "weak", "a glossary term")
            elif d:
                add(a, name, "strong" if entity else "weak",
                    "a team, org or product" if entity else "a glossary term")
            elif entity and titled and any(_norm_token(t) not in allowed for t in toks):
                add(a, name, "weak", "a team or product name")
        if people:
            for cell in rest:
                for m in CAPNAME.finditer(_clean(cell)):
                    toks = m.group(0).split()
                    while toks and toks[0] in LEADING:
                        toks = toks[1:]
                    if len(toks) >= 2 and distinct(toks[-1]) and len(_norm_token(toks[-1])) >= 3:
                        add(" ".join(toks), name, "strong", "a person")
    return list(terms.values()), allowed, texts


def scan(content: str, own: str, index=None):
    """Foreign glossary terms named in content, judged against engagement `own`.
    Returns (strong_hits, weak_hits), each a list of (term, engagement, why)."""
    terms, _allowed, texts = index or build_index()
    own_text = texts.get(own, "")
    strong, weak, seen = [], [], set()
    for term, eng, weight, why in terms:
        if eng == own or term in seen:
            continue
        pat = _pattern(term)
        if not pat.search(content) or pat.search(own_text):
            continue
        seen.add(term)
        (strong if weight == "strong" else weak).append((term, eng, why))
    # A longer strong hit already covers its parts ("Jane Roe" covers "Jane").
    weak = [w for w in weak if not any(w[0] in s[0].split() for s in strong)]
    return strong, weak


# ---------------------------------------------------------------- bash write targets

_HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
_WRAPPERS = {"sudo", "env", "command", "exec", "nohup", "time", "nice", "caffeinate", "xargs"}
_WRITE_CMDS = {"tee", "touch", "mkdir", "rm", "rmdir", "truncate"}
_DEST_CMDS = {"cp", "mv", "install", "rsync", "ln", "ditto"}
_INPLACE_CMDS = {"sed", "gsed", "perl"}
_GIT_WRITES = {"add", "commit", "mv", "rm", "apply", "am", "merge", "rebase", "cherry-pick",
               "revert", "reset", "restore", "checkout", "switch", "stash", "pull", "push",
               "worktree", "tag", "branch", "init", "clone"}


def _strip_heredocs(cmd: str) -> str:
    out, term = [], None
    for line in cmd.split("\n"):
        if term is not None:
            if line.strip() == term:
                term = None
            continue
        out.append(line)
        m = _HEREDOC.search(line)
        if m:
            term = m.group(2)
    return "\n".join(out)


def _split(seg: str):
    try:
        return shlex.split(seg, comments=True)
    except ValueError:
        return seg.split()


def bash_targets(cmd: str, cwd):
    """(targets, sources): absolute paths a Bash command clearly writes, and cp/mv source files."""
    s = _strip_heredocs(cmd)
    base = os.path.expanduser(cwd) if cwd else os.getcwd()
    targets, sources = [], []
    for seg in re.split(r"&&|\|\||[;\n]", s):
        for red in re.finditer(r"(?:^|[^<>&\d])(?:\d?>>?|&>>?|>\|)\s*([^\s;&|<>()]+)", seg):
            tok = red.group(1).strip("\"'")
            if tok and not tok.startswith("&") and not tok.startswith("/dev/"):
                targets.append(_abs(tok, base))
        for piece in seg.split("|"):
            toks = _split(re.sub(r"\d?>>?\s*\S+|&>>?\s*\S+|<<?-?\s*\S+", " ", piece))
            while toks and (re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", toks[0]) or toks[0] in _WRAPPERS):
                toks = toks[1:]
            if not toks:
                continue
            c = os.path.basename(toks[0])
            args = [t for t in toks[1:] if t and not t.startswith("-") and not re.fullmatch(r"[<>|&]+", t)]
            if c == "cd":
                if args:
                    base = _abs(args[0], base)
                continue
            if c in _WRITE_CMDS:
                targets += [_abs(a, base) for a in args]
            elif c in _DEST_CMDS and args:
                targets.append(_abs(args[-1], base))
                sources += [_abs(a, base) for a in args[:-1]]
            elif c in _INPLACE_CMDS and any(t.startswith("-i") or t.startswith("-pi") for t in toks[1:]):
                targets += [_abs(a, base) for a in args if "/" in a or "." in a]
            elif c == "git":
                where, i = base, 1
                while i < len(toks) and toks[i].startswith("-"):
                    if toks[i] == "-C" and i + 1 < len(toks):
                        where = _abs(toks[i + 1], where)
                        i += 2
                        continue
                    i += 2 if toks[i] == "-c" else 1
                if i < len(toks) and toks[i] in _GIT_WRITES:
                    targets.append(where)
                    if toks[i] in ("worktree", "clone"):
                        targets += [_abs(a, where) for a in toks[i + 1:] if not a.startswith("-")][-1:]
            elif c.startswith("python") and len(toks) > 2 and toks[1].endswith(".agents/bin/session") \
                    and toks[2] in ("start", "land", "finish"):
                targets.append(_abs(toks[1], base))
    return targets, sources


# ---------------------------------------------------------------- decision

def _content_of(payload: dict) -> str:
    ti = payload.get("tool_input") or {}
    parts = [ti.get("content"), ti.get("new_string"), ti.get("new_source")]
    for e in ti.get("edits") or []:
        if isinstance(e, dict):
            parts.append(e.get("new_string"))
    return "\n".join(p for p in parts if isinstance(p, str))


def decide(payload: dict):
    """{'mismatches': [(session_eng, target_eng, path)],
        'memory': [(memory_dir, memory_eng, strong_hits, weak_hits, path)]}"""
    none = {"mismatches": [], "memory": []}
    tool = payload.get("tool_name") or ""
    ti = payload.get("tool_input") or {}
    cwd = payload.get("cwd") or os.getcwd()
    session = engagement_of(cwd)
    if tool in FILE_TOOLS:
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        targets, sources, content = ([_abs(path, cwd)] if path else []), [], None
    elif tool == "Bash":
        cmd = ti.get("command") or ""
        if not session and not any(k in cmd for k in ("Engagements", "projects", ".agents/bin/session")):
            return none
        targets, sources = bash_targets(cmd, cwd)
        content = cmd
    else:
        return none

    mismatches, memory, index = [], [], None
    for t in dict.fromkeys(targets):
        mem = memory_dir_of(t)
        if mem:
            memdir, eng = mem
            if not eng:
                continue
            if content is None:
                content = _content_of(payload)
            text = content
            for src in sources:
                if os.path.isfile(src) and os.path.getsize(src) <= MAX_SOURCE_BYTES:
                    text += "\n" + _read(src)
            index = index or build_index()
            strong, weak = scan(text, eng[1], index)
            if strong or weak:
                memory.append((memdir, eng, strong, weak, t))
            continue
        te = engagement_of(t)
        if session and te and te[1] != session[1] and not any(m[1] == te for m in mismatches):
            mismatches.append((session, te, t))
    return {"mismatches": mismatches, "memory": memory}


# ---------------------------------------------------------------- output

def _warned(session_id: str, eng: str) -> bool:
    """True if this session was already told about eng; records it otherwise."""
    now = time.time()
    try:
        state = json.loads(_read(STATE_FILE) or "{}")
    except Exception:
        state = {}
    state = {s: v for s, v in state.items()
             if isinstance(v, dict) and any(now - ts < WARN_TTL for ts in v.values())}
    seen = state.setdefault(session_id, {})
    if eng in seen:
        return True
    seen[eng] = now
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        tmp = STATE_FILE + ".tmp"
        with open(tmp, "w") as fh:
            json.dump(state, fh)
        os.replace(tmp, STATE_FILE)
    except Exception:
        pass
    return False


def _mismatch_text(session, target, path) -> str:
    prim = primary_of(target)
    return "\n".join([
        f"ADVISORY (cross-engagement-write-guard, not a block): this session's folder belongs to the "
        f"{session[1]} engagement, and this call writes into the {target[1]} engagement ({path}).",
        "Federation rule (AGENTS.md): inherit down, promote up, never leak sideways. A granted session "
        f"worktree of {target[1]} is a legitimate workaround for one sitting. Make it deliberate:",
        f"  1. Work in a {target[1]} session worktree, never its primary checkout:",
        f"       python3 {prim}/.agents/bin/session start <task> --own <path>",
        "     then request_directory on the worktree it prints, and use absolute paths.",
        "  2. Before this session ends, fill <that worktree>/.agents/handoffs/<yyyy-mm-dd>-claude-<task>.md",
        "     (status, outputs, checks, open rulings, safest next action) and land it with session land.",
        f"  3. Move the next round to a new desktop session opened from {prim}. The app cannot move",
        "     this one: change_directory is refused for its worktrees.",
        f"Memory learned here about {target[1]} goes to {PROJECTS}/{_encode(prim)}/memory/, never to "
        f"{session[1]}'s. Tell Brien in one line that the session folder and the task disagree.",
        f"Shown once per session per engagement. Bypass: {BYPASS}=1. Signal: {SIGNAL}",
    ])


def _memory_block_text(eng, strong, weak, path) -> str:
    engs = _engagements()
    others = sorted({e for _t, e, _w in strong + weak})
    homes = [f"{PROJECTS}/{_encode(primary_of((engs.get(o, ('Consulting',))[0], o)))}/memory/" for o in others]
    return "\n".join([
        "",
        "BLOCKED: cross-engagement-write-guard: this memory names another engagement's people or products",
        "",
        f"  Memory:  {path}",
        f"  Owner:   the {eng[1]} engagement (every later {eng[1]} session auto-loads this directory)",
        f"  Names that belong to another engagement's glossary and not to {eng[1]}'s:",
        *[f"    - \"{t}\" ({e} glossary: {why})" for t, e, why in strong + weak],
        "",
        "  Federation rule (AGENTS.md): inherit down, promote up, never leak sideways.",
        "",
        "  Do this instead:",
        "    1. Write the version with the names into that engagement's own project memory:",
        *[f"         {h}" for h in homes],
        "    2. Keep here only a name-free general lesson. Engagement names alone are fine.",
        f"    3. If a flagged name is genuinely {eng[1]} vocabulary too (a person or tool {eng[1]} also",
        f"       has), add it to {primary_of(eng)}/glossary.md and retry: a term {eng[1]}'s own",
        "       glossary uses is never flagged.",
        "",
        "  Bypass only with a reason you would put in the commit message (logged):",
        f"    {BYPASS}=1 in the session environment, or as an inline prefix on a Bash command",
        f"  Signal: {SIGNAL}",
        "",
    ])


def _memory_advice_text(eng, weak, path) -> str:
    t, e, why = weak[0]
    return (f"ADVISORY (cross-engagement-write-guard, not a block): this write to the {eng[1]} project "
            f"memory ({path}) names \"{t}\", which the {e} glossary lists as {why} and {eng[1]}'s glossary "
            f"does not use. If it means {e}'s, reword it or move the lesson to {e}'s project memory; "
            f"one more name from another engagement in the same write would block. If it is {eng[1]} "
            f"vocabulary too, add it to {primary_of(eng)}/glossary.md. Signal: {SIGNAL}")


def _handle(payload: dict) -> int:
    tool = payload.get("tool_name") or ""
    if tool not in FILE_TOOLS and tool != "Bash":
        return 0
    session_id = payload.get("session_id") or os.environ.get("CLAUDE_SESSION_ID") or "unknown"
    if tool == "Bash" and re.search(r"\b" + BYPASS + r"=1\b", (payload.get("tool_input") or {}).get("command") or ""):
        _log(f"BYPASS inline session={session_id}")
        return 0
    result = decide(payload)
    blocks = [m for m in result["memory"] if m[2] or len(m[3]) >= 2]
    if blocks:
        for _memdir, eng, strong, weak, _path in blocks:
            _log(f"BLOCK memory eng={eng[1]} strong={len(strong)} weak={len(weak)} "
                 f"from={sorted({e for _t, e, _w in strong + weak})} session={session_id}")
        print("".join(_memory_block_text(eng, s, w, p) for _d, eng, s, w, p in blocks), file=sys.stderr)
        return 2
    notes, user_lines = [], []
    for _memdir, eng, _strong, weak, path in result["memory"]:
        _log(f"ADVISE memory eng={eng[1]} weak=1 from={weak[0][1]} session={session_id}")
        notes.append(_memory_advice_text(eng, weak, path))
    for session, target, path in result["mismatches"]:
        if _warned(session_id, target[1]):
            continue
        _log(f"WARN repo session_eng={session[1]} target_eng={target[1]} session={session_id} path={path}")
        notes.append(_mismatch_text(session, target, path))
        user_lines.append(f"Session folder is {session[1]}, but this writes into {target[1]}. Fix: the "
                          f"{target[1]} session kit, a filled handoff, then a new session from the "
                          f"{target[1]} folder.")
    if notes:
        out = {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                      "additionalContext": "\n\n".join(notes)}}
        if user_lines:
            out["systemMessage"] = "cross-engagement-write-guard: " + " ".join(user_lines)
        print(json.dumps(out))
    return 0


# ---------------------------------------------------------------- selftest

ALPHA_GLOSSARY = """---
name: Alpha glossary (selftest fixture)
---
# Alpha

## Client and platform

| Term | Meaning |
|------|---------|
| Alpha | Alpha Industries, the client entity |
| Skyloom | The customer platform the team supports |

## People

| Name | Role |
|------|------|
| Morgan Whitlock | Sponsor; also known on the Beta side |
| Zephyrine Okonkwo | Team coach |

## Delivery vocabulary

| Term | Meaning |
|------|---------|
| Definition of Ready | Entry criteria for a sprint |
"""

BETA_GLOSSARY = """---
name: Beta glossary (selftest fixture)
---
# Beta

## Org Structure & Programs

| Term | Meaning | Disambiguation Risk |
|------|---------|---------------------|
| Beta Motors | Beta Motors of America, the end client | none |
| Harbor Light | CRM platform team; reports to Thaddeus Quillfeather | not a metaphor |
| BetaNet | Dealer portal team | none |

## People

| Name | Role | First Observed |
|------|------|----------------|
| Thaddeus Quillfeather | VP over Harbor Light and BetaNet | start |
| Orsolya Brandvik ("Orsi") | First product owner | start |
| Morgan Whitlock | Sponsor-adjacent here too | start |
| Vendor roster | Kestrel Ashdown and Ilse Varnhagen, both vendor developers; Not Otto Pruell | start |

## Program & Planning Vocabulary

| Term | Meaning |
|------|---------|
| Big Rocks | The annual portfolio of large investments |
| Definition of Ready | Entry criteria |
"""

GAMMA_GLOSSARY = """# Gamma

| Term | Meaning |
|------|---------|
| Gamma | Advising client, the client entity |
| Quorvex | The client's own tool |
"""

CENTRAL_GLOSSARY = """# Glossary

**Active engagement glossaries:**
| Engagement | Path |
|------------|------|
| Alpha / ALP | `Work/Consulting/Engagements/Alpha/glossary.md` |
| Beta Motors (BMA) | `Work/Consulting/Engagements/Beta/glossary.md` |

### BRD
| Scope | Meaning |
|-------|---------|
| `general` | Business Requirements Document |
"""

# The 2026-09-24 shape, in fixture names: a lesson learned on Beta work, written from an Alpha
# app worktree into Alpha memory, naming Beta's product team and two Beta people by first name
# or nickname, a person both engagements know (Morgan), and both engagement names.
REPLAY_FIXTURE = """---
name: feedback-target-state-is-destination-not-gate
metadata:
  type: feedback
---
Brien, 24 September, on the Harbor Light planning road trip: the atlas read as a gate.
The pitch to the team is what its leaders need going forward (for Harbor Light: visibility and
predictability for Thaddeus, Orsi, Morgan and the Base team). Filed from an Alpha session on
Beta work; Beta Motors is the client.
"""

NAME_FREE = """---
name: feedback-target-state-is-destination-not-gate
metadata:
  type: feedback
---
When writing a target operating state for another engagement's team, frame it as the destination.
The engagement-specific version lives in the Beta project memory, not here. Alpha coaching work
writes target operating states too, with Morgan and the Skyloom team; Definition of Ready stays.
"""

REAL_SOURCE = "Work/Consulting/Engagements/Subaru"
REAL_SESSION = "Work/Consulting/Engagements/JohnsonControls"
REAL_LESSON = "feedback-target-state-is-destination-not-gate.md"
REAL_REPAIRED = ("feedback-session-folder-must-match-engagement.md",
                 "feedback-target-state-is-destination-not-gate.md",
                 "feedback_deliverables_in_visible_openable_paths.md")


def _write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text)


def _selftest() -> int:
    global _DICT
    real_home = HOME
    results = []

    def check(label, ok, detail=""):
        results.append((bool(ok), label, detail))

    # ---- The real 2026-09-24 replay, when its material is on this machine. No client person
    # or product name is written into this file: the content is read from the Subaru project
    # memory, where the repair filed the version of the lesson that names them.
    src_primary = f"{WORKSPACES}/{REAL_SOURCE}"
    ses_primary = f"{WORKSPACES}/{REAL_SESSION}"
    lesson = f"{PROJECTS}/{_encode(src_primary)}/memory/{REAL_LESSON}"
    ses_mem = f"{PROJECTS}/{_encode(ses_primary)}/memory"
    if os.path.isfile(lesson) and os.path.isfile(f"{src_primary}/glossary.md") and os.path.isdir(ses_primary):
        index = build_index()
        cwd = f"{ses_primary}/.claude/worktrees/replayed-session-2026-09-24"
        text = _read(lesson)
        r = decide({"tool_name": "Write", "cwd": cwd,
                    "tool_input": {"file_path": f"{ses_mem}/{REAL_LESSON}", "content": text}})
        mem = r["memory"]
        s = len(mem[0][2]) if mem else 0
        w = len(mem[0][3]) if mem else 0
        check("REAL replay 2026-09-24: JCI app worktree, the Subaru lesson into JCI memory: blocked",
              s or w >= 2, f"{s} strong, {w} weak hits")
        r = decide({"tool_name": "Write", "cwd": cwd, "tool_input": {"file_path": lesson, "content": text}})
        check("REAL replay: the same lesson into Subaru's own memory, from the JCI session: allowed",
              not r["memory"], f"{len(r['memory'])} memory findings")
        for f in REAL_REPAIRED:
            p = f"{ses_mem}/{f}"
            if not os.path.isfile(p):
                print(f"SKIP real repaired memory {f}: not on this machine")
                continue
            s_hits, w_hits = scan(_read(p), REAL_SESSION.rsplit("/", 1)[1], index)
            check(f"REAL repaired JCI memory stays writable: {f}", not s_hits and len(w_hits) < 2,
                  f"{len(s_hits)} strong, {len(w_hits)} weak")
    else:
        print("SKIP real 2026-09-24 replay: the Subaru lesson or the glossaries are not on this machine")

    tmp = os.path.realpath(tempfile.mkdtemp(prefix="xeng-guard-selftest-"))
    try:
        _configure(os.path.join(tmp, "home"))
        _DICT = None
        eng = f"{WORKSPACES}/Work/Consulting/Engagements"
        adv = f"{WORKSPACES}/Work/Advising/Engagements"
        _write(f"{eng}/Alpha/glossary.md", ALPHA_GLOSSARY)
        _write(f"{eng}/Beta/glossary.md", BETA_GLOSSARY)
        _write(f"{adv}/Gamma/glossary.md", GAMMA_GLOSSARY)
        _write(f"{WORKSPACES}/memory/glossary.md", CENTRAL_GLOSSARY)
        beta_wt = f"{eng}/Beta-wt-2026-09-24-planning"
        os.makedirs(beta_wt, exist_ok=True)
        alpha_wt = f"{eng}/Alpha/.claude/worktrees/harbor-light-planning-b005d6"
        os.makedirs(alpha_wt, exist_ok=True)
        alpha_mem = f"{PROJECTS}/{_encode(eng + '/Alpha')}/memory"
        beta_mem = f"{PROJECTS}/{_encode(eng + '/Beta')}/memory"
        root_mem = f"{PROJECTS}/{_encode(WORKSPACES)}/memory"

        # Engagement resolution.
        for label, path, want in [
            ("primary", f"{eng}/Alpha/working/x.md", "Alpha"),
            ("app worktree", f"{alpha_wt}/working/x.md", "Alpha"),
            ("kit sibling", f"{beta_wt}/x.md", "Beta"),
            ("advising", f"{adv}/Gamma/notes.md", "Gamma"),
            ("root desktop worktree", f"{WORKSPACES}/.claude/worktrees/s1/Work/Consulting/Engagements/Beta/x", "Beta"),
            ("engagements index file", f"{eng}/CONTEXT.md", None),
            ("Core", f"{WORKSPACES}/Core/x.md", None),
            ("outside Workspaces", f"{tmp}/x.md", None),
        ]:
            got = engagement_of(path)
            check(f"resolve {label}", (got[1] if got else None) == want, f"got {got}")
        for label, path, want in [
            ("engagement memory", f"{alpha_mem}/a.md", "Alpha"),
            ("app-worktree project memory", f"{PROJECTS}/{_encode(alpha_wt)}/memory/a.md", "Alpha"),
            ("sibling project memory", f"{PROJECTS}/{_encode(eng + '/Beta-wt-x')}/memory/a.md", "Beta"),
            ("root memory has no engagement", f"{root_mem}/a.md", None),
        ]:
            got = memory_dir_of(path)
            check(f"memory dir {label}", got is not None and (got[1][1] if got[1] else None) == want, f"got {got}")
        check("not a memory dir: a project transcript",
              memory_dir_of(f"{PROJECTS}/{_encode(alpha_wt)}/x.jsonl") is None)

        # Term index.
        terms, allowed, _texts = build_index()
        names = {t[0]: t[2] for t in terms}
        check("index: a full name is strong", names.get("Thaddeus Quillfeather") == "strong")
        check("index: a long surname is strong", names.get("Quillfeather") == "strong")
        check("index: a first name is weak", names.get("Thaddeus") == "weak")
        check("index: a quoted nickname is kept", names.get("Orsi") == "weak")
        check("index: a dictionary-word team name is weak", names.get("Harbor Light") == "weak")
        check("index: a non-dictionary product name is strong", names.get("BetaNet") == "strong")
        check("index: names inside a roster cell", "Kestrel Ashdown" in names and "Otto Pruell" in names,
              f"{sorted(n for n in names if ' ' in n)}")
        check("index: vocabulary sections are skipped", "Big Rocks" not in names and "Definition of Ready" not in names)
        check("index: engagement names are allowed", {"Alpha", "Beta", "Gamma", "Motors"} <= allowed)
        check("index: a client row is an alias, not a term", "Beta Motors" not in names)

        me = os.path.abspath(__file__)

        def run(label, payload, want_rc, want_out, want_warn=False, extra_env=None):
            p = dict(payload)
            p.setdefault("session_id", "selftest-session")
            env = dict(os.environ, HOME=HOME)
            env.pop(BYPASS, None)
            env.update(extra_env or {})
            r = subprocess.run([sys.executable, me], input=json.dumps(p), capture_output=True, text=True,
                               timeout=60, env=env)
            out = r.stdout.strip()
            warn = "cross-engagement-write-guard" in out
            ok = r.returncode == want_rc and bool(out) == want_out and warn == want_warn
            first = (r.stderr.strip().splitlines()[1:2] or [out[:100]])[0][:100]
            check(label, ok, f"rc={r.returncode} stdout={'yes' if out else 'no'} :: {first}")

        # Case 1: the 2026-09-24 shape, in fixture names. Blocked.
        replay = {"tool_name": "Write", "cwd": alpha_wt,
                  "tool_input": {"file_path": f"{alpha_mem}/feedback-target-state.md", "content": REPLAY_FIXTURE}}
        run("REPLAY: Alpha app worktree, a Beta lesson into Alpha memory: blocked", replay, 2, False)
        run("REPLAY via a Bash heredoc into Alpha memory: blocked",
            {"tool_name": "Bash", "cwd": alpha_wt,
             "tool_input": {"command": f"cat > {alpha_mem}/f.md <<'EOF'\n{REPLAY_FIXTURE}EOF"}}, 2, False)
        _write(f"{beta_mem}/lesson.md", REPLAY_FIXTURE)
        run("REPLAY via cp of a Beta memory into Alpha memory: blocked",
            {"tool_name": "Bash", "cwd": alpha_wt,
             "tool_input": {"command": f"cp {beta_mem}/lesson.md {alpha_mem}/lesson.md"}}, 2, False)
        run("bypass env set: the replay write passes", replay, 0, False, extra_env={BYPASS: "1"})
        run("repair: the same lesson into Beta's own memory, from the Alpha session: silent",
            {"tool_name": "Write", "cwd": alpha_wt,
             "tool_input": {"file_path": f"{beta_mem}/feedback-target-state.md", "content": REPLAY_FIXTURE}},
            0, False)
        run("repair: a name-free lesson into Alpha memory (engagement names, own names): silent",
            {"tool_name": "Write", "cwd": alpha_wt,
             "tool_input": {"file_path": f"{alpha_mem}/feedback-target-state.md", "content": NAME_FREE}},
            0, False)
        run("one weak foreign name in Alpha memory: advisory, not a block",
            {"tool_name": "Edit", "cwd": alpha_wt,
             "tool_input": {"file_path": f"{alpha_mem}/x.md", "old_string": "a",
                            "new_string": "Retro note: ask Orsi how the planning went."}}, 0, True, True)
        run("one strong foreign name in Alpha memory (MultiEdit): blocked",
            {"tool_name": "MultiEdit", "cwd": alpha_wt,
             "tool_input": {"file_path": f"{alpha_mem}/x.md",
                            "edits": [{"old_string": "a", "new_string": "Thaddeus Quillfeather said so."}]}},
            2, False)
        run("a non-engagement (root) memory is out of scope",
            {"tool_name": "Write", "cwd": WORKSPACES,
             "tool_input": {"file_path": f"{root_mem}/x.md", "content": REPLAY_FIXTURE}}, 0, False)

        # Case 2: same-engagement writes are silent.
        run("same engagement: Alpha app worktree writes an Alpha primary path: silent",
            {"tool_name": "Write", "cwd": alpha_wt,
             "tool_input": {"file_path": f"{eng}/Alpha/working/notes.md", "content": "x"}}, 0, False)
        run("same engagement: a relative path inside the Alpha worktree: silent",
            {"tool_name": "Edit", "cwd": alpha_wt,
             "tool_input": {"file_path": "working/notes.md", "old_string": "a", "new_string": "b"}}, 0, False)
        run("same engagement: a Bash redirect inside Alpha: silent",
            {"tool_name": "Bash", "cwd": alpha_wt,
             "tool_input": {"command": f"echo hi > {eng}/Alpha/working/x.txt"}}, 0, False)

        # Case 3: a cross-engagement repo write warns exactly once per session.
        run("cross engagement: Alpha session writes into a Beta sibling: one warning",
            {"tool_name": "Write", "cwd": alpha_wt,
             "tool_input": {"file_path": f"{beta_wt}/atlas.md", "content": "x"}}, 0, True, True)
        run("cross engagement: a second Beta write, same session: silent",
            {"tool_name": "Edit", "cwd": alpha_wt,
             "tool_input": {"file_path": f"{beta_wt}/atlas.md", "old_string": "x", "new_string": "y"}}, 0, False)
        run("cross engagement: a Bash git commit in Beta, same session: silent",
            {"tool_name": "Bash", "cwd": alpha_wt,
             "tool_input": {"command": f"git -C {beta_wt} commit -m x"}}, 0, False)
        run("cross engagement: a new session is warned again (cd, then git commit)",
            {"tool_name": "Bash", "cwd": alpha_wt, "session_id": "selftest-session-2",
             "tool_input": {"command": f"cd {beta_wt} && git commit -m x"}}, 0, True, True)
        run("cross engagement: the kit start in another engagement warns",
            {"tool_name": "Bash", "cwd": alpha_wt, "session_id": "selftest-session-3",
             "tool_input": {"command": f"python3 {adv}/Gamma/.agents/bin/session start plan --own x"}},
            0, True, True)
        run("cross engagement: a read-only Bash command is silent",
            {"tool_name": "Bash", "cwd": alpha_wt, "session_id": "selftest-session-4",
             "tool_input": {"command": f"cat {eng}/Beta/glossary.md && git -C {eng}/Beta status"}}, 0, False)
        run("cross engagement: a heredoc that only mentions a Beta path is silent",
            {"tool_name": "Bash", "cwd": alpha_wt, "session_id": "selftest-session-4",
             "tool_input": {"command": f"git commit -F - <<'EOF'\ntouch {eng}/Beta/x\nEOF"}}, 0, False)
        run("a session outside any engagement writes into Beta: silent",
            {"tool_name": "Write", "cwd": f"{WORKSPACES}/Core", "session_id": "selftest-session-5",
             "tool_input": {"file_path": f"{eng}/Beta/x.md", "content": "x"}}, 0, False)
        run("an inline bypass on Bash is silent",
            {"tool_name": "Bash", "cwd": alpha_wt, "session_id": "selftest-session-6",
             "tool_input": {"command": f"{BYPASS}=1 touch {eng}/Beta/x.md"}}, 0, False)
        run("other tools are ignored",
            {"tool_name": "Read", "cwd": alpha_wt, "tool_input": {"file_path": f"{eng}/Beta/x.md"}}, 0, False)

        # Bash target parsing.
        t, _s = bash_targets(f"cd {eng}/Beta && echo x >> notes.md 2>&1 && tee -a {tmp}/log < /dev/null", alpha_wt)
        check("bash: cd, then a relative redirect, resolves into Beta", f"{eng}/Beta/notes.md" in t, f"{t}")
        check("bash: 2>&1 and < are not targets",
              not any(x.endswith(("/1", "&1", "/<")) for x in t), f"{t}")
        t, _s = bash_targets(f"sed -i '' 's/a/b/' {eng}/Beta/x.md", alpha_wt)
        check("bash: the file of sed -i is a target", f"{eng}/Beta/x.md" in t, f"{t}")
    finally:
        _configure(real_home)
        _DICT = None
        subprocess.run(["rm", "-rf", tmp], timeout=30)

    bad = 0
    for ok, label, detail in results:
        bad += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} {label}{' :: ' + detail if detail else ''}")
    print(f"selftest {len(results) - bad}/{len(results)}")
    return 0 if bad == 0 else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()
    if os.environ.get(BYPASS) == "1":
        _log(f"BYPASS env session={os.environ.get('CLAUDE_SESSION_ID', 'unknown')}")
        return 0
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        return _handle(json.loads(raw))
    except Exception as e:  # a guard bug must never wedge writes
        _log(f"ERROR fail-open {type(e).__name__}: {e}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
