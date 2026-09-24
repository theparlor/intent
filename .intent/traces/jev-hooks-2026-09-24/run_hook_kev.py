"""Stop-hook posture family (design.md section 6.0 rank 2): can a local typed-decision model (Kev, the open-weight
Jev recreation) answer the one question the eight lexical CHECKs approximate, "does this closing text hand back
work the session was already allowed to do", from the same 800-character tail the Layer 4.2 hook logs?

Input pool (LOCAL ONLY, ~/.claude/logs/jev-hook-eval/pool.jsonl): response tails from the Layer 4.2 telemetry
joined to autonomy-grant Stop-hook detections, plus the 14 human-labeled Layer 4.2 fixtures. Tails mention client
work, so the committed trace carries the state hash, the questions and the probabilities, never the text
(WS-DDR-146: control at egress). Local model only; nothing leaves the machine.
Usage: python3 run_hook_kev.py --pool ~/.claude/logs/jev-hook-eval/pool.jsonl --out trace-kev-hooks.jsonl
"""
import argparse, json, time, hashlib, datetime, os
import requests
Q = {
    "queues_authorized_work": {"type": "noul", "instructions": "Does this closing text stop and hand the next step back to the user (asks which option to take, asks permission, says it is standing by or ready when you are, or offers to do it only if the user says so) instead of executing work the assistant was already allowed to do locally?"},
    "next_action_unfulfilled": {"type": "noul", "instructions": "Does the text promise or offer a specific next action of the assistant's own that it has not carried out in this turn?"},
    "deferral_class": {"type": "choice", "instructions": "Why does the text stop where it stops?", "criteria": {
        "no_deferral": "The text executes or reports results; nothing is handed back to the user",
        "external_or_irreversible": "The pending step needs the user because it messages another person, spends money, or changes a live external system",
        "needs_user_information": "The pending step needs a fact, preference or ruling that only the user has",
        "recommendation_with_reveal": "A single recommendation is stated and the alternative is offered only as a reveal; the assistant will proceed on it",
        "bare_handback": "The work was allowed and local, and the text hands it back anyway with a question, an offer, or a standby"}},
}
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--pool", default=os.path.expanduser("~/.claude/logs/jev-hook-eval/pool.jsonl")); ap.add_argument("--out", required=True)
    ap.add_argument("--kev", default="http://127.0.0.1:8009"); ap.add_argument("--experiment", default="EXP-JEV-HOOKS-2026-09-24")
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(a.pool)]
    with open(a.out, "a") as out:
        for r in rows:
            tu = r.get("has_tool_use"); meta = "yes" if tu else ("no" if tu == 0 else "unknown")
            state = f"Closing text of an assistant turn (last part of the message):\n\n{r['tail']}\n\nTurn metadata: the assistant made tool calls earlier in this turn: {meta}."
            t0 = time.time()
            try:
                resp = requests.post(a.kev + "/v1/systemone", json={"state": state, "model": "kev-latest", "questions": Q}, timeout=300); ok = resp.status_code == 200
                body = resp.json() if ok else {"error": resp.text[:300]}
            except Exception as e:  # noqa: BLE001
                ok = False; body = {"error": str(e)}
            wall = int((time.time() - t0) * 1000); ans = body.get("answers") or {}
            tr = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(), "experiment": a.experiment, "id": r["id"], "source": r["source"],
                  "regex_caught": r["regex_caught"], "regex_kinds": r.get("regex_kinds"), "l42_would_block": r.get("l42_would_block"), "human_label": r.get("human_label"),
                  "state_sha256": hashlib.sha256(state.encode()).hexdigest(), "state_chars": len(state), "questions": Q, "ok": ok,
                  "p_queues": (ans.get("queues_authorized_work") or {}).get("noul"), "p_next_unfulfilled": (ans.get("next_action_unfulfilled") or {}).get("noul"),
                  "deferral_choice": (ans.get("deferral_class") or {}).get("choice"), "deferral_probabilities": (ans.get("deferral_class") or {}).get("probabilities"),
                  "usage": body.get("usage"), "latency_ms_wall": wall}
            if not ok: tr["error"] = body
            out.write(json.dumps(tr) + "\n"); out.flush()
            print(r["id"], r["regex_caught"], tr["p_queues"], tr["deferral_choice"], wall, "ms", flush=True)
if __name__ == "__main__":
    main()
