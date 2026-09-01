# Concepts

The conceptual layer: what is portable, what is AWS-specific, and how much of this transfers if you leave.

| | |
| --- | --- |
| 🧠 **[Portable GenAI concepts](genai-core-concepts.md)** | Ten ideas true regardless of cloud, vendor or framework — next-token prediction, token economics, the context budget, the agent loop, tools as contracts, memory as a decision, retrieval, multi-agent topology, evaluation, guardrails |
| ☁️ **[Where AWS comes in](aws-service-map.md)** | The stack bottom to top, service by service, with what each replaces if you built it yourself and the module that teaches it |
| ⚖️ **[Portability matrix](portability-matrix.md)** | An honest, itemised answer on lock-in — and how to structure a build so it stays narrow |
| 📖 **[Glossary](glossary.md)** | Terms as used in this curriculum, including where the industry definition is contested |

---

## Read them in this order

1. **[Portable concepts](genai-core-concepts.md)** first. Most of what matters is here, and none of it is
   AWS-specific.
2. **[AWS service map](aws-service-map.md)** second — now each service is "the managed version of a thing
   you already understand", rather than a new thing to memorise.
3. **[Portability matrix](portability-matrix.md)** when someone asks how locked in you are. The short
   answer: less than you would think, and the lock-in concentrates in the platform layer.

## The one-line summary

> The majority of this curriculum is portable by design. The AWS-specific surface is concentrated in the
> platform layer — which is also where the managed services earn their cost.

---

[⬅️ Docs](../) · [📚 Curriculum](../../modules/) · [🧭 Field guide](../../cheatsheets/)
