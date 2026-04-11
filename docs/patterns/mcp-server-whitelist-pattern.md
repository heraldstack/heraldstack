# mcp server whitelist pattern

declare an explicit, minimal mcpServers block in every agent definition — never inherit a global set by omission.

## problem

when an agent definition omits the `mcpServers` field, the harness loads every server configured for the session. a research agent inherits a filesystem MCP it never calls. a REST-only subagent inherits valkey, qdrant, and github tools that sit idle but consume context and expand the attack surface. the cost is invisible until you audit token usage or trace an unexpected tool call in a session log.

in Claude Code agent definitions, the `mcpServers` field is optional. omitting it does not mean "no servers" — it means "inherit all servers from the session's `.mcp.json`."

## pattern

every agent definition declares its MCP server list explicitly.

### REST-only agents (no MCP tools needed)

```yaml
mcpServers: []
```

an empty array is unambiguous: no servers load for this agent. applies to agents that work entirely through native tools (Bash, Read, Grep, Edit, Write) or make calls over HTTP without needing an MCP server.

examples: `hs-shannon-theseus-orin-github-ops` (uses `gh` CLI via Bash), `hs-shannon-theseus-stratia-codebase-mapper` (read-only native tools), validation agents whose output is pure reasoning.

### agents with bounded tool needs

list only what the agent actually calls:

```yaml
mcpServers:
  - qdrant-shared
  - context7
```

not the full session set. if the agent does one semantic query and nothing else, it gets one server.

### agents that legitimately need the full session set

leave the field absent — but document why. add a comment or a note in the agent's `## mcp` section explaining that full server inheritance is intentional. this makes the omission a deliberate choice rather than an oversight.

## how to audit

run a pass over all agent definitions in `.claude/agents/`:

```bash
grep -L "mcpServers" .claude/agents/*.md
```

files missing `mcpServers` are candidates for review. for each: check whether the agent calls MCP tools. if not, add `mcpServers: []`. if it does, enumerate the specific servers it needs.

also check for dead `disallowedTools` blocks that were added to compensate for inherited servers. when `mcpServers: []` is explicit, there is nothing to disallow — remove the block.

## applied across the heraldstack

| repo                             | agents updated                          | result                                   |
| -------------------------------- | --------------------------------------- | ---------------------------------------- |
| shannon-claude-code-cli          | 6 REST-only agents                      | mcpServers: [] + disallowedTools removed |
| ux-testing-moodle-uploader       | 2 agents (liora, orin)                  | mcpServers: []                           |
| chrome-extension-moodle-uploader | 6 REST-only agents, 1 chrome-only agent | mcpServers: [] / ["chrome-devtools"]     |

## reference

- source pattern: shannon audit (2026-04-11), propagated to ux-testing PR #14, chrome-extension PR #503
- first captured: heraldstack/shannon-claude-code-cli issue #52
