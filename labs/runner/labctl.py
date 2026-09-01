#!/usr/bin/env python3
"""labctl — the L.A.B. Simulator command line.

    python labs/runner/labctl.py list
    python labs/runner/labctl.py show  RET-04
    python labs/runner/labctl.py start RET-04
    python labs/runner/labctl.py run   RET-04     # public checks
    python labs/runner/labctl.py break RET-04     # the Break phase
    python labs/runner/labctl.py submit RET-04    # public + hidden, records the attempt
    python labs/runner/labctl.py next
    python labs/runner/labctl.py progress
    python labs/runner/labctl.py verify           # maintainers: validate every lab

No third-party dependencies. Python 3.11+.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import sys
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
LABS = HERE.parent
CATALOG = LABS / "catalog"
WORKSPACE = LABS / "workspace"
PROGRESS = LABS / ".progress.json"

sys.path.insert(0, str(HERE))
import harness  # noqa: E402

DIFF_ORDER = {"easy": 0, "medium": 1, "hard": 2}
PHASES = ("public", "hidden", "break")

C = {
    "reset": "\033[0m", "dim": "\033[2m", "b": "\033[1m",
    "green": "\033[32m", "red": "\033[31m", "yellow": "\033[33m",
    "blue": "\033[34m", "cyan": "\033[36m", "grey": "\033[90m",
}
if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    C = {k: "" for k in C}


def c(s, colour):
    return f"{C[colour]}{s}{C['reset']}"


# ------------------------------------------------------------------ loading
@dataclass
class Lab:
    id: str
    path: Path
    meta: dict

    def __getattr__(self, item):
        try:
            return self.meta[item]
        except KeyError as e:
            raise AttributeError(item) from e

    @property
    def title(self): return self.meta["title"]
    @property
    def track(self): return self.meta["track"]
    @property
    def difficulty(self): return self.meta["difficulty"]
    @property
    def est(self): return self.meta.get("est_minutes", 0)
    @property
    def prereqs(self): return self.meta.get("prerequisites", [])

    def file(self, name): return self.path / name

    def workspace_solution(self) -> Path:
        return WORKSPACE / self.id / "solution.py"


def load_labs() -> dict[str, Lab]:
    labs: dict[str, Lab] = {}
    if not CATALOG.exists():
        return labs
    for toml in sorted(CATALOG.rglob("lab.toml")):
        meta = tomllib.loads(toml.read_text(encoding="utf-8"))
        lab = Lab(id=meta["id"], path=toml.parent, meta=meta)
        labs[lab.id] = lab
    return labs


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _purge_foreign_lab_modules(keep: Path) -> None:
    """Drop cached modules that came from a different lab.

    Labs each keep a local `_fixtures.py`. Without this, the first lab to import
    one wins for the whole process and every later lab silently gets the wrong
    fixtures — which fails as a confusing ImportError, or worse, does not fail.
    """
    for name, mod in list(sys.modules.items()):
        f = getattr(mod, "__file__", None)
        if not f:
            continue
        try:
            path = Path(f).resolve()
        except (OSError, ValueError):
            continue
        if CATALOG in path.parents and keep not in path.parents and path.parent != keep:
            del sys.modules[name]


def load_checks(lab: Lab, phase: str):
    fname = {"public": "checks_public.py", "hidden": "checks_hidden.py", "break": "checks_break.py"}[phase]
    p = lab.file(fname)
    if not p.exists():
        return []
    harness.reset()
    _purge_foreign_lab_modules(lab.path)
    sys.path.insert(0, str(lab.path))
    try:
        load_module(p, f"checks_{lab.id.replace('-', '_')}_{phase}")
        return harness.collect()
    finally:
        sys.path.pop(0)


# ----------------------------------------------------------------- progress
def read_progress() -> dict:
    if PROGRESS.exists():
        try:
            return json.loads(PROGRESS.read_text())
        except json.JSONDecodeError:
            pass
    return {"labs": {}}


def write_progress(p: dict) -> None:
    PROGRESS.write_text(json.dumps(p, indent=2, sort_keys=True))


def record(lab_id: str, **fields) -> None:
    p = read_progress()
    entry = p["labs"].setdefault(lab_id, {"status": "started", "attempts": 0})
    entry.update(fields)
    entry["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    write_progress(p)


def status_of(lab_id: str) -> str:
    return read_progress()["labs"].get(lab_id, {}).get("status", "not started")


# ------------------------------------------------------------------ running
def resolve_target(lab: Lab, use_reference: bool) -> tuple[object | None, str]:
    _purge_foreign_lab_modules(lab.path)
    src = lab.file("reference.py") if use_reference else lab.workspace_solution()
    if not src.exists():
        if use_reference:
            return None, f"lab {lab.id} has no reference.py"
        return None, (f"no solution yet — run:\n    python labs/runner/labctl.py start {lab.id}")
    sys.path.insert(0, str(lab.path))
    try:
        return load_module(src, f"sol_{lab.id.replace('-', '_')}"), ""
    except Exception:  # noqa: BLE001
        import traceback
        return None, "your file did not import:\n" + traceback.format_exc(limit=3)
    finally:
        sys.path.pop(0)


def run_phase(lab: Lab, phase: str, *, use_reference=False, quiet=False):
    checks = load_checks(lab, phase)
    if not checks:
        return True, 0, 0
    target, err = resolve_target(lab, use_reference)
    if target is None:
        if not quiet:
            print(c("\n  " + err, "red"))
        return False, 0, len(checks)

    passed = 0
    if not quiet:
        label = {"public": "PUBLIC CHECKS", "hidden": "HIDDEN CHECKS", "break": "BREAK PHASE"}[phase]
        print(f"\n{c(label, 'b')}  {c('· ' + lab.id, 'grey')}\n")
    for chk in checks:
        ok, msg = harness.run_one(chk, target)
        passed += ok
        if quiet:
            continue
        mark = c("PASS", "green") if ok else c("FAIL", "red")
        print(f"  {mark}  {chk.name}")
        if chk.description:
            print(f"        {c(chk.description, 'grey')}")
        if not ok:
            for line in msg.rstrip().splitlines():
                print(f"        {c(line, 'yellow')}")
            if chk.teaches:
                print(f"        {c('why this matters: ' + chk.teaches, 'cyan')}")
        if not ok or chk.description:
            print()
    return passed == len(checks), passed, len(checks)


# ----------------------------------------------------------------- commands
def cmd_list(args):
    labs = load_labs()
    rows = sorted(labs.values(), key=lambda l: (l.track, DIFF_ORDER.get(l.difficulty, 9), l.id))
    if args.track:
        rows = [l for l in rows if l.track == args.track]
    if args.difficulty:
        rows = [l for l in rows if l.difficulty == args.difficulty]
    prog = read_progress()["labs"]
    if args.status:
        rows = [l for l in rows if prog.get(l.id, {}).get("status", "not started") == args.status]

    if not rows:
        print("No labs match those filters."); return
    solved = sum(1 for l in labs.values() if prog.get(l.id, {}).get("status") == "solved")
    started = sum(1 for l in labs.values() if prog.get(l.id, {}).get("status") == "started")
    print(f"\n{c('L.A.B. SIMULATOR', 'b')}   {c(f'{solved} solved · {started} started · {len(labs)-solved-started} not started', 'grey')}\n")
    print(f"  {'':2} {'ID':<8} {'LAB':<52} {'DIFF':<7} {'TRACK':<13} {'EST':>4}")
    print(f"  {c('─' * 92, 'grey')}")
    for l in rows:
        st = prog.get(l.id, {}).get("status", "not started")
        glyph = {"solved": c("●", "green"), "started": c("◐", "yellow")}.get(st, c("○", "grey"))
        dcol = {"easy": "green", "medium": "yellow", "hard": "red"}[l.difficulty]
        print(f"  {glyph}  {c(l.id, 'b'):<17} {l.title[:52]:<52} {c(l.difficulty, dcol):<16} {l.track:<13} {l.est:>3}m")
    print()


def cmd_show(args):
    labs = load_labs()
    lab = labs.get(args.id.upper())
    if not lab:
        print(f"Unknown lab: {args.id}"); sys.exit(1)
    readme = lab.file("README.md")
    print(readme.read_text(encoding="utf-8") if readme.exists() else "(no README)")


def cmd_start(args):
    labs = load_labs()
    lab = labs.get(args.id.upper())
    if not lab:
        print(f"Unknown lab: {args.id}"); sys.exit(1)
    missing = [p for p in lab.prereqs if status_of(p) != "solved"]
    if missing and not args.force:
        print(c(f"\n  Prerequisites not solved: {', '.join(missing)}", "yellow"))
        print(c("  These labs build on each other. Use --force to start anyway.\n", "grey"))
        sys.exit(1)
    dest = lab.workspace_solution()
    if dest.exists() and not args.force:
        print(f"Already started: {dest.relative_to(LABS.parent)}"); return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(lab.file("starter.py"), dest)
    record(lab.id, status="started")
    print(f"\n  {c('Started', 'green')} {c(lab.id, 'b')} — {lab.title}")
    print(f"  Edit  {c(str(dest.relative_to(LABS.parent)), 'cyan')}")
    print(f"  Brief python labs/runner/labctl.py show {lab.id}")
    print(f"  Run   python labs/runner/labctl.py run  {lab.id}\n")


def cmd_run(args):
    lab = _need(args.id)
    ok, p, t = run_phase(lab, "public", use_reference=args.reference)
    _tail(ok, p, t, lab, "run")


def cmd_break(args):
    lab = _need(args.id)
    ok, p, t = run_phase(lab, "break", use_reference=args.reference)
    if t == 0:
        print(f"\n  {lab.id} has no Break phase.\n"); return
    _tail(ok, p, t, lab, "break")
    if ok:
        record(lab.id, broke=True)


def cmd_submit(args):
    lab = _need(args.id)
    okp, pp, tp = run_phase(lab, "public", use_reference=args.reference)
    okh, ph, th = run_phase(lab, "hidden", use_reference=args.reference)
    total, passed = tp + th, pp + ph
    prog = read_progress()["labs"].get(lab.id, {})
    attempts = prog.get("attempts", 0) + 1
    if okp and okh:
        record(lab.id, status="solved", attempts=attempts, passed=passed, total=total)
        print(f"\n  {c('SOLVED', 'green')}  {lab.id} — {passed}/{total} checks, attempt {attempts}\n")
        nxt = lab.meta.get("pdlc", {}).get("produces")
        if nxt:
            print(f"  {c('Artefact:', 'b')} {nxt}")
            print(f"  {c('Record it in labs/workspace/' + lab.id + '/DECISION.md', 'grey')}\n")
        if lab.file("checks_break.py").exists() and not prog.get("broke"):
            print(f"  {c('Now break it:', 'yellow')} python labs/runner/labctl.py break {lab.id}\n")
    else:
        record(lab.id, status="started", attempts=attempts, passed=passed, total=total)
        print(f"\n  {c('NOT YET', 'red')}  {lab.id} — {passed}/{total} checks, attempt {attempts}\n")
        sys.exit(1)


def cmd_next(args):
    labs = load_labs()
    prog = read_progress()["labs"]
    done = {i for i, v in prog.items() if v.get("status") == "solved"}
    ready = [l for l in labs.values()
             if l.id not in done and all(p in done for p in l.prereqs)]
    if not ready:
        print("\n  Nothing unlocked — either you have solved everything, or check `progress`.\n"); return
    ready.sort(key=lambda l: (DIFF_ORDER.get(l.difficulty, 9), l.track, l.id))
    started = [l for l in ready if prog.get(l.id, {}).get("status") == "started"]
    print(f"\n{c('NEXT UP', 'b')}\n")
    if started:
        print(f"  {c('Resume:', 'yellow')}")
        for l in started[:3]:
            print(f"    {c(l.id, 'b')}  {l.title}")
        print()
    print(f"  {c('Unlocked:', 'green')}")
    for l in [l for l in ready if l not in started][:6]:
        print(f"    {c(l.id, 'b'):<17} {l.title:<50} {c(l.difficulty, 'grey')} · {l.est}m")
    print()


def cmd_progress(args):
    labs = load_labs()
    prog = read_progress()["labs"]
    by_track: dict[str, list[Lab]] = {}
    for l in labs.values():
        by_track.setdefault(l.track, []).append(l)
    print(f"\n{c('PROGRESS', 'b')}\n")
    tot_s = 0
    for track in sorted(by_track):
        ls = by_track[track]
        s = sum(1 for l in ls if prog.get(l.id, {}).get("status") == "solved")
        tot_s += s
        bar_w = 24
        filled = int(bar_w * s / len(ls)) if ls else 0
        bar = c("█" * filled, "green") + c("░" * (bar_w - filled), "grey")
        print(f"  {track:<14} {bar} {s}/{len(ls)}")
    print(f"\n  {c('total', 'b'):<14} {tot_s}/{len(labs)} labs solved\n")


def _need(lab_id: str) -> Lab:
    lab = load_labs().get(lab_id.upper())
    if not lab:
        print(f"Unknown lab: {lab_id}"); sys.exit(1)
    return lab


def _tail(ok, passed, total, lab, mode):
    if ok:
        word = "All public checks pass" if mode == "run" else "Survived the break"
        print(f"  {c(word, 'green')} — {passed}/{total}")
        if mode == "run":
            print(f"  {c('Submit to run the hidden checks:', 'grey')} python labs/runner/labctl.py submit {lab.id}\n")
        else:
            print()
    else:
        print(f"  {c(f'{passed}/{total} checks passing', 'yellow')}\n")
        sys.exit(1)


def cmd_verify(args):
    """Maintainer gate: every lab must be internally consistent."""
    labs = load_labs()
    if not labs:
        print("No labs found."); sys.exit(1)
    required_meta = ["id", "title", "track", "difficulty", "est_minutes"]
    required_files = ["README.md", "starter.py", "reference.py", "checks_public.py", "checks_hidden.py", "SOLUTION.md"]
    problems: list[str] = []
    ids = set(labs)

    for lab in sorted(labs.values(), key=lambda l: l.id):
        p = lab.id
        for k in required_meta:
            if k not in lab.meta:
                problems.append(f"{p}: lab.toml missing '{k}'")
        if lab.meta.get("difficulty") not in DIFF_ORDER:
            problems.append(f"{p}: difficulty must be easy|medium|hard")
        for f in required_files:
            if not lab.file(f).exists():
                problems.append(f"{p}: missing {f}")
        for pre in lab.prereqs:
            if pre not in ids:
                problems.append(f"{p}: prerequisite {pre} does not exist")
        if lab.id in lab.prereqs:
            problems.append(f"{p}: depends on itself")

        # the reference solution must pass everything
        for phase in PHASES:
            if not lab.file({"public": "checks_public.py", "hidden": "checks_hidden.py",
                             "break": "checks_break.py"}[phase]).exists():
                continue
            ok, passed, total = run_phase(lab, phase, use_reference=True, quiet=True)
            if not ok:
                problems.append(f"{p}: reference.py fails {phase} checks ({passed}/{total})")

        # the starter must NOT pass — otherwise the lab teaches nothing
        stub = lab.workspace_solution()
        tmp = lab.path / "_starter_probe.py"
        try:
            shutil.copy2(lab.file("starter.py"), tmp)
            saved, lab.meta["_probe"] = None, True
            mod, err = None, ""
            try:
                mod = load_module(tmp, f"probe_{lab.id.replace('-', '_')}")
            except Exception:  # noqa: BLE001
                mod = None
            if mod is not None:
                harness.reset()
                sys.path.insert(0, str(lab.path))
                try:
                    load_module(lab.file("checks_public.py"), f"probe_checks_{lab.id.replace('-','_')}")
                    checks = harness.collect()
                finally:
                    sys.path.pop(0)
                if checks and all(harness.run_one(ck, mod)[0] for ck in checks):
                    problems.append(f"{p}: starter.py already passes every public check — the TODOs are not real")
        finally:
            tmp.unlink(missing_ok=True)

    # cycle detection over the prerequisite DAG
    colour: dict[str, int] = {}

    def visit(n, stack):
        if colour.get(n) == 1:
            problems.append(f"prerequisite cycle: {' -> '.join(stack + [n])}"); return
        if colour.get(n) == 2:
            return
        colour[n] = 1
        for m in labs[n].prereqs:
            if m in labs:
                visit(m, stack + [n])
        colour[n] = 2

    for n in labs:
        visit(n, [])

    print(f"\n{c('VERIFY', 'b')}  {len(labs)} labs\n")
    if problems:
        for p in problems:
            print(f"  {c('FAIL', 'red')}  {p}")
        print(f"\n  {len(problems)} problem(s)\n")
        sys.exit(1)
    print(f"  {c('OK', 'green')}  schema valid · references pass · starters fail · DAG acyclic\n")


INDEX_START = "<!-- LABS:START -->"
INDEX_END = "<!-- LABS:END -->"

TRACK_META = {
    "product":     ("\U0001F4CB", "Product & PDLC", "Decide what to build before building it"),
    "agent-loop":  ("\U0001F501", "Agent Loop", "The loop, by hand, until nothing is magic"),
    "tools":       ("\U0001F527", "Tools", "Schemas, contracts and honest failure"),
    "memory":      ("\U0001F9E0", "Memory", "What the agent keeps, and what it drops"),
    "retrieval":   ("\U0001F4DA", "Retrieval", "Grounding you can actually verify"),
    "multi-agent": ("\U0001F578\uFE0F", "Multi-Agent", "Topologies, and what they cost"),
    "evaluation":  ("\U0001F52C", "Evaluation", "Proving it works, and blocking it when it does not"),
    "production":  ("\U0001F680", "Production", "Deployed, observable, reversible"),
}
TRACK_ORDER = ["product", "agent-loop", "tools", "memory", "retrieval",
               "multi-agent", "evaluation", "production"]


def build_index() -> str:
    labs = load_labs()
    by_track: dict[str, list[Lab]] = {}
    for l in labs.values():
        by_track.setdefault(l.track, []).append(l)

    total_min = sum(l.est for l in labs.values())
    out = [INDEX_START, ""]
    out.append(f"**{len(labs)} labs built** \u00b7 {total_min // 60}h {total_min % 60}m of hands-on work "
               f"\u00b7 every one runs offline, with no AWS account.\n")

    for track in TRACK_ORDER + [t for t in sorted(by_track) if t not in TRACK_ORDER]:
        ls = sorted(by_track.get(track, []), key=lambda l: (DIFF_ORDER.get(l.difficulty, 9), l.id))
        if not ls:
            continue
        emoji, name, tagline = TRACK_META.get(track, ("\u2022", track.title(), ""))
        out.append(f"### {emoji} {name}")
        out.append(f"<sub>{tagline}</sub>\n")
        out.append("| Lab | Difficulty | Time | Teaches | Break phase |")
        out.append("| --- | --- | --- | --- | --- |")
        for l in ls:
            rel = l.path.relative_to(LABS)
            badge = {"easy": "`easy`", "medium": "`medium`", "hard": "`hard`"}[l.difficulty]
            concepts = ", ".join(l.meta.get("concepts", [])[:3])
            brk = "\u2713" if l.file("checks_break.py").exists() else "\u2014"
            out.append(f"| **[{l.id}]({rel}/)** \u00b7 {l.title} | {badge} | {l.est}m | {concepts} | {brk} |")
        out.append("")
    out.append(INDEX_END)
    return "\n".join(out)


def cmd_index(args):
    md = build_index()
    readme = LABS / "README.md"
    if not readme.exists():
        print("labs/README.md not found"); sys.exit(1)
    text = readme.read_text(encoding="utf-8")
    if INDEX_START not in text or INDEX_END not in text:
        print("labs/README.md has no <!-- LABS:START --> / <!-- LABS:END --> markers"); sys.exit(1)
    head, rest = text.split(INDEX_START, 1)
    _, tail = rest.split(INDEX_END, 1)
    updated = head + md + tail
    if args.check:
        if updated != text:
            print(c("labs/README.md index is stale — run: python labs/runner/labctl.py index --write", "red"))
            sys.exit(1)
        print(c("index is up to date", "green")); return
    if args.write:
        readme.write_text(updated, encoding="utf-8")
        print(f"wrote index into labs/README.md ({len(load_labs())} labs)")
    else:
        print(md)


def main():
    ap = argparse.ArgumentParser(prog="labctl", description="L.A.B. Simulator")
    sub = ap.add_subparsers(dest="cmd", required=True)

    l = sub.add_parser("list", help="list labs")
    l.add_argument("--track"); l.add_argument("--difficulty"); l.add_argument("--status")
    l.set_defaults(func=cmd_list)

    for name, fn, helptext in [("show", cmd_show, "print the brief"),
                               ("run", cmd_run, "public checks"),
                               ("break", cmd_break, "the Break phase"),
                               ("submit", cmd_submit, "public + hidden checks")]:
        s = sub.add_parser(name, help=helptext)
        s.add_argument("id")
        s.add_argument("--reference", action="store_true", help="grade the reference solution instead of yours")
        s.set_defaults(func=fn)

    s = sub.add_parser("start", help="copy the starter into your workspace")
    s.add_argument("id"); s.add_argument("--force", action="store_true"); s.set_defaults(func=cmd_start)

    sub.add_parser("next", help="what to do next").set_defaults(func=cmd_next)
    sub.add_parser("progress", help="your progress").set_defaults(func=cmd_progress)
    sub.add_parser("verify", help="maintainers: validate every lab").set_defaults(func=cmd_verify)

    i = sub.add_parser("index", help="maintainers: regenerate the catalog table in labs/README.md")
    i.add_argument("--write", action="store_true"); i.add_argument("--check", action="store_true")
    i.set_defaults(func=cmd_index)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
