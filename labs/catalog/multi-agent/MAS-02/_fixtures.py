def spec(shape, specialists=0, base=2000, handoff=800, result=400, orch_turns=0, rounds=1):
    return {"shape": shape, "specialists": specialists, "base_context_tokens": base,
            "handoff_context_tokens": handoff, "result_tokens": result,
            "orchestrator_turns": orch_turns, "rounds": rounds}


SINGLE = spec("single")
DELEGATION_2 = spec("delegation", specialists=2, orch_turns=2)
DELEGATION_4 = spec("delegation", specialists=4, orch_turns=4)
CRITIQUE_1 = spec("critique", specialists=1, orch_turns=1, rounds=1)
SWARM_UNBOUNDED = spec("swarm", specialists=3, orch_turns=1, rounds=0)
