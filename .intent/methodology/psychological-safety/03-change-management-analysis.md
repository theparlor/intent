# Change Management Analysis — Intent Adoption Through Bridges + Kotter

> The Org Design panel's verdict: *"A system design masquerading as a change program. Will work in adhocracies; dies in machine bureaucracies. Change work is the missing muscle."*
>
> This document applies William Bridges' transition model and John Kotter's 8-step framework to Intent adoption, with the power-shift table the panel produced. The goal: name the change work Intent has not yet done.

## Why change management matters here

Intent's current adoption narrative is entirely about what to START doing: write signals, run the loop, adopt the ontology, ship the CLI. There is almost nothing about what to STOP doing, who loses power in the transition, what rituals are ending, or what the neutral zone between old and new looks like.

William Bridges' research is unambiguous: transformations fail when the **ending** is unacknowledged. Not when the new beginning is underbuilt — when the grief of what's being released is treated as trivial or absent. Teams don't resist change because the new thing is bad. They resist because the old thing held meaning the change ignored.

Intent has a change management gap for five specific reasons:
1. The site is all "new beginning" — architecture, loop, ontology, dashboards
2. The losers are never named
3. The rituals being replaced are never acknowledged
4. The neutral zone (4-8 weeks of operating in both modes) has no playbook
5. The cultural prerequisites are assumed, not surfaced

This document addresses each.

---

## The power shift (from the Org Design panel)

| Gains power | Loses power | Will actively resist |
|---|---|---|
| Solo ICs with high spec clarity (can now command agent execution) | Scrum Masters, RTEs, Delivery Coaches (artifacts are obsolete) | **PMOs** — roll-up reports depend on ticket hierarchies |
| Architects (Practitioner-Architect is the canonical persona) | Traditional PMs whose value was prioritization committees | **Finance/Capacity planning** — story points were headcount allocation proxies |
| AI-fluent senior engineers | Junior engineers whose role was "do the ticket" (the productive struggle disappears) | **Auditors/Compliance** — Git-as-source-of-truth is alien to SOX/ITIL shops |
| "The operator" reviewing specs | Anyone whose identity was "good at running Jira" | **Middle management** translating strategy to tickets |

### What the site should say but doesn't

This table — or a version of it — should appear on the Intent site. Not hidden in docs. Above the fold of a "Who loses" page. Hiding the losers from the pitch guarantees resistance you never see coming, because the resistance forms in rooms you're not in.

**The proposed page:**

> **Honest up front: what Intent takes from people**
>
> If your team adopts Intent, some roles change substantively. Some jobs become more valuable. Some become less differentiating. Some disappear into other roles. You should know this before you try.
>
> [The table above, rendered clearly]
>
> **What this means for the humans affected:**
>
> - Scrum Masters and delivery coaches: your craft of orchestrating human coordination is less load-bearing when the human team is smaller (2–7) and AI agents handle cross-step handoffs. Your craft of facilitating team learning and psychological safety is MORE load-bearing. Intent needs you for the safety work; it doesn't need you for the standup.
>
> - Junior engineers who "did the tickets": the productive struggle of implementing well-defined work disappears. That's a real loss — it was how craft developed. Intent teams need to replace the productive struggle with something else, probably structured spec-shaping apprenticeship. This is not solved.
>
> - PMOs: Intent's git-native event streams do not roll up into the reports your stakeholders expect. You'll either translate between the two worlds or push back on Intent adoption. Both are legitimate.

## Bridges' transition model applied to Intent

Bridges: every transition has three phases, and they happen in this order:

1. **Ending, Losing, Letting Go** — naming what's being released
2. **The Neutral Zone** — the in-between, where the old is gone but the new isn't yet fluent
3. **The New Beginning** — when the new way becomes "just how we work"

Intent's site currently only has content for #3. Here's what #1 and #2 should contain.

### Phase 1 — Ending, Losing, Letting Go (what is Intent asking teams to grieve?)

Being explicit about what ends:

- **Sprint cadence and its rituals.** Sprint planning, retro, review, demo. These are not trivial — they provide predictable rhythm, social cohesion, and the closure of "done." Intent's continuous loop offers none of these. Teams that adopt Intent will feel arrhythmic for weeks.

- **The shared language of story points, velocity, burndown.** An entire vocabulary of estimation becomes obsolete. Estimators lose their craft; stakeholders lose their coordination proxy. The vocabulary took years to learn and now belongs to a defunct operating model.

- **The "done" event.** In sprint-based work, a ticket moves to Done and the person who wrote it gets a small dopamine hit. Intent's event streams are continuous — there is no "done this week" moment. For people who run on weekly completion satisfaction, Intent is emotionally flat.

- **The ceremonies as social glue.** Standups aren't just about coordination — they're where teammates see each other's faces, hear each other's obstacles, and feel part of a whole. If Intent replaces standups with async signal capture, it replaces social presence with text. That's a loss, not a neutral substitution.

