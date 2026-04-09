# Interview Protocol — Discovery Wave 1 (Mom Test applied to Intent)

> The Mom Test (Rob Fitzpatrick) says: never ask "would you use X?" Ask about past behavior, specific struggles, and real money/time commitments. If you have to convince someone the problem is real, it isn't real enough.

## Purpose

Run 10 structured discovery interviews with senior ICs and PMs using Claude Code (or equivalent AI dev tools) daily, to validate or invalidate Intent's core hypothesis:

**Hypothesis:** When AI collapses implementation cost, the bottleneck moves upstream to specification clarity, and existing ticket-based coordination tools optimize for the wrong thing.

**What success looks like:** 7 of 10 participants describe the spec-clarity bottleneck in their own words, unprompted, with specific recent examples — OR the hypothesis is invalidated and we learn something else is actually the bottleneck.

**What we do NOT do:** Ask "would you use Intent?" or "does this sound useful?" Those questions generate polite lies.

## Interview format

- **Length:** 45 minutes (30 min structured + 15 min buffer)
- **Format:** Remote, video on, recorded with permission
- **Protocol:** Open-ended exploration first, structured probes second, NO demo/pitch until the interview is complete (and only if asked)
- **Note-taker:** Separate person if available (Brien can't both lead and note); otherwise record + transcribe
- **Confidentiality:** Participant can review notes before publishing, can request anonymization, can withdraw at any time

## What we are NOT allowed to do

❌ "Would you use a tool that..."
❌ "Do you think X is a problem?"
❌ "Does this sound useful?"
❌ Show the Intent site during the interview
❌ Describe the Notice→Spec→Execute→Observe loop
❌ Mention Intent by name until the closing minutes
❌ Ask hypothetical future questions ("if you could...")
❌ Lead the witness toward the hypothesis
❌ Celebrate agreement or push back on disagreement

## What we ARE trying to do

✅ Hear about specific recent situations in the participant's own words
✅ Learn what they actually do (not what they say they'd do)
✅ Find out what they've paid for, hacked together, or given up on
✅ Discover pains we haven't thought of
✅ Discover that our hypothesis is wrong (this is a valid outcome)
✅ Listen 80%, talk 20%

## The five acts

### Act 1 — Warm-up and context (5 min)

Purpose: establish trust, understand their work environment, not lead.

**Questions:**
1. "Tell me about your current role and team. How big is the team? What do you ship?"
2. "How long have you been using Claude Code / Cursor / Copilot / [their tool] daily?"
3. "Walk me through yesterday. What did you actually do between sitting down at your desk and closing your laptop?"

**What to listen for:**
- Is AI tooling genuinely daily-use, or aspirational?
- What does their team rhythm look like? Sprints? Continuous? Project-based?
- What's the scale of work? (feature work, infra, migrations, greenfield)

**Anti-pattern:** "What do you think about AI changing software development?" — too abstract, generates opinions not evidence.

### Act 2 — Recent friction (10 min)

Purpose: surface the most recent painful moment and understand what made it painful.

**Questions:**
1. "Think of the last time you felt frustrated with your tooling or process. What happened?"
2. "[Let them answer fully.] Tell me more about that specific moment. What had you just done? What did you want to do next?"
3. "Was that a one-off, or does that happen a lot? Roughly how often?"
4. "What did you end up doing to work around it?"
5. "Who else on your team has hit the same thing?"

**What to listen for:**
- Specificity — vague answers ("the tools are slow") are weak signal; specific moments ("yesterday when I was trying to hand off the Stripe webhook spec") are strong signal
- Workarounds — what they've hacked together is stronger signal than what they complain about
- Frequency — once a month vs. daily changes the economics
- Who else — is this idiosyncratic or team-wide?

**Anti-pattern:** "Is clarity a problem for your specs?" — leads the witness.

### Act 3 — The actual work (10 min)

Purpose: understand their real workflow between "I have an idea" and "AI writes code against it."

**Questions:**
1. "Walk me through how a piece of work moves from 'someone has an idea' to 'code is merged.' Use a real recent example."
2. "At what points do you write things down? Where do they live?"
3. "When you hand something to Claude / Cursor / [their AI], what format is it in? A ticket? A doc? A chat message? Something else?"
4. "How often does the AI output match what you actually needed the first time? What do you do when it doesn't?"
5. "What happens when two people disagree about what should be built?"

**What to listen for:**
- Where does specification actually live? (Tickets? Docs? Slack? Their heads?)
- What's the rework rate? (Zero rework = we might be solving a non-problem)
- How is disagreement resolved? (Meeting? Senior opinion? Written back-and-forth?)
- Is there a pattern of "I thought I was being clear but the AI went sideways"?

**Anti-pattern:** "How could specification be better?" — hypothetical, not behavioral.

### Act 4 — Money, time, and hacks (7 min)

Purpose: find out what they've ALREADY invested in solving this pain — time, money, or tool adoption.

**Questions:**
1. "Have you tried anything specifically to make this better? What did you try?"
2. "Do you pay for any tools that are supposed to help with this? Which ones? Do they actually help?"
3. "Is anyone on your team building a hack or workaround for this? Tell me about it."
4. "If you could wave a wand and change one thing about how your team works with AI tools, what would it be? [Note: the only hypothetical allowed — and only at the end of Act 4]"

**What to listen for:**
- Money — paid tools are a stronger signal than complaints
- Hacks — internal scripts, custom workflows, team conventions are strongest signal
- The wand answer — what they describe without our constraints is what they actually want

**Anti-pattern:** "Would you pay for a tool that...?" — future commitment questions are worth nothing.

### Act 5 — Closing and exit (3 min)

Purpose: close cleanly, offer reciprocity, DO NOT PITCH.

**Questions:**
1. "Is there anything you were expecting me to ask that I didn't?"
2. "Who else should I be talking to? Anyone on your team or in your network who hits these kinds of issues?"
3. "I can share the synthesis of all these interviews with you once it's done — would you like me to?"
4. "Is there anything you'd want to add, correct, or emphasize before we wrap?"

**ONLY if they ask what you're building:** brief, honest answer with hypothesis framing:
> "I'm testing a hypothesis that AI tools have moved the bottleneck from implementation to specification clarity, and that ticket-based tools optimize for the old bottleneck. I'm not ready to show anything — I'm trying to find out if the hypothesis is even right by listening to people like you. I'll share the synthesis once I've talked to ten people."

**Do NOT:** show the site, demo Intent, pitch the loop, ask for commitment.

## Signal quality rubric

After each interview, score the signal on these axes (each 0–1):

| Dimension | Score | What it means |
|-----------|-------|---------------|
| **Specificity** | 0–1 | Did they cite specific recent moments? (vague = 0, specific with dates = 1) |
| **Frequency** | 0–1 | How often does the pain recur? (annual = 0.2, weekly = 0.7, daily = 1) |
| **Investment** | 0–1 | Have they already tried to solve it? (no = 0, built a hack = 0.7, paid for a tool = 1) |
| **Team-wide** | 0–1 | Is it just them or the team? (just them = 0.3, team consensus = 1) |
| **Disconfirmation** | 0–1 | Did they describe something that DISAGREES with our hypothesis? (this is valuable; high disconfirmation = high signal) |

Overall signal strength = weighted average, with **disconfirmation weighted highest** because confirming signals are cheap and misleading.

## Output per interview

For each interview, write a file at `.intent/signals/external/2026-04-XX-interview-[participant-slug].md` using the external signal template. See `02-external-signal-template.md`.

Also capture:
- Verbatim quotes (3-5 per interview, short enough to quote in synthesis)
- Specific anecdotes (1-2 per interview, usable as case studies)
- Disconfirmation moments (anything that contradicted our hypothesis)
- Surprise findings (anything we didn't expect)

## Process safeguards

1. **Brien does not conduct more than 2 interviews per day.** Interview fatigue degrades listening quality.
2. **After every 3 interviews, run a panel-review.** Use the panel-review primitive (INT-007) to have the Discovery/UX panel critique the interview findings for confirmation bias. This is a double-loop safeguard.
3. **If 3 of the first 5 interviews disconfirm the hypothesis, PAUSE.** Don't run the remaining 5 — reopen the hypothesis and redesign the protocol. That's Torres's rule: surprising disconfirmation is cheaper to address early.
4. **Brien cannot edit quotes before synthesis.** Raw transcripts go into the file first. Interpretation comes later. Separating data from analysis is how you avoid confirmation bias.

## Contract with participants

- **Their time is the cost.** Offer to share the synthesis before publication.
- **Their words are the data.** Quotes are attributed or anonymized per their choice.
- **Their pain is valid.** If they describe something we didn't expect, that's the finding — not a deviation from script.
- **Their "no" is the gift.** If they say Intent's hypothesis is wrong, we thank them and record it. Disconfirming signals are more valuable than confirming ones.

## Related artifacts

- `02-external-signal-template.md` — per-interview signal format
- `03-participant-profile.md` — candidate selection criteria
- `04-outreach-template.md` — recruitment message template
- `05-synthesis-template.md` — cross-interview synthesis format
- `06-opportunity-tree-template.md` — Torres OST format for the final output

## Lineage

- **Mom Test** — Rob Fitzpatrick, 2014
- **Continuous Discovery Habits** — Teresa Torres, 2021 (opportunity solution trees, interview snapshots, assumption tests)
- **Customer Development** — Steve Blank, 2005 (get out of the building)
- **Jobs to Be Done** — Clayton Christensen (struggling moments, forces of progress)
