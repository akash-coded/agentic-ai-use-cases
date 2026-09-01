#!/usr/bin/env bash
# Runs each time you attach. Shows where you are, not a wall of text.
set -euo pipefail
cat <<'BANNER'

  ┌─────────────────────────────────────────────────────────────┐
  │  L.A.B. Simulator — ready. No setup needed.                 │
  └─────────────────────────────────────────────────────────────┘

BANNER
python3 labs/runner/labctl.py next 2>/dev/null || true
cat <<'TIPS'
  lab list                 the whole catalog
  lab start AGL-01         copy a starter into your workspace
  lab run   AGL-01         public checks
  lab break AGL-01         survive the failures that end real runs

  Notebooks under modules/ need the heavier deps:  lab deps
  AWS is optional — every lab runs offline.

TIPS
