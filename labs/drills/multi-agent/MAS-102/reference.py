def run_swarm(step, task, max_rounds=8, max_tokens=50_000):
    state, spent, rounds = {}, 0, 0
    while rounds < max_rounds:
        state, done, tokens = step(task, state)
        rounds += 1; spent += tokens
        if done:
            return {"outcome": "completed", "state": state, "tokens": spent, "rounds": rounds}
        if spent > max_tokens:
            return {"outcome": "stopped", "reason": f"token budget: spent {spent} > {max_tokens} after {rounds} rounds",
                    "state": state, "tokens": spent, "rounds": rounds}
    return {"outcome": "stopped", "reason": f"round cap: {max_rounds} rounds without convergence (spent {spent} tokens)",
            "state": state, "tokens": spent, "rounds": rounds}
