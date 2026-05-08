# deepagents harness

> target repo: github.com/heraldstack/heraldstack
> target path: canonical/deepagents-harness.md
> status: staged — orin lands this via gh API or post-clone commit

the splintercells deepagents harness is one of the canonical AI agent surfaces in the heraldstack collective. it provides a LangGraph-orchestrated multi-agent system with bedrock nova as the coordinator model, exposed to all heraldstack collectives as an mcp tool surface.

---

## what it is

splintercells (`BryanChasko/splintercells-deep-agents-cli`) is the heraldstack-branded LangGraph harness. 11 herald agents plus a monitor coordinate through a central router. the harness runs local-first on rocm-aibox (ollama + qdrant + AMD ROCm) with optional bedrock nova as the cloud coordinator model.

as of sprint E, the harness also integrates AWS Nova Act for cloud-hosted web automation workflows.

---

## mcp surface (port 8170)

any heraldstack collective (shannon, haunting, gander, ibeji, squad) reaches the harness via the `nova-mcp` mcp server at `http://localhost:8170/mcp`. three tools are available:

| tool                       | what it does                                                                                          |
| -------------------------- | ----------------------------------------------------------------------------------------------------- |
| `invoke_herald_nova`       | sends a query to the nova coordinator; returns text response; supports langgraph thread_id continuity |
| `query_session_history`    | retrieves checkpoint history for a thread_id; backed by valkey or sqlite                              |
| `invoke_nova_act_workflow` | runs an aws nova act workflow; subject to valkey rate limiter (max 3 concurrent, 30min timeout)       |

the server is a systemd service under the `hs-shannon` user account on rocm-aibox.

---

## warm-context retrieval

longer sessions use the `splintercells-checkpoints` qdrant collection (port 6333, mcp endpoint at port 8106) for checkpoint summaries. checkpoint saver env vars:

```
HERALDSTACK_CHECKPOINT_BACKEND=valkey
VALKEY_URL=redis://localhost:6379/0
```

---

## aws auth

bedrock calls authenticate via x509 client cert + IAM RolesAnywhere: awsaerospace account (211125425201) → kiro account (946179428633), us-east-1. no long-lived iam keys on disk.

IAM stack: chasko-labs/secure-access#26
budget policy: chasko-labs/secure-access#28 ($50/mo cap, 50/80/100% sns thresholds)

---

## implementation home

- code: `BryanChasko/splintercells-deep-agents-cli`
- architecture: `docs/architecture.md` in that repo
- iam + cert lifecycle: `chasko-labs/secure-access`
- spawn runtime (microvm path): `heraldstack/heraldstack-firecracker`
- mcp registry entry: `heraldstack/heraldstack-mcp` — `registry.yaml` → `nova-mcp`

---

## collective coexistence

splintercells is independent of shannon, haunting, gander, ibeji, and squad. the five other collectives can consume the nova-mcp tools over localhost without running any splintercells tooling themselves. per `user_collective_vocabulary` memory: deepagents artifacts belong to splintercells — do not route deepagents implementation work to shannon or gander tooling.
