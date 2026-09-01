"""Latency budget helpers. The illustrative budget is taken from the advanced-track deck; measured timings come from the notebook itself."""
import time
from contextlib import contextmanager

# Illustrative p95 budget for one grounded answer, in milliseconds. Not a measurement of this toolkit.
ILLUSTRATIVE_P95 = [
    ("Query embed and rewrite", 150), ("Hybrid retrieve, N=100", 90), ("Fusion and dedup", 20),
    ("Cross-encoder rerank, 50", 220), ("Pack and guardrail checks", 50), ("Generation, about 450 output tokens", 1550), ("Headroom for the tail", 420),
]


class Timer:
    """Collects wall-clock milliseconds per named stage."""

    def __init__(self):
        self.ms = {}

    @contextmanager
    def stage(self, name: str):
        t = time.perf_counter()
        try:
            yield
        finally:
            self.ms[name] = self.ms.get(name, 0.0) + (time.perf_counter() - t) * 1000.0

    def table(self):
        import pandas as pd
        return pd.DataFrame([{"stage": k, "ms": round(v, 2)} for k, v in self.ms.items()])
