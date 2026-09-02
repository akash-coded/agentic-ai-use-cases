# RET-101 · Predict what fits in the budget

`retrieval` · **medium** · `predict` · ~10 min · no AWS account

No code to write. Read the packer, read the input, and say what comes out — **before** you run anything.

```python
def pack(chunks, budget):
    out, used = [], 0
    for c in chunks:                       # already ranked, best first
        if used + c["tokens"] > budget:
            continue                       # skip, but keep looking
        out.append(c["id"]); used += c["tokens"]
    return out
```

```python
chunks = [{"id": "c1", "tokens": 400},
          {"id": "c2", "tokens": 900},
          {"id": "c3", "tokens": 350},
          {"id": "c4", "tokens": 200},
          {"id": "c5", "tokens": 300}]
budget = 1000
```

## Your answer

Which ids does `pack(chunks, 1000)` return, in order? Post it as a one-line python block:

````markdown
/drill RET-101

```python
answer = ["c1", "..."]
```
````

Then — and this is the actual question — **is that the right set to have packed?** Say why or why not in a sentence above the code block. The bot grades the list; other people grade the sentence.

## What this proves

That you can trace a budget by hand, and that you noticed the packer's policy has a consequence: `continue` rather than `break` means a big chunk near the top does not stop smaller, lower-ranked ones from getting in behind it. That is a design decision, and it is not obviously right.
