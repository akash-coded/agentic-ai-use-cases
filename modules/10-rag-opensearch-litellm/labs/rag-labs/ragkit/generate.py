"""Generation. An interface, a mock simulator, and the answer record.

The mock is not a language model. It is a simulator of the generation stage with three
documented knobs, so retrieval, packing and evaluation can be exercised offline:

  grounded          A perfectly grounded generator answers only when every gold span for
                    the question is present in the packed context, cites the chunks that
                    carry them, and abstains with a stated gap otherwise.
  p_parametric      With this probability the generator answers from "memory" regardless
                    of the evidence. For an answerable question that produces the right
                    answer without support (correct by chance). For a null question it
                    produces the distractor answer (a fabrication).
  position_depth    Retention of a span decays with its distance from the ends of the
                    context, by up to this fraction in the middle. This simulates the
                    lost-in-the-middle shape. It is a simulation, not the effect itself.

A real provider replaces it through the same `LLM.generate` interface.
"""
import re
from dataclasses import dataclass, field
import numpy as np


@dataclass
class Answer:
    text: str
    citations: list = field(default_factory=list)
    abstained: bool = False
    grounded_path: bool = True          # how the mock produced it; real models do not expose this
    used_spans: list = field(default_factory=list)
    missing: list = field(default_factory=list)
    tokens_out: int = 0

    def __str__(self):
        return self.text


class LLM:
    name = "abstract"

    def generate(self, prompt: str, **kw) -> str:
        raise NotImplementedError


def _norm(s: str) -> str:
    return " ".join(s.split())


class MockGenerator(LLM):
    name = "mock"

    def __init__(self, p_parametric: float = 0.0, position_depth: float = 0.0, seed: int = 7):
        self.p_parametric = p_parametric
        self.position_depth = position_depth
        self.rng = np.random.default_rng(seed)

    def _retention(self, position: int, n: int) -> float:
        """1.0 at either end, 1 minus depth in the exact middle, linear in between."""
        if n <= 1 or self.position_depth <= 0:
            return 1.0
        x = position / (n - 1)                  # 0 .. 1
        dist_from_end = min(x, 1 - x) * 2       # 0 at ends, 1 in the middle
        return 1.0 - self.position_depth * dist_from_end

    def answer(self, question, packed_chunk_ids: list, texts: dict) -> Answer:
        """Answer a benchmark Question from a packed context."""
        # 1. which gold spans are present, and where
        found, missing, cites = [], [], []
        n = len(packed_chunk_ids)
        for doc_id, span in question.gold:
            ns = _norm(span)
            pos = next((i for i, cid in enumerate(packed_chunk_ids) if ns in _norm(texts[cid])), None)
            if pos is None:
                missing.append((doc_id, span))
                continue
            keep = self.rng.random() < self._retention(pos, n)
            if keep:
                found.append((doc_id, span))
                cites.append(packed_chunk_ids[pos])
            else:
                missing.append((doc_id, span))
        # 2. parametric path
        if self.rng.random() < self.p_parametric:
            if question.answer is None:
                return Answer(question.distractor_answer, [], False, False, [], [], 8)
            return Answer(question.answer, cites, False, False, found, missing, 12)
        # 3. grounded path
        if question.answer is None:
            return Answer("INSUFFICIENT EVIDENCE. The corpus does not state this.", [], True, True, [], [], 10)
        if not missing:
            return Answer(f"{question.answer} {' '.join('[' + c + ']' for c in cites)}", cites, False, True, found, [], 14)
        if found:
            gap = "; ".join(f"{d}: {s[:40]}..." for d, s in missing)
            return Answer(f"INSUFFICIENT EVIDENCE. Found part of the chain {' '.join('[' + c + ']' for c in cites)} but could not confirm: {gap}",
                          cites, True, True, found, missing, 24)
        return Answer("INSUFFICIENT EVIDENCE. None of the required facts are in the evidence.", [], True, True, [], missing, 10)

    def generate(self, prompt: str, **kw) -> str:
        return "MockGenerator.generate only echoes; use answer(question, packed_ids, texts) for benchmark questions."


CITE = re.compile(r"\[([a-z0-9]+:\d+:[0-9a-f]+)\]")


def citations_in(text: str) -> list:
    return CITE.findall(text)


# Test inputs and expected outcomes
# from ragkit.corpus import ANCHOR
# g = MockGenerator(); texts = {"c1": ANCHOR.gold[0][1], "c2": ANCHOR.gold[1][1]}
# g.answer(ANCHOR, ["c1","c2"], texts).text.startswith("Vega Dynamics, 2023")   -> True
# g.answer(ANCHOR, ["c1"], texts).abstained                                      -> True (partial chain, stated gap)
# MockGenerator(p_parametric=1.0).answer(ANCHOR, [], {}).grounded_path            -> False (correct by chance)
# MockGenerator(position_depth=0.5)._retention(2, 5)                             -> 0.5 (exact middle)
