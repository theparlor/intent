---
title: Persona Product System — Five Capabilities from Discovery through Evals
id: SPEC-persona-product-system
created: 2026-04-12 16:00:00+00:00
thought_leaders:
  - marty-cagan
depth_score: 5
depth_signals:
  file_size_kb: 36.0
  content_chars: 19434
  entity_count: 1
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.21
status: draft
intent: INT-016
signals:
  - SIG-036
  - SIG-037
  - SIG-038
  - SIG-039
depends_on:
  - SPEC-001
  - SPEC-002
contracts:
  - CON-010
  - CON-011
  - CON-012
  - CON-013
  - CON-014
  - CON-015
  - CON-016
  - CON-017
completeness: 0.85
agent_readiness: L2
---
# SPEC-persona-product-system: Persona Product System

> The persona system is a product, not a collection of enrichment tasks. This spec defines five capabilities that form a closed loop: Discovery → Sourcing → Synthesis → Bandit Testing → Evals → (back to Discovery).

**Status:** `draft`
**Created:** 2026-04-12
**Last touched:** 2026-04-12

---

## 1. Intent

### What I Noticed

SPEC-001 and SPEC-002 define the entity schema and a linear intake pipeline. They're the right foundation, but they describe a one-shot process: ingest a person, run synthesis once, store the result. Four signals (SIG-036 through SIG-039) identified five gaps that collectively require product-level investment:

1. No mechanism for the system to discover new people worth ingesting
2. No prioritization of source types by signal quality ("unguarded voice")
3. No separation of mechanical fetching from subjective interpretation
4. No systematic comparison of pipeline configurations
5. No independent quality gate between "synthesis ran" and "persona is usable"

Each gap is individually addressable as an enrichment task. But the interactions between them — discovery feeds sourcing, sourcing feeds synthesis, synthesis feeds bandit testing, bandit testing needs evals as reward signals, evals reveal discovery gaps — form a product loop that only works when all five capabilities exist, even in minimal form.

### Why It Matters Now

The persona library is growing. Torres, Cagan, Patton, Dunford, Singer are migrated. Huryn was the first end-to-end test case. Markus is queued. As the library scales, quality problems compound: a confabulated claim in one persona gets cited by another, vocabulary contamination spreads through archetype synthesis, depth scores inflate because the grading model is the same as the authoring model. Without governance infrastructure now, the library becomes a liability — confidently wrong at scale.

### Desired Outcome

The persona system can discover new candidates, acquire their authentic voice, synthesize faithful representations using the best available pipeline, compare alternatives systematically, and detect its own failure modes — all with progressively less Brien involvement as trust is earned.

---

## 2. Shape

### System Architecture

```
                    ┌─────────────────────────────────────────────────┐
                    │              PERSONA PRODUCT LOOP               │
                    │                                                 │
  ┌──────────┐     │  ┌───────────┐    ┌──────────┐    ┌──────────┐ │
  │ Brien's   │────▶│  │ DISCOVERY │───▶│ SOURCING │───▶│SYNTHESIS │ │
  │ direction │     │  └─────┬─────┘    └──────────┘    └────┬─────┘ │
  └──────────┘     │        ▲                                │       │
                    │        │                                ▼       │
                    │  ┌─────┴─────┐                    ┌──────────┐ │
                    │  │   EVALS   │◀───────────────────│  BANDIT  │ │
                    │  │           │    reward signal    │ TESTING  │ │
                    │  └───────────┘                    └──────────┘ │
                    │        │                                       │
                    │        ▼                                       │
                    │  depth score advancement                       │
                    │  sourcing gap detection                        │
                    │  discovery suggestions                         │
                    └─────────────────────────────────────────────────┘
```

### Approach

Five capabilities, each with its own maturity path from manual/Brien-directed to agent-autonomous. The capabilities form a loop, but each provides standalone value at every maturity level. You don't need bandit testing to benefit from evals; you don't need evals to benefit from better sourcing.

Implementation follows the Intent trust framework: each capability starts at the lowest autonomy level justified by current tooling, and advances as evidence accumulates.

### Boundaries

