# Synthesis Template — Discovery Wave 1

> This is the output of 10 interviews, NOT the aggregate of interpretations. Keep raw signals and synthesis separate.

## How to use this template

After all 10 interviews are complete:

1. Read all 10 external signal files back-to-back in one sitting. No laptop distractions.
2. Note patterns ONLY after reading all 10. Do not synthesize one-at-a-time.
3. Run a panel review (via INT-007) with the Discovery/UX panel to critique the synthesis for confirmation bias BEFORE publishing.
4. The synthesis is published at `knowledge/themes/THM-external-discovery-wave-1.md` and produces an opportunity tree at `knowledge/domain-models/DOM-spec-pain-OST.md`.

## Template

```markdown
---
id: THM-external-discovery-wave-1
wave: 1
interview_count: 10
date_range: 2026-04-XX to 2026-04-XX
status: draft
panel_reviewed: false
confirmation_bias_check: pending
---

# External Discovery Wave 1 — Synthesis

## Methodology

- 10 structured interviews, 45 min each, Mom Test protocol
- Participants: [demographic summary — roles, company sizes, AI tools, geo]
- Interviewers: [who conducted]
- Hypothesis being tested: "When AI collapses implementation cost, the bottleneck moves upstream to specification clarity, and existing ticket-based tools optimize for the wrong thing."

## Participant demographics

| Role | Count |
|------|-------|
| Staff/Principal Engineer | X |
| Senior Engineer | X |
| Engineering Manager | X |
| Principal/Senior PM | X |

| Company stage | Count |
|---------------|-------|
| Startup (<30 eng) | X |
| Scaleup (30-300) | X |
| Mid-enterprise (300-3000) | X |
| Large enterprise (3000+) | X |

## Hypothesis outcome

**[CHOOSE ONE]**
- ✅ CONFIRMED — X of 10 participants described the spec clarity bottleneck in their own words, unprompted, with specific recent examples.
- ⚠️ PARTIALLY CONFIRMED — X of 10 described something LIKE the hypothesis, but with important modifications: [list modifications].
- ❌ DISCONFIRMED — X of 10 described a different bottleneck. The actual bottleneck according to these practitioners is: [what they said]. Our hypothesis was wrong in the following ways: [be specific].
- ❓ INCONCLUSIVE — Signal was noisy, mixed, or too diverse to support a clear conclusion. [Explain]

## The 5 strongest quotes (verbatim, attributed)

> "[Strongest quote 1]"
> — [Participant attribution, role, company stage]

> "[Strongest quote 2]"
> — [Participant attribution]

> "[Strongest quote 3]"
> — [Participant attribution]

> "[Strongest quote 4]"
> — [Participant attribution]

> "[Strongest quote 5]"
> — [Participant attribution]

## The patterns we heard (synthesis, not interpretation)

### Pattern 1: [Pattern name in their words]

- Observed in: X of 10 interviews
- Participants who named it: [slugs]
- Canonical example: [one specific recent moment]
- Variant forms: [how it differed across participants]
- What they're already doing about it: [workarounds and tools]

### Pattern 2: [next pattern]
[...]

### Pattern 3: [next pattern]
[...]

## Surprises (what we didn't expect)

[CRITICAL SECTION — surprises are where the learning is]

### Surprise 1: [what we didn't expect to hear]

- Heard from: [participants]
- Why it surprises us: [our prior assumption]
- What it might mean: [first-pass interpretation]

### Surprise 2: [next surprise]
[...]

## Disconfirmations (quotes that challenge our hypothesis)

[CRITICAL SECTION — if there are none of these, we probably did discovery wrong]

> "[Disconfirming quote]"
> — [Participant]

Context: [why this disconfirms the hypothesis]

## What we thought vs. what they said

| Our assumption | What participants said | Delta |
|----------------|------------------------|-------|
| Spec clarity is the new bottleneck | [their actual answer] | [gap] |
| Tickets don't work anymore | [their actual answer] | [gap] |
| AI outputs match spec well when spec is clear | [their actual answer] | [gap] |
| Teams are building workarounds | [their actual answer] | [gap] |

## Opportunity tree (OST) — separate file

See: `knowledge/domain-models/DOM-spec-pain-OST.md`

The OST structure (Torres format):
- Desired outcome
- Opportunities (the patterns above, framed as opportunities)
- Solutions (only AFTER opportunities are validated — NOT from this synthesis yet)
- Assumption tests (what we need to validate next)

## What this means for Intent

[CAREFUL SECTION — this is where bias sneaks in]

### What Intent got right (validated by this discovery)

- [Claims that are supported by external evidence]
- [With specific participant citations]

### What Intent got wrong (invalidated or challenged)

- [Claims that need revision]
- [With specific participant citations]
- [What the correct version might be]

### What Intent didn't address (gaps discovered)

- [Pains we hadn't thought of]
- [Opportunities we hadn't sized]

## Next actions from this synthesis

1. [Specific change to site content, linked to which participants surfaced it]
2. [Specific change to methodology, linked to which participants surfaced it]
3. [Specific hypothesis to test next]
4. [Specific opportunity to size]
5. [Specific disconfirmation that needs deeper investigation]

## Panel review of this synthesis

Before publishing, run:
```
panel-review target=THM-external-discovery-wave-1 panels=discovery,product,strategy depth=thorough
```

Questions for the panel:
- Are we laundering confirmation bias through apparent rigor?
- Did we over-weight quotes that support the hypothesis?
- Did we under-weight disconfirmations?
- Did we synthesize ACROSS participants, or pattern-match to our prior beliefs?
- What would we have written if we'd never heard of Intent before reading these 10 signals?

## Appendix: raw external signal files

- [Link to each of the 10 signal files in `.intent/signals/external/`]
```

## Signal-to-synthesis discipline

Three rules to prevent confirmation bias:

1. **Raw data comes first, interpretation comes last.** The quotes and patterns section is data. The "what this means for Intent" section is interpretation. If you write interpretation first, you'll pattern-match the data to it.

2. **Disconfirmations get a dedicated section with equal visual weight to confirmations.** If the disconfirmation section is shorter than the patterns section, you probably missed them.

3. **The panel review of the synthesis is mandatory.** Not optional. If the panel flags confirmation bias, revise before publishing. This is the double-loop check that separates discovery from confirmation theater.