- **The identity "I'm good at running our process."** Scrum Masters, team leads, ops people, PMOs — many humans built their identity around being the person who runs the ceremony stack. Intent makes that identity obsolete. The humans are still needed; their specific craft pattern is not.

- **Large-team safety-in-numbers.** Over-7-person teams are explicitly out of scope (DEC-20260409-02). For people whose career has been building and managing large teams, Intent is a hostile methodology. It says their coordination craft is a symptom of the wrong operating model.

**What the site should say (proposed Ending page):**

> **Intent asks you to release:**
>
> The sprint rhythm. Story points and velocity. Burndown charts. The "done this week" closure moment. Standups as social presence. The identity "I'm the person who keeps our process running." Large-team coordination craft.
>
> These are not trivial releases. They were real scaffolding. Teams that release them too fast will feel arrhythmic, disoriented, and socially thinner. Teams that try to keep them while also adopting Intent will get half of both — the overhead of the old without the leverage of the new.
>
> If you're adopting Intent, give yourself permission to grieve. Name what's ending out loud in a team meeting. Let people say what the old way gave them that the new way doesn't yet match. Do this before you start writing signals.

### Phase 2 — The Neutral Zone (what does week 3 look like?)

Bridges calls the neutral zone "chaos, creativity, and confusion." For Intent, it's the period (maybe 4–8 weeks) where the team has stopped doing the old thing fluently but hasn't yet developed muscle memory for the new thing. This is where most transformations die — not in Phase 1 from grief, and not in Phase 3 from failure to learn, but in Phase 2 from exhaustion.

Intent has NO neutral zone playbook. This is a specific deliverable we owe.

**What a neutral zone playbook needs to contain:**

