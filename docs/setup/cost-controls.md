# Cost Controls

Do this before Module 02. Not after your first surprise.

## Set a budget alarm first

**AWS Billing → Budgets → Create budget → Cost budget**. A monthly figure you would be annoyed but not
harmed by. Alerts at 50%, 80% and 100%.

A budget alarm does not stop spending. It tells you. That is still the difference between noticing on day
two and noticing on day thirty.

## Where money actually goes on this curriculum

| Source | Typical driver | Order of magnitude |
| --- | --- | --- |
| Bedrock model invocation | Tokens in + tokens out | Cents per exercise, dollars per module |
| OpenSearch Serverless | **Provisioned capacity, billed while it exists** | The one that surprises people |
| AgentCore Runtime | Deployed agents, billed while running | Real if left up |
| Knowledge Base storage | Vectors and their backing store | Small but persistent |
| Lambda | Invocations | Negligible at learning scale |

**The two that bite:** OpenSearch Serverless collections and AgentCore runtimes both cost money for
existing, not for being used. Delete them when you finish the module.

## Teardown checklist

After [Module 10](../../modules/10-rag-opensearch-litellm/):
- [ ] Delete OpenSearch Serverless collections
- [ ] Delete knowledge bases and their vector stores
- [ ] Empty and delete the S3 data source buckets

After [Module 11](../../modules/11-bedrock-agentcore/) and [14](../../modules/14-end-to-end-production/):
- [ ] Delete AgentCore runtimes
- [ ] Delete gateways
- [ ] Delete memory stores
- [ ] `cdk destroy` any CDK stacks

After [Modules 03–04](../../modules/03-bedrock-agents/):
- [ ] Delete Bedrock agents and their aliases
- [ ] Delete Lambda functions and log groups

## Controlling spend while you learn

1. **Use a smaller model for exercises.** Most exercises teach a mechanism, not a capability. A cheaper
   model exercises the same code path.
2. **Cap `maxTokens`.** An unbounded output is an unbounded bill.
3. **Cap loop iterations.** A runaway agent loop is the classic way to lose money overnight — see the
   [Module 05 LLD](../architecture/lld/05-agent-loop-no-framework-to-strands.md).
4. **Do not leave a swarm running.** Swarms without a stop rule do not stop.
5. **Watch the token count.** Every notebook in Module 02 prints it. That habit is the point.

## Model the cost before you build

Three workbooks, in increasing specificity:

- [Token-cost calculator](../../modules/00-agentic-foundations/activities/H2-03_Token-Cost_Calculator.xlsx) — per interaction
- [Bedrock cost estimator](../../modules/06-strands-foundations/activities/Bedrock_Cost_Estimator.xlsx) — per workload
- [AgentCore cost and capacity workbench](../../modules/11-bedrock-agentcore/activities/AgentCore_Cost_and_Capacity_Workbench.xlsx) — deployed

Current pricing is on the [Bedrock pricing page](https://aws.amazon.com/bedrock/pricing/). This repo
deliberately does not hard-code prices, because they change and stale numbers are worse than none.
