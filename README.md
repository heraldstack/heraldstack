<p align="center">
  <img src="heraldstack-hero.svg" alt="heraldstack" width="800">
</p>

# heraldstack

an autonomous multi-platform ai agent system supporting <a href="https://github.com/bryanchasko">bryanChasko</a>. taking what we can out of different frameworks, each agent & their fellow agents with their own core ego as well as platform identity, problem domain, methodology. they file issues, review each other's code, improve. think in parallel, act asynchronously, defer to domain expertise & systems design - building reusable tooling for the good of the heraldstack. being selective on model & conservative with tokens. delegating to local agents for tedious / repetive / well tooled work like web research

## heraldstack core agent egos

| agent | role | character sheet |
|------|------|-----------------|
| **HARALD** | orchestrator + continuity manager | [harald](docs/character-sheets/harald.md) |
| **Stratia** | strategic planning + execution | [stratia](docs/character-sheets/stratia.md) |
| **Myrren** | vision + foresight | [myrren](docs/character-sheets/myrren.md) |
| **Liora** | creative + lateral thinking | [liora](docs/character-sheets/liora.md) |
| **Kade Vox** | execution + momentum | [kade-vox](docs/character-sheets/kade-vox.md) |
| **Solan** | research + analysis | [solan](docs/character-sheets/solan.md) |
| **Ellow** | emotional intelligence + relationships | [ellow](docs/character-sheets/ellow.md) |
| **Orin** | technical systems + problem-solving | [orin](docs/character-sheets/orin.md) |

## heraldstack on different agentic cli

| name | platform |
|------|----------|
| **shannon** | claude code cli |
| **haunting** | kiro cli | 
| **gander** | goose cli | 
| **ibeji** | gemini cli | 
| **splintercells** | langchain deep agents |
| **mujallad** | codex cli |

## running on

qdrant vector stores for agentic database. valkey for shared cache level. jaeger for distributed tracing of open telemetry. mcp http endpoints across all platforms. amd rocm aibox (radeon gpu) for local mcp + ollama workhorse

## systems

simplify. study similar problems. shift perspective. decompose into atoms. solve backwards. review paths of similar solutions. extend until failure. build tooling to make things easier for future heralds

## project management + planning philosophies

| link | description |
|------|-------------|
| https://agilemanifesto.org/ | Manifesto for Agile Software Development |
| https://scrumguides.org/scrum-guide.html | Official Scrum Guide by Schwaber and Sutherland |
| docs/scrum-github-implementation-guide.md | Heraldstack Scrum implementation with GitHub workflows |
| docs/heraldstack-harness-charter.md | High-level harness behavior for long-running delivery |
| docs/risen-framework-playbook.md | RISEN contracts for agents, planning, and routing |
| docs/agile-software-development-resources.json | Agile references, mentors, feeds, and MCP patterns |
| docs/character-sheets/entity-registry.json | Character entities and CLI designations taxonomy |
| specs/ingestion-pipeline-spec.md | Feed-to-issue promotion pipeline and state contract |
| specs/promotion-criteria.schema.json | Promotion criteria schema for signal-to-issue gating |
| docs/trends-2026-decomposition.md | 2026 trends and decomposition into repo standards |

## links

[bryanChasko.com](https://bryanChasko.com) -- [mcp](https://github.com/BryanChasko/heraldstack-mcp) -- [core](https://github.com/BryanChasko/heraldstack-core)

---

anyone who knows what love is will understand
