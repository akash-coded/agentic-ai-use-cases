def abstention_target(counts):
    should_abstain = counts["ambiguous"] + counts["out_of_scope"] + counts["unretrievable"]
    total = sum(counts.values())
    rate = should_abstain / total
    return {"target": round(rate, 3), "band": (round(rate - 0.05, 3), round(rate + 0.05, 3)), "n": total}
