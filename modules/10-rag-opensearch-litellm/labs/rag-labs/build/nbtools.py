"""Notebook assembly helpers shared by every nbNN.py builder."""
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import diag

IMG = "/home/claude/nb/build/img"


def md(text: str):
    return new_markdown_cell(text.strip("\n"))


def code(src: str):
    return new_code_cell(src.strip("\n"))


def fig(nodes, edges, rankdir="LR", alt="diagram", caption=None, **kw) -> str:
    return diag.flow(nodes, edges, rankdir=rankdir, alt=alt, caption=caption, **kw)


def deck(name: str, alt: str = None, caption: str = None) -> str:
    return diag.image_md(f"{IMG}/{name}.png", alt=alt or name, caption=caption)


SETUP = '''
# One-click setup. The notebook runs offline on numpy, pandas, matplotlib, scikit-learn and sqlite3.
# `ragkit` ships in the same folder as this notebook.
import sys, os
from pathlib import Path
for p in [Path.cwd(), *Path.cwd().parents]:
    if (p / "ragkit").is_dir():
        sys.path.insert(0, str(p)); break
import numpy as np, pandas as pd
import ragkit as rk
from ragkit import table, verdict_style, bars, lines, decision
rk.palette.style()
pd.set_option("display.width", 160)
print("ragkit", rk.__version__, "| provider:", rk.config()["provider"], "| tokenizer:", rk.TOKENIZER)
'''


def header(number: int, title: str, promise: str, spine: str, needs: str, runs_before: str, runs_after: str) -> list:
    """Standard title block: what this notebook does, how to run it, where it sits."""
    cells = [md(f"""
# {number:02d} · {title}

**FDE Academy · Accelerator track · Retrieval, RAG and Evals · Lab notebook {number} of 8**

{promise}

| How to run | What it needs | Runs before | Runs after |
|---|---|---|---|
| Run All, top to bottom. Every cell executes offline in under a minute or two. | Python 3.10 or later with numpy, pandas, matplotlib and scikit-learn. `boto3` and `tiktoken` are optional and detected automatically. | {runs_before} | {runs_after} |

{needs}
"""),
             md(f"""
## Where this sits on the pipeline

{spine}
""")]
    return cells


def recap(items: list, next_title: str, next_line: str) -> list:
    rows = "\n".join(f"| {i + 1} | {t} |" for i, t in enumerate(items))
    return [md(f"""
## What to carry out of this notebook

| # | The line worth remembering |
|---|---|
{rows}

**Next: {next_title}.** {next_line}
""")]


def write(cells: list, path: str, title: str):
    nb = new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.metadata["language_info"] = {"name": "python"}
    nb.metadata["title"] = title
    nbformat.write(nb, path)
    return path
