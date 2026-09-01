"""Token accounting and cost. Every rate here is a parameter, never a constant to quote.

Categories on one request: uncached input, cache write, cache read, output.
The cache simulator models a prefix cache: a request hits when its stable prefix was
written within the TTL, exactly byte for byte. That is how both major providers work
(verified 2026-08-31: Anthropic 1.25x write for 5 minutes or 2x for 1 hour, 0.1x read;
OpenAI GPT-5.6 1.25x write, 0.1x read, 30-minute minimum). Dollar rates change; the
multipliers are the structure.
"""
import hashlib
from dataclasses import dataclass, field
from .context import count_tokens


@dataclass
class Rates:
    """Per-million-token rates. Defaults are the deck's illustrative figures, not a quote."""
    input: float = 3.0
    output: float = 15.0
    cache_write_mult: float = 1.25
    cache_read_mult: float = 0.10
    ttl_s: int = 300
    label: str = "illustrative: 3 in, 15 out, 5-minute cache"


PROVIDER_MULTIPLIERS = [
    # verified 2026-08-31 against provider documentation; dollar rates deliberately omitted here
    {"provider": "Anthropic, 5-minute cache", "cache_write_mult": 1.25, "cache_read_mult": 0.10, "ttl": "5 min, refreshed on hit", "note": "cache_control on blocks or automatic; up to 4 breakpoints"},
    {"provider": "Anthropic, 1-hour cache", "cache_write_mult": 2.00, "cache_read_mult": 0.10, "ttl": "1 hour", "note": "pays back after two reads instead of one"},
    {"provider": "OpenAI GPT-5.6 and later", "cache_write_mult": 1.25, "cache_read_mult": 0.10, "ttl": "30 min minimum", "note": "explicit breakpoints via prompt_cache_breakpoint; prompt_cache_key recommended"},
]


@dataclass
class Request:
    prefix: str            # the stable part: system, tools, shots, tenant config
    body: str              # the volatile part: history, evidence, question
    output_tokens: int
    t: float = 0.0         # seconds since epoch of the simulation


@dataclass
class Bill:
    uncached_input: int = 0
    cache_write: int = 0
    cache_read: int = 0
    output: int = 0
    hits: int = 0
    misses: int = 0
    lines: list = field(default_factory=list)

    def cost(self, r: Rates) -> float:
        return (self.uncached_input * r.input + self.cache_write * r.input * r.cache_write_mult +
                self.cache_read * r.input * r.cache_read_mult + self.output * r.output) / 1e6

    def table(self, r: Rates):
        import pandas as pd
        rows = [("uncached input", self.uncached_input, r.input, self.uncached_input * r.input / 1e6),
                ("cache write", self.cache_write, r.input * r.cache_write_mult, self.cache_write * r.input * r.cache_write_mult / 1e6),
                ("cache read", self.cache_read, r.input * r.cache_read_mult, self.cache_read * r.input * r.cache_read_mult / 1e6),
                ("output", self.output, r.output, self.output * r.output / 1e6)]
        df = pd.DataFrame(rows, columns=["category", "tokens", "rate per M", "dollars"])
        df["dollars"] = df["dollars"].round(5)
        return df


class CacheSimulator:
    """A prefix cache keyed on the exact prefix bytes, with a TTL refreshed on hit."""

    def __init__(self, rates: Rates):
        self.rates = rates
        self.store = {}     # prefix hash -> last-seen time

    def run(self, requests: list, caching: bool = True) -> Bill:
        bill = Bill()
        for req in requests:
            p_tok, b_tok = count_tokens(req.prefix), count_tokens(req.body)
            key = hashlib.sha1(req.prefix.encode()).hexdigest()
            hit = caching and key in self.store and (req.t - self.store[key]) <= self.rates.ttl_s
            if not caching:
                bill.uncached_input += p_tok + b_tok; bill.misses += 1; kind = "no cache"
            elif hit:
                bill.cache_read += p_tok; bill.uncached_input += b_tok; bill.hits += 1; kind = "hit"
            else:
                bill.cache_write += p_tok; bill.uncached_input += b_tok; bill.misses += 1; kind = "write"
            if caching:
                self.store[key] = req.t
            bill.output += req.output_tokens
            bill.lines.append({"t": req.t, "prefix_tokens": p_tok, "body_tokens": b_tok, "outcome": kind})
        return bill


def breakeven_reads(write_mult: float, read_mult: float) -> float:
    """Reads needed for a cached prefix to cost less than sending it uncached each time.

    Sending n times uncached costs n. Caching costs write_mult + (n - 1) * read_mult.
    Solve write_mult + (n - 1) * read_mult < n.
    """
    return (write_mult - read_mult) / (1.0 - read_mult)


def cumulative_cost_curve(prefix_tokens: int, n_max: int, rates: Rates):
    """Cost of sending the same prefix n times, cached and uncached, for the plot."""
    unc = [n * prefix_tokens * rates.input / 1e6 for n in range(1, n_max + 1)]
    cac = [(prefix_tokens * rates.input * rates.cache_write_mult + (n - 1) * prefix_tokens * rates.input * rates.cache_read_mult) / 1e6 for n in range(1, n_max + 1)]
    return list(range(1, n_max + 1)), unc, cac


def query_cost(prefix_tokens: int, evidence_tokens: int, question_tokens: int, output_tokens: int, rates: Rates, cached: bool = True,
               rerank_dollars: float = 0.0, embed_dollars: float = 0.0) -> dict:
    """Line items for one answered query, prefix served from cache or not."""
    prefix_cost = prefix_tokens * rates.input * (rates.cache_read_mult if cached else 1.0) / 1e6
    ev = evidence_tokens * rates.input / 1e6; qn = question_tokens * rates.input / 1e6; out = output_tokens * rates.output / 1e6
    total = prefix_cost + ev + qn + out + rerank_dollars + embed_dollars
    return {"prefix": prefix_cost, "evidence": ev, "question": qn, "output": out, "rerank": rerank_dollars, "embed": embed_dollars, "total": total}


# Test inputs and expected outcomes
# breakeven_reads(1.25, 0.10)  -> about 1.28, so the second send of a 5-minute-cached prefix is already cheaper
# breakeven_reads(2.0, 0.10)   -> 2.11, so the 1-hour cache needs three sends in total
# sim = CacheSimulator(Rates()); sim.run([Request("P", "q1", 10, 0), Request("P", "q2", 10, 10)]).hits  -> 1
# sim.run([Request("P " + str(t), "q", 10, t) for t in range(3)]).hits                                   -> 0 (a changing prefix never hits)
