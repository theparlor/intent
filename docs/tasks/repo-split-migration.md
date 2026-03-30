# Task: Split intent-site into its own repository

> Migration spec for separating the marketing/documentation site from the product repo.
> **Mixed execution:** Some steps require human action (repo creation, GitHub Pages config). Terminal handles file moves and commits.

## Why

The product repo (`theparlor/intent`) should contain only the methodology, CLI tools, MCP servers, and signal pipeline — what someone clones to *use* Intent. The marketing and documentation site is a separate concern with a separate audience. Consumers of the framework should not pull down HTML pages, SVG radar visuals, and site governance specs.

## Target State

**`theparlor/intent`** (product repo) — what people clone to adopt Intent
```
intent/
├── .intent/           ← Dogfood: Intent's own signals, intents, specs, events
├── bin/               ← CLI tools (intent-signal, intent-intent, intent-spec, intent-status)
├── tools/             ← MCP server
├── spec/              ← Methodology specs (source of truth for all content)
├── artifacts/         ← React JSX artifacts
├── notice/            ← Loop directories
├── execute/
├── observe/
├── reference/
├── CLAUDE.md          ← Product-focused (remove site-specific sections)
├── CHANGELOG.md
├── VERSION
├── README.md          ← Updated: points to live site for docs/marketing
└── TASKS.md
```

No `docs/` folder. No HTML. No CSS. No site governance files.

**`theparlor/intent-site`** (site repo) — what powers theparlor.github.io/intent/
```
intent-site/
├── docs/              ← GitHub Pages source (or root-level, TBD)
│   ├── *.html         ← All 18 pages
│   ├── styles.css
│   └── visual-brief-app/
├── site-ia.md         ← IA specification
├── site-spec.md       ← Page inventory and baselines
├── site-contracts.md  ← Verifiable assertions
├── content-map.md     ← Traces site claims → product repo specs (NEW)
├── tasks/             ← Handoff task specs
├── CLAUDE.md          ← Site-focused agent instructions
└── README.md          ← Site development guide
```

## Migration Steps

### Phase 1: Create the site repo (HUMAN REQUIRED)

Brien must:
1. Create `theparlor/intent-site` on GitHub (public repo, no template, no README)
2. Enable GitHub Pages: Settings → Pages → Source: main branch, `/docs` folder (or root)

**Decision needed:** Should the site URL stay at `theparlor.github.io/intent/` or move to `theparlor.github.io/intent-site/`? Keeping the original URL requires either:
- A custom domain, OR
- Using the `intent` repo's GitHub Pages as a redirect to the new repo, OR
- Renaming the site repo to `intent-site` and accepting the new URL

### Phase 2: Populate the site repo (TERMINAL)

```bash
# Clone the new empty repo
cd ~/Workspaces/Core/frameworks
git clone git@github.com:theparlor/intent-site.git
cd intent-site

# Copy site files from product repo
cp -r ~/Workspaces/Core/frameworks/intent/docs ./docs
cp ~/Workspaces/Core/frameworks/intent/docs/site-ia.md ./site-ia.md
cp ~/Workspaces/Core/frameworks/intent/docs/site-spec.md ./site-spec.md
cp ~/Workspaces/Core/frameworks/intent/docs/site-contracts.md ./site-contracts.md

# Move task specs out of docs
mkdir tasks
cp -r ~/Workspaces/Core/frameworks/intent/docs/tasks/* ./tasks/
rm -rf ./docs/tasks
rm ./docs/site-ia.md ./docs/site-spec.md ./docs/site-contracts.md
```

### Phase 3: Create site-specific CLAUDE.md (TERMINAL)

Create a new `CLAUDE.md` in the site repo root that contains ONLY the site-relevant sections from the product repo's CLAUDE.md:
- Design System (palette, persona colors)
- Site Information Architecture (IA v2 — Three Pillars) — full section
- CSS Strategy — CRITICAL RULES
- Content Preservation Rules
- Footer pattern
- Agent Handoff Protocol (site-focused version)
- Site IA Implementation Notes

Strip all product-specific content (CLI tools, MCP server, repo structure for `.intent/`, event system, deployment topology, etc.)

### Phase 4: Create content-map.md (TERMINAL)

This is the bridge between the two repos. It maps every factual claim the site makes to its source of truth in the product repo.

