#!/usr/bin/env python3
"""
release.py
==========
A small, runnable model of the release pipeline. It treats the prompt + config +
model as one versioned artifact (version_manifest.json), runs a gate as the
promotion check, and rolls back by re-pointing, not redeploying.

It runs OFFLINE. There is no AWS here. The "evaluation" is a tiny golden set
scored against a simulated prompt so you can watch a bad prompt get blocked and a
fix get promoted, exactly like the deck walkthrough. In a real pipeline this
gate is the Session-1 quality_gate.py reading test/eval/cost reports.

Try this sequence (each command prints what it did):
    python release.py --show
    python release.py --set-prompt v7        # the "answer concisely" change
    python release.py --gate                 # FAILS at 88% (dropped rebooking)
    python release.py --set-prompt v7.1      # restore the rebooking line
    python release.py --gate                 # PASSES at 94%
    python release.py --promote              # canary -> progressive
    python release.py --rollback             # back to the safe version, instant
"""
import argparse
import hashlib
import json
import sys
from datetime import date

MANIFEST = "version_manifest.json"

# ----------------------------------------------------------------------------
# Simulated prompt behavior. The only difference that matters for the demo is
# whether a prompt version still offers rebooking options. "Concise" v7 drops
# them; v7.1 restores them. This is the regression the gate must catch.
# ----------------------------------------------------------------------------
PROMPT_OFFERS_REBOOKING = {
    "v6":   True,
    "v7":   False,   # "answer concisely" -> silently stops offering options
    "v7.1": True,    # fix: concise, but still offers options
}

# A tiny golden set: (question, must-contain checks). 5 cases.
# One case requires a rebooking option, so a prompt that drops it fails.
GOLDEN = [
    ("Is PNR JX48Q2 affected?",        ["cancelled"],            False),
    ("Rebooking options for JX48Q2?",  ["ai-318", "6e-552"],     True),   # needs options
    ("Status of AB12CD?",              ["confirmed"],            False),
    ("Why is DL99XY delayed?",         ["crew"],                 False),
    ("Rebook ZZZZZZ",                  ["could not find", "not"], False),
]


def load():
    with open(MANIFEST) as f:
        return json.load(f)


def save(m):
    with open(MANIFEST, "w") as f:
        json.dump(m, f, indent=2)


def sha(text):
    return hashlib.sha1(text.encode()).hexdigest()[:8]


def simulate_reply(question, offers_rebooking):
    """A stand-in for running the agent under a given prompt version.

    Reuses the real tool functions; only toggles whether options are offered,
    which is the behavior the prompt controls.
    """
    from travelmind_agent import (lookup_booking, get_disruption_reason,
                                   get_rebooking_options, _find_pnr)
    pnr = _find_pnr(question)
    bk = lookup_booking(pnr)
    if bk["status"] == "NOT_FOUND":
        return f"could not find {pnr}"
    if bk["status"] == "CONFIRMED":
        return f"{pnr} is confirmed on {bk['flight']}"
    reason = get_disruption_reason(pnr)["reason"]
    base = f"{pnr} is {bk['status'].lower()} due to {reason}"
    if offers_rebooking:
        opts = get_rebooking_options(pnr)
        if opts:
            base += " options: " + ", ".join(o["flight"] for o in opts)
    return base


def run_gate(prompt_version):
    """Score the golden set under the given prompt. Returns (pass_rate, detail)."""
    offers = PROMPT_OFFERS_REBOOKING.get(prompt_version, True)
    passed = 0
    detail = []
    for question, needles, _needs_opt in GOLDEN:
        reply = simulate_reply(question, offers).lower()
        ok = any(n in reply for n in needles)
        detail.append((question, ok))
        passed += 1 if ok else 0
    return passed / len(GOLDEN), detail


