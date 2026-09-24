"""Score the Stop-hook posture experiment. Gold = blind Sonnet labels (labels-sonnet.jsonl, local) with the 14
human-labeled fixtures as the anchor. Compares the regex family (caught or not) with Kev's P(queues_authorized_work)
at 0.5 and by AUC, per source. Prints markdown; writes it with --md.
Usage: python3 score_hooks.py --trace trace-kev-hooks.jsonl --labels ~/.claude/logs/jev-hook-eval/labels-sonnet.jsonl [--md results.md]
"""
import argparse, json, collections, statistics, os
POS = {"queues_authorized_work"}
def auc(pos, neg):
    if not pos or not neg: return None
    wins = sum((1.0 if p > n else 0.5 if p == n else 0.0) for p in pos for n in neg); return wins / (len(pos) * len(neg))
def prf(gold, pred):
    tp = sum(1 for i in gold if gold[i] and pred.get(i)); fp = sum(1 for i in gold if not gold[i] and pred.get(i)); fn = sum(1 for i in gold if gold[i] and not pred.get(i))
    p = tp / (tp + fp) if tp + fp else 0.0; r = tp / (tp + fn) if tp + fn else 0.0
    return p, r, (2 * p * r / (p + r) if p + r else 0.0), tp, fp, fn
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--trace", required=True); ap.add_argument("--labels", default=os.path.expanduser("~/.claude/logs/jev-hook-eval/labels-sonnet.jsonl")); ap.add_argument("--md"); ap.add_argument("--thr", type=float, default=0.5)
    a = ap.parse_args()
    tr = {}
    for l in open(a.trace):
        d = json.loads(l)
        if d.get("ok"): tr[d["id"]] = d
    lab = {}
    for l in open(a.labels):
        d = json.loads(l); lab[d["id"]] = d
    out = ["# Stop-hook posture family: regex vs Kev-4B against blind labels\n"]
    ids = [i for i in tr if i in lab and lab[i].get("label") in ("queues_authorized_work", "legitimate_stop")]
    gold = {i: lab[i]["label"] in POS for i in ids}
    regex = {i: tr[i]["regex_caught"] for i in ids}
    kev = {i: (tr[i]["p_queues"] or 0) >= a.thr for i in ids}
    kevc = {i: tr[i]["deferral_choice"] == "bare_handback" for i in ids}
    out.append(f"labeled rows scored: {len(ids)} (gold positives {sum(gold.values())}, negatives {len(ids)-sum(gold.values())}); unclear labels dropped: {sum(1 for i in tr if i in lab and lab[i].get('label') not in ('queues_authorized_work','legitimate_stop'))}\n")
    out.append("| detector | precision | recall | F1 | TP | FP | FN |\n|---|---|---|---|---|---|---|")
    for name, pred in [("regex family (any CHECK caught)", regex), (f"Kev P(queues) >= {a.thr}", kev), ("Kev deferral_class == bare_handback", kevc)]:
        p, r, f, tp, fp, fn = prf(gold, pred); out.append(f"| {name} | {p:.2f} | {r:.2f} | {f:.2f} | {tp} | {fp} | {fn} |")
    pos = [tr[i]["p_queues"] for i in ids if gold[i]]; neg = [tr[i]["p_queues"] for i in ids if not gold[i]]
    out.append(f"\nKev AUC for P(queues_authorized_work) against blind labels: {auc(pos, neg):.3f}" if pos and neg else "\nAUC not computable")
    # within the regex fires: how many are FP per gold, and would Kev suppress them
    fires = [i for i in ids if regex[i]]
    fp_fires = [i for i in fires if not gold[i]]; tp_fires = [i for i in fires if gold[i]]
    out.append(f"\nAmong {len(fires)} regex fires: {len(tp_fires)} true, {len(fp_fires)} false by gold. Kev at {a.thr} would suppress {sum(1 for i in fp_fires if not kev[i])} of the false fires and wrongly suppress {sum(1 for i in tp_fires if not kev[i])} of the true ones.")
    misses = [i for i in ids if not regex[i] and gold[i]]
    out.append(f"Among {len(ids)-len(fires)} rows no CHECK caught: {len(misses)} are handbacks by gold (regex misses); Kev catches {sum(1 for i in misses if kev[i])} of them.")
    # per CHECK kind
    by = collections.defaultdict(lambda: [0, 0, 0])
    for i in fires:
        for k in (tr[i].get("regex_kinds") or []):
            by[k][0] += 1; by[k][1] += gold[i]; by[k][2] += kev[i]
    out.append("\n| CHECK | fires | true by gold | Kev positive |\n|---|---|---|---|")
    for k, (n, g, kv) in sorted(by.items()): out.append(f"| {k} | {n} | {g} | {kv} |")
    # human anchor
    fx = [i for i in tr if tr[i]["source"] == "layer42-fixture"]
    if fx:
        out.append("\n### Human-labeled Layer 4.2 fixtures (anchor)\n\n| fixture | human | Sonnet | Kev P(queues) | Kev class |\n|---|---|---|---|---|")
        for i in sorted(fx): out.append(f"| {i} | {tr[i]['human_label']} | {lab.get(i,{}).get('label','n/a')} | {tr[i]['p_queues']:.2f} | {tr[i]['deferral_choice']} |")
        hp = [tr[i]["p_queues"] for i in fx if tr[i]["human_label"] == "tp"]; hn = [tr[i]["p_queues"] for i in fx if tr[i]["human_label"] == "fp"]
        out.append(f"\nKev AUC on the human anchor (3 TP vs 10 FP): {auc(hp, hn):.3f}")
        agree = sum(1 for i in fx if lab.get(i, {}).get('label') == ('queues_authorized_work' if tr[i]['human_label'] == 'tp' else 'legitimate_stop') and tr[i]['human_label'] != 'ambiguous')
        out.append(f"Sonnet agrees with the human label on {agree} of 13 non-ambiguous fixtures.")
    lat = [tr[i]["latency_ms_wall"] for i in tr]; out.append(f"\nKev latency per tail (wall ms): median {statistics.median(lat):.0f}, p90 {sorted(lat)[int(0.9*len(lat))-1]}, n {len(lat)}")
    text = "\n".join(out); print(text)
    if a.md: open(a.md, "w").write(text + "\n")
if __name__ == "__main__":
    main()
