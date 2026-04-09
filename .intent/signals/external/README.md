# External Signals — Discovery Interview Outputs

## What lives here

This directory holds external signals — one file per discovery interview. These are distinct from the internal signals in the parent `.intent/signals/` directory.

**Internal signals** (parent directory): Observations from Brien and agents building Intent. Useful for improving Intent's own loop but subject to confirmation bias when treated as discovery.

**External signals** (this directory): Verbatim observations from practitioners who don't know Intent, don't care about its internal narrative, and have no incentive to confirm its hypothesis. These are the signals that validate or invalidate Intent's claims.

## Naming

`YYYY-MM-DD-interview-[participant-slug].md`

- `participant-slug` can be:
  - `firstname-lastname` (if participant consented to named attribution)
  - `role-company-anon` (if anonymized)
  - `p-NN` (if fully anonymous)

## Template

Use `.intent/discovery/wave-1/02-external-signal-template.md` as the starting format.

## Discipline rules

1. **Raw data first.** Paste verbatim quotes before writing any interpretation. Interpretation goes in a clearly-labeled section at the bottom.

2. **Disconfirmations are the gift.** If a participant contradicts Intent's hypothesis, that is the most valuable signal in the file. Give it a dedicated section. Do not bury it.

3. **Quality scoring before publishing.** Use the rubric in `01-interview-protocol.md`:
   - Specificity (cited real recent moments?)
   - Frequency (daily/weekly/monthly?)
   - Investment (built or bought anything?)
   - Team-wide (just them or consensus?)
   - Disconfirmation (did they challenge us?)

4. **Consent before publishing.** No external signal is published publicly or synthesized into themes until the participant has reviewed their quotes.

5. **Separate signal from interpretation.** Brien's interpretation goes in a dedicated section labeled "Interpretation (first-pass, unvalidated)." The interpretation does not count as finding until validated across all 10 interviews.

## Synthesis

After all interviews in a wave are complete:
1. Read all signals back-to-back in one sitting
2. Write synthesis using `.intent/discovery/wave-1/05-synthesis-template.md`
3. Build opportunity tree using `.intent/discovery/wave-1/06-opportunity-tree-template.md`
4. Run panel-review for confirmation bias check before publishing
5. Publish synthesis to `knowledge/themes/` and OST to `knowledge/domain-models/`

## Wave tracking

| Wave | Dates | Count | Status |
|------|-------|-------|--------|
| 1 | 2026-04-XX to 2026-04-XX | 10 (planned) | planned |

## Relationship to Intent

External signals feed INT-010 (External Discovery Interviews) and DEC-20260409-01 (Post-panel review response). They are the direct corrective to SIG-043 (Discovery theater — N=1 external voice).

Every external signal captured here is a step toward invalidating or validating Intent's hypothesis with actual evidence from practitioners who have nothing to prove to us.
