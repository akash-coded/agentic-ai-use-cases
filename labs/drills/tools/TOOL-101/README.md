# TOOL-101 · Fill in the honest empty result

`tools` · **easy** · `blank` · ~8 min · no AWS account

A policy search finds nothing and returns `[]`. The model reads that and writes *"there are no restrictions on this fare"* — the opposite of what the tool meant. Fill in the four blanks so the return value cannot be misread.

```python
def search_policy(query, corpus, index_ready=True):
    if not index_ready:
        return {"status": ____1____,            # the corpus was NOT searched
                "advice": "The policy corpus was not searched. Do not state what policy says; "
                          "tell the user you could not check and escalate."}

    matches = [p for p in corpus if query.lower() in p["text"].lower()]
    if not matches:
        return {"status": ____2____,            # searched, held nothing
                "searched_count": ____3____,    # evidence the search happened
                "advice": ____4____}            # what the model must NOT conclude
    return {"status": "ok", "matches": matches}
```

## The blanks

| | What goes here |
| --- | --- |
| `____1____` | A status string meaning *the corpus was never searched* |
| `____2____` | A status string meaning *searched, and nothing matched* — it must differ from blank 1 |
| `____3____` | How many passages were searched |
| `____4____` | A sentence that **forbids** the wrong conclusion and names the next action |

Post the completed function:

````markdown
/drill TOOL-101

```python
def search_policy(query, corpus, index_ready=True):
    ...
```
````

## What this proves

That your tools encode the difference between two absences the model reliably confuses. Whatever you do not put in the payload, the model cannot recover downstream.
