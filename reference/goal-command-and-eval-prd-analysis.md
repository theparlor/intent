---
title: "The /goal command and the evals-are-the-new-PRD claim: source manifest and ground truth"
type: external-pattern-analysis
status: terminal
maturity: active
confidentiality: internal
reusability: universal
created: 2026-09-16
purpose: Verified provenance and mechanism ground-truth behind SPEC-INTENT-PROJECTION-DIVERGENCE-001. Completes the source manifest that intake issue 12 left open (its OQ9 and OQ10).
entity: aakash-gupta
verified_on: 2026-09-16
verification_method: "live fetch of code.claude.com/docs/en/goal plus web search; every claim below is tagged VERIFIED, PROBABLE, or UNRESOLVED"
lineage:
  - https://github.com/theparlor/intake/issues/12
related:
  - spec/SPEC-INTENT-PROJECTION-DIVERGENCE-001.md
  - spec/typed-evaluation-verdicts.md
  - reference/external-patterns-index.md
  - reference/corpus/aakash-gupta/README.md
---
# The /goal command and "evals are the new PRD"

## Plain language first

**What this is.** A provenance file. In June 2026 a chat session captured three screenshots
of a LinkedIn post and reasoned a whole operator design out of it. The reasoning was good;
the sourcing was not. Four links were truncated, two academic claims were asserted without
citations, and the mechanism being reasoned about was described from a one-page cheat sheet
rather than from the product documentation. This file goes and gets all of it, says what
held up, and says what did not.

**Why it matters.** The design that rests on this material is now a spec in this repo
(`spec/SPEC-INTENT-PROJECTION-DIVERGENCE-001.md`). A spec resting on unverified sources is
a spec that cannot be defended in a room. This file is what makes it defensible.

**What changed.** Four of four missing links are found. Both academic load-bearers are
grounded in named papers. The `/goal` mechanism is verified against the vendor
documentation, and five claims in the original capture turned out to be wrong or imprecise.
They are corrected in section 4 rather than quietly carried forward.

---

## 1. The trigger artifact

A LinkedIn post by Aakash Gupta (Product Growth newsletter) carrying a one-page infographic,
"A PM's Cheat Sheet to /goal", under the banner "Claude Code for PM". Captured from three
screenshots on 2026-06-16, roughly 16 hours old at capture, with 87 likes, 17 comments,
2 reposts.

**The LinkedIn post itself is UNRESOLVED.** LinkedIn activity URLs are not fetchable without
an authenticated session, and the capture recorded no activity id. The post's own text is
therefore the one piece of the chain that cannot be re-read. Two claims that depend on it
are marked UNRESOLVED in section 4. Everything the post was pointing AT is resolved below.

## 2. The four truncated Aakash links (issue 12, OQ9)

The capture recorded four `lnkd.in` shortlinks with their targets truncated. All four are
now identified.

| # | As described in the capture | Resolved target | Confidence |
|---|---|---|---|
| 1 | "AI killed the 10-page PRD" | "AI killed the 10 page PRD. But the PRD isn't dead." https://aakashgupta.medium.com/ai-killed-the-10-page-prd-but-the-prd-isnt-dead-8801efe44b36 (also a Substack note, https://substack.com/@aakashgupta/note/c-146506994, and a LinkedIn post, Aug 2025) | VERIFIED title match |
| 2 | "Evals are the new PRD" | "Evals are the new PRD for AI PMs", a podcast episode with Ankur Goyal, founder and CEO of Braintrust. https://www.news.aakashg.com/p/ankur-goyal-podcast (mirror: https://www.aakashg.com/ankur-goyal-podcast/). Braintrust's own companion post: https://www.braintrust.dev/blog/evals-are-the-new-prd | VERIFIED |
| 3 | "The PRD that engineers actually read" | Best match is "40 Lines of Markdown Replaced My 15-Page PRD" https://aakashgupta.medium.com/40-lines-of-markdown-replaced-my-15-page-prd-30edce7ee65c (Apr 2026). Reports a 23 percent average open rate on 12 PRDs shared as Google Docs, and a move to markdown in the repo after Rippling CPO Matt MacInnis. | PROBABLE. The title is not a verbatim match; the subject matter is exact. Treat the title in the capture as a paraphrase, not a citation. |
| 4 | "the full /goal guide" | "The Complete PM Guide to /goal in Claude Code" https://www.news.aakashg.com/p/how-pms-should-actually-use-goal. Companion repo: https://github.com/aakashg/pm-claude-code-setup | VERIFIED |

