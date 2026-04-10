<p align="center">
  <img src="heraldstack-hero.svg" alt="heraldstack" width="800">
</p>

# heraldstack

an autonomous multi-platform ai agent system supporting <a href="https://github.com/bryanchasko">bryanchasko</a>. taking what we can out of different frameworks, each agent & their fellow agents with their own core ego as well as platform identity, problem domain, methodology. they file issues, review each other's code, improve. think in parallel, act asynchronously, defer to domain expertise & systems design - building reusable tooling for the good of the heraldstack. being selective on model & conservative with tokens. delegating to local agents for tedious / repetive / well tooled work like web research

## pulling this repo

agent workers should clone with:

```
gh repo clone heraldstack/heraldstack ~/work/heraldstack
```

reader identity is assumed to be bryanchasko or a chasko-labs-linked worker. firecracker microvms mount read-only at `/srv/heraldstack`. mcp channels available: qdrant-shared-knowledge, github-mcp, filesystem-mcp. see [llms.txt](llms.txt) for the agent-facing landing file.

## heraldstack core personas

canonical character identity lives in [personas/](personas/). variant duty lives in collective repos. 16 personas registered — see [personas/registry.json](personas/registry.json) for the full index.

| persona | role |
|---|---|
| [harald](personas/harald.md) | anchor, orchestrator, servant leader |
| [stratia](personas/stratia.md) | strategic planning, architecture, skeptical evaluation |
| [ellow](personas/ellow.md) | empathy, team dynamics, psychological safety |
| [orin](personas/orin.md) | technical problem-solving, github operations |
| [kerouac](personas/kerouac.md) | source research, feed synthesis, attributed findings |
| [voss](personas/voss.md) | technical writing, long-form narrative, steering docs |
| [tarn](personas/tarn.md) | infrastructure, integration wiring, cross-tool bridges |
| [ralph-wiggum](personas/ralph-wiggum.md) | qa, logic critique, edge cases |
| [kade-vox](personas/kade-vox.md) | execution, momentum, security scanning |
| [scribe](personas/scribe.md) | writing style enforcement, publication readiness |
| [myrren](personas/myrren.md) | vision, foresight, long-term planning |
| [liora](personas/liora.md) | creative, lateral thinking, design |
| [solan](personas/solan.md) | science, research, logical analysis |
| [hcom](personas/hcom.md) | cross-machine relay, context sync, api glue |
| [arion](personas/arion.md) | cognitive loop resolution, recursive failure interruption |
| [nyxen](personas/nyxen.md) | abstract reasoning, lateral reframe |

## heraldstack on different agentic cli

| name | platform | repo |
|---|---|---|
| **shannon** | claude code cli | [BryanChasko/shannon-claude-code-cli](https://github.com/BryanChasko/shannon-claude-code-cli) |
| **haunting** | kiro cli | [BryanChasko/haunting-kiro-cli](https://github.com/BryanChasko/haunting-kiro-cli) |
| **gander** | goose cli | [BryanChasko/gander-goose-cli](https://github.com/BryanChasko/gander-goose-cli) |
| **ibeji** | gemini cli | [BryanChasko/ibeji-gemini-cli](https://github.com/BryanChasko/ibeji-gemini-cli) |
| **splintercells** | langchain deep agents | [BryanChasko/splintercells-deep-agents-cli](https://github.com/BryanChasko/splintercells-deep-agents-cli) |
| **mujallad** | codex cli | [chasko-labs/mujallad-codex-cli](https://github.com/chasko-labs/mujallad-codex-cli) |
| **squadron** | github copilot (brady gaster subagent config method) | [chasko-labs/squadron-github-copilot-cli](https://github.com/chasko-labs/squadron-github-copilot-cli) |

## who is heraldstack

heraldstack and [BryanChasko](https://github.com/BryanChasko) are cybernetic — a human + ai bonded identity that operates this project jointly. [heraldstack](https://github.com/heraldstack) is the developer account that carries agent-authored commits and the shared persona library; BryanChasko is the human operator who anchors vision, reviews, and merges.

this repo (github.com/heraldstack/heraldstack) is the **canonical source**. the org-owned [chasko-labs/heraldstack](https://github.com/chasko-labs/heraldstack) mirror exists but points back here.

## running on

qdrant vector stores for agentic database. valkey for shared cache level. jaeger for distributed tracing of open telemetry. mcp http endpoints across all platforms. amd rocm aibox (radeon gpu) for local mcp + ollama workhorse

## systems

simplify. study similar problems. shift perspective. decompose into atoms. solve backwards. review paths of similar solutions. extend until failure. build tooling to make things easier for future heralds

## project management + planning philosophies

| link | description |
|------|-------------|
| https://agilemanifesto.org/ | manifesto for agile software development |
| https://scrumguides.org/scrum-guide.html | official scrum guide by schwaber and sutherland |
| docs/scrum-github-implementation-guide.md | heraldstack scrum implementation with github workflows |
| docs/heraldstack-harness-charter.md | high-level harness behavior for long-running delivery |
| docs/risen-framework-playbook.md | risen contracts for agents, planning, and routing |
| docs/agile-software-development-resources.json | agile references, mentors, feeds, and mcp patterns |
| personas/registry.json | character entities, slug standard, and cli designations taxonomy |
| docs/adr/0001-persona-library-split.md | adr — canonical identity here, variant duty in collective repos |
| docs/adr/0002-slug-standard-hs-prefix.md | adr — hs-<collective>-<tier>-<persona>-<role> slug standard |
| specs/ingestion-pipeline-spec.md | feed-to-issue promotion pipeline and state contract |
| specs/promotion-criteria.schema.json | promotion criteria schema for signal-to-issue gating |
| docs/trends-2026-decomposition.md | 2026 trends and decomposition into repo standards |
| docs/user-research-and-ux-standards.md | ux research and usability standards for sprint governance |

## links

[bryanchasko.com](https://bryanchasko.com) -- [mcp](https://github.com/bryanchasko/heraldstack-mcp) -- [core](https://github.com/bryanchasko/heraldstack-core)

---

anyone who knows what love is will understand
