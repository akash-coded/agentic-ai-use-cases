# Interview Guides

Both sides of the table, for five roles. Each guide gives the questions that separate people, what weak
and strong answers sound like, a practical exercise, and red and green flags.

---

| Guide | For hiring | For being hired |
| --- | --- | --- |
| 🛠️ **[Agent Engineer](agent-engineer.md)** | Can they debug the loop, not just build with a framework? | Three stories, and be able to write the loop by hand |
| 🏛️ **[Solutions Architect](solutions-architect.md)** | Judgement under cost constraint | One reference architecture with its cost model |
| 📋 **[Product Manager](product-manager.md)** | Can they specify a probabilistic system? | A story where you narrowed scope and it got better |
| 📊 **[Business Analyst](business-analyst.md)** | Can they produce the golden set? | Describe how you would build one |
| 🔬 **[QA Engineer](qa-engineer.md)** | Do they understand rate-based testing? | A gate you built that correctly blocked a release |
| 🎯 **[Hiring guide](as-the-interviewer.md)** | Running the loop, calibration, what not to ask | — |

---

## The four questions that work on everyone

Whatever the role, these separate people who have operated agents from people who have demoed them:

1. **"What does the system do when it doesn't know?"**
2. **"How do you know it works?"** — listen for an [evidence rung](../frameworks/evidence-ladder.md)
3. **"Tell me about something you decided *not* to build."**
4. **"What did you get wrong, and what changed as a result?"**

Question 4 is the highest-signal question in the field. Nobody with production experience struggles with
it; nobody without it answers it well.

## If you are preparing

The fastest preparation is not reading — it is building something small and measuring it.

| Have this ready | Why |
| --- | --- |
| One agent you built, **with the cost per task** | Numbers beat adjectives |
| One failure you caused and the guard you added | Question 4 |
| One time you argued against building an agent | Question 3 |
| Your evidence rung, stated | Question 2 |

**Then:** [Module 05](../../modules/05-agent-loop-no-framework-to-strands/) if you cannot write the agent
loop by hand, and [Module 13](../../modules/13-agentic-qa-and-evaluation/) if you have never built a gate.
Those two modules answer more interview questions than the other fourteen combined.

---

[⬅️ Field guide](../) · [🧠 Frameworks](../frameworks/) · [📋 Playbooks](../playbooks/)
