# 🚀 Weekend Sprint

**For:** you want a working agent by Sunday night, and depth can come later.
**Time:** ~12 hours. **Finish line:** a Bedrock agent that calls your own tools and answers from your own documents.

> Prerequisite: an AWS account with Bedrock model access enabled. Do
> [`docs/setup/aws-account-setup.md`](../setup/aws-account-setup.md) *before* Saturday morning — access
> approval is not always instant.

## Saturday morning · 3 h — get a model answering

| | Step |
| --- | --- |
| 1 | [Module 01 deck](../../modules/01-llm-and-aws-bridge/slides/Day1.5_LLM_AWS_Bridge.pptx) — skim for model choice and the regional prefix rule |
| 2 | [`00_Bedrock_Onboarding.ipynb`](../../modules/02-bedrock-essentials/notebooks/00_Bedrock_Onboarding.ipynb) — prove access works |
| 3 | [`converse_api_masterclass.ipynb`](../../modules/02-bedrock-essentials/notebooks/converse_api_masterclass.ipynb) — the API you will use all weekend |

## Saturday afternoon · 3 h — give it hands

| | Step |
| --- | --- |
| 4 | [`travelmind_refund_agent.ipynb`](../../modules/02-bedrock-essentials/notebooks/travelmind_refund_agent.ipynb) — tool use, properly |
| 5 | [Exercise 3 · tool use and KBs](../../modules/02-bedrock-essentials/exercises/Exercise_3_Tool_Use_and_Knowledge_Bases.pdf) |

## Sunday morning · 3 h — the loop, then the framework

| | Step |
| --- | --- |
| 6 | [`Day6_Demo_1_NoStrands.ipynb`](../../modules/05-agent-loop-no-framework-to-strands/notebooks/Day6_Demo_1_NoStrands.ipynb) — write the loop yourself. **Do not skip this.** |
| 7 | [`Day6_Demo_2_Strands.ipynb`](../../modules/05-agent-loop-no-framework-to-strands/notebooks/Day6_Demo_2_Strands.ipynb) — the same thing, in a tenth of the code |

## Sunday afternoon · 3 h — make it yours

| | Step |
| --- | --- |
| 8 | [`01_strands_foundations.ipynb`](../../modules/06-strands-foundations/notebooks/01_strands_foundations.ipynb) |
| 9 | [Build 1 · give the agent a job](../../modules/06-strands-foundations/exercises/build-1-give-the-agent-a-job.md) — swap in your own domain |
| 10 | [`Day6_Capstone_TravelMind_Desk.ipynb`](../../modules/05-agent-loop-no-framework-to-strands/exercises/Day6_Capstone_TravelMind_Desk.ipynb) if you have energy left |

## You are done when

Your agent calls at least two tools you wrote, handles a multi-step request, and you can explain what
Strands is doing on your behalf.

## Where to go next

[🛠️ Agent Engineer](agent-engineer.md) picks up exactly here and takes it to production.
