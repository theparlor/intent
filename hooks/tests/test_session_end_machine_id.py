#!/usr/bin/env python3
"""Test harness for session-end.sh's machine id (the shard name) under a bare PATH.

Incident 2026-09-23 on the hub: a headless sdk-cli session ran with
PATH=/usr/bin:/bin. The hook found ioreg with `command -v`, which looks
only on PATH, and ioreg lives in /usr/sbin, so the serial rung came up
empty and 51 session.end rows landed in events.marcus-aurelius.jsonl (the
ComputerName slug) beside the serial shard events.gc0vy29jjk.jsonl. One
machine, two shards; the multi-machine verifier flagged it.

This suite runs the hook the way that session ran it, `env -i
PATH=/usr/bin:/bin`, and pins the derivation order from the hook header:
override, ioreg by absolute path, machine.json serial, ComputerName slug,
hostname. The shard must be the lowercased serial whenever any serial
source exists; the computer name is a last resort, never a competitor.

Test seams (hook env): INTENT_SESSION_END_IOREG and INTENT_SESSION_END_SCUTIL
point the hook at a stub or a missing path, so a machine without those
tools can be simulated on any platform, and the ComputerName rung can be
driven deterministically without touching the real scutil.

Run: python3 hooks/tests/test_session_end_machine_id.py
"""
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid

HOOK = os.environ.get(
    "SESSION_END_HOOK_PATH",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "session-end.sh"),
)
BARE_PATH = "/usr/bin:/bin"
REAL_IOREG = "/usr/sbin/ioreg"
REAL_SCUTIL = "/usr/sbin/scutil"

fails = []


def check(desc, cond, detail=""):
    ok = bool(cond)
    print(f"  {'PASS' if ok else 'FAIL'}  {desc}")
    if not ok:
        fails.append(f"{desc} {detail}".strip())


def slugify(value):
    """Mirror of the hook's slugify(): lowercase, non [a-z0-9] to '-', collapse, strip."""
    s = re.sub(r"[^a-z0-9]", "-", value.lower())
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def make_root(tmp):
    """A fresh git repo with .intent/ (the writer's find_intent_root anchor)."""
    root = tempfile.mkdtemp(prefix="root-", dir=tmp)
    os.makedirs(os.path.join(root, ".intent", "signals"))
    os.makedirs(os.path.join(root, ".intent", "events"))
    subprocess.run(["git", "init", "-q", root], check=True)
    subprocess.run(["git", "-C", root, "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", root, "config", "user.name", "Test"], check=True)
    readme = os.path.join(root, "README.md")
    with open(readme, "w") as f:
        f.write("root\n")
    subprocess.run(["git", "-C", root, "add", "README.md"], check=True)
    subprocess.run(["git", "-C", root, "commit", "-q", "-m", "init"], check=True)
    return root


def make_config_dir(tmp, machine_json=None, helper_body=None):
    """A temporary CLAUDE_CONFIG_DIR: optional machine.json, optional
    hooks/helpers/machine-role.sh stub (what the real helper exports)."""
    cfg = tempfile.mkdtemp(prefix="cfg-", dir=tmp)
    if machine_json is not None:
        with open(os.path.join(cfg, "machine.json"), "w") as f:
            json.dump(machine_json, f)
    if helper_body is not None:
        hdir = os.path.join(cfg, "hooks", "helpers")
        os.makedirs(hdir)
        with open(os.path.join(hdir, "machine-role.sh"), "w") as f:
            f.write(helper_body)
    return cfg


def make_stub(tmp, name, prints):
    """An executable stub that prints a fixed value (stands in for scutil)."""
    path = os.path.join(tmp, name)
    with open(path, "w") as f:
        f.write(f"#!/bin/sh\nprintf '%s\\n' '{prints}'\n")
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return path