1. **Permission to be bad at both.** Week 3 of Intent adoption: your team is bad at sprints (you stopped) and bad at Intent (you haven't internalized it). That is normal and temporary. Name it out loud.

2. **A weekly ritual that replaces the retro.** Something structured and recurring so people have a predictable moment to process the transition. Not Intent's continuous loop — a separate ritual specifically for "how are we adjusting?"

3. **A safety valve back to the old way.** Teams need to know they can go back if Intent doesn't work. Irreversible adoption creates panic. Reversible adoption creates curiosity.

4. **A visible "practice board" showing what's being tried.** Intent's event stream is not this — it's work output. The practice board is a meta-view of "what adoption experiments are we running this week?"

5. **Weekly check-in with psychological safety specifically on the agenda.** Not a vibes check — a structured conversation about whether people feel safe capturing signals, disagreeing with specs, and asking for help.

6. **Ending dates on old tools.** "We will stop running standups on 2026-05-01." Teams need a clear ending, not a gradual fade. Bridges is explicit about this.

7. **A "buddies" structure.** Pair each person with a buddy for the transition. The buddy is not a mentor — they're someone to vent to about the transition without it being a team discussion.

**What the site should say (proposed Neutral Zone playbook page):**

> **Weeks 3–8 of Intent adoption are the hardest part. Here's the playbook.**
>
> [The seven elements above, written as practical guidance]
>
> The neutral zone feels chaotic because you've released the old and haven't yet internalized the new. That's expected. The playbook above isn't a fix — it's a scaffold to keep the team intact while the new muscle memory develops.

### Phase 3 — The New Beginning (what the site already has)

This is what the current Intent site is 95% of: architecture, loop, ontology, CLI, agents, observability. All valid, all necessary for Phase 3, all premature without Phases 1 and 2.

**Rebalance needed:** When the site is rebuilt (INT-012), the Phase 1 (Ending) and Phase 2 (Neutral Zone) content should take roughly equal visual weight to the Phase 3 (New Beginning) content. Not because they're equally long, but because their presence changes the emotional reception of the whole site.

---

## Kotter's 8-step framework applied to Intent

John Kotter's research on why 70% of change initiatives fail identifies 8 steps that successful transformations follow. Most methodologies address steps 5–8 and skip 1–4. Intent is no exception.

### Step 1 — Establish a sense of urgency

**What Kotter demands:** Name the present danger. Make the cost of the status quo concrete.

**What Intent has:** The pitch page names the urgency for the CTO (AI changed the constraint, your toolchain didn't), but not for the practitioner on the team. The practitioner doesn't feel present danger — their work is slightly annoying, not burning.

**Gap:** Translate the urgency to the IC experience. What does the IC lose this year if their team doesn't adapt? (Answer: probably their job as an IC, in 18 months, when the senior leadership realizes the 12-person team should be a 4-person team. This is uncomfortable to say but it's the actual urgency.)

### Step 2 — Form a guiding coalition

**What Kotter demands:** Assemble a team with enough power to lead the change.

**What Intent has:** Nothing. There is no concept of a guiding coalition for Intent adoption. The implicit assumption is that one architect adopts it and the team follows.

**Gap:** For team-level adoption, who is the coalition? Probably: 1 senior engineer + 1 PM + 1 engineering manager + 1 skeptic. The skeptic is critical — a guiding coalition without a skeptic is an echo chamber.

### Step 3 — Develop a vision and strategy

**What Intent has:** Plenty. Notice→Spec→Execute→Observe, three-layer architecture, trust-scored autonomy.

**Gap:** The vision is too abstract for adoption. "The operating model for AI-augmented teams" is a vision for the industry, not a vision for one team trying it next month. A team-level vision would be: "By week 8, we will capture friction as signals, resolve ambiguity as specs, and let agents execute the clear work. We'll ship faster on the unambiguous work and spend more time on the ambiguous."

### Step 4 — Communicate the change vision

**What Kotter demands:** Communicate the vision 10x more than you think you need to, through many channels.

**What Intent has:** The site. One channel. Written once.

**Gap:** Teams adopting Intent need repeated communication. Kotter's rule is that the vision is communicated 10x more than intuition suggests. Intent has no "what to say in your team meeting" talking points, no "how to explain it to your skeptic" script, no "how to report progress to leadership" template.

### Step 5 — Empower broad-based action

**What Intent has:** The loop and the CLI. Empowers ICs to capture signals and shape specs without permission.

**Assessment:** Intent is reasonably strong on Step 5. The disambiguation signal pattern is an empowerment primitive — anyone can surface friction without asking.

### Step 6 — Generate short-term wins

**What Kotter demands:** Plan for visible wins at week 2, week 4, week 8. Celebrate them.

**What Intent has:** Nothing explicit. Intent adoption is presented as an all-or-nothing methodological shift.

**Gap:** What's the week 2 win? Probably: "we captured 10 signals, clustered them into 2 intents, and shipped one spec to Claude Code that worked first-try." That's a concrete, short-term, celebratable moment. The adoption playbook should list these week-by-week milestones with explicit celebration instructions.

### Step 7 — Consolidate gains and produce more change

**What Intent has:** The loop itself is self-reinforcing if it works. The continuous feedback is the consolidation mechanism.

**Assessment:** Reasonably strong if Phases 1–2 have been handled.

### Step 8 — Anchor new approaches in the culture

**What Kotter demands:** Explicit cultural integration. "This is how we do things here." New hires learn the new way, not the old.

**Gap:** Intent has no guidance on how to onboard new team members into a team that's already adopted Intent. The new hire walks into a team that uses vocabulary and rituals (signals, intents, specs, contracts) that aren't in any onboarding doc. This is a durable culture-integration hole.

---

## Summary: Intent's change management gap

Intent addresses Kotter steps 3 and 5 reasonably well. It has almost nothing for steps 1, 2, 4, 6, 7, 8, or Bridges' Phases 1 and 2.

**The change work Intent owes its adopters:**

1. **An "Ending" page** — what teams release, with explicit permission to grieve
2. **A "Neutral Zone playbook"** — the 4-8 weeks between old and new, with specific rituals
3. **A "Who loses power" page** — the honest-upfront version of the power shift table
4. **A "Week-by-week adoption playbook"** — Kotter steps 1, 4, 6, 8 made concrete
5. **A "Guiding coalition" template** — who to recruit before adopting
6. **An "Onboarding a new hire to an Intent team" guide** — Kotter step 8 concretized
7. **Cultural readiness checklist** — Schein-level assumptions surfaced
8. **Talking points for the skeptic** — how to explain Intent to someone who thinks Jira works fine

This is substantial work. It is a parallel track to the engineering hardening and content rebuild. It becomes INT-013 (see `04-int-013-outline.md`).

## Connection to psychological safety

The change management work is NOT separable from the psychological safety work. They are two views of the same problem:

- Psychological safety asks: "Is it safe to be here while this is changing?"
- Change management asks: "Is the change being led in a way that honors what's ending?"

A team with great psych safety and bad change management will panic. A team with great change management and bad psych safety will comply and lie. You need both.

This is why INT-013 is a combined **Safety + Change workstream**, not two separate intents.

## Lineage and attribution

- **William Bridges** — *Managing Transitions* (2009, 4th ed.) — the ending / neutral zone / new beginning framework
- **John Kotter** — *Leading Change* (1996, updated 2012) — 8 steps and the 70% failure statistic
- **Edgar Schein** — *Organizational Culture and Leadership* (2016) — cultural assumptions surfacing
- **Amy Edmondson** — *The Fearless Organization* and *Teaming* — interpersonal safety as change prerequisite
- **Jonathan Smart** — *Sooner Safer Happier* — change work as a first-class engineering discipline
- **Org Design panel, 2026-04-09** — critiqued Intent's change management gap as the biggest adoption risk
- **Brien's session of 2026-04-09** — committed target user, infrastructure prerequisites, safety contract stance
