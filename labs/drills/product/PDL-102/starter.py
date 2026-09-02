def abstention_target(counts):
    should_abstain = counts["____1____"] + counts["____2____"] + counts["____3____"]
    total = "____4____"
    rate = should_abstain / total
    return {"target": round(rate, 3), "band": (round(rate - 0.05, 3), round(rate + 0.05, 3)), "n": total}
