# FAQ

**Do I need an AWS account?**
For most of it, yes. Modules 00, 01 and 15 need nothing.
[`rag_by_hand.py`](../../modules/10-rag-opensearch-litellm/src/rag_by_hand.py) and
[`quality_gate.py`](../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py) also run offline.

**What will this cost me?**
Tens of dollars if you tear down as you go, considerably more if you leave OpenSearch Serverless
collections and AgentCore runtimes running. Read [cost controls](../setup/cost-controls.md) before Module 02.

**Do I need to know Python?**
Enough to read and modify a function. You do not need to be strong at it — the code is written to be read.

**Do I need machine learning background?**
No. There is no maths in this curriculum. [Module 01](../../modules/01-llm-and-aws-bridge/) builds the
model intuition from zero.

**Why write the agent loop by hand in Module 05 when Strands exists?**
Because a framework you cannot reimplement is a framework you cannot debug. It takes about an hour and it
changes how you read every later module.

**Strands or LangChain — which should I learn?**
Both are here, and [Module 08](../../modules/08-langchain-and-langgraph/) puts them side by side on the
same task. Strands if you are AWS-native and starting fresh; LangChain if you are joining an existing
codebase, which is most people.

**How locked in to AWS is this?**
Less than you would think. See the [portability matrix](../concepts/portability-matrix.md) — the majority
of the curriculum is portable by design, and the lock-in concentrates in the platform layer.

**Are there videos?**
Not yet. The written material is complete and self-contained. Progress is tracked in the
[video index](video-index.md).

**Can I use this to teach?**
Yes — MIT licensed. Attribution is appreciated; [`CITATION.cff`](../../CITATION.cff) has the format. The
[training frameworks playbook](training-frameworks-playbook.md) covers the instructional design behind the
structure.

**Why is TravelMind in everything?**
One domain carried across sixteen modules means you are never learning a new business problem at the same
time as a new technical concept. It starts as a single Bedrock call and ends as a deployed, gated,
multi-agent service.

**The notebooks have outputs committed. Is that deliberate?**
Yes. Seeing expected output is part of the teaching. Outputs are scrubbed of account IDs and local paths —
see [notebook hygiene](../setup/local-environment.md#notebook-hygiene-before-committing) before you commit
your own.

**Something is wrong / out of date. What do I do?**
Open an issue, or a PR. [`CONTRIBUTING.md`](../../CONTRIBUTING.md) has the details. Corrections to AWS
behaviour that has changed are especially welcome.

**Can I use a different cloud?**
Modules 00, 01, 05, 07, 09 and 13 transfer with little change.
[LiteLLM in Module 10](../../modules/10-rag-opensearch-litellm/) is specifically about provider portability.
The AgentCore modules are AWS-specific by nature.