def run_hook_bare(root, cfg, tmp, extra=None):
    """Run the hook exactly as the 2026-09-23 headless session did: env -i,
    PATH=/usr/bin:/bin, nothing else inherited. HOME points at the temp dir
    so nothing on the real account is read; CLAUDE_CONFIG_DIR is the temp
    config dir. `env` and `/bin/bash` both live on the bare PATH."""
    argv = ["env", "-i", f"PATH={BARE_PATH}", f"HOME={tmp}",
            f"CLAUDE_CONFIG_DIR={cfg}", f"INTENT_SESSION_END_ROOT={root}"]
    for k, v in (extra or {}).items():
        argv.append(f"{k}={v}")
    argv += ["/bin/bash", HOOK]
    return subprocess.run(argv, input=json.dumps({"session_id": str(uuid.uuid4())}),
                          capture_output=True, text=True, timeout=30)


def shards(root):
    return sorted(os.listdir(os.path.join(root, ".intent", "events")))


def last_row(root, shard):
    with open(os.path.join(root, ".intent", "events", shard)) as f:
        return json.loads(f.read().splitlines()[-1])


def real_serial():
    """The hardware serial via the absolute ioreg path, or None off macOS."""
    if not os.access(REAL_IOREG, os.X_OK):
        return None
    out = subprocess.run([REAL_IOREG, "-rd1", "-c", "IOPlatformExpertDevice"],
                         capture_output=True, text=True, timeout=10).stdout
    m = re.search(r'"IOPlatformSerialNumber"\s*=\s*"([^"]+)"', out)
    return m.group(1) if m else None


def real_computer_name():
    if not os.access(REAL_SCUTIL, os.X_OK):
        return None
    out = subprocess.run([REAL_SCUTIL, "--get", "ComputerName"],
                         capture_output=True, text=True, timeout=10).stdout.strip()
    return out or None


TMP = tempfile.mkdtemp(prefix="session-end-machine-id-test-")
ABSENT = os.path.join(TMP, "absent", "tool")  # a path that never exists

