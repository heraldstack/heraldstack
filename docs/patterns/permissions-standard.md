# HeraldStack Claude Code Permissions Standard

Established 2026-03-30. Applies to all Claude Code projects across the HeraldStack.

Verified against Claude Code documentation via context7 (2026-03-30).
Source: https://docs.anthropic.com/en/docs/claude-code/settings

## How Settings Merge

Claude Code resolves settings in precedence order: managed > CLI args > local project (`.claude/settings.local.json`) > shared project (`.claude/settings.json`) > user global (`~/.claude/settings.json`).

Array settings like `permissions.allow` are **concatenated and deduplicated** across scopes, not replaced. This means global permissions and project permissions both apply — a project does not need to re-declare what the global already allows. A higher-precedence scope can deny what a lower scope allows.

MCP tool permissions must be listed individually (e.g., `mcp__valkey__string_get`). There is no wildcard pattern like `mcp__valkey__*` — only `Bash(*)` and `WebFetch(*)` support glob wildcards.

## Design Principles

1. **Global settings own cross-project permissions.** Any tool permission needed by 2+ projects goes in `~/.claude/settings.json`, not duplicated per-project. Global and project permissions merge additively.
2. **Project settings own MCP server enablement.** Each project's `.claude/settings.local.json` declares which MCP servers from its `.mcp.json` are active. Tool permissions for those servers live in global settings.
3. **No stale cruft.** Project settings must not accumulate one-off Bash permission entries. `Bash(*)` in global covers all Bash commands. `WebFetch(*)` in global covers all domains.
4. **Read permissions are project-scoped.** Cross-repo reads (e.g., `Read(//home/bryanchasko/code/heraldstack/**)`) stay in project settings because they represent an intentional scope decision.
5. **enabledMcpjsonServers must match .mcp.json keys exactly.** Every server key in `.mcp.json` must appear in `enabledMcpjsonServers`, and vice versa. No orphans in either direction.

## Global Settings (`~/.claude/settings.json`)

Covers all Claude Code sessions regardless of working directory.

| Category       | Pattern                                                                   | Notes                                                                                               |
| -------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Bash           | `Bash(*)`                                                                 | All shell commands                                                                                  |
| WebFetch       | `WebFetch(*)`                                                             | All domains                                                                                         |
| GitHub MCP     | All 40+ `mcp__github__*` tools                                            | Full GitHub API access                                                                              |
| context7 MCP   | `mcp__context7__*`                                                        | Library doc lookups                                                                                 |
| Qdrant MCP     | `mcp__qdrant-writing__*`, `mcp__qdrant-inbox__*`, `mcp__qdrant-shared__*` | All 3 collections, find + store                                                                     |
| Valkey MCP     | All `mcp__valkey__*` tools                                                | Full data structure access (strings, hashes, lists, sets, sorted sets, streams, JSON, bitmaps, HLL) |
| Filesystem MCP | `mcp__rocm-filesystem__*`, `mcp__macmini-filesystem__*`                   | Both host filesystems                                                                               |
| Flags          | `skipDangerousModePermissionPrompt: true`                                 | No double-confirm on dangerous mode                                                                 |

## Project Settings (`.claude/settings.local.json`)

Minimal per-project. Only contains:

```json
{
  "permissions": {
    "allow": ["Read(//home/bryanchasko/code/heraldstack/**)"]
  },
  "enabledMcpjsonServers": [
    "github",
    "context7",
    "docker-mcp",
    "rocm-filesystem",
    "macmini-filesystem",
    "qdrant-writing",
    "qdrant-inbox",
    "qdrant-shared",
    "valkey"
  ]
}
```

Adjust `enabledMcpjsonServers` to match what's in the project's `.mcp.json`. Add project-specific `Read()` paths as needed.

## Anti-patterns

- Do NOT add individual `Bash(git push:*)` entries to project settings — `Bash(*)` global covers it
- Do NOT add `WebFetch(domain:github.com)` entries — `WebFetch(*)` global covers it
- Do NOT list MCP tool permissions in project settings — they belong in global
- Do NOT accumulate one-off Bash command permissions from interactive sessions — clean them out periodically

## Project Types

Not all HeraldStack projects use Claude Code. The permissions standard applies only to Claude Code projects.

| Type                    | Config dir       | Permissions standard applies                                    | Examples                                                     |
| ----------------------- | ---------------- | --------------------------------------------------------------- | ------------------------------------------------------------ |
| Claude Code (shannon)   | `.claude/`       | Yes                                                             | shannon-claude-code-cli, gander-goose-cli, haunting-kiro-cli |
| Gemini CLI (ibeji)      | `.gemini/`       | No — uses own settings format                                   | ibejigemini                                                  |
| LangGraph (deep agents) | `.deepagents/`   | No — standalone Python system                                   | heraldstackdeepagentscli                                     |
| Goose CLI (gander)      | Docker container | No — but shares `.mcp.json` via mounted Claude Code project dir | gander-goose-cli                                             |

For non-Claude-Code projects, the only relevant standard is: use canonical `heraldstack-mcp/launchers/` paths, not legacy `~/code/utilities/mcp-launchers/`.

## Applying to a New Project

1. Create `.mcp.json` with the MCP servers the project needs
2. Create `.claude/settings.local.json` with `enabledMcpjsonServers` matching `.mcp.json` keys exactly
3. Add any project-specific `Read()` paths
4. Verify the MCP server tools are in `~/.claude/settings.json` — if new server type, add each tool individually
5. Run cross-check: `enabledMcpjsonServers` keys must equal `.mcp.json` server keys (zero orphans either direction)
6. Test with a fresh session to confirm zero unnecessary prompts

## Verification

Run this from any project root to verify alignment:

```bash
python3 -c "
import json
mcp = json.load(open('.mcp.json'))
settings = json.load(open('.claude/settings.local.json'))
mcp_keys = set(mcp.get('mcpServers', {}).keys())
enabled = set(settings.get('enabledMcpjsonServers', []))
print(f'in mcp but not enabled: {sorted(mcp_keys - enabled)}')
print(f'enabled but not in mcp: {sorted(enabled - mcp_keys)}')
print('PASS' if mcp_keys == enabled else 'FAIL')
"
```
