# AGL-101 · Pull the answer out of a model message

`agent-loop` · **easy** · `implement` · ~8 min · no AWS account

A model's final message is not a string. It is a list of content blocks, and only some of them carry text. Every agent loop has a line that turns that list into the sentence a user reads — and it is a line people get subtly wrong for months.

## The shape

```python
{"role": "assistant",
 "content": [{"text": "Let me check that booking."},
             {"toolUse": {"toolUseId": "t1", "name": "get_booking", "input": {}}},
             {"text": "It was cancelled by the carrier, so it is refundable."}]}
```

Three blocks. Two are text. One is a tool request the loop has already handled. The answer is the two text blocks, in order, joined — **not** the last block, and **not** the first.

## Implement

```python
def answer_text(message: dict) -> str:
    """Return the user-facing text of an assistant message.

    - Join every text block, in order, with a single space.
    - Ignore non-text blocks (toolUse, image, document …).
    - Strip leading/trailing whitespace from the result.
    - A message with no text blocks returns "" — never None, never raises.
    """
    # TODO
```

Copy the block, fill it in, and post it as a comment:

````markdown
/drill AGL-101

```python
def answer_text(message):
    ...
```
````

## What this proves

That you read the message *shape* rather than assuming the answer is `content[0]["text"]` or `content[-1]["text"]`. Both assumptions pass a demo and fail the first time the model narrates before calling a tool.
