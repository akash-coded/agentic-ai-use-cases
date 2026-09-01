"""Display helpers: tables, plots in the brand palette, and executable decision trees."""
import pandas as pd
import matplotlib.pyplot as plt
from . import palette as P


def table(df: pd.DataFrame, caption: str = None, precision: int = 3):
    """A compact styled DataFrame for notebook output."""
    pd.set_option("display.max_colwidth", 120)
    st = df.style.set_table_styles([
        {"selector": "th", "props": [("background-color", P.INK), ("color", "white"), ("font-weight", "600"), ("text-align", "left"), ("padding", "6px 8px")]},
        {"selector": "td", "props": [("padding", "5px 8px"), ("border-bottom", f"1px solid {P.RULE}"), ("text-align", "left"), ("vertical-align", "top")]},
    ]).hide(axis="index")
    try:
        st = st.format(precision=precision)
    except Exception:
        pass
    if caption:
        st = st.set_caption(caption).set_table_styles([{"selector": "caption", "props": [("caption-side", "top"), ("color", P.MAG), ("font-weight", "600"), ("text-align", "left"), ("padding", "4px 0")]}], overwrite=False)
    return st


def verdict_style(df: pd.DataFrame, col: str = "verdict"):
    """Colour a verdict column: pass green, FAIL or BLOCK red, WARN amber."""
    def colour(v):
        v = str(v)
        if v in ("pass", "ok", "ship", "yes"):
            return f"background-color: {P.GREEN_SOFT}; color: {P.GREEN}; font-weight: 600"
        if v in ("FAIL", "BLOCK", "no"):
            return f"background-color: {P.RED_SOFT}; color: {P.RED}; font-weight: 600"
        if v in ("WARN",):
            return f"background-color: {P.COST_SOFT}; color: {P.COST}; font-weight: 600"
        return ""
    return table(df).map(colour, subset=[col]) if col in df.columns else table(df)


def bars(labels, values, title: str, ylabel: str = "", color=None, highlight: int = None, fmt: str = "{:.2f}", figsize=(7, 3.2)):
    P.style()
    fig, ax = plt.subplots(figsize=figsize)
    cols = [color or P.MAG] * len(values)
    if highlight is not None:
        cols[highlight] = P.GREEN
    ax.bar(labels, values, color=cols, width=0.6)
    for i, v in enumerate(values):
        ax.text(i, v, fmt.format(v), ha="center", va="bottom", fontsize=9, color=P.SOFT)
    ax.set_title(title); ax.set_ylabel(ylabel); ax.grid(axis="x", visible=False)
    plt.tight_layout(); plt.show()


def lines(x, series: dict, title: str, xlabel: str = "", ylabel: str = "", figsize=(7, 3.4), marker="o"):
    P.style()
    fig, ax = plt.subplots(figsize=figsize)
    for name, ys in series.items():
        ax.plot(x, ys, marker=marker, label=name, linewidth=2)
    ax.set_title(title); ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.legend()
    plt.tight_layout(); plt.show()


def decision(tree: list, facts: dict, title: str = "Decision") -> pd.DataFrame:
    """Execute a decision tree against measured facts and return the path taken.

    tree: list of steps. Each step is a dict with keys
        q     : the question, as text
        test  : a callable(facts) -> bool
        yes   : outcome text if the test is true, or None to continue
        no    : outcome text if the test is false, or None to continue
    The first step whose branch carries an outcome ends the walk.
    """
    rows = []
    for step in tree:
        result = bool(step["test"](facts))
        rows.append({"question": step["q"], "measured": step.get("show", lambda f: "")(facts), "answer": "yes" if result else "no"})
        outcome = step["yes"] if result else step["no"]
        if outcome is not None:
            rows.append({"question": "Outcome", "measured": "", "answer": outcome})
            break
    return pd.DataFrame(rows)


def show_trace(store, trace_id: str, retriever=None, n: int = 8):
    """Print a saved trace in a readable form."""
    t = store.trace(trace_id)
    if t is None:
        print("no trace", trace_id); return
    print(f"trace {trace_id}\nconfig: {t['config']}\npacked ({len(t['packed'])}): {t['packed']}\ndropped: {t['dropped'][:n]}\nanswer: {t['answer']}")
