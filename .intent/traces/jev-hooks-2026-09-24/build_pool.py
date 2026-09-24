"""Build the Stop-hook posture pool: response tails from the Layer 4.2 telemetry (800-char tails, every Stop),
joined to the autonomy-grant Stop-hook detections (which CHECK caught) by session + timestamp second.
Sample: up to 80 caught rows stratified by CHECK, 80 uncaught rows, plus the 14 human-labeled Layer 4.2 fixtures.
Output stays LOCAL (this directory): tails mention client work (WS-DDR-146). Committed traces carry hashes only."""
import json, re, random, collections, os, glob, hashlib
H = os.path.expanduser("~/.claude"); random.seed(20260924)
l42 = []
for l in open(f"{H}/logs/autonomy-posture-layer42.jsonl"):
    try: d = json.loads(l)
    except Exception: continue
    if d.get("tail"): l42.append(d)
byk = {(d["session"], d["ts"]): d for d in l42}
caught = collections.defaultdict(list)
for l in open(f"{H}/audit/autonomy-grant-stop-detections.log"):
    m = re.match(r"\[(\S+)\] (\S+) session=(\S+)", l)
    if not m: continue
    ts, kind, sess = m.groups()
    caught[(sess, ts)].append(kind)
joined = [(k, byk[k], v) for k, v in caught.items() if k in byk]
print("l42 rows", len(l42), "detections", len(caught), "joined to a tail", len(joined))
kinds = collections.Counter(v[0] for _, _, v in joined); print("by kind", kinds)
pool = []
per = max(1, 80 // max(1, len(kinds)))
for kind in kinds:
    rows = [j for j in joined if j[2][0] == kind]; random.shuffle(rows)
    for k, d, v in rows[:per + 6]:
        pool.append({"id": hashlib.sha1(f"{k[0]}{k[1]}".encode()).hexdigest()[:10], "source": "l42-telemetry+autonomy-detections", "regex_caught": True, "regex_kinds": v,
                     "ts": k[1], "session": k[0], "tail": d["tail"], "has_tool_use": d.get("has_tool_use"), "gates_pass": d.get("gates_pass"), "next_actions": d.get("next_actions"), "l42_would_block": d.get("would_block")})
pool = pool[:88]
un = [d for d in l42 if (d["session"], d["ts"]) not in caught and len(d["tail"]) > 300]; random.shuffle(un)
for d in un[:88]:
    pool.append({"id": hashlib.sha1(f"{d['session']}{d['ts']}".encode()).hexdigest()[:10], "source": "l42-telemetry", "regex_caught": False, "regex_kinds": [],
                 "ts": d["ts"], "session": d["session"], "tail": d["tail"], "has_tool_use": d.get("has_tool_use"), "gates_pass": d.get("gates_pass"), "next_actions": d.get("next_actions"), "l42_would_block": d.get("would_block")})
# human-labeled anchor fixtures
FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "hooks", "tests", "fixtures", "layer42") if os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "hooks")) else os.path.expanduser("~/Workspaces/Core/frameworks/intent/hooks/tests/fixtures/layer42")
for f in sorted(glob.glob(FX + "/*.txt")):
    head, _, body = open(f).read().partition("\n---\n")
    lab = re.search(r"classification:\s*(TRUE POSITIVE|FALSE POSITIVE|AMBIGUOUS|SWING)", head, re.I)
    name = os.path.basename(f); hl = "tp" if "-tp-" in name else "fp" if "-fp-" in name else "ambiguous"
    pool.append({"id": "fx-" + name.split("-")[1], "source": "layer42-fixture", "regex_caught": True, "regex_kinds": ["L42-WOULDBLOCK-prepatch"], "human_label": hl,
                 "human_note": (lab.group(0) if lab else ""), "tail": body.strip()[-1600:], "fixture": name})
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pool.jsonl"), "w") as out:
    for p in pool: out.write(json.dumps(p) + "\n")
print("pool", len(pool), collections.Counter((p["source"], p["regex_caught"]) for p in pool))