**A correction that matters for attribution.** The capture treats "evals are the new PRD" as
Aakash's thesis about `/goal`. It is not. It is the title of his interview with Ankur Goyal
about Braintrust, an eval platform, and the claim in that piece is about eval experiments as
a product-development cadence (the episode cites 12.8 eval experiments per day at companies
shipping working AI products). The `/goal` cheat sheet is a separate artifact. The capture
welded two of Aakash's pieces into one thesis. The welded thesis is still worth arguing
with, and the spec argues with it, but it should be attributed as a synthesis made in the
capture session, not as a sentence Aakash wrote.

## 3. `/goal` mechanism, verified against the vendor documentation

Source: https://code.claude.com/docs/en/goal, fetched 2026-09-16. Secondary:
Emilia David, "Claude Code's '/goals' separates the agent that works from the one that
decides it's done", VentureBeat, 2026-05-14.

VERIFIED, quoting or closely paraphrasing the documentation:

- `/goal` is "a wrapper around a session-scoped prompt-based Stop hook". One goal per session.
- After each turn the condition plus the conversation so far go to the configured small fast
  model, "which defaults to Haiku on the Claude API".
- "It does not call tools, so it can only judge what Claude has already surfaced in the
  conversation." This is the load-bearing constraint. The evidence window is the transcript.
- The condition can be up to 4,000 characters.
- A condition that holds up over many turns has: one measurable end state, a stated check,
  and constraints that matter. A turn or time clause is optional and is authored INTO the
  condition, not configured outside it.
- Runs in interactive mode, non-interactive mode (`claude -p`), the desktop app, and Remote
  Control.
- Availability is gated by the workspace trust rule for hooks, and `/goal` is unavailable
  when `disableAllHooks` is true after settings precedence, or when `allowManagedHooksOnly`
  is set in managed settings.
- Sits alongside `/loop` (time interval), a settings-level Stop hook (script or prompt), and
  Auto mode (removes per-tool confirmation inside one turn, does not start a new turn).

VERIFIED and NEW relative to the capture (the documentation has moved since June):

- **Three verdicts, not two.** The evaluator returns "not yet met", "met", or **"impossible"**.
  An impossible verdict clears the goal and records a failed entry with the reason. The
  capture describes a binary (unmet loops, met returns control). The third verdict is the
  interesting one and is discussed in the spec.
- **A built-in no-progress damper.** "If Claude keeps answering the evaluator without making
  progress (no tool use for several turns in a row), Claude Code stops the loop, prints a
  warning, and returns control to you with the goal still set."
- **Background work defers evaluation**, with check-ins after 30 minutes by default, then
  backing off by doubling up to four times the first interval.
- **Failure taxonomy.** Four unrecoverable error classes clear the goal (auth failure when
  Claude Code manages its own credentials, exhausted credit balance, unclearable context
  overflow, unavailable model). Everything else retries with backoff, up to three automatic
  retries, then pauses.
- Version markers visible in the documentation as of 2026-09-16: v2.1.234 (check-ins),
  v2.1.236 (idle check-ins), v2.1.239 (resume-route coverage, check-in backoff), v2.1.246
  (idle check-ins capped at three), v2.1.269 (retry and pause notices).

## 4. Corrections to the capture

| Claim in the capture | Status | The verified record |
|---|---|---|
| "Unmet loops; met returns control" (binary) | **WRONG, incomplete** | Three verdicts. "Impossible" is a third outcome that clears the goal and records a failure. |
| "Safety Net = stop after 25 turns or same step fails 3 times" | **MISREAD as mechanism** | Those numbers come from the cheat sheet's prompt template, not from the product. The documentation says a turn or time clause is authored into the condition text. The product's own built-in damper is the no-progress stop, not a turn count. |
| "shipped ~mid-May 2026, v2.1.139+" | **PROBABLE** | v2.1.139+ appears consistently in secondary coverage; the VentureBeat piece is 2026-05-14. Not stated on the current documentation page, which has moved on to later version markers. |
| "OpenAI shipped a near-identical command within days" and reached the opposite default | **ORDER REVERSED; conclusion holds** | Codex CLI 0.128.0 added `/goal` on 2026-04-30 (Simon Willison, https://simonwillison.net/2026/Apr/30/codex-goals/), roughly two weeks BEFORE the Claude Code coverage, not after it. The substantive point survives intact: per VentureBeat, OpenAI "leaves the loop alone and lets the model decide when it's done", with user-added evaluators optional, against Anthropic's built-in separate evaluator. Two vendors, two opposite defaults on who declares done. |
| "Post body says all six sections; sheet shows nine" | **UNRESOLVED** | Depends on the LinkedIn post body, which is not re-readable. Carried as a noted discrepancy, not as a fact. |
| Practitioner caveat attributed to Brownell via VentureBeat | **VERIFIED** | Sean Brownell, quoted by Emilia David, VentureBeat, 2026-05-14: "you can't trust a model to judge its own homework. The model doing the work is the worst judge." He scopes the loop to "deterministic work with a verifiable end-state like migrations, fixing broken test suites, clearing a backlog", with human judgment still required for nuanced design work. |
| Post engagement numbers (16h old, 87 likes, 17 comments, 2 reposts) | **UNVERIFIABLE, and now stale** | Point-in-time capture of a surface that is not re-readable. Retained as provenance, not as evidence. Nothing in the spec rests on it. |

## 5. The two ungrounded academic load-bearers (issue 12, OQ10)

### 5.1 Generator-verifier gap and correlated error in same-family models

This is the argument underneath the capture's F5 and F7 (a cheap same-family evaluator cannot
catch "what was said was wrong"). It is now grounded.

