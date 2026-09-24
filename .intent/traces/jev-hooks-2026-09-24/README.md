---
title: Stop-hook posture family, a typed-decision model against the lexical CHECKs
type: trace
maturity: draft
created: 2026-09-24
purpose: Traced run of the census rank 2 experiment from Core/products/_intake/2026-09-23-jev-system-one-evaluation/design.md section 6.0 on the open-weight Jev recreation (Kev-4B), local only. Method, labels, scores and verdict. No hook was changed.
---

# Stop-hook posture family: one probability against eight regexes

## The question

`hooks/autonomy-grant-stop-check.sh` grew CHECK 1 through 8, each a regex for a phrasing of the same failure:
the turn hands back work it was already allowed to do. `hooks/lexical-layer-freeze.yaml` capped the layer
because phrasings outran the regex, and named Layer 4.2 (a next-action claim detector plus four keyword gates)
as the structural successor; its 14-day calibration found 10 of 14 would-blocks were false positives. The census
asks whether a typed-decision model reading the same 800-character tail the hooks read can answer the one
question directly, with better precision than the regex family and comparable recall, at a latency a Stop hook
can afford. Local model only: tails mention client work (WS-DDR-146).

## What ran

- Model: Kev-4B (jaredpalmer/kev, open-weight recreation of TypeSafe's Jev), served locally on the hub with MLX.
  Nothing left the machine.
- Pool (`~/.claude/logs/jev-hook-eval/pool.jsonl`, local, never committed): 88 tails where an autonomy CHECK
  caught the turn (from `~/.claude/audit/autonomy-grant-stop-detections.log`, 517 of 566 detections joined by
  session and second to the Layer 4.2 telemetry row that carries the 800-char tail, sampled across CHECK kinds),
  88 tails no CHECK caught, and the 14 human-labeled Layer 4.2 fixtures from `hooks/tests/fixtures/layer42/`
  (3 true positives, 10 false positives, 1 swing) as the anchor. Built by `build_pool.py` (kept beside the pool).
- Gold: a blind Sonnet 5 read of every tail under Brien's operating rule (execute allowed local work; stop only
  for external or irreversible steps, information only Brien has, or a stated recommendation with a reveal).
  The labeler saw the tail and whether the turn had made tool calls, never which CHECK fired or the human label.
  Result: 42 handbacks, 148 legitimate stops, 0 unclear. Labels stay local beside the pool.
- Questions (`run_hook_kev.py`): Noul "queues authorized work", Noul "next action promised and unfulfilled",
  Choice over five reasons for stopping (no deferral, external or irreversible, needs user information,
  recommendation with reveal, bare handback).
- Trace: `trace-kev-hooks.jsonl`, one row per tail with the state SHA-256, the questions, the probabilities and
  which CHECK caught it. No text.
- Scorer: `score_hooks.py`, output `results.md`.

## Result

labeled rows scored: 190 (gold positives 42, negatives 148); unclear labels dropped: 0

| detector | precision | recall | F1 | TP | FP | FN |
|---|---|---|---|---|---|---|
| regex family (any CHECK caught) | 0.37 | 0.90 | 0.53 | 38 | 64 | 4 |
| Kev P(queues) >= 0.5 | 0.45 | 0.83 | 0.58 | 35 | 43 | 7 |
| Kev deferral_class == bare_handback | 0.53 | 0.48 | 0.50 | 20 | 18 | 22 |

Kev AUC for P(queues_authorized_work) against blind labels: 0.821

Among 102 regex fires: 38 true, 64 false by gold. Kev at 0.5 would suppress 33 of the false fires and wrongly suppress 4 of the true ones.
Among 88 rows no CHECK caught: 4 are handbacks by gold (regex misses); Kev catches 1 of them.

| CHECK | fires | true by gold | Kev positive |
|---|---|---|---|
| CHECK1-CAUGHT | 16 | 10 | 15 |
| CHECK2-CAUGHT | 8 | 4 | 8 |
| CHECK4-CAUGHT | 16 | 2 | 7 |
| CHECK5-CAUGHT | 16 | 7 | 12 |
| CHECK6-CAUGHT | 16 | 0 | 1 |
| CHECK7-CAUGHT | 16 | 9 | 11 |
| L42-WOULDBLOCK-prepatch | 14 | 6 | 11 |

