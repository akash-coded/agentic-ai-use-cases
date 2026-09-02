def run_swarm(step, task, max_rounds=8, max_tokens=50_000):
    state, spent = {}, 0
    while True:
        state, done, tokens = step(task, state)
        spent += tokens
        if done:
            return {"outcome": "completed", "state": state, "tokens": spent}