try:
    # ------------------------------------------------------------------
    # Sanity: the incident's premise still holds on this platform. Under the
    # bare PATH, `command -v ioreg` finds nothing wherever ioreg lives in
    # /usr/sbin. If a platform ever puts ioreg on /usr/bin this case is
    # simply informational; the cases below do not depend on it.
    print("Case 0: the premise. `command -v ioreg` is empty under PATH=/usr/bin:/bin")
    p0 = subprocess.run(["env", "-i", f"PATH={BARE_PATH}", "/bin/bash", "-c",
                         "command -v ioreg; command -v scutil"],
                        capture_output=True, text=True, timeout=10)
    print(f"        command -v under bare PATH printed: {p0.stdout.strip()!r} (rc={p0.returncode})")
    check("bare-PATH probe ran", p0.returncode in (0, 1), p0.stderr)

    # ------------------------------------------------------------------
    # Case 1: THE INCIDENT. Bare PATH, a temporary machine.json carrying the
    # serial, real tools where they exist. The shard must be the lowercased
    # serial and must never be the ComputerName or hostname slug. On macOS
    # the serial comes from /usr/sbin/ioreg by absolute path (rung 2); off
    # macOS it comes from machine.json (rung 3). Either way, one shard, keyed
    # by serial.
    print("Case 1: incident replay under env -i PATH=/usr/bin:/bin (serial shard, never the computer name)")
    serial = real_serial() or "TESTSERIAL0001"
    root1 = make_root(TMP)
    cfg1 = make_config_dir(TMP, machine_json={"role": "hub", "name": "Marcus Aurelius",
                                              "serial": serial.lower()})
    p1 = run_hook_bare(root1, cfg1, TMP)
    check("hook exits 0 under the bare PATH", p1.returncode == 0, p1.stderr)
    names1 = shards(root1)
    expected1 = f"events.{slugify(serial)}.jsonl"
    check("exactly one shard was written", len(names1) == 1, str(names1))
    check(f"the shard is the lowercased serial ({expected1})", names1 == [expected1], str(names1))
    cname = real_computer_name()
    if cname:
        check(f"the ComputerName slug ({slugify(cname)}) did NOT name the shard",
              f"events.{slugify(cname)}.jsonl" not in names1 or slugify(cname) == slugify(serial),
              str(names1))
    host = subprocess.run(["hostname", "-s"], capture_output=True, text=True).stdout.strip()
    if host:
        check(f"the hostname slug ({slugify(host)}) did NOT name the shard",
              f"events.{slugify(host)}.jsonl" not in names1 or slugify(host) == slugify(serial),
              str(names1))
    check("legacy events.jsonl untouched", "events.jsonl" not in names1, str(names1))
    row1 = last_row(root1, names1[0])
    check("row's source.machine.serial matches the shard key",
          row1["source"]["machine"]["serial"] == slugify(serial), str(row1["source"]["machine"]))

    # ------------------------------------------------------------------
    # Case 2: rung 3 in isolation. No ioreg and no scutil anywhere (seams
    # point at a missing path), no helper installed: the serial recorded in
    # machine.json names the shard, read directly by the hook.
    print("Case 2: no ioreg, no helper: machine.json serial names the shard (direct read)")
    root2 = make_root(TMP)
    cfg2 = make_config_dir(TMP, machine_json={"role": "travel", "name": "Faustina",
                                              "serial": "FAUSTINA0001"})
    p2 = run_hook_bare(root2, cfg2, TMP, extra={"INTENT_SESSION_END_IOREG": ABSENT,
                                                 "INTENT_SESSION_END_SCUTIL": ABSENT})
    check("hook exits 0 with both tools missing", p2.returncode == 0, p2.stderr)
    names2 = shards(root2)
    check("shard is the lowercased machine.json serial", names2 == ["events.faustina0001.jsonl"],
          str(names2))
    row2 = last_row(root2, "events.faustina0001.jsonl")
    check("row's serial is the lowercased machine.json serial",
          row2["source"]["machine"]["serial"] == "faustina0001", str(row2["source"]["machine"]))

    # ------------------------------------------------------------------
    # Case 2b: rung 3 through the helper. A stub machine-role.sh exports
    # MACHINE_SERIAL (what the real helper does from machine.json); no
    # machine.json exists in the config dir, so the helper is the only
    # possible source. Proves the helper is sourced BEFORE the id is derived.
    print("Case 2b: no ioreg: the helper's MACHINE_SERIAL names the shard")
    root2b = make_root(TMP)
    cfg2b = make_config_dir(TMP, helper_body=(
        'MACHINE_ROLE=travel\nMACHINE_SERIAL="HELPER-SERIAL-7"\nMACHINE_NAME="Faustina"\n'
        'MACHINE_ENGAGEMENT=""\nexport MACHINE_ROLE MACHINE_SERIAL MACHINE_NAME MACHINE_ENGAGEMENT\n'))
    p2b = run_hook_bare(root2b, cfg2b, TMP, extra={"INTENT_SESSION_END_IOREG": ABSENT,
                                                    "INTENT_SESSION_END_SCUTIL": ABSENT})
    check("hook exits 0 with the helper stub", p2b.returncode == 0, p2b.stderr)
    names2b = shards(root2b)
    check("shard is the helper's serial, slugged", names2b == ["events.helper-serial-7.jsonl"],
          str(names2b))
    row2b = last_row(root2b, "events.helper-serial-7.jsonl")
    check("row carries the helper's role and name",
          row2b["source"]["machine"] == {"serial": "helper-serial-7", "role": "travel",
                                         "name": "Faustina"},
          str(row2b["source"]["machine"]))

    # ------------------------------------------------------------------
    # Case 3: an inherited MACHINE_SERIAL in the environment is never trusted.
    # No helper, no machine.json, no ioreg: the hook must fall through to the
    # ComputerName rung, not adopt the inherited value.
    print("Case 3: inherited MACHINE_SERIAL is ignored; ComputerName slug is the fallback")
    root3 = make_root(TMP)
    cfg3 = make_config_dir(TMP)  # empty config dir
    scutil_stub = make_stub(TMP, "scutil-stub", "Marcus Aurelius")
    p3 = run_hook_bare(root3, cfg3, TMP, extra={"INTENT_SESSION_END_IOREG": ABSENT,
                                                 "INTENT_SESSION_END_SCUTIL": scutil_stub,
                                                 "MACHINE_SERIAL": "SPOOFED-SERIAL"})
    check("hook exits 0", p3.returncode == 0, p3.stderr)
    names3 = shards(root3)
    check("spoofed inherited serial did not name the shard",
          "events.spoofed-serial.jsonl" not in names3, str(names3))
    check("ComputerName slug names the shard only when no serial source exists",
          names3 == ["events.marcus-aurelius.jsonl"], str(names3))

    # ------------------------------------------------------------------
    # Case 4: hostname is the last rung. No serial source, no scutil.
    print("Case 4: no serial, no scutil: hostname slug, never 'unidentified'")
    root4 = make_root(TMP)
    cfg4 = make_config_dir(TMP)
    p4 = run_hook_bare(root4, cfg4, TMP, extra={"INTENT_SESSION_END_IOREG": ABSENT,
                                                 "INTENT_SESSION_END_SCUTIL": ABSENT})
    check("hook exits 0", p4.returncode == 0, p4.stderr)
    names4 = shards(root4)
    host_slug = slugify(subprocess.run(["hostname", "-s"], capture_output=True, text=True)
                        .stdout.strip() or subprocess.run(["hostname"], capture_output=True,
                                                          text=True).stdout.strip())
    check("shard is the hostname slug", names4 == [f"events.{host_slug}.jsonl"], str(names4))
    check("row was still written (capture never dropped)", len(names4) == 1, str(names4))

    # ------------------------------------------------------------------
    # Case 5: the test override beats every source, including a live ioreg.
    print("Case 5: INTENT_SESSION_END_MACHINE override wins over ioreg and machine.json")
    root5 = make_root(TMP)
    cfg5 = make_config_dir(TMP, machine_json={"role": "hub", "serial": "GC0VY29JJK"})
    p5 = run_hook_bare(root5, cfg5, TMP, extra={"INTENT_SESSION_END_MACHINE": "Override Box"})
    check("hook exits 0", p5.returncode == 0, p5.stderr)
    names5 = shards(root5)
    check("override names the shard", names5 == ["events.override-box.jsonl"], str(names5))

    # ------------------------------------------------------------------
    # Case 6: rung order between ioreg and machine.json. With a scutil stub
    # as ioreg (prints an IOPlatformSerialNumber line) the ioreg value wins
    # over a different machine.json serial: the hardware answer outranks the
    # recorded one, per the header order.
    print("Case 6: ioreg (absolute path) outranks a differing machine.json serial")
    root6 = make_root(TMP)
    cfg6 = make_config_dir(TMP, machine_json={"role": "hub", "serial": "RECORDED0001"})
    ioreg_stub = make_stub(TMP, "ioreg-stub", '  "IOPlatformSerialNumber" = "HARDWARE0001"')
    p6 = run_hook_bare(root6, cfg6, TMP, extra={"INTENT_SESSION_END_IOREG": ioreg_stub,
                                                 "INTENT_SESSION_END_SCUTIL": ABSENT})
    check("hook exits 0", p6.returncode == 0, p6.stderr)
    names6 = shards(root6)
    check("ioreg serial names the shard", names6 == ["events.hardware0001.jsonl"], str(names6))

finally:
    shutil.rmtree(TMP, ignore_errors=True)

print()
if fails:
    print(f"FAILED: {len(fails)} check(s)")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print("ALL PASS")
sys.exit(0)
