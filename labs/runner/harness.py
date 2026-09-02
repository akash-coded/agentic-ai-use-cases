"""Check harness for the L.A.B. Simulator.

Checks are plain functions decorated with @check. They receive the learner's
module and assert against it. No third-party dependencies: a lab must be
runnable with nothing but a Python 3.11+ interpreter.
"""
from __future__ import annotations

import traceback
from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable

_REGISTRY: list["Check"] = []


@dataclass
class Check:
    name: str
    description: str
    fn: Callable
    phase: str = "public"
    weight: int = 1
    teaches: str = ""          # what a failure here should teach you
    tags: list[str] = field(default_factory=list)


def check(name: str, description: str = "", *, teaches: str = "", weight: int = 1, tags=None):
    """Register a check. `name` is what the learner sees in the run output."""
    def deco(fn):
        _REGISTRY.append(Check(name=name, description=description, fn=fn,
                               weight=weight, teaches=teaches, tags=list(tags or [])))
        return fn
    return deco


def collect() -> list[Check]:
    return list(_REGISTRY)


def reset() -> None:
    _REGISTRY.clear()


# ---------------------------------------------------------------- assertions
# Deliberately small and readable: the failure message is teaching material,
# so it names the expectation rather than dumping a diff.

class CheckFailure(AssertionError):
    pass


def expect(condition, message: str = ""):
    if not condition:
        raise CheckFailure(message or "the expectation this check makes did not hold")


def expect_eq(actual, expected, message: str = ""):
    if actual != expected:
        raise CheckFailure(f"{message or 'values differ'}\n   expected: {expected!r}\n   actual:   {actual!r}")


def expect_in(needle, haystack, message: str = ""):
    if needle not in haystack:
        raise CheckFailure(f"{message or 'missing'}\n   looked for: {needle!r}\n   inside:     {_trim(haystack)}")


def expect_not_in(needle, haystack, message: str = ""):
    if needle in haystack:
        raise CheckFailure(f"{message or 'should not be present'}\n   found: {needle!r}\n   inside: {_trim(haystack)}")


def expect_raises(exc_type, fn, message: str = ""):
    try:
        fn()
    except exc_type:
        return
    except Exception as e:  # noqa: BLE001
        raise CheckFailure(f"{message or 'wrong exception'}\n   expected {exc_type.__name__}, got {type(e).__name__}: {e}")
    raise CheckFailure(message or f"expected {exc_type.__name__}, but nothing was raised")


def _trim(obj, limit: int = 400) -> str:
    s = repr(obj)
    return s if len(s) <= limit else s[:limit] + " …"


def run_one(chk: Check, target) -> tuple[bool, str]:
    try:
        chk.fn(target)
        return True, ""
    except CheckFailure as e:
        return False, str(e)
    except NotImplementedError as e:
        return False, f"not implemented yet — {e}"
    except BaseException as e:  # noqa: BLE001
        return False, _learner_traceback(e)


def _learner_traceback(exc: BaseException) -> str:
    """Show only the frames from the learner's own file.

    A stack that starts in the harness and ends in a check teaches nothing; the
    learner needs the line in their solution and the exception it raised.
    """
    frames = traceback.extract_tb(exc.__traceback__)
    mine = [f for f in frames
            if "/runner/" not in (f.filename or "")
            and "checks_" not in (f.filename or "")]
    head = f"{type(exc).__name__}: {exc}"
    if not mine:
        return f"error while running your code — {head}"
    lines = [f"error in your code — {head}", ""]
    for f in mine[-3:]:
        where = f.filename.split("/workspace/")[-1] if "/workspace/" in f.filename else Path(f.filename).name
        lines.append(f"   {where}:{f.lineno}  in {f.name}()")
        if f.line:
            lines.append(f"      {f.line.strip()}")
    return "\n".join(lines)
