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
              labels(first:10){ nodes{ name } }
              comments(last:30){ totalCount nodes{ createdAt } } } } } }""" % (OWNER, REPO),
            **({"after": cursor} if cursor else {}))
        page = d["repository"]["discussions"]
        for n in page["nodes"]:
            recent = sum(1 for c in n["comments"]["nodes"] if _age_days(c["createdAt"]) <= 7)
            summaries.append({"number": n["number"], "title": n["title"], "url": n["url"],
                              "updated": n["updatedAt"], "created": n["createdAt"],
                              "category": n["category"]["slug"], "answerable": n["category"]["isAnswerable"],
                              "answered": n["isAnswered"], "comments": n["comments"]["totalCount"],
                              "recent": recent,
                              "guide": any(l["name"] == "type: guide" for l in n["labels"]["nodes"])})
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
                     "best": (f"{max(x.get('passed', 0) for x in a)}/{a[0].get('total', '?')}" if a else "—"),
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

# --------------------------------------------------------------- leaderboard
def leaderboard_md(agg: dict, top: int = 10) -> str:
    rows = list(agg["rows"].values()); labs = agg["labs"]
    by_l = defaultdict(list)
    for r in rows: by_l[r["learner"]].append(r)
    if not rows:
        return "No attempts recorded yet. Post `/drill <ID>` with a ```python block and you will be the first row."
    def score(rs):
        p = len([r for r in rs if r["outcome"] == "Passed"]); pr = len([r for r in rs if r["outcome"] == "Passed after retry"])
        return p * 2 + pr * 3           # a pass after a retry is worth more, on purpose
    ranked = sorted(by_l.items(), key=lambda kv: (-score(kv[1]), -sum(r["attempts"] for r in kv[1])))
    L = ["### 🏆 Leaderboard", "", "| # | Learner | Passed | After retry | In progress | Attempts |", "| --- | --- | --- | --- | --- | --- |"]
    for i, (l, rs) in enumerate(ranked[:top], 1):
        L.append(f"| {i} | @{l} | {len([r for r in rs if r['outcome']=='Passed'])} | {len([r for r in rs if r['outcome']=='Passed after retry'])} | "
                 f"{len([r for r in rs if r['outcome'] in ('Attempted','Retrying')])} | {sum(r['attempts'] for r in rs)} |")
    by_i = defaultdict(list)
    for r in rows:
        if r["attempts"]: by_i[r["item"]].append(r)
    hard = sorted(by_i.items(), key=lambda kv: (len([r for r in kv[1] if r["outcome"].startswith("Passed")]) / len(kv[1]), -len(kv[1])))[:3]
    if hard:
        L += ["", "**Hardest right now:** " + " · ".join(
            f"`{it}` ({100*len([r for r in rs if r['outcome'].startswith('Passed')])//len(rs)}% pass, {len(rs)} tried)" for it, rs in hard)]
    L += ["", "<sub>Scoring: a pass after a retry outranks a first-time pass — retrying is the behaviour being rewarded. "
          f"Full detail on the [scoreboard]({URL}/wiki/Scoreboard).</sub>"]
    return "\n".join(L)

def progress_md(agg: dict, learner: str) -> str:
    rs = sorted([r for r in agg["rows"].values() if r["learner"] == learner.lower()], key=lambda r: (r["outcome"], r["item"]))
    if not rs:
        return (f"No attempts from @{learner} yet. Start with `/drill AGL-101` — eight minutes, no setup — "
                f"or see [the sequence]({URL}/discussions/75).")
    labs = agg["labs"]
    L = [f"### 📊 @{learner}", "", "| Item | Outcome | Attempts | Best | Next |", "| --- | --- | --- | --- | --- |"]
    icon = {"Passed": "✅", "Passed after retry": "✅🔁", "Retrying": "🔁", "Attempted": "🔁", "Assigned": "📌"}
    for r in rs:
        meta = labs.get(r["item"]); nxt = (meta.meta.get("next") if meta else "") or ""
        L.append(f"| [`{r['item']}`]({r['url']}) {r['title'][:40]} | {icon.get(r['outcome'],'')} {r['outcome']} | {r['attempts']} | {r['best']} | "
                 f"{('`/drill ' + nxt + '`') if nxt and r['outcome'].startswith('Passed') else ''} |")
    todo = [r for r in rs if r["outcome"] == "Assigned"]
    if todo: L += ["", f"**Assigned, not yet attempted:** " + ", ".join(f"`{r['item']}`" + (f" (due {r['due']})" if r["due"] else "") for r in todo)]
    return "\n".join(L)

def digest_md(agg: dict, summaries: list[dict]) -> str:
    rows = list(agg["rows"].values()); ents = [e for e in agg["entries"] if e.get("type") == "attempt"]
    week = [e for e in ents if _age_days(e.get("ts", "2000-01-01T00:00:00+00:00")) <= 7]
    learners = {e.get("learner") for e in week}; passes = [e for e in week if e.get("ok")]
    L = [f"Seven days to {NOW.strftime('%d %b %Y')}. Rebuilt from the repository's own activity; nothing here was written by hand.", ""]
    # --- Arena
    L += ["## 🧪 Arena", ""]
    if week:
        by_item = defaultdict(list)
        for e in week: by_item[e["item"]].append(e)
        hardest = sorted(by_item.items(), key=lambda kv: (sum(1 for e in kv[1] if e.get("ok")) / len(kv[1]), -len(kv[1])))[0]
        busiest = max(by_item.items(), key=lambda kv: len(kv[1]))
        pl = lambda n, w: f"{n} {w}" + ("" if n == 1 else "s")
        L += [f"**{pl(len(week), 'attempt')}** by **{pl(len(learners), 'learner')}**, **{len(passes)} passed**. "
              f"Most attempted: `{busiest[0]}` ({len(busiest[1])}). Hardest: `{hardest[0]}` "
              f"({100*sum(1 for e in hardest[1] if e.get('ok'))//len(hardest[1])}% pass rate)."]
        todo = [r for r in rows if r["outcome"] == "Assigned"]
        if todo: L += ["", f"**{len(todo)} assigned items not yet attempted** — see the [scoreboard]({URL}/wiki/Scoreboard#assigned-not-yet-attempted)."]
    else:
        L += ["No attempts this week. The [drill sequence]({URL}/discussions/75) takes eight minutes to start.".replace("{URL}", URL)]
    # --- questions
    open_q = [s for s in summaries if s["category"] == "q-a" and s["answerable"] and not s["answered"] and not s.get("guide")]
    L += ["", "## ❓ Questions waiting for an answer", ""]
    if open_q:
        for s in sorted(open_q, key=lambda s: s["created"])[:6]:
            L.append(f"- [{s['title']}]({s['url']}) — {int(_age_days(s['created']))}d old, {s['comments']} replies")
        L.append(""); L.append("If you know one of these, two minutes of your time saves someone an evening.")
    else:
        L.append("Every question has a marked answer. Rare, and worth saying.")
    # --- hot threads
    hot = sorted([s for s in summaries if s["recent"] >= 2 and s["category"] != "announcements"], key=lambda s: (-s["recent"], -s["comments"]))[:6]
    if hot:
        L += ["", "## 🔥 Where the conversation is", ""] + [f"- [{s['title']}]({s['url']}) — {s['recent']} new this week" for s in hot]
    # --- content
    log = subprocess.run(["git", "log", "--since=7 days ago", "--name-only", "--pretty=format:"], capture_output=True, text=True, cwd=ROOT).stdout
    areas = defaultdict(int)
    for f in filter(None, log.splitlines()):
        top = f.split("/")[0]; areas[top if top in ("modules", "labs", "cheatsheets", "docs", "wiki") else "other"] += 1
    n_commits = subprocess.run(["git", "rev-list", "--count", "--since=7 days ago", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    if areas:
        L += ["", "## 📝 What changed", "", f"{n_commits} commits. " + ", ".join(f"**{v}** files in `{k}/`" for k, v in sorted(areas.items(), key=lambda kv: -kv[1]) if k != "other") + f". [Changelog]({URL}/blob/main/CHANGELOG.md)."]
    L += ["", "---", "", f"<sub>Posted automatically every Monday · [how the Arena works]({URL}/blob/main/labs/ARENA.md) · "
          f"[Repo Pulse](https://github.com/users/{OWNER}/projects/10) · reply here if something looks wrong</sub>"]
    return "\n".join(L)


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
        unanswered = s["answerable"] and not s["answered"] and s["category"] == "q-a" and not s.get("guide") and _age_days(s["created"]) > 2
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
    ap.add_argument("--leaderboard", action="store_true", help="print the leaderboard markdown and exit")
    ap.add_argument("--progress", metavar="LOGIN", help="print one learner's progress markdown and exit")
    ap.add_argument("--digest", action="store_true", help="print the weekly digest markdown and exit")
    a = ap.parse_args()
    if a.fixture:
        entries = [json.loads(l) for l in Path(a.fixture).read_text().splitlines() if l.strip()]
        for e in entries: e.setdefault("_url", f"{URL}/discussions/{e.get('discussion','')}")
        summaries = []
    else:
        entries, summaries = read_ledger_from_discussions()
    agg = aggregate(entries)
    if a.leaderboard:
        print(leaderboard_md(agg)); return
    if a.progress:
        print(progress_md(agg, a.progress)); return
    if a.digest:
        print(digest_md(agg, summaries)); return
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
