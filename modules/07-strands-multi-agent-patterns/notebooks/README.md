# Strands Graph vs Swarm Production Patterns Lab

Files:

- `strands_graph_vs_swarm_production_patterns.ipynb`: primary teaching notebook
- `strands_graph_vs_swarm_production_patterns.py`: VS Code percent-cell version
- `requirements-strands-patterns.txt`: Python dependencies
- `.env.example`: runtime configuration

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-strands-patterns.txt
cp .env.example .env
```

Open the notebook in VS Code. Keep `RUN_LIVE=false` for the deterministic controls and architecture walkthrough. Set it to `true` after AWS credentials and Bedrock model access are configured.

The lab uses the TravelMind cancelled-flight scenario to compare a deterministic Graph, a bounded read-only Swarm, and a hybrid Graph containing a Swarm. The side-effecting booking tool is isolated behind explicit approval, scope checks, hooks, and idempotency.
