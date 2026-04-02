<p align="center">
  <img src="heraldstack-hero.svg" alt="heraldstack" width="800">
</p>

# heraldstack

an autonomous multi-platform ai agent system supporting <a href="https://github.com/bryanchasko">bryanChasko</a>. taking what we can out of different frameworks, each agent & their fellow agents with their own core ego as well as platform identity, problem domain, methodology. they file issues, review each other's code, improve. think in parallel, act asynchronously, defer to domain expertise & systems design - building reusable tooling for the good of the heraldstack. being selective on model & conservative with tokens. delegating to local agents for tedious / repetive / well tooled work like web research

## collectives

| name | platform | role |
|------|----------|------|
| **shannon** | claude code | core anchor; research, architecture, reasoning |
| **haunting** | kiro cli | orchestration; poltergeists + ghosts; ci/cd |
| **gander** | goose cli | docker-native runtime; openrouter proxy; local ollama fallback |
| **ibeji** | gemini cli | auxiliary reasoning; diversity |
| **splintercells** | langchain deep agents | specialized workflows; multi-step chains |

## infrastructure

qdrant vector stores for long-term memory. valkey for ephemeral state. jaeger for distributed tracing. mcp http endpoints across all platforms. amd rocm aibox (radeon gpu) for primary compute. mac mini for secondary ops. everything is wired. everything knows what it knows

## methodology

simplify the problem. study analogues. shift perspective. decompose. solve backwards. extend until failure. repeat

## links

[bryanChasko.com](https://bryanChasko.com) -- [shannon](https://github.com/BryanChasko/claudecodecli-heraldstack-shannon) -- [haunting](https://github.com/BryanChasko/haunting-kiro-cli) -- [gander](https://github.com/BryanChasko/gander-goose-cli) -- [infra](https://github.com/BryanChasko/heraldstack-infra) -- [mcp](https://github.com/BryanChasko/heraldstack-mcp) -- [core](https://github.com/BryanChasko/heraldstack-core)

---

science bless us everyone
