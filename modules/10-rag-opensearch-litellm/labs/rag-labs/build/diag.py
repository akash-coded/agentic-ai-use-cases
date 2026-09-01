"""One diagram spec -> graphviz PNG (base64, embedded) + Mermaid source (collapsed beneath).

Node kinds: proc, dec, data, start, end, ok, fail, cost, tool, note
Edges: (src, dst) or (src, dst, label)
"""
import base64
import html
import graphviz

INK, SOFT, MUTED, RULE, PANEL = "#1A1A2E", "#3F3F58", "#8A88A4", "#E4E2EE", "#F6F4FA"
PINK, MAG, ROSE = "#FF4989", "#C2007A", "#FFF1F6"
GREEN, GREEN_SOFT = "#157F5F", "#E1F1EB"
RED, RED_SOFT = "#C0392B", "#FBE3E0"
COST, COST_SOFT = "#B26A00", "#FBEBD2"
TOOL, TOOL_SOFT = "#2F5FA6", "#E1EAF5"
FONT = "Poppins"

KIND = {
    "proc":  dict(shape="box", style="rounded,filled", fillcolor="white", color=INK, fontcolor=INK, penwidth="1.4"),
    "dec":   dict(shape="diamond", style="filled", fillcolor=ROSE, color=MAG, fontcolor=MAG, penwidth="1.4"),
    "data":  dict(shape="cylinder", style="filled", fillcolor=PANEL, color=MUTED, fontcolor=SOFT, penwidth="1.2"),
    "start": dict(shape="box", style="rounded,filled", fillcolor=INK, color=INK, fontcolor="white", penwidth="1.2"),
    "end":   dict(shape="box", style="rounded,filled", fillcolor=MAG, color=MAG, fontcolor="white", penwidth="1.2"),
    "ok":    dict(shape="box", style="rounded,filled", fillcolor=GREEN_SOFT, color=GREEN, fontcolor=GREEN, penwidth="1.4"),
    "fail":  dict(shape="box", style="rounded,filled", fillcolor=RED_SOFT, color=RED, fontcolor=RED, penwidth="1.4"),
    "cost":  dict(shape="box", style="rounded,filled", fillcolor=COST_SOFT, color=COST, fontcolor=COST, penwidth="1.4"),
    "tool":  dict(shape="box", style="rounded,filled", fillcolor=TOOL_SOFT, color=TOOL, fontcolor=TOOL, penwidth="1.4"),
    "note":  dict(shape="note", style="filled", fillcolor=PANEL, color=RULE, fontcolor=SOFT, penwidth="1.0"),
}
MM_SHAPE = {"proc": ('["', '"]'), "dec": ('{"', '"}'), "data": ('[("', '")]'), "start": ('(["', '"])'), "end": ('(["', '"])'),
            "ok": ('["', '"]'), "fail": ('["', '"]'), "cost": ('["', '"]'), "tool": ('["', '"]'), "note": ('["', '"]')}
MM_CLASS = {"dec": "dec", "start": "start", "end": "endpt", "ok": "ok", "fail": "fail", "cost": "cost", "tool": "tool", "data": "data", "note": "note"}


def _png(nodes, edges, rankdir, splines="spline", nodesep="0.35", ranksep="0.45", ratio=None):
    g = graphviz.Digraph(format="png", engine="dot")
    g.attr(rankdir=rankdir, dpi="150", bgcolor="white", pad="0.15", nodesep=nodesep, ranksep=ranksep, splines=splines, fontname=FONT)
    g.attr("node", fontname=FONT, fontsize="11", margin="0.14,0.08", height="0.4")
    g.attr("edge", fontname=FONT, fontsize="9.5", color=MUTED, fontcolor=SOFT, arrowsize="0.8", penwidth="1.2")
    for n in nodes:
        nid, label, kind = (n + ("proc",))[:3]
        g.node(nid, label=label, **KIND[kind])
    for e in edges:
        if len(e) == 2:
            g.edge(e[0], e[1])
        else:
            g.edge(e[0], e[1], label=" " + e[2] + " ")
    return base64.b64encode(g.pipe()).decode("ascii")


def _mm_label(label: str) -> str:
    """Graphviz line breaks (literal \\n or a real newline) become <br/>; quotes are escaped."""
    return label.replace("\\n", "<br/>").replace(chr(10), "<br/>").replace('"', "&quot;")


def _mermaid(nodes, edges, rankdir):
    lines = [f"flowchart {'LR' if rankdir == 'LR' else 'TD'}"]
    for n in nodes:
        nid, label, kind = (n + ("proc",))[:3]
        a, b = MM_SHAPE[kind]
        lines.append(f"    {nid}{a}{_mm_label(label)}{b}")
    for e in edges:
        if len(e) == 2:
            lines.append(f"    {e[0]} --> {e[1]}")
        else:
            lines.append(f"    {e[0]} -->|{e[2]}| {e[1]}")
    for n in nodes:
        nid, _, kind = (n + ("proc",))[:3]
        if kind in MM_CLASS:
            lines.append(f"    class {nid} {MM_CLASS[kind]}")
    lines += [f"    classDef dec fill:{ROSE},stroke:{MAG},color:{MAG}",
              f"    classDef start fill:{INK},stroke:{INK},color:#fff",
              f"    classDef endpt fill:{MAG},stroke:{MAG},color:#fff",
              f"    classDef ok fill:{GREEN_SOFT},stroke:{GREEN},color:{GREEN}",
              f"    classDef fail fill:{RED_SOFT},stroke:{RED},color:{RED}",
              f"    classDef cost fill:{COST_SOFT},stroke:{COST},color:{COST}",
              f"    classDef tool fill:{TOOL_SOFT},stroke:{TOOL},color:{TOOL}",
              f"    classDef data fill:{PANEL},stroke:{MUTED},color:{SOFT}",
              f"    classDef note fill:{PANEL},stroke:{RULE},color:{SOFT}"]
    return "\n".join(lines)


def flow(nodes, edges, rankdir="LR", alt="diagram", caption=None, **kw) -> str:
    """Markdown for a diagram: embedded PNG, optional caption, Mermaid source collapsed."""
    png = _png(nodes, edges, rankdir, **kw)
    mm = _mermaid(nodes, edges, rankdir)
    cap = f"\n\n*{caption}*" if caption else ""
    return (f'<img src="data:image/png;base64,{png}" alt="{html.escape(alt)}" style="max-width:100%;">' + cap +
            f"\n\n<details><summary>Mermaid source</summary>\n\n```mermaid\n{mm}\n```\n\n</details>")


def image_md(path: str, alt: str = "diagram", caption: str = None) -> str:
    """Embed an existing PNG file (for example a diagram rendered from the slide deck)."""
    with open(path, "rb") as f:
        png = base64.b64encode(f.read()).decode("ascii")
    cap = f"\n\n*{caption}*" if caption else ""
    return f'<img src="data:image/png;base64,{png}" alt="{html.escape(alt)}" style="max-width:100%;">' + cap


if __name__ == "__main__":
    md = flow([("a", "Query", "start"), ("b", "Retrieve"), ("c", "Enough\nevidence?", "dec"), ("d", "Answer", "end")],
              [("a", "b"), ("b", "c"), ("c", "d", "yes"), ("c", "b", "no")], caption="smoke test")
    print(md[:120], "...", len(md), "chars")
