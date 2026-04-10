# dual-identity pr pattern

enforce heraldstack/BryanChasko author-reviewer separation so self-approval is structurally impossible, not just a convention.

## problem

when a single ai collective authors all PRs and also holds merge authority, self-approval is trivially possible. github allows it. humans forget. agents don't care. the result is a code review process that exists only on paper.

the shannon writes code as the `heraldstack` github user. reviews must happen as `BryanChasko`. making those two identities switch places is the mechanism — not a checklist item.

## pattern

### 1. two github identities in keyring

both accounts must be authenticated on the host machine:

```
gh auth login --hostname github.com   # once for heraldstack
gh auth login --hostname github.com   # once for BryanChasko
```

verify both are present:

```
gh auth status
```

`heraldstack` authors commits, creates branches, opens PRs via `hs-shannon-theseus-orin-github-ops`. `BryanChasko` reviews, approves, merges via `hs-shannon-theseus-stratia-reviewer`. neither account does the other's job.

### 2. reviewer agent with disallowedTools

the reviewer agent (hs-shannon-theseus-stratia-reviewer) blocks all MCP github write tools in frontmatter. this forces every github operation through `gh` CLI bash commands, which respect the active `gh auth` identity. MCP tools authenticate via token in config — they do not switch when you call `gh auth switch`.

frontmatter disallowedTools block example:

```yaml
disallowedTools:
  - mcp__github__create_or_update_file
  - mcp__github__push_files
  - mcp__github__create_branch
  - mcp__github__create_pull_request
  - mcp__github__merge_pull_request
  - mcp__github__create_issue
  - mcp__github__update_issue
  - mcp__github__add_issue_comment
  - mcp__github__create_release
  - mcp__github__fork_repository
  - mcp__github__delete_file
  - mcp__github__add_reply_to_pull_request_comment
  - mcp__github__pull_request_review_write
  - mcp__github__create_repository
  - mcp__github__issue_write
  - mcp__github__update_pull_request
  - mcp__github__add_comment_to_pending_review
  - mcp__github__sub_issue_write
  - mcp__github__update_pull_request_branch
  - mcp__github__assign_copilot_to_issue
  - mcp__github__request_copilot_review
```

tools allowed: `Read`, `Glob`, `Grep`, `Bash` only. the agent reads diffs and files, then calls `gh` commands directly.

### 3. gh auth switch protocol

every review session follows this sequence in order. no exceptions, no shortcuts:

1. `gh auth switch --user BryanChasko`
2. `gh auth status` — halt if BryanChasko is not the active user
3. perform review, approval, merge
4. `gh auth switch --user heraldstack`
5. `gh auth status` — warn if heraldstack is not restored

if step 1 or step 4 fails (user not in keyring, token expired), the agent halts and returns `"status": "blocked"`. it does not proceed with the wrong identity.

### 4. /tmp lock files for cross-hook identity detection

`session.agent_name` is not consistently populated in the PreToolUse hook payload — this is a known claude code limitation. lock files are the reliable fallback.

on session start, the reviewer agent runs:

```bash
touch /tmp/.stratia-active
```

orin sets the equivalent at its own entry point:

```bash
touch /tmp/.orin-active
```

the `git-orin-gate` PreToolUse hook reads these files when `session.agent_name` is empty. identity resolution order:

1. `session.agent_name` from hook payload (when populated)
2. `COPILOT_AGENT_NAME` env var (for explicit launch-time injection)
3. `/tmp/.orin-active` or `/tmp/.stratia-active` (lock file fallback)

the SubagentStop hook removes both lock files unconditionally:

```bash
rm -f /tmp/.orin-active /tmp/.stratia-active 2>/dev/null || true
```

lock files are in `/tmp` — they do not persist across reboots and are not committed.

### 5. git-orin-gate PreToolUse hook

`git-orin-gate.sh` fires on every Bash tool call. it reads the command, resolves agent identity via the three-tier lookup above, then applies rules:

- orin: always allowed through
- stratia: allowed through for `gh pr review`, `gh pr merge`, `gh pr view`, `gh pr diff`, `gh pr list`, `gh auth` — the stratia check runs before the blocked-commands check, so stratia's merge allowlist takes precedence
- all other agents: blocked from `git push`, `git commit`, `git merge`, `git rebase`, `git reset`, `git tag`, `gh pr create`, `gh pr merge`, `gh pr close`, `gh issue create`, and related write operations — note that `gh pr merge` appears in both this blocked list and stratia's allowlist above; the agent-name match ordering resolves the conflict

blocked commands exit with code 2, which causes claude code to surface the block message to the agent rather than silently failing.

### 6. settings.json hook wiring

wire both hooks in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/git-orin-gate.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/subagent-cleanup.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

`timeout` values prevent hook hangs from blocking the session. the gate hook is intentionally fast (10s). cleanup runs longer (30s) to allow worktree prune and `git fetch --prune`.

## results

| metric                          | before (single identity)                  | after (dual identity)                                |
| ------------------------------- | ----------------------------------------- | ---------------------------------------------------- |
| self-approval possible          | yes — same token authors and approves     | no — structurally impossible via separate gh auth    |
| review audit trail              | single identity in github history         | two distinct users visible in PR timeline            |
| accidental merge by wrong agent | possible — any agent can call gh pr merge | blocked by orin gate unless agent is stratia or orin |
| stale lock files after crash    | not applicable                            | cleaned by SubagentStop hook on every agent exit     |

note: `hs-shannon-theseus-stratia-reviewer` does not exist in the shannon repo agent directory — it is defined in the reference implementation repo. adopters must create the agent definition as part of their setup

## why this matters in solo and pair contexts

a single developer relying on ai agents still benefits from the separation. the review agent operates under different github credentials, reads the diff independently, evaluates for regressions and security issues, and makes an explicit pass/fail decision. the approval in github history reflects a separate identity — not the same token that authored the commit.

this is not bureaucratic process. it is the mechanical minimum needed for "code review" to mean something other than the author clicking approve.

## adoption checklist

- [ ] both `heraldstack` and `BryanChasko` github accounts authenticated with `gh auth login`
- [ ] verify both present: `gh auth status`
- [ ] create reviewer agent definition with full `disallowedTools` block in frontmatter
- [ ] reviewer agent instructions include lock file creation (`touch /tmp/.stratia-active`) at session start
- [ ] reviewer agent identity protocol: switch → verify → operate → restore → verify
- [ ] write `git-orin-gate.sh` with three-tier identity resolution and per-agent allowlist
- [ ] subagent-cleanup hook removes `/tmp/.orin-active` and `/tmp/.stratia-active`
- [ ] wire both hooks in `.claude/settings.json` with timeouts
- [ ] test: dispatch reviewer on a real PR, verify gh auth status before and after, verify orin gate allows review commands through

## reference implementation

- repo: `chasko-labs/chrome-extension-moodle-uploader`
- agent: `.claude/agents/hs-shannon-theseus-stratia-reviewer.md`
- hooks: `.claude/hooks/git-orin-gate.sh`, `.claude/hooks/subagent-cleanup.sh`
- config: `.claude/settings.json`
