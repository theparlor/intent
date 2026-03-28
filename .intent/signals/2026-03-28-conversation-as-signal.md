# Signal: Conversations as the Notice Layer

ID: SIG-003
Date: 2026-03-28
Status: Captured

## Problem

The notice layer (capture of signals) is often manual: transcripts, meeting notes, Slack summaries. This is lossy and creates friction.

## Insight

Conversations (design sessions, pair programming, interviews) are signal sources. They should feed the notice layer with minimal friction.

## Three Mechanisms

### 1. During-Session Signal Writing

While discussing a problem, one person writes signals into `.intent/signals/` in real-time:

```markdown
# Signal: Permission model unclear

ID: SIG-004
Date: 2026-03-28
Duration: 2026-03-28T14:00Z to 2026-03-28T14:45Z
Participants: Alice, Bob, Carol
Context: Design session for ACL redesign

## Observation

"We're building role-based access but not sure if users with 'viewer' role should see metadata."

## Constraint

"GDPR compliance requires we don't expose certain fields even to viewers."

## Decision

"Viewers can see resource list but not audit logs or change history."
```

### 2. Post-Session Extraction

After a meeting, run a tool to extract signals from transcript:

```
python3 extract_signals.py transcript.txt --output .intent/signals/
```

Output: Markdown file with extracted signals, organized by theme.

### 3. Scheduled Observe-Cycle

Daily (or per-sprint) "observe" session reviews what was built and feeds back:

```markdown
# Signal: Permission model works, but slow

ID: SIG-005
Date: 2026-03-28
Source: Observe cycle
Context: Post-deployment monitoring

## Observation

ACL checks are taking 200ms avg per request (p99: 800ms).

## Impact

API endpoints are 15% slower since ACL rollout. Users report timeouts.

## Proposed Direction

Cache roles in memory, invalidate on update.
```

## Design Constraint

**High precision, low volume.** Not every mention of a problem is a signal. Signals should be:
- **Specific**: Not "performance is bad", but "ACL checks take 200ms avg"
- **Actionable**: Includes enough context for someone to write a spec
- **Traceable**: Links to source (meeting date, monitoring alert, etc.)

## Integration

- Signals live in git, so they're under version control
- Each signal is a file, so it's independently linkable
- Signals feed Intents, which feed Specs
- The notice layer is transparent and auditable

## Benefits

- No separate "transcription" system
- Signals are git-native, integrated with code review
- Conversations naturally flow into work
- Easy to reference signals in spec discussions ("This spec responds to SIG-003")
