#!/usr/bin/env python3
"""Rebuild the scoreboard and the project boards from the Arena's own replies.

Source of truth: `<!-- lab-ledger {...} -->` lines the bot leaves at the end of
every grading and assignment reply in the Hands-on Labs category. This script
never writes to Discussions; it only reads them and derives:

  wiki page 'Scoreboard'    always (published by pulse.yml with GITHUB_TOKEN)
  Hands-on Tracker board    only when PROJECT_TOKEN is set (GITHUB_TOKEN cannot touch Projects v2)
  Repo Pulse board          same

Usage: sync_boards.py [--scoreboard PATH] [--boards] [--fixture FILE]
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "labs" / "runner"))
import labctl  # noqa: E402

OWNER, REPO = "akash-coded", "aws-bedrock-agentcore-strands"
URL = f"https://github.com/{OWNER}/{REPO}"
BOT = ("github-actions", "github-actions[bot]")
NOW = datetime.now(timezone.utc)

def gh(query: str, token: str | None = None, **vars) -> dict:
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in vars.items():
        cmd += ["-f", f"{k}={v}"]
    env = dict(os.environ)
    if token: env["GH_TOKEN"] = token
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if r.returncode:
        raise RuntimeError(r.stderr[:500])
    out = json.loads(r.stdout)
    if out.get("errors"):
        raise RuntimeError(json.dumps(out["errors"])[:500])
    return out["data"]

LEDGER_RE = re.compile(r"<!--\s*lab-ledger\s+(\{.*?\})\s*-->", re.S)

# ------------------------------------------------------------------ collect
def _category_id(slug: str) -> str | None:
    d = gh('{repository(owner:"%s",name:"%s"){discussionCategories(first:20){nodes{id slug}}}}' % (OWNER, REPO))
    for c in d["repository"]["discussionCategories"]["nodes"]:
        if c["slug"] == slug: return c["id"]
    return None

def read_ledger_from_discussions() -> tuple[list[dict], list[dict]]:
    """Two queries, sized under GitHub's 500k-node budget.

    Ledger: only the Hands-on Labs category, deep (comments + replies).
    Pulse:  every category, shallow (no replies) — just enough for heat.
    """
    entries, summaries = [], []
    cat = _category_id("hands-on-labs")
    cursor = None
    while cat:
        d = gh("""
        query($after:String,$cat:ID!){ repository(owner:"%s",name:"%s"){
          discussions(first:15, after:$after, categoryId:$cat, orderBy:{field:UPDATED_AT,direction:DESC}){
            pageInfo{hasNextPage endCursor}
            nodes{ number url
              comments(first:60){ nodes{ author{login}
                replies(first:30){ nodes{ author{login} body } } } } } } } }""" % (OWNER, REPO),
            **({"cat": cat} | ({"after": cursor} if cursor else {})))
        page = d["repository"]["discussions"]
        for n in page["nodes"]:
            for c in n["comments"]["nodes"]:
                for rp in c["replies"]["nodes"]:
                    if (rp["author"] or {}).get("login") in BOT:
                        for m in LEDGER_RE.finditer(rp["body"] or ""):
                            try:
                                e = json.loads(m.group(1)); e["_url"] = n["url"]; entries.append(e)
                            except json.JSONDecodeError:
                                pass
        if not page["pageInfo"]["hasNextPage"]: break
        cursor = page["pageInfo"]["endCursor"]

    cursor = None
    while True:
        d = gh("""
        query($after:String){ repository(owner:"%s",name:"%s"){
          discussions(first:50, after:$after, orderBy:{field:UPDATED_AT,direction:DESC}){
            pageInfo{hasNextPage endCursor}
            nodes{ number title url updatedAt createdAt isAnswered
              category{ slug isAnswerable }
              comments(last:30){ totalCount nodes{ createdAt } } } } } }""" % (OWNER, REPO),
            **({"after": cursor} if cursor else {}))
        page = d["repository"]["discussions"]
        for n in page["nodes"]:
            recent = sum(1 for c in n["comments"]["nodes"] if _age_days(c["createdAt"]) <= 7)
            summaries.append({"number": n["number"], "title": n["title"], "url": n["url"],
                              "updated": n["updatedAt"], "created": n["createdAt"],
                              "category": n["category"]["slug"], "answerable": n["category"]["isAnswerable"],
                              "answered": n["isAnswered"], "comments": n["comments"]["totalCount"],
                              "recent": recent})
        if not page["pageInfo"]["hasNextPage"]: break
        cursor = page["pageInfo"]["endCursor"]
    return entries, summaries

def _age_days(iso: str) -> float:
    return (NOW - datetime.fromisoformat(iso.replace("Z", "+00:00"))).total_seconds() / 86400

# ---------------------------------------------------------------- aggregate
def aggregate(entries: list[dict]) -> dict:
    labs = {**labctl.load_labs(), **labctl.load_drills()}
    att = defaultdict(list)       # (learner,item) -> attempts sorted by ts
    assign = {}                   # (learner,item) -> latest assignment
    for e in sorted(entries, key=lambda x: x.get("ts", "")):
        if e.get("type") == "attempt" and e.get("learner") and e.get("item"):
            att[(e["learner"].lower(), e["item"].upper())].append(e)
        elif e.get("type") == "assignment":
            for l in e.get("learners", []):
                for it in e.get("items", []):
                    assign[(l.lower(), it.upper())] = e
    rows = {}
    for key in set(att) | set(assign):
        a = att.get(key, []); asg = assign.get(key)
        passes = [x for x in a if x.get("ok")]
        first_pass = passes[0] if passes else None
        failed_before = any(not x.get("ok") for x in a[: a.index(first_pass)]) if first_pass else False
        if not a: outcome = "Assigned"
        elif first_pass: outcome = "Passed after retry" if failed_before else "Passed"
        elif len(a) > 1: outcome = "Retrying"
        else: outcome = "Attempted"
        meta = labs.get(key[1])
        rows[key] = {"learner": key[0], "item": key[1],
                     "title": meta.title if meta else key[1],
                     "track": meta.track if meta else (a[0].get("track") if a else ""),
                     "level": meta.difficulty if meta else (a[0].get("level") if a else ""),
                     "is_drill": bool(meta and meta.is_drill),
                     "attempts": len(a), "outcome": outcome,
                     "first": a[0]["ts"][:10] if a else "", "passed_on": first_pass["ts"][:10] if first_pass else "",
                     "last": a[-1]["ts"] if a else (asg or {}).get("ts", ""),
                     "best": f"{max((x.get('passed',0) for x in a), default=0)}/{a[0].get('total','?') if a else '?'}",
                     "session": (asg or {}).get("session", ""), "by": (asg or {}).get("by", ""),
                     "due": (asg or {}).get("due", ""), "url": (a[-1] if a else asg).get("_url", "")}
    return {"rows": rows, "labs": labs, "entries": entries}

# --------------------------------------------------------------- scoreboard
def scoreboard(agg: dict) -> str:
    rows = list(agg["rows"].values()); labs = agg["labs"]
    by_learner = defaultdict(list); by_item = defaultdict(list)
    for r in rows: by_learner[r["learner"]].append(r); by_item[r["item"]].append(r)
    attempts = sum(r["attempts"] for r in rows)
    passed = [r for r in rows if r["outcome"].startswith("Passed")]
    L = []; A = L.append
    A("# Scoreboard"); A("")
    A(f"<sub>Rebuilt {NOW.strftime('%Y-%m-%d %H:%M UTC')} from the Arena's own replies · "
      f"[how this works]({URL}/blob/main/labs/ARENA.md#tracking) · [tracker board](https://github.com/users/{OWNER}/projects/9)</sub>"); A("")
    A(f"**{len(by_learner)} learners** · **{attempts} attempts** · **{len(passed)} passes** across "
      f"**{len(by_item)} items** · pass rate **{(100*len(passed)/max(1,len([r for r in rows if r['attempts']]))):.0f}%** of attempted items")
    A("")
    todo = [r for r in rows if r["outcome"] == "Assigned"]
    if todo:
        A("## Assigned, not yet attempted"); A("")
        A("| Learner | Item | Session | Due | Assigned by |"); A("| --- | --- | --- | --- | --- |")
        for r in sorted(todo, key=lambda x: (x["due"] or "9", x["learner"])):
            A(f"| @{r['learner']} | `{r['item']}` {r['title']} | {r['session']} | {r['due']} | @{r['by']} |")
        A("")
    A("## By learner"); A("")
    A("| Learner | Items tried | Passed | Passed after retry | Still on it | Last active |"); A("| --- | --- | --- | --- | --- | --- |")
    for l, rs in sorted(by_learner.items(), key=lambda kv: -len([r for r in kv[1] if r['outcome'].startswith('Passed')])):
        tried = [r for r in rs if r["attempts"]]
        A(f"| @{l} | {len(tried)} | {len([r for r in rs if r['outcome']=='Passed'])} | "
          f"{len([r for r in rs if r['outcome']=='Passed after retry'])} | "
          f"{len([r for r in rs if r['outcome'] in ('Attempted','Retrying')])} | "
          f"{max((r['last'] for r in rs), default='')[:10]} |")
    A("")
    A("## By item"); A("")
    A("| Item | Level | Learners | Attempts | Pass rate | Avg attempts to pass |"); A("| --- | --- | --- | --- | --- | --- |")
    for it, rs in sorted(by_item.items(), key=lambda kv: kv[0]):
        tried = [r for r in rs if r["attempts"]]; ps = [r for r in tried if r["outcome"].startswith("Passed")]
        rate = f"{100*len(ps)/len(tried):.0f}%" if tried else "—"
        avg = f"{sum(r['attempts'] for r in ps)/len(ps):.1f}" if ps else "—"
        meta = labs.get(it); kind = "drill" if (meta and meta.is_drill) else "lab"
        A(f"| [`{it}`]({URL}/tree/main/{meta.path.relative_to(ROOT) if meta else 'labs'}) {meta.title if meta else ''} <sub>{kind}</sub> | "
          f"{meta.difficulty if meta else ''} | {len(rs)} | {sum(r['attempts'] for r in rs)} | {rate} | {avg} |")
    A("")
    recent = sorted([e for e in agg["entries"] if e.get("type") == "attempt"], key=lambda e: e.get("ts", ""), reverse=True)[:15]
    if recent:
        A("## Recent attempts"); A("")
        A("| When | Learner | Item | Result |"); A("| --- | --- | --- | --- |")
        for e in recent:
            A(f"| {e.get('ts','')[:16].replace('T',' ')} | @{e.get('learner')} | [`{e.get('item')}`]({e.get('_url','')}) | "
              f"{'✅' if e.get('ok') else '🔁' if e.get('outcome')=='partial' else '❌'} {e.get('passed')}/{e.get('total')} |")
        A("")
    A("---"); A("")
    A(f"To appear here: post `/drill <ID>` or `/lab <ID>` with a ```python block in any "
      f"[Hands-on Labs]({URL}/discussions/categories/hands-on-labs) thread. Maintainers assign with `/assign`.")
    return "\n".join(L) + "\n"

# ------------------------------------------------------------------- boards
def _q(s): return json.dumps(str(s))
def upsert_tracker(agg: dict, cfg: dict, token: str):
    pid, F, O = cfg["id"], cfg["fields"], cfg["options"]
    existing = {}
    d = gh('{node(id:%s){... on ProjectV2{items(first:100){nodes{id content{... on DraftIssue{title}}}}}}}' % _q(pid), token)
    for it in d["node"]["items"]["nodes"]:
        t = (it.get("content") or {}).get("title")
        if t: existing[t] = it["id"]
    n_new = 0
    for r in agg["rows"].values():
        title = f"{r['learner']} · {r['item']}"
        iid = existing.get(title)
        if not iid:
            body = f"{r['title']}\n\n{r['url']}"
            iid = gh('mutation($p:ID!,$t:String!,$b:String!){addProjectV2DraftIssue(input:{projectId:$p,title:$t,body:$b}){projectItem{id}}}',
                     token, p=pid, t=title, b=body)["addProjectV2DraftIssue"]["projectItem"]["id"]; n_new += 1
        sets = []
        def sel(field, val):
            oid = O.get(field, {}).get(val)
            if oid: sets.append(f'{{fieldId:{_q(F[field])},value:{{singleSelectOptionId:{_q(oid)}}}}}')
        def txt(field, val):
            if val: sets.append(f'{{fieldId:{_q(F[field])},value:{{text:{_q(val)}}}}}')
        def num(field, val):
            sets.append(f'{{fieldId:{_q(F[field])},value:{{number:{float(val)}}}}}')
        def dat(field, val):
            if val: sets.append(f'{{fieldId:{_q(F[field])},value:{{date:{_q(val)}}}}}')
        txt("Learner", r["learner"]); txt("Item", r["item"]); sel("Track", r["track"])
        sel("Level", {"easy":"foundational","medium":"intermediate","hard":"advanced"}.get(r["level"], r["level"]))
        sel("Outcome", r["outcome"]); num("Attempts", r["attempts"]); dat("First attempt", r["first"])
        dat("Passed on", r["passed_on"]); txt("Session", r["session"]); txt("Assigned by", r["by"]); dat("Due", r["due"]); txt("Thread", r["url"])
        muts = " ".join(f's{i}:updateProjectV2ItemFieldValue(input:{{projectId:{_q(pid)},itemId:{_q(iid)},{s[1:-1]}}}){{projectV2Item{{id}}}}' for i, s in enumerate(sets))
        gh(f"mutation{{ {muts} }}", token)
    return n_new, len(agg["rows"])

def pulse_rows(summaries: list[dict], entries: list[dict]) -> list[dict]:
    """A live view of what deserves attention — deliberately small.

    Discussions appear only when they are hot (real engagement this week) or
    are unanswered questions; a thread merely edited recently is not news.
    """
    rows = []
    hot = []
    for s in summaries:
        unanswered = s["answerable"] and not s["answered"] and s["category"] == "q-a" and _age_days(s["created"]) > 2
        if unanswered:
            rows.append({"kind": "Unanswered Q&A", "title": f"❓ #{s['number']} {s['title']}", "heat": "🔥 Hot" if s["recent"] else "Warm",
                         "engagement": s["comments"], "last": s["updated"][:10], "area": "discussions", "link": s["url"]})
        elif s["recent"] >= 2 or (s["recent"] >= 1 and s["comments"] >= 3):
            hot.append(s)
    hot.sort(key=lambda s: (-s["recent"], -s["comments"]))
    for s in hot[:12]:
        rows.append({"kind": "Discussion", "title": f"🔥 #{s['number']} {s['title']}", "heat": "🔥 Hot",
                     "engagement": s["comments"], "last": s["updated"][:10], "area": "discussions", "link": s["url"]})
    for kind, ep in (("Issue", "issues"), ("Pull request", "pulls")):
        r = subprocess.run(["gh", "api", f"repos/{OWNER}/{REPO}/{ep}?state=open&per_page=50"], capture_output=True, text=True)
        for it in (json.loads(r.stdout) if r.returncode == 0 else []):
            if ep == "issues" and "pull_request" in it: continue
            rows.append({"kind": kind, "title": f"#{it['number']} {it['title']}", "heat": "🔥 Hot" if _age_days(it["updated_at"]) < 2 else "Warm",
                         "engagement": it.get("comments", 0), "last": it["updated_at"][:10], "area": "workflows" if ep == "pulls" else "docs", "link": it["html_url"]})
    log = subprocess.run(["git", "log", "--since=7 days ago", "--name-only", "--pretty=format:"], capture_output=True, text=True, cwd=ROOT).stdout
    areas = defaultdict(int)
    for f in filter(None, log.splitlines()):
        top = f.split("/")[0]
        areas[top if top in ("modules","labs","cheatsheets","docs","wiki") else ("workflows" if f.startswith(".github") else None)] += 1
    for area, n in areas.items():
        if area: rows.append({"kind": "Content changed", "title": f"📝 {n} files changed in {area}/ this week", "heat": "🔥 Hot" if n >= 10 else "Warm",
                              "engagement": n, "last": NOW.strftime("%Y-%m-%d"), "area": area, "link": f"{URL}/commits/main/{area}"})
    week = [e for e in entries if e.get("type") == "attempt" and _age_days(e.get("ts", "2000-01-01T00:00:00+00:00")) <= 7]
    if week:
        learners = {e.get("learner") for e in week}
        rows.append({"kind": "Arena activity", "title": f"🧪 {len(week)} Arena attempts by {len(learners)} learners this week", "heat": "🔥 Hot" if len(week) >= 5 else "Warm",
                     "engagement": len(week), "last": NOW.strftime("%Y-%m-%d"), "area": "labs", "link": f"{URL}/wiki/Scoreboard"})
    return rows

def rebuild_pulse(rows: list[dict], cfg: dict, token: str):
    pid, F, O = cfg["id"], cfg["fields"], cfg["options"]
    d = gh('{node(id:%s){... on ProjectV2{items(first:100){nodes{id content{... on DraftIssue{title}}}}}}}' % _q(pid), token)
    existing = {((it.get("content") or {}).get("title")): it["id"] for it in d["node"]["items"]["nodes"]}
    want = {r["title"]: r for r in rows}
    for title, iid in existing.items():
        if title and title not in want:
            gh('mutation($p:ID!,$i:ID!){deleteProjectV2Item(input:{projectId:$p,itemId:$i}){deletedItemId}}', token, p=pid, i=iid)
    for title, r in want.items():
        iid = existing.get(title) or gh('mutation($p:ID!,$t:String!,$b:String!){addProjectV2DraftIssue(input:{projectId:$p,title:$t,body:$b}){projectItem{id}}}',
                                        token, p=pid, t=title, b=r["link"])["addProjectV2DraftIssue"]["projectItem"]["id"]
        sets = [f'{{fieldId:{_q(F["Kind"])},value:{{singleSelectOptionId:{_q(O["Kind"][r["kind"]])}}}}}',
                f'{{fieldId:{_q(F["Heat"])},value:{{singleSelectOptionId:{_q(O["Heat"][r["heat"]])}}}}}',
                f'{{fieldId:{_q(F["Engagement"])},value:{{number:{float(r["engagement"])}}}}}',
                f'{{fieldId:{_q(F["Last activity"])},value:{{date:{_q(r["last"])}}}}}',
                f'{{fieldId:{_q(F["Link"])},value:{{text:{_q(r["link"])}}}}}']
        if r["area"] in O.get("Area", {}): sets.append(f'{{fieldId:{_q(F["Area"])},value:{{singleSelectOptionId:{_q(O["Area"][r["area"]])}}}}}')
        muts = " ".join(f's{i}:updateProjectV2ItemFieldValue(input:{{projectId:{_q(pid)},itemId:{_q(iid)},{s[1:-1]}}}){{projectV2Item{{id}}}}' for i, s in enumerate(sets))
        gh(f"mutation{{ {muts} }}", token)
    return len(want), len([t for t in existing if t and t not in want])

# --------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scoreboard", default="out/Scoreboard.md")
    ap.add_argument("--boards", action="store_true")
    ap.add_argument("--fixture", help="JSONL of ledger entries, instead of reading Discussions")
    a = ap.parse_args()
    if a.fixture:
        entries = [json.loads(l) for l in Path(a.fixture).read_text().splitlines() if l.strip()]
        for e in entries: e.setdefault("_url", f"{URL}/discussions/{e.get('discussion','')}")
        summaries = []
    else:
        entries, summaries = read_ledger_from_discussions()
    agg = aggregate(entries)
    Path(a.scoreboard).parent.mkdir(parents=True, exist_ok=True)
    Path(a.scoreboard).write_text(scoreboard(agg), encoding="utf-8")
    print(f"scoreboard: {len(entries)} ledger entries → {len(agg['rows'])} learner×item rows → {a.scoreboard}")
    if a.boards:
        token = os.environ.get("PROJECT_TOKEN", "")
        if not token:
            print("boards: PROJECT_TOKEN not set — skipped (GITHUB_TOKEN cannot access Projects v2). Add the secret to enable."); return
        cfg = json.loads((ROOT / ".github" / "boards.json").read_text())
        n_new, n_all = upsert_tracker(agg, cfg["tracker"], token)
        print(f"tracker board: {n_all} rows ({n_new} new)")
        if summaries:
            n, gone = rebuild_pulse(pulse_rows(summaries, entries), cfg["pulse"], token)
            print(f"pulse board: {n} live items ({gone} stale removed)")

if __name__ == "__main__":
    main()
