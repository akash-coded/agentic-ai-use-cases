# Community Answers

The best answers from [Discussions](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions), curated. Faster than asking again, and faster than scrolling 66 threads.

**Answered questions carry a ✅ in Q&A.** This page is the human-curated layer on top: grouped by what you are actually trying to do.

---

## The loop and tools

| Question | Short answer |
| --- | --- |
| **[Why does my agent call the same tool twice?](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/58)** | You appended the tool result but not the assistant message that requested it. From the model's side it never asked. Append the assistant message verbatim first |
| Why is `[]` more dangerous than an exception? | An exception cannot be misread as data. `[]` reads as "nothing applies" when it means "I found nothing". Return an explicit status. [TOOL-03](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs/catalog/tools/TOOL-03) |
| Why does `except Exception` not catch everything? | `SystemExit` and `KeyboardInterrupt` inherit from `BaseException`. In a dispatcher, `except BaseException` is correct — it is a boundary |

## Bedrock and AWS

| Question | Short answer |
| --- | --- |
| **[What does `ValidationException` on the model ID mean?](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/59)** | You passed a bare model ID where an inference profile ID is required. `aws bedrock list-inference-profiles` |
| **[What will this cost me?](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/60)** | Inference is cheap; idle OpenSearch collections and AgentCore runtimes are not. Tear down as you go |
| Why does access fail only sometimes? | A geographic inference profile routes across regions. You need model access in every destination |

## Frameworks

| Question | Short answer |
| --- | --- |
| **[Strands or LangChain first?](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/61)** | Neither — learn the loop first. Then whichever your codebase uses, which for most people is LangChain |

## Retrieval and evaluation

| Question | Short answer |
| --- | --- |
| **[My citation does not support the claim. What are we measuring wrong?](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/62)** | Citation theatre. Retrieved ≠ cited ≠ verified; you are measuring the first two. Spot-check five per release |
| **[How do I know if my golden set is any good?](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/63)** | How many cases did it fail the day you froze it? If almost none, it is a mirror |

---

## Ask a new one

[Q&A](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/q-a). Four things get you answered fast: the **module or lab**, the **exact error** in full, your **region**, and **what you tried**.

⚠️ Remove your account ID and credentials before pasting. Placeholder is `123456789012`.

## Curating this page

When a Q&A thread gets a good answer, add a row: the question as a link, and a one-sentence answer that is useful **without clicking**. That last constraint is what makes this page worth having — a list of links is just the Q&A category again.

Anyone can edit. [How](Contributing-to-this-Wiki).