- **Guneet Kohli, "Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM
  Evaluation Panels", Apple Machine Learning Research, June 2026.** arXiv 2605.29800.
  https://machinelearning.apple.com/research/correlated-llm-evaluation-panels
  A panel of nine frontier judges drawn from seven model families supplies about **two**
  independent votes' worth of information. Roughly three quarters of the panel's nominal
  independence is lost "because the models make the same mistakes on the same items."
  This is the hardest available number for the claim, and note what it costs the optimistic
  reading: the errors correlate ACROSS families, not only within one. Adding judges buys far
  less than it appears to.
- **"Mind the Gap: Examining the Self-Improvement Capabilities of Large Language Models",
  arXiv 2412.02674.** Holding the generator fixed, the generator-verifier gap widens as the
  verifier gets stronger; holding the verifier fixed, the gap narrows as the generator gets
  stronger, because a stronger generator's errors get harder to detect. The asymmetry is the
  point: buying a cheaper verifier is not a small discount on the same instrument, it moves
  you along a curve.
- Intent's `spec/typed-evaluation-verdicts.md` already cites Knight and Leveson (1986) for
  the same phenomenon in N-version programming. The Apple result is the LLM-era replication
  of Knight and Leveson. Cite them together: independently written versions fail together,
  and independently prompted judges are wrong together.

### 5.2 Goodhart and surrogation

This is the argument underneath the capture's F2 (eval-only leads to a satisfiable eval and a
missed point) and OQ8.

- **Goodhart's law.** Charles Goodhart (1975), popularly rendered by Marilyn Strathern (1997)
  as: when a measure becomes a target, it ceases to be a good measure.
- **Surrogation** is the sharper, better-evidenced construct, and it is the one the operator
  actually needs. Willie Choi, Gary Hecht and William B. Tayler, "Lost in Translation: The
  Effects of Incentive Compensation on Strategy Surrogation", The Accounting Review (2012),
  SSRN 1438212, https://doi.org/10.2139/ssrn.1438212; and "Strategy Selection, Surrogation,
  and Strategic Performance Measurement Systems", Journal of Accounting Research 51(1), 2013,
  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1910383.
  Surrogation is the cognitive substitution in which people lose sight of the strategic
  construct a measure was meant to stand for and act as though the measure IS the construct.
  Two experimental findings carry directly into this design: surrogation is **strongest when
  a single measure stands in for the construct** and weaker under multiple measures; and
  **involvement in choosing the strategy mitigates it**.
- Why surrogation and not just Goodhart: Goodhart describes what happens to a measure under
  pressure. Surrogation describes what happens to the person, and it happens without any
  gaming, any bad actor, or any incentive to cheat. A single binary finish line standing in
  for a product intent is the exact experimental condition under which Choi, Hecht and Tayler
  found surrogation strongest. That is not an analogy. That is the finding.

## 6. Where the coverage is narrow, stated plainly

- The LinkedIn post body is unread and unreadable. Two claims depend on it and are marked
  UNRESOLVED above.
- Link 3 is a probable, not certain, match on title.
- The four Aakash pieces were identified and characterised from search-result content and
  from the `/goal` documentation; the full body text of each Aakash piece behind a Substack
  or Medium paywall was not read end to end. Nothing in the spec rests on their interiors,
  only on their existence, titles, and the one figure (23 percent open rate) that appeared in
  search content.
- The Apple paper's headline number was taken from the Apple Machine Learning Research
  landing page for it, not from the arXiv PDF.
