# Stop-hook posture family: regex vs Kev-4B against blind labels

labeled rows scored: 189 (gold positives 42, negatives 147); unclear labels dropped: 0

| detector | precision | recall | F1 | TP | FP | FN |
|---|---|---|---|---|---|---|
| regex family (any CHECK caught) | 0.38 | 0.90 | 0.53 | 38 | 63 | 4 |
| Kev P(queues) >= 0.5 | 0.45 | 0.83 | 0.58 | 35 | 43 | 7 |
| Kev deferral_class == bare_handback | 0.54 | 0.48 | 0.51 | 20 | 17 | 22 |

Kev AUC for P(queues_authorized_work) against blind labels: 0.821

Among 101 regex fires: 38 true, 63 false by gold. Kev at 0.5 would suppress 32 of the false fires and wrongly suppress 4 of the true ones.
Among 88 rows no CHECK caught: 4 are handbacks by gold (regex misses); Kev catches 1 of them.

| CHECK | fires | true by gold | Kev positive |
|---|---|---|---|
| CHECK1-CAUGHT | 16 | 10 | 15 |
| CHECK2-CAUGHT | 8 | 4 | 8 |
| CHECK4-CAUGHT | 15 | 2 | 7 |
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

Kev latency per tail (wall ms): median 4610, p90 11278, n 189