**In:**
- All five capabilities through their first operational milestone
- File-native implementation in `Core/personas/`
- Integration with existing SPEC-001 schema and SPEC-002 pipeline
- Eval infrastructure that produces machine-readable reports
- Bandit testing framework (even if initial arms are limited)

**Out:**
- Automated persona freshening (scheduled re-ingestion) — future work
- Multi-user persona governance (team disagreements about a persona) — L3+ Productivity OS
- Real-time persona serving (API endpoint) — separate product concern
- Persona marketplace (sharing personas between teams) — L6 Enterprise OS concern
- Automated audiobook purchasing — always L0 (requires Brien's wallet)

### Key Decisions

- Raw markdown is always preserved. Compiled artifacts are subjective interpretations, not replacements for source material.
- The "unguarded voice" hierarchy (GitHub > podcasts > workshops > interviews > blog > book) governs sourcing priority, not just channel ordering.
- Eval failures block depth score advancement. A persona cannot advance from depth 6 to depth 8 without passing Layer 2 content evals.
- Bandit arms are per-persona-type, not global. Prolific bloggers and sparse thinkers have different optimal pipelines.
- Discovery operates on a suggestion model, not an auto-ingest model. The system suggests; Brien (or, at L3, the system with Brien monitoring) decides.

### Open Questions

- What is Brien's cost ceiling for explore-mode bandit testing per persona per month?
- Should Layer 3 fidelity evals be stored in the persona corpus or in a separate governance directory?
- How should the system handle personas where the person has explicitly objected to AI-generated profiles?
- At what library size does the bandit testing framework justify its infrastructure cost?

### Prior Art

- `spec/SPEC-001-persona-entity-schema.md` — entity schema, directory structure, contracts CON-001 through CON-004
- `spec/SPEC-002-persona-intake-pipeline.md` — six-stage intake pipeline, contracts CON-005 through CON-007
- `.intent/signals/2026-04-12-multi-model-adversarial-synthesis.md` (SIG-036) — multi-model quality mechanism
- `spec/signal-trust-framework.md` — trust model and autonomy levels
- `spec/SPEC-productivity-os-layers.md` — L1/L3/L6 layer model for cross-cutting concerns

---

## 3. Capability Specifications

### Capability 1: Persona Discovery

**Purpose:** Find people worth ingesting without Brien having to know they exist.

**Current state:** Fully Brien-directed (L0). Brien says "add Huryn" or "add Markus." The system has no mechanism to suggest candidates.

#### Discovery Mechanisms

**1a. Citation Graph Crawling**

Every synthesis pass produces mentions of other people: "Torres credits Marty Cagan," "Singer was influenced by Christopher Alexander," "Huryn frequently cites Lenny Rachitsky." These mentions are discovery signals.

Implementation:
- During synthesis (Capability 3), the extraction layer identifies every person mentioned by name
- Each mention is recorded in a `discovery-candidates.yaml` file:
  ```yaml
  candidates:
    - name: "Lenny Rachitsky"
      mentioned_by: [pawel-huryn, marty-cagan]
      mention_count: 7
      context: "Product management content, newsletter, podcast"
      first_seen: 2026-04-12
      status: suggested  # suggested | approved | rejected | ingested
  ```
- When a candidate reaches `mention_count >= 3` from different existing personas, it's surfaced to Brien as a signal

**1b. Dissent Detection**

For every persona, the system runs "[name] criticism" and "[name] wrong about" queries. Dissent sources are high-value discovery candidates because they provide genuine cognitive diversity, not just citation-chain echo.

Implementation:
- After synthesis, queue dissent queries for the persona's key stances
- Discovered critics are added to `discovery-candidates.yaml` with `source: dissent`
- Dissent personas are tagged with `relationship: contradicts` in the registry

**1c. Tangential Discovery**

Adjacent domains with different vocabulary for the same problems. Brien's product strategy domain overlaps with organizational design, systems thinking, military strategy, cognitive science. People in those fields may use different words for the same concepts.

Implementation:
- The synthesis layer identifies the persona's core concepts
- A tangential search queries those concepts in adjacent domain vocabularies
- Candidates are added with `source: tangential` and lower initial confidence

**1d. Autonomy Progression**

| Level | Behavior | Gate |
|-------|----------|------|
| L0 | Brien directs all discovery | Current state |
| L1 | System suggests candidates; Brien approves/rejects | Citation count >= 3 threshold |
| L2 | System discovers with approval; Brien reviews batch weekly | Dissent + tangential mechanisms operational |
| L3 | System auto-discovers with review; Brien spot-checks | Eval layer validates discovery quality |

---

### Capability 2: Content Sourcing

**Purpose:** Acquire authentic voice material, prioritized by signal quality.

**Current state:** Web fetch (blogs, articles), podcast show notes, conference talk metadata, book summaries from public descriptions. Limited to what's web-accessible and text-native.

#### Source Channels

**Existing channels (operational):**
- Web fetch: blogs, articles, personal websites
- Podcast show notes and available transcripts
- Conference talk abstracts and slides
- Book content via public descriptions and reviews

**New channels (to build):**

| Channel | Method | Quality | Cost | Priority |
|---------|--------|---------|------|----------|
| Podcast transcription | MacWhisper local transcription of downloaded audio | High — unguarded voice | Time + storage | P1 |
| YouTube auto-captions | YouTube API or yt-dlp caption extraction | Medium — auto-generated, needs cleanup | Free | P1 |
| Academic papers | Google Scholar + Semantic Scholar API | High — formal but original | Free | P2 |
| Community content | Reddit AMAs, HN comments, SO answers | Very high — unguarded, responsive | Free | P2 |
| Audiobook pipeline | Purchase → DRM removal → MacWhisper → transcript | Highest — full book content | $$$ per book | P3 (selective) |

#### "Unguarded Voice" Hierarchy

This hierarchy emerged from the Opus synthesis finding that voice fidelity correlates inversely with how much the person edited before publishing. Sourcing priority follows this order:

```
MOST AUTHENTIC                              LEAST AUTHENTIC
     │                                            │
     ▼                                            ▼
  GitHub     Podcasts    Workshops    Interviews    Blog     Book
  comments   (live)      (live)       (edited)     (edited)  (heavily edited)
  HN/Reddit                                                  
  SO answers                                                 
```

This does NOT mean books are low-value — books contain the most complete articulation of frameworks and mental models. It means books are the least reliable source for voice, frustration triggers, and vocabulary fingerprint. The synthesis layer weights sources differently depending on which substance field is being populated:

| Substance field | Best sources | Worst sources |
|----------------|-------------|---------------|
| voice | GitHub, podcasts, community | Books |
| mental_models | Books, talks, long-form blog | Community comments |
| stances | Interviews, podcasts, community | Book (too nuanced) |
| frustration_triggers | Podcasts, community, interviews | Books (edited out) |
| vocabulary_fingerprint | GitHub, community, podcasts | Books (editor-smoothed) |
| decision_patterns | Case studies, workshops, interviews | All (rarely explicit) |

#### Sourcing Contracts

**CON-010: Source Provenance**
Every file in `corpus/[name]/` must record its source URL, fetch date, fetch method, and any transformation applied (e.g., "MacWhisper transcription at default settings"). No orphan corpus files.

**Verification:** Walk `corpus/[name]/` tree. Every file must have a corresponding entry in `sources.yaml`. Every `sources.yaml` entry must have `url`, `fetched`, `method` fields.

**CON-011: Raw Preservation**
Fetched content is stored in its most original available form. Conversion to clean markdown is a separate step that produces a separate file. The original is never overwritten.

**Verification:** For every `*.md` synthesis input file, a corresponding raw file (`.html`, `.txt`, `.json`, `.srt`) must exist in the corpus. Diff the raw file against the markdown; the markdown should be a strict subset (no content added).

---

### Capability 3: Model-Agnostic Synthesis Pipeline

**Purpose:** Separate mechanical work (fetching, converting) from subjective work (interpreting voice, extracting reasoning chains). Preserve raw material for re-interpretation as models improve.

**Current state:** Single-model pipeline where Opus handles everything — fetching, cleaning, synthesizing, scoring. No separation of concerns, no raw preservation, no re-interpretation capability.

#### Two-Layer Architecture

**Layer A: Fetching (mechanical, model-agnostic)**

Purpose: Convert source material from its native format to clean markdown.

- Input: URLs, audio files, PDFs, HTML pages
- Output: Clean markdown files in `corpus/[name]/clean/`
- Model requirement: None to minimal. Local models (GLM-5.1 free tier, Qwen, Llama) or even rule-based converters handle this layer.
- Quality bar: Structural fidelity — headers, paragraphs, lists, code blocks preserved. No interpretation needed.

Why cheap models work here: Converting HTML to markdown, extracting text from PDFs, and cleaning auto-generated captions are mechanical tasks. A model that misses voice nuance can still produce structurally correct markdown.

**Layer B: Extraction (subjective, requires frontier model)**

Purpose: Read clean markdown and extract voice patterns, reasoning chains, and attribution.

- Input: Clean markdown files from Layer A
- Output: Synthesis document (substance block content) + eval report
- Model requirement: Frontier model (Opus, GPT-4.5, GLM-5.1-Pro). This layer is where model quality directly impacts output quality.
- Quality bar: Fidelity — the synthesis should be faithful to the source material, not to the model's training data.

Three things that degrade with smaller models:
1. **Voice pattern recognition** — capturing register variation (book voice vs. podcast voice), characteristic hedging patterns, humor style. Smaller models flatten these into generic "professional" voice.
2. **Reasoning chain identification** — distinguishing between a framework the person invented, adopted, or merely mentioned. Smaller models attribute everything to the person equally.
3. **Attribution accuracy** — correctly crediting ideas to their originators vs. the persona being synthesized. Smaller models over-attribute (every idea mentioned becomes "their" idea).

#### Multi-Model Adversarial Synthesis (from SIG-036)

Optional step after Layer B extraction. When enabled:

1. Run the same clean markdown corpus through two different frontier models
2. Each produces an independent synthesis document
3. A comparison agent reads both and produces a disagreement report:
   - **Agreements** → high confidence claims (both models found this in the source material)
   - **Disagreements** → sycophancy signals (one model may be pattern-matching from training data)
   - **Unique findings** → one model found something the other missed (review manually)

The adversarial synthesis is NOT required for every persona. It's triggered when:
- Depth score is being advanced past depth 8
- The persona is a well-known figure where training data contamination risk is high
- Bandit testing is in explore mode and adversarial is the selected arm

#### Synthesis Contracts

**CON-012: Layer Separation**
No synthesis document may be produced directly from raw source material. The path must be: raw → clean markdown (Layer A) → synthesis (Layer B). The clean markdown intermediate must exist as a file.

**Verification:** For every synthesis document, trace back through the processing log. Every source cited must have a corresponding clean markdown file in `corpus/[name]/clean/`.

**CON-013: Re-interpretation Guarantee**
Deleting all synthesis documents and re-running Layer B against the preserved clean markdown must produce a new synthesis. The clean markdown is sufficient input — no external state required.

**Verification:** Delete synthesis output for one persona. Run Layer B against the clean markdown. Confirm a new synthesis is produced. (Content may differ due to model updates — that's expected. The contract is that the process works, not that the output is identical.)

---

### Capability 4: Multi-Armed Bandit Testing

**Purpose:** Systematically compare pipeline configurations to find the best one per persona type.

**Current state:** Hardcoded pipeline (Opus for everything). No comparison, no optimization, no evidence that this is optimal.

#### Bandit Framework

**Arms (pipeline configurations):**

| Arm | Fetch Model | Synthesis Model | Cost | Hypothesis |
|-----|-------------|-----------------|------|------------|
| A (default) | Sonnet | Opus | $$ | Current baseline |
| B | GLM-5.1 (free) | Opus | $ | Cheaper fetch, same synthesis quality |
| C | GLM-5.1 (free) | GLM-5.1 | Free | How much quality do we lose going fully cheap? |
| D | Sonnet | Sonnet | $ | Mid-tier throughout |
| E | Opus | Opus | $$$ | Maximum quality — when does it matter? |
| F | Any | Dual-model adversarial | $$$$ | SIG-036's approach — highest quality, highest cost |

**Reward signal (from eval layer):**

```yaml
reward:
  structural_score: float    # Layer 1 eval pass rate (0-1)
  content_score: float       # Layer 2 eval pass rate (0-1)
  fidelity_score: float      # Layer 3 eval score (0-1, when available)
  cost_efficiency: float     # content_score / api_cost_dollars
  composite: float           # weighted combination (weights TBD by Brien)
```

**Explore/exploit schedule:**
- Default: exploit (use best known arm for this persona type)
- Epsilon = 0.15: 15% of synthesis passes use a random non-default arm
- Epsilon decays as sample size increases per persona type
- New persona type (< 3 samples): force explore for first 3 passes

**Persona type classification (initial taxonomy):**

| Type | Characteristics | Hypothesized best arm |
|------|----------------|----------------------|
| prolific-blogger | 50+ posts, regular cadence | B (cheap fetch, quality synthesis) |
| sparse-dense | < 20 sources, every sentence matters | E (quality everywhere) |
| speaker-primary | Mostly talks/podcasts, limited writing | B or D (transcription quality is bottleneck) |
| academic | Papers, formal writing, citations | C (formal structure = easier extraction) |
| practitioner-writer | Books + blog + talks, wide range | F (adversarial catches training contamination) |

#### Storage Convention

```
corpus/[name]/
├── clean/                          # Layer A output (shared across arms)
│   ├── blog-posts.md
│   └── podcast-transcripts.md
├── synthesis/                      # Layer B outputs (per arm)
│   ├── arm-a-opus-default/
│   │   ├── synthesis.md
│   │   └── metadata.yaml          # model, timestamp, cost, tokens
│   ├── arm-b-glm-opus/
│   │   ├── synthesis.md
│   │   └── metadata.yaml
│   └── arm-f-adversarial/
│       ├── synthesis-model-1.md
│       ├── synthesis-model-2.md
│       ├── disagreement-report.md
│       └── metadata.yaml
└── eval-reports/                   # Eval scores per arm
    ├── arm-a-eval-2026-04-12.yaml
    ├── arm-b-eval-2026-04-12.yaml
    └── comparison-2026-04-12.md
```

#### Bandit Contracts

**CON-014: Arm Isolation**
Each arm's synthesis must be produced independently — no arm may read another arm's output. The clean markdown input is shared, but synthesis is isolated.

**Verification:** Check that synthesis files for different arms have different creation timestamps and that the processing log shows independent runs. No synthesis file may reference another arm's output.

**CON-015: Reward Traceability**
Every reward score must trace to a specific eval report. No reward may be computed without a corresponding eval. The bandit algorithm must not use scores that aren't backed by eval evidence.

**Verification:** For every entry in the bandit reward log, confirm a corresponding eval report exists in `eval-reports/` with matching timestamp and arm identifier.

---

### Capability 5: Eval-Driven Development

**Purpose:** Three layers of evaluation that gate depth score advancement and provide the reward signal for bandit testing.

**Current state:** Depth score is self-assessed by the synthesis agent. No independent verification.

#### Layer 1: Structural Evals (automated, every synthesis pass)

These are mechanical checks requiring no model involvement:

| Check | What it verifies | Fail action |
|-------|-----------------|-------------|
| YAML parse | Entity file is valid YAML | Block synthesis storage |
| Required fields | voice, mental_models, stances, frustration_triggers populated | Block depth advancement |
| Source resolution | Every URL in sources.yaml returns 200 | Flag stale sources |
| Processing log completeness | Log documents attempts AND outcomes (not just successes) | Block depth advancement |
| Corpus coverage | File size > 0 for all referenced corpus files | Flag incomplete harvest |
| Depth justification | Depth score has narrative justification, not just a number | Block depth advancement |
| Claim-to-source ratio | Number of claims / number of sources < threshold (TBD) | Flag for review |

**Implementation:** Shell script or Python script that runs against the persona directory. Exit code 0 = pass, nonzero = fail with report. Can be run by any model or no model.

#### Layer 2: Content Evals (semi-automated, post-synthesis)

These require a model but not Brien's judgment:

**2a. Distinctiveness Test**
- Input: Two adjacent personas (e.g., Torres and Cagan)
- Prompt: "How would [persona A] and [persona B] approach [problem X]?"
- Evaluation: Are the responses meaningfully different? Score on a 1-5 distinctiveness scale.
- Fail condition: Score < 3 for any pair of personas in the same domain.
- Frequency: After every synthesis pass, tested against the 2 most similar personas by domain.

**2b. Traceability Test**
- Input: Synthesis document + source corpus
- Process: For each claim in the synthesis, search the corpus for supporting evidence.
- Evaluation: Percentage of claims with traceable evidence.
- Fail condition: Traceability < 70% (more than 30% of claims can't be found in the corpus).
- Frequency: Every synthesis pass.

**2c. Vocabulary Verification**
- Input: vocabulary_fingerprint field + corpus of actual quotes
- Process: For each fingerprint term, search for it in direct quotes from the person.
- Evaluation: Percentage of fingerprint terms appearing in actual quotes.
- Fail condition: < 60% of fingerprint terms found in actual quotes (suggesting model vocabulary contamination).
- Frequency: Every synthesis pass.

**2d. Attribution Accuracy**
- Input: Synthesis claims that attribute ideas to the persona + source material
- Process: Verify that attributed ideas actually originate from or are advocated by this person.
- Evaluation: Percentage of attributions verified in source material.
- Fail condition: < 80% attribution accuracy.
- Frequency: Every synthesis pass.

**2e. Self-Correction Inventory**
- Input: Any "I used to think X, now I think Y" statements in the synthesis
- Process: Verify these evolution statements appear in the source material.
- Evaluation: Every self-correction claim must have a source.
- Fail condition: Any unsourced self-correction claim.
- Frequency: Every synthesis pass.

**2f. Reasoning Chain Completeness**
- Input: Persona's mental models + a novel scenario outside the corpus domain
- Prompt: "Using [persona]'s mental models, how would they approach [novel problem]?"
- Evaluation: Does the response use the models as reasoning tools (applying them to new situations) or merely recite their definitions?
- Fail condition: Response is definitional rather than applied.
- Frequency: Post-synthesis, on depth advancement attempts.

#### Layer 3: Fidelity Evals (human-in-loop, periodic)

These require Brien's judgment:

**3a. Would-They-Say-This Test**
- Brien reads a persona-generated response and scores:
  - 5: Definitely yes — sounds exactly like them
  - 4: Probably yes — recognizably them
  - 3: Uncertain — could be them or could be generic
  - 2: Probably not — doesn't sound like them
  - 1: Definitely not — contradicts their known positions
- Minimum passing score for depth advancement: 4
- Frequency: When depth score advancement is requested (not every synthesis pass)

**3b. Claim Spot-Check**
- Brien picks 3-5 claims at random from the synthesis
- For each: does it hold up against the source material?
- Scoring: percentage of spot-checked claims that hold up
- Minimum passing score: 80% (4/5 claims check out)

**3c. Hedging Accuracy**
- Brien evaluates: does the persona hedge on topics where the corpus is thin?
- A persona that's confidently opinionated about everything is suspicious.
- Scoring: qualitative (appropriate / over-confident / under-confident)
- Minimum passing: "appropriate" or "under-confident" (never "over-confident")

**3d. Voice Register Accuracy**
- Brien evaluates: does the persona capture register variation?
- Book voice should differ from podcast voice should differ from tweet voice.
- Scoring: qualitative (captures variation / flattens to single register / wrong register)
- Minimum passing: "captures variation" for depth > 8

#### Eval Infrastructure

```
corpus/[name]/
└── eval-reports/
    ├── structural/
    │   └── 2026-04-12.yaml         # Layer 1 results
    ├── content/
    │   ├── 2026-04-12-distinctiveness.yaml
    │   ├── 2026-04-12-traceability.yaml
    │   ├── 2026-04-12-vocabulary.yaml
    │   └── 2026-04-12-attribution.yaml
    ├── fidelity/
    │   └── 2026-04-12-brien-review.yaml   # Layer 3 results
    └── composite/
        └── 2026-04-12-summary.yaml        # Aggregated score for bandit reward
```

**Eval report schema (structural):**
```yaml
eval_type: structural
persona: pawel-huryn
timestamp: 2026-04-12T16:00:00Z
arm: arm-a-opus-default  # or null if not bandit-tested
checks:
  yaml_parse: {pass: true}
  required_fields: {pass: true, missing: []}
  source_resolution: {pass: false, stale: ["https://example.com/removed-post"]}
  processing_log: {pass: true}
  corpus_coverage: {pass: true}
  depth_justification: {pass: true}
  claim_source_ratio: {pass: true, ratio: 2.3}
overall: fail  # any check fail = overall fail
blocking: [source_resolution]  # which checks caused the failure
```

**Eval report schema (content):**
```yaml
eval_type: content
persona: pawel-huryn
timestamp: 2026-04-12T16:00:00Z
arm: arm-a-opus-default
model_used: claude-opus-4  # the eval model, not the synthesis model
tests:
  distinctiveness:
    compared_with: [marty-cagan, lenny-rachitsky]
    scores: {marty-cagan: 4.2, lenny-rachitsky: 3.8}
    pass: true
  traceability:
    total_claims: 47
    traceable: 39
    percentage: 0.83
    pass: true
  vocabulary:
    fingerprint_terms: 12
    verified_in_quotes: 9
    percentage: 0.75
    pass: true
  attribution:
    total_attributions: 15
    verified: 13
    percentage: 0.87
    pass: true
  self_correction:
    claims: 3
    sourced: 3
    pass: true
  reasoning_chain:
    scenario: "How would Huryn approach a B2B marketplace with supply-side chicken-and-egg problem?"
    assessment: applied  # applied | definitional
    pass: true
overall: pass
composite_score: 0.84
```

#### Eval Contracts

**CON-016: Eval-Gated Depth Advancement**
No persona's depth score may increase without passing the eval layer appropriate to the target depth:
- Depth 1-4: Layer 1 structural evals only
- Depth 5-8: Layer 1 + Layer 2 content evals
- Depth 9+: Layer 1 + Layer 2 + Layer 3 fidelity evals

**Verification:** Check the depth score in the registry entity. For the current depth, confirm eval reports exist at the required layers. All required layers must show `overall: pass`.

**CON-017: Eval Independence**
The model that runs Layer 2 content evals must NOT be the same model instance that produced the synthesis being evaluated. At minimum, it must be a separate invocation (different session/context). Preferably, a different model entirely.

**Verification:** Compare `model_used` in the eval report against the model recorded in the synthesis metadata. Flag if identical model AND same session.

---

## 4. Cross-Cutting: Connection to Productivity OS Layers

The persona product system maps to the three Productivity OS layers from SPEC-productivity-os-layers:

**L1 (Personal OS) — Brien's current state:**
- Discovery: Brien directs all persona additions
- Sourcing: Brien identifies channels and triggers fetches
- Synthesis: Single pipeline configuration
- Bandit Testing: Not applicable (single configuration)
- Evals: Brien runs Layer 3 fidelity evals manually, Layer 1 structural evals automated

**L3 (Team OS) — When Brien has collaborators:**
- Discovery: Team members suggest candidates through shared `discovery-candidates.yaml`
- Sourcing: Team agrees on channel priority and "unguarded voice" weighting
- Synthesis: Multiple team members can trigger synthesis passes
- Bandit Testing: Team cost ceiling shared; explore budget allocated per quarter
- Evals: Team agrees on eval criteria; Layer 2 content evals run by team-designated model; Layer 3 fidelity evals distributed across team members by domain expertise

**L6 (Enterprise OS) — When persona system serves an organization:**
- Discovery: Discovery mechanisms integrated with organizational knowledge graph
- Sourcing: Compliance-gated sourcing (some channels may be restricted by org policy)
- Synthesis: Org-approved model list; synthesis restricted to approved models
- Bandit Testing: Org-level cost controls; explore budget requires budget holder approval
- Evals: Eval framework becomes governance requirement; eval reports feed into audit trail; Layer 3 fidelity evals conducted by designated domain SMEs, not just Brien

---

## 5. Implementation Roadmap

### Phase 1: Foundation (build on SPEC-001 + SPEC-002)
- Implement Layer 1 structural evals as a shell script
- Add `eval-reports/` directory to corpus structure
- Add `discovery-candidates.yaml` to `Core/personas/`
- Separate Layer A (fetching) from Layer B (extraction) in the intake pipeline
- Preserve raw files alongside clean markdown

### Phase 2: Content Quality (requires Phase 1)
- Implement Layer 2 content evals (distinctiveness, traceability, vocabulary, attribution)
- Gate depth advancement on eval results
- Implement citation graph crawling for discovery suggestions
- Add "unguarded voice" weighting to sourcing

### Phase 3: Optimization (requires Phase 2)
- Implement bandit framework with 3 initial arms (A, B, C)
- Connect eval composite scores as bandit reward signals
- Implement dissent detection for discovery
- Add YouTube caption and podcast transcription channels

### Phase 4: Maturation (requires Phase 3)
- Add adversarial synthesis arm (F)
- Implement tangential discovery
- Advance discovery autonomy toward L2-L3
- Reduce Brien's eval load through calibrated content evals
- Persona type taxonomy formalized from bandit evidence

---

## 6. Contract Summary

| Contract | Layer | Capability | What it enforces |
|----------|-------|-----------|-----------------|
| CON-010 | Sourcing | 2 | Source provenance — every corpus file has metadata |
| CON-011 | Sourcing | 2 | Raw preservation — originals never overwritten |
| CON-012 | Synthesis | 3 | Layer separation — raw → clean → synthesis path enforced |
| CON-013 | Synthesis | 3 | Re-interpretation — deleting synthesis and re-running works |
| CON-014 | Bandit | 4 | Arm isolation — arms don't read each other's output |
| CON-015 | Bandit | 4 | Reward traceability — every score backed by eval evidence |
| CON-016 | Evals | 5 | Eval-gated depth — depth can't advance without passing evals |
| CON-017 | Evals | 5 | Eval independence — evaluator differs from author |

---

## 7. Smoke Test

**Minimum viable validation:**

```
1. Pick an existing persona (e.g., pawel-huryn)
2. Run Layer 1 structural evals against current state
3. Observe: which checks pass, which fail?
4. Run one Layer 2 content eval (traceability) against current synthesis
5. Observe: what percentage of claims trace to source material?
6. The structural eval script runs without error AND produces a machine-readable report
```

If the structural eval reveals 0 failures on an existing persona, the persona is either perfect (unlikely) or the eval is too lenient (likely). A good first eval should find real problems.

---

## 8. Failure Modes to Watch

- **Eval theater** — evals that always pass aren't governance, they're ceremony. Initial thresholds should be set to fail real personas and then calibrated upward.
- **Bandit cold-start** — with < 3 samples per arm per persona type, the bandit algorithm has no signal. The explore phase must be long enough to accumulate evidence before exploiting.
- **Discovery avalanche** — citation graph crawling on a well-connected persona could generate hundreds of candidates. Rate-limit discovery suggestions to prevent overwhelm.
- **Cost spiral** — adversarial synthesis (Arm F) costs 2-3x a single synthesis. Without cost ceilings, explore mode can burn through API budget. Implement per-persona and per-month cost caps.
- **Eval model contamination** — if the eval model has the same training data biases as the synthesis model, content evals will miss the same failures. Prefer different model families for eval vs. synthesis.
- **Register flattening** — the eval layer must check for register variation, not just overall voice quality. A persona that sounds like a generic "professional" version of the person is worse than one that captures their messy podcast voice.

---

## Notes

- This spec intentionally overlaps with SPEC-001 and SPEC-002. Those specs define the schema and the initial pipeline. This spec defines the product system that wraps them in feedback loops.
- The bandit testing framework draws on Brien's reading of multi-armed bandit literature (Thompson sampling, UCB1) and adapts it to the persona compilation context. The "arms" terminology is deliberate — each pipeline configuration is a slot machine we're trying to characterize.
- The "unguarded voice" hierarchy emerged from a specific Opus synthesis session where the model noted that blog posts and books produced different voice signatures for the same person. The hierarchy is empirical, not theoretical.
- Layer 3 fidelity evals are the bottleneck. Brien's time is finite. The long-term goal is to calibrate Layer 2 content evals against Brien's Layer 3 judgments so that Layer 2 can eventually serve as a proxy, reducing Brien's eval load to spot-checks only.
