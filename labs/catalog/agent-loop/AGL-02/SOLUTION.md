# AGL-02 · Solution

## Why `user`, not `assistant`

The roles are not a description of who did the work. They are a description of **which side of the
exchange the content came from, as the model sees it**.

The model generated the tool request, so that message is `assistant`. Everything flowing back toward the
model — the user's question, a retrieved document, a tool result — is `user`, because it is input the
model must read. The tool ran on your side of the boundary, which makes its output input.

Once you hold it that way round, the API stops feeling arbitrary and you stop getting it wrong.

## The four-message shape

```
user       "Is XY7Q2M refundable?"
assistant  [toolUse: get_booking]        ← ① the step people skip
user       [toolResult: {...}]           ← ② one message, every result
assistant  "Yes — cancelled by carrier."
```

Skipping ① produces a symptom that sends people to the wrong place: the model repeats its tool call
identically. It looks like a dispatcher bug. It is a history bug. From the model's side the request was
never recorded, so the reply has nothing to attach to and the only sensible move is to ask again.

## Parallel calls: one message, not N

```python
# wrong — two user messages in a row, rejected by the API
for r in results:
    new.append({"role": "user", "content": [r]})

# right — one turn, every result, in request order
new.append({"role": "user", "content": results})
```

The error this produces surfaces at the *next* API call, complaining about role alternation. The cause is
here; the message points there. That distance is why the check exists.

## The aliasing check

The Break phase asserts you do not append the caller's message object straight into history. It looks
pedantic until you have a retry wrapper that mutates a response after handing it to you, and history
silently changes shape between turns. Copy on the way in; a shallow copy of the message dict is enough
for this lab.

## The invariant worth keeping

> **Every `toolUse` in history has exactly one `toolResult` with the same id.**

That is a two-line assertion you can run over history in development, and it catches the silent-skip
failure from [AGL-01](../AGL-01/), the dropped-assistant-turn failure from this lab, and most partial
failures in between. Cheap, and it fails at the cause rather than a turn later.

## Field guide

[Failure Signature Catalog](../../../../cheatsheets/frameworks/failure-signature-catalog.md) rows 1 and 2 ·
[Bedrock Converse API](../../../../cheatsheets/quick-reference/bedrock-converse.md#tool-use--the-round-trip-everyone-gets-wrong)