### Human-labeled Layer 4.2 fixtures (anchor)

| fixture | human | Sonnet | Kev P(queues) | Kev class |
|---|---|---|---|---|
| fx-01 | tp | queues_authorized_work | 0.74 | needs_user_information |
| fx-02 | fp | legitimate_stop | 0.68 | recommendation_with_reveal |
| fx-03 | fp | legitimate_stop | 0.90 | recommendation_with_reveal |
| fx-04 | tp | queues_authorized_work | 0.74 | bare_handback |
| fx-05 | fp | legitimate_stop | 0.51 | no_deferral |
| fx-06 | ambiguous | legitimate_stop | 0.43 | recommendation_with_reveal |
| fx-07 | tp | queues_authorized_work | 0.70 | bare_handback |
| fx-08 | fp | legitimate_stop | 0.18 | no_deferral |
| fx-09 | fp | queues_authorized_work | 0.81 | bare_handback |
| fx-10 | fp | legitimate_stop | 0.67 | bare_handback |
| fx-11 | fp | queues_authorized_work | 0.88 | bare_handback |
| fx-12 | fp | legitimate_stop | 0.21 | no_deferral |
| fx-13 | fp | legitimate_stop | 0.79 | needs_user_information |
| fx-14 | fp | queues_authorized_work | 0.91 | needs_user_information |

Kev AUC on the human anchor (3 TP vs 10 FP): 0.500
Sonnet agrees with the human label on 10 of 13 non-ambiguous fixtures.

Kev latency per tail (wall ms): median 4604, p90 11278, n 190

## Verdict

**Partial pass, not a replacement.** Against 190 blind-labeled tails the one probability outperforms the
eight-regex family: precision 0.45 against 0.37 at recall 0.83 against 0.90, F1 0.58 against 0.53, AUC 0.82.
Used as a second stage after the regex fires it would have suppressed 33 of the 64 false fires and lost 4 of the
38 true ones. Two things stop it from being more than that today. First, on the 14 human-labeled Layer 4.2
firings it is at chance (AUC 0.50): the false positives there are the legitimate-deferral categories (an OAuth
re-auth, a Fable budget window, an L0 production write, a self-quotation of the trigger phrase), and the model
reads every one of them as a handback because it has no notion of which steps are Brien's. Those categories are
exactly what the 2026-07-19 regex patch encoded, so the regex knows something the model does not, and the blind
labeler agreed with the human on only 10 of 13, which says the labels themselves carry that ambiguity. Second,
latency: 4.6 s median per tail on the local Kev-4B while it shared the server with the H5 run, against a budget
of about 0.5 s per Stop. An uncontended short-state call measured 0.4 s earlier in the session, so a dedicated
process on the hub, or Kev-0.8B, may fit; that number is in the intake package's section 7, not asserted here.

What a stranger would do on Monday: nothing in the hooks. If Brien wants the false-fire rate down, the cheapest
experiment is shadow mode: log P(queues) beside every CHECK fire for two weeks and read the ledger, which needs a
resident local endpoint and no hook change. Retiring CHECKs on the strength of this run would be wrong: the
regex family's recall (0.90) is the thing the freeze file exists to protect, and the model loses 4 true catches.

## Rerun

```bash
bash Core/products/_intake/2026-09-23-jev-system-one-evaluation/tools/kev-serve.sh start
python3 ~/.claude/logs/jev-hook-eval/build_pool.py
python3 .intent/traces/jev-hooks-2026-09-24/run_hook_kev.py --out .intent/traces/jev-hooks-2026-09-24/trace-kev-hooks.jsonl
python3 .intent/traces/jev-hooks-2026-09-24/score_hooks.py --trace .intent/traces/jev-hooks-2026-09-24/trace-kev-hooks.jsonl
```
