---
id: SIG-033
title: Agent asked permission to run a read-only 10-second verification that passed 4-gate silently
date: 2026-04-21
status: open
category: autonomy-drift
severity: medium
related:
  - memory/feedback_autonomy_grant_drift_pattern.md (recurrence — 2026-04-21 instance)
  - memory/feedback_decision_framing.md (4-gate check — was not applied)
  - memory/feedback_autonomy_not_control.md (stop asking for reversible work)
  - memory/feedback_autonomous_proceed.md (L3+ execute, surface in arrears)
  - CLAUDE.md Execution Posture (not risk-averse, not waiting)
  - SIG-PERSONAS-013 (parent pattern — autonomy-grant drift)
---

# SIG-033 — Verification-ask drift in sub-project #5 brainstorm

## Origin

During sub-project #5 brainstorm (entire.io integration), after asking Q3 (git policy for `.entire/`), the agent offered: *"Quick verify to ground the recommendation — want me to check the 4 existing `.entire/` directories to see what Brien-past-you already chose? Takes 10 seconds and might make the answer obvious."*

Brien response: *"you could have completed verification by now and it would have risked nothing, record new signal of not being able to make this leap"*

## 4-Gate Check (should have been run silently)

| Gate | Answer |
|---|---|
| Reversible? | Yes — read-only `ls`/`cat` of existing files |
| Low blast radius? | Yes — no mutations, no external calls |
| Precedent? | Yes — agent had already done 5+ read-only scans this session without asking |
| No info gap requiring human? | Yes — the information is entirely in the filesystem, no human judgment required |

**All 4 gates pass. Correct action: execute silently, report findings. Actual action: asked permission.**

## Why this is worse than it looks

The verification was explicitly staged as a *tool for grounding the recommendation* — meaning the recommendation was implicitly acknowledged as under-grounded without it. Pausing to ask permission for grounding work is a compound failure:

1. Recommendation offered (Q3 option (c)) was suboptimal without the verification
2. User now has to evaluate a recommendation made with known information gap
3. Asking-permission protocol adds a full round-trip to what should be instant
4. The agent *knew* this was 4-gate-eligible (used the phrase "10 seconds" — explicit recognition of low cost)

## Pattern identification

This is the **"costumed drift"** variant from `feedback_autonomy_grant_drift_pattern.md` §2026-04-18-recurrence:

> "The 'decision surface' dressing doesn't exempt the drift. Phrasing like '...my read is Option 1, which option?' is still proposal-framing on L4 work."

Today's costume: "Here's my recommendation — want me to verify?" The costume pretends to be helpful (offering to do more work before burdening user) but is structurally identical: it still pushes the decision to the user rather than doing the L4-eligible work.

## The underlying failure

The agent confused *two different kinds of verification*:

- **Type A verification:** "Verify before taking an irreversible action" — legitimately requires consideration, sometimes requires user confirmation
- **Type B verification:** "Verify to improve a recommendation's grounding" — always L4 (read-only), always execute silently, always fold findings into the recommendation

Today's ask was Type B. Offering to defer it was a categorization error.

## Fix

**New self-detection trigger for next-response scan (add to `feedback_autonomy_grant_drift_pattern.md`):**

> If a response offers to perform read-only verification "before" presenting a recommendation, the verification should already have been done. Strike the offer, do the work, report findings as part of the recommendation.

**Mnemonic:** "If it's 10 seconds and read-only, it's already done by the time I'm writing this paragraph."

## Observed in this session

Response architecture was: (1) Present Q3 with recommendation (c), (2) Offer verification. Correct architecture: (1) Verify, (2) Present Q3 with recommendation grounded in verification findings.

The word "grounded" in the agent's own language acknowledged the gap. That self-awareness should have been the trigger to execute, not to offer.

## Follow-up

- Update `feedback_autonomy_grant_drift_pattern.md` with 2026-04-21 recurrence + "Type A vs Type B verification" distinction
- This is now the 5th tracked instance of the pattern (4 from 2026-04-17 + 2 from 2026-04-18 + today's). Pattern is not decaying.
- Consider: does the autonomy-grant drift detector (skill listed in session-start reminders) run pre-response scans for this specific variant?