```markdown
# Content Map — intent-site ↔ intent

> Maps site content claims to their source of truth in the product repo.
> When the product repo changes, this map identifies which site pages need updating.

## Source: spec/signal-trust-framework.md
| Site page | Claim | Quote/reference |
|-----------|-------|-----------------|
| architecture.html | Trust formula | "clarity × 0.30 + ..." |
| architecture.html | L0-L4 autonomy levels | Trust table |
| arb.html | Tech radar items | Adopt/Trial/Assess/Hold technologies |
| signals.html | Trust scoring on signal cards | Confidence and trust scores |

## Source: spec/intent-methodology.md
| Site page | Claim | Quote/reference |
|-----------|-------|-----------------|
| pitch.html | The four-phase loop | Notice→Spec→Execute→Observe |
| methodology.html | Full methodology explanation | Entire page |
| flow-diagram.html | Loop diagram | SVG + phase cards |

## Source: spec/event-catalog.md
| Site page | Claim | Quote/reference |
|-----------|-------|-----------------|
| event-catalog.html | Event types | Full page |
| dogfood.html | Event stream | Live events section |

## Source: spec/product-roadmap.md
| Site page | Claim | Quote/reference |
|-----------|-------|-----------------|
| roadmap.html | Phase timeline and items | Full page |
| arb.html | Atomized Roadmap tab | Phase cards |

## Source: bin/ (CLI tools)
| Site page | Claim | Quote/reference |
|-----------|-------|-----------------|
| flow-diagram.html | CLI tool references | intent-signal, intent-spec |
| work-system.html | CLI commands | Status, signal management |

## Source: tools/intent-mcp/server.py
| Site page | Claim | Quote/reference |
|-----------|-------|-----------------|
| architecture.html | MCP server ports and tools | Server cards, tool lists |
| deployment.html | FastMCP deployment | Configuration blocks |
```

### Phase 5: Clean the product repo (TERMINAL)

```bash
cd ~/Workspaces/Core/frameworks/intent

# Remove docs/ entirely
rm -rf docs/

# Update CLAUDE.md — remove site-specific sections, keep product-only
# Add pointer: "Site: see theparlor/intent-site repo"

# Update README.md — add link to live site
# "Documentation and marketing site: https://theparlor.github.io/intent/"

git add -A
git commit -m "Remove docs/ — site moved to theparlor/intent-site

The marketing and documentation site now lives in its own repo
(theparlor/intent-site). This repo contains only the methodology,
CLI tools, MCP servers, and signal pipeline — what teams clone
to adopt Intent.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push origin main
```

### Phase 6: First site repo commit (TERMINAL)

```bash
cd ~/Workspaces/Core/frameworks/intent-site

git add -A
git commit -m "Initial commit — Intent marketing and documentation site

Migrated from theparlor/intent/docs. Three-pillar IA (The Story,
The System, The Build). 18 pages, unified CSS strategy, verifiable
site contracts, content map tracing claims to product repo specs.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push origin main
```

### Phase 7: Verify (TERMINAL)

```bash
cd ~/Workspaces/Core/frameworks/intent-site

# Run all site contracts
# (execute each contract from site-contracts.md, adjusting paths as needed)

# Verify GitHub Pages is serving
curl -s -o /dev/null -w "%{http_code}" https://theparlor.github.io/intent-site/
# Should return 200 (once Pages is enabled)
```

## Verification Checklist

- [ ] `theparlor/intent-site` repo exists and is public
- [ ] GitHub Pages enabled and serving
- [ ] All 18 HTML pages present in site repo
- [ ] styles.css and visual-brief-app/ present
- [ ] site-ia.md, site-spec.md, site-contracts.md at repo root (not in docs/)
- [ ] content-map.md exists with all source mappings
- [ ] Site-specific CLAUDE.md at repo root
- [ ] All 10 site contracts pass
- [ ] Product repo has NO docs/ folder
- [ ] Product repo CLAUDE.md has no site-specific nav/CSS sections
- [ ] Product repo README.md links to live site
- [ ] Live site loads and renders correctly

## Future: Automated Freshness Checks

Once the split is done, a GitHub Action in the site repo can periodically:
1. Fetch key spec files from the product repo via GitHub API
2. Compare checksums against last-known versions stored in content-map.md
3. Open an issue when a source spec changes, listing which site pages need review

This turns the content map from a static document into an active staleness detector — a Notice agent for the site's own signal stream.
