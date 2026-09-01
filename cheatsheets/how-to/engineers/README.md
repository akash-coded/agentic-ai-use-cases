# How-to · Engineers

Practical recipes. Each is a working session, not an article.

| How-to | Time | Prevents |
| --- | --- | --- |
| 🔧 **[Add a tool the model actually calls correctly](add-a-tool-properly.md)** | 30 min | Wrong-tool selection, confident-wrong on empty results |
| 🚀 **[Deploy any agent to AgentCore](deploy-any-agent-to-agentcore.md)** | 60–90 min | Untestable agents, unbounded memory cost |
| 🚦 **[Build a quality gate that actually blocks](build-a-quality-gate.md)** | half day | Shipping regressions |
| 🔁 **[Migrate LangChain ↔ Strands](migrate-langchain-to-strands.md)** | 1 day | Migrating for its own sake; silent behaviour change |
| 🧠 **[Memory that does not grow forever](memory-that-doesnt-grow-forever.md)** | 2 h | Context overflow, surprise storage bills |

## The order that works if you are new

1. [Write the loop by hand](../../../modules/05-agent-loop-no-framework-to-strands/) — nothing else makes
   sense until you have
2. [Add a tool properly](add-a-tool-properly.md)
3. [Memory that does not grow forever](memory-that-doesnt-grow-forever.md)
4. [Build a quality gate](build-a-quality-gate.md) — **before** deploying, not after
5. [Deploy to AgentCore](deploy-any-agent-to-agentcore.md)

Step 4 before step 5 is deliberate. Deploying something you cannot evaluate is how you end up unable to
change it.

---

[⬅️ All how-tos](../) · [🧠 Frameworks](../../frameworks/) · [📖 Quick reference](../../quick-reference/)