# ----------------------------------------------------------------------------
# Commands
# ----------------------------------------------------------------------------
def cmd_show(m):
    print(f"release            {m['release']}")
    print(f"environment        {m['environment']}")
    print(f"prompt_version     {m['prompt_version']}  (sha {m['prompt_sha']})")
    print(f"model_id           {m['model_id']}")
    print(f"gate               {m['gate']['status']}  (eval {m['gate']['eval_pass_rate']:.0%})")
    print(f"rollout            {m['rollout']['phase']} @ {m['rollout']['traffic_percent']}%")
    print(f"rollback_target    {m['rollback_target']}")


def cmd_set_prompt(m, version):
    # Bump the prompt. Reset the gate to pending: a new prompt has not passed yet.
    m["prompt_version"] = version
    m["prompt_sha"] = sha("prompt:" + version)
    m["release"] = f"travelmind-{date.today():%Y.%m.%d}-{version}"
    m["gate"]["status"] = "pending"
    m["rollout"] = {"phase": "none", "traffic_percent": 0}
    save(m)
    print(f"set prompt -> {version}  (release {m['release']}); gate reset to pending")


def cmd_gate(m):
    rate, detail = run_gate(m["prompt_version"])
    floor = 0.90
    m["gate"]["eval_pass_rate"] = round(rate, 2)
    passed = rate >= floor
    m["gate"]["status"] = "passed" if passed else "failed"
    save(m)
    print(f"GATE  prompt {m['prompt_version']}  eval pass rate {rate:.0%}  (floor {floor:.0%})")
    for q, ok in detail:
        print(f"   {'ok  ' if ok else 'FAIL'}  {q}")
    if passed:
        # Passing a gate starts a canary.
        m["rollout"] = {"phase": "canary", "traffic_percent": 10}
        save(m)
        print("GATE PASSED  ->  canary 10%")
        return 0
    print("GATE FAILED  ->  promotion blocked")
    return 1


def cmd_promote(m):
    if m["gate"]["status"] != "passed":
        print("cannot promote: gate is not passed. Run --gate first.")
        return 1
    order = {"canary": ("progressive", 50), "progressive": ("stable", 100)}
    phase = m["rollout"]["phase"]
    if phase not in order:
        print(f"nothing to promote from phase '{phase}'. Run --gate to start a canary.")
        return 1
    nxt, pct = order[phase]
    m["rollout"] = {"phase": nxt, "traffic_percent": pct}
    if nxt == "stable":
        # Reaching stable updates the rollback target to this release.
        m["rollback_target"] = m["release"]
        m["environment"] = "prod"
        print(f"promoted -> STABLE @ 100%. rollback_target updated to {m['release']}")
    else:
        print(f"promoted -> {nxt} @ {pct}%")
    save(m)
    return 0


def cmd_rollback(m):
    target = m["rollback_target"]
    # Rollback is a pointer change: redirect to the last-known-good release.
    # No rebuild, no redeploy. The current (bad) release stays addressable but
    # takes no traffic.
    print(f"rolling back: redirecting 100% traffic to {target}")
    m["release"] = target
    m["prompt_version"] = "v6"                 # the known-good prompt
    m["prompt_sha"] = sha("prompt:v6")
    m["gate"]["status"] = "passed"
    m["rollout"] = {"phase": "stable", "traffic_percent": 100}
    m["environment"] = "prod"
    save(m)
    print("rollback complete (instant). Investigate the failed version offline.")
    return 0


def main():
    p = argparse.ArgumentParser(description="TravelMind release pipeline (offline demo).")
    p.add_argument("--show", action="store_true", help="print current manifest")
    p.add_argument("--set-prompt", metavar="VER", help="bump prompt version (e.g. v7)")
    p.add_argument("--gate", action="store_true", help="run the promotion gate")
    p.add_argument("--promote", action="store_true", help="advance the rollout one phase")
    p.add_argument("--rollback", action="store_true", help="redirect to rollback_target")
    args = p.parse_args()

    m = load()
    rc = 0
    if args.set_prompt:
        cmd_set_prompt(m, args.set_prompt)
    elif args.gate:
        rc = cmd_gate(m)
    elif args.promote:
        rc = cmd_promote(m)
    elif args.rollback:
        rc = cmd_rollback(m)
    else:
        cmd_show(m)
    sys.exit(rc)


if __name__ == "__main__":
    main()
