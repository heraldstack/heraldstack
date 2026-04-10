# patterns

operational patterns observed across heraldstack collectives. patterns here are canonical — when a collective refines a pattern, the refinement is promoted back here

## index

| pattern | origin collective | summary |
|---|---|---|
| [agent-splitting-pattern](agent-splitting-pattern.md) | shannon | when to split an agent into multiple variants vs keeping it unified |
| [agent-tooling-pattern](agent-tooling-pattern.md) | shannon | tool selection discipline for theseus agents — minimum viable tool set, disallowedTools as a write-access guardrail |
| [context-efficiency-pattern](context-efficiency-pattern.md) | shannon | reducing token consumption via lazy reads, structured tool results, and subagent offloading |
| [dual-identity-pr-pattern](dual-identity-pr-pattern.md) | shannon | commit under service account, review under human account — psych-safe separation for agentic prs |
| [hook-governance-pattern](hook-governance-pattern.md) | shannon | when to use hooks vs in-agent logic, hook scoping, failure recovery |
| [lazy-context-pattern](lazy-context-pattern.md) | shannon | defer context loading until the moment it is load-bearing, never pre-read speculative files |
| [partition-by-intent-pr-pattern](partition-by-intent-pr-pattern.md) | shannon | group dirty files by intent and open one pr per intent — zero data loss, zero mashups |
| [permissions-standard](permissions-standard.md) | shannon | permissionMode defaults per agent tier, write-access policy, disallowedTools matrix |
| [worktree-isolation-scope-pattern](worktree-isolation-scope-pattern.md) | shannon | agents with `isolation: worktree` bind to their defining repo — cross-repo ops run inline |

## origin note

patterns here emerged from shannon (claude code cli) operations as the most mature collective. they are framed in claude code vocabulary (hooks, subagents, mcp servers) but the underlying principles generalize to goose, kiro, gemini, codex, and github copilot collectives. when porting a pattern to another collective, preserve the principle and translate the mechanism

## promotion

new patterns land in a collective's own `docs/` first. once a pattern has been applied in at least two collectives without modification, it is promoted here as canonical. promotion is a pr to this repo that moves the pattern file and adds a row to the table above
