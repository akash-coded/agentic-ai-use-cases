# PDL-101 · A classifier that promotes by default

`product` · **easy** · `fix` · ~8 min · no AWS account

This classifier decides whether a use case is a script, a workflow or an agent. It gives the right answer whenever every question has been answered. It gives the **wrong** answer whenever one has not — and in discovery, most have not.

```python
def classify(use_case):
    known    = use_case.get("steps_known_upfront", False)
    language = use_case.get("needs_language", True)
    branches = use_case.get("branches_on_tool_output", True)

    if known and not language:
        return "script"
    if known or not branches:
        return "workflow"
    return "agent"
```

## Find it

Call it with an empty dict — a use case nobody has described yet. What comes back? Should an unanswered question ever move something *up* the ladder?

Fix the defaults so an unknown answer is always the least autonomous reading, without changing the result for fully described cases.

````markdown
/drill PDL-101

```python
def classify(use_case):
    ...
```
````

## What this proves

That you know the tie-breaker: when in doubt, build the simpler thing and let it fail cheaply. And that a default is a decision someone made — usually without noticing.
