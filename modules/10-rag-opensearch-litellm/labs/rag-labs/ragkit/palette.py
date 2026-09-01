"""FDE Academy palette for plots. Brand tokens plus a semantic category set."""
INK = "#1A1A2E"; SOFT = "#3F3F58"; MUTED = "#8A88A4"; DIM = "#A6A3BC"; RULE = "#E4E2EE"; PANEL = "#F6F4FA"
PINK = "#FF4989"; MAG = "#C2007A"; ROSE = "#FFF1F6"
GREEN = "#157F5F"; GREEN_SOFT = "#E1F1EB"   # correct, pass
RED = "#C0392B"; RED_SOFT = "#FBE3E0"       # fails
COST = "#B26A00"; COST_SOFT = "#FBEBD2"     # cost, tokens
TOOL = "#2F5FA6"; TOOL_SOFT = "#E1EAF5"     # tooling, semantic layer
SERIES = [MAG, TOOL, GREEN, COST, RED, MUTED]

def style():
    """Apply the palette to matplotlib. Safe to call repeatedly."""
    import matplotlib as mpl
    mpl.rcParams.update({
        "figure.facecolor": "white", "axes.facecolor": "white",
        "axes.edgecolor": RULE, "axes.labelcolor": SOFT, "axes.titlecolor": INK,
        "axes.titleweight": "bold", "axes.titlesize": 12, "axes.labelsize": 10,
        "xtick.color": MUTED, "ytick.color": MUTED, "grid.color": RULE, "axes.grid": True,
        "axes.spines.top": False, "axes.spines.right": False,
        "font.family": "sans-serif", "legend.frameon": False, "figure.dpi": 110,
        "axes.prop_cycle": mpl.cycler(color=SERIES),
    })
