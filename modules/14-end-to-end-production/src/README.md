# TravelMind End-to-End Kit

Everything the End-to-End day promised, runnable. Take one agent from a laptop to
a versioned, governed service: **deploy, version, roll back, route.**

Everything here runs **offline by default**. A deterministic mock stands in for
the model, so you can do the whole thing with no AWS account. Flip a `LIVE` flag
(in each notebook) or set credentials to use the real Bedrock model.

---

## Setup once

**VS Code (3 steps)**
```bash
python -m venv .venv && source .venv/bin/activate     # 1. activate venv
aws configure                                         # 2. creds + region (only if LIVE)
pip install -r requirements.txt                       # 3. install deps
```

**Google Colab (3 steps)**
```python
!pip install -q strands-agents bedrock-agentcore boto3 litellm   # 1. install
import os                                                          # 2. creds via Colab Secrets (if LIVE)
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"                    # 3. region
```

To run a notebook offline you do not even need step 2. Just open and run.

---

## What is in the kit

| File | What it is | Runs offline? |
|---|---|---|
| `travelmind_agent.py` | the agent under test: 3 pure-Python tools + a lazy real-model build + an offline mock | yes |
| `travelmind_runtime.py` | the AgentCore Runtime wrap (entrypoint, `/invocations` + `/ping`, port 8080) | yes (in-process) |
| `Dockerfile` | packages the agent for Runtime; the `EXPOSE 8080` contract | n/a |
| `requirements.txt` | pinned versions (strands 1.42.0, bedrock-agentcore 1.14.0) | n/a |
| `deploy_e2e.ipynb` | **Segment 1.** Wrap -> test contract -> containerize -> configure -> launch -> invoke, with the 404/403 fixes | yes |
| `deploy_runbook.md` | the same deployment, as a step-by-step manual (console + CLI) | n/a |
| `iam_invoke_policy.json` | the least-privilege policy that clears the 403 | n/a |
| `version_manifest.json` | **Segment 2.** one release = prompt + config + model, pinned | yes |
| `release.py` | the release loop you can run: bump -> gate -> promote -> rollback | yes |
| `release_pipeline.md` | versioning, rollout, rollback, the gate as promotion check, as a manual | n/a |
| `gateway_routing.ipynb` | **Segment 3.** LiteLLM from scratch: task routing, fallback chain, circuit breaker, plus the honest "when you do not need it" | yes |
| `reference_architecture.png` | **Segment 4.** the whole pipeline in one diagram | n/a |
| `readiness_checklist.md` | the 10-item production readiness gate | n/a |

---

## Suggested path

Do it in pipeline order. Each piece lights another stage.

1. **Deploy.** Open `deploy_e2e.ipynb`, run it top to bottom (offline). Read
   `deploy_runbook.md` alongside for the cloud commands. You now have the wrap,
   the contract test, the container, and the 404/403 fixes.
2. **Release.** Run the loop and watch a bad prompt get blocked:
   ```bash
   python release.py --set-prompt v7      # FAILS the gate: silently drops rebooking
   python release.py --gate
   python release.py --set-prompt v7.1     # fix it
   python release.py --gate                # PASSES -> canary
   python release.py --rollback            # instant, redirect to the safe version
   ```
   Read `release_pipeline.md` for the why.
3. **Route.** Open `gateway_routing.ipynb`, run it offline. You get task routing,
   a forced fallback, and a circuit breaker, then the honest read on when a
   Bedrock-only stack can skip LiteLLM entirely.
4. **Architect.** Look at `reference_architecture.png` and check your work
   against `readiness_checklist.md`.

---

## Going live (when you have AWS)

In `deploy_e2e.ipynb` and `gateway_routing.ipynb`, set `LIVE = True` in the
config cell. The real model and real LiteLLM paths are already written and
guarded; the offline cells become live calls. The deploy `launch`/`invoke` steps
are run in your terminal (the runbook has every command).

`release.py` stays offline by design: in a real pipeline its gate is your
Session-1 `quality_gate.py` reading the `test_report.json`, `eval_report.json`,
and `cost_latency.json` from the QA kit.

---

## The one connected pipeline

The same TravelMind agent threads through all of it. By the end every stage is
real: `Local -> Wrap -> Containerize -> Deploy -> Version + Gate -> Rollout /
Rollback -> Route`. Swap the tools, data, and prompt and the same pipeline ships
a second domain (CargoTrace, logistics). You did not build one agent. You built a
way to ship agents.
