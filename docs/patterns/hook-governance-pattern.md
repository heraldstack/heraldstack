# hook governance pattern

enforce delegation boundaries at the tool layer — not by convention — using a triad of PreToolUse and PostToolUse hooks that block, route, and repair in real time.

## problem

shannon operates on a strict delegation model: entropy orchestrates, theseus subagents execute. in practice, nothing enforces this at runtime. entropy can call Edit on source files. any agent can call `git push`. code written by subagents accumulates lint drift between writes. when the model drifts from the pattern, the human discovers it only at PR review or when a merge goes wrong.

convention is not enforcement. hooks are.

## pattern

three hooks form the governance triad. two run PreToolUse (before the action is taken), one runs PostToolUse (after the write lands). together they cover all three boundary risks: who writes code, who touches git, what quality state the file is in after every write.

---

### 1. harald-code-gate.sh

**event:** `PreToolUse` — matcher `Edit|Write`

**purpose:** block the main entropy session from writing source code. entropy orchestrates. subagents write.

**behavior:**

- reads `FILE_PATH` from the hook payload via jq (falls back to grep if jq is absent)
- checks `session.is_subagent` flag — if `true`, exits 0 (subagents always pass)
- fallback: if `session.is_subagent` is absent or `false` (hook payload version variance), checks `/tmp` for any lock file matching `chrome-developer-*.lock`, `hs-shannon-theseus-*.lock`, or `myrren-*.lock` — any match exits 0
- applies allowlist — paths entropy CAN edit inline without delegation:
  - `.claude/agents/*`
  - `.claude/hooks/*`
  - `.claude/settings*`
  - `.claude/projects/*/memory/*`
  - `CLAUDE.md`, `MEMORY.md`, `TODO.md`, `TASKS.md`
- blocks writes to `src/`, `tests/`, `scripts/`, `mock/` at the project root — exits 2 with a clear message naming the correct subagent

**exit codes:** `0` = allow, `2` = block (Claude Code treats any nonzero as a hook block)

---

### 2. git-orin-gate.sh

**event:** `PreToolUse` — matcher `Bash`

**purpose:** block all agents except orin from git write operations and gh CLI write operations.

**behavior:**

- reads `COMMAND` and `AGENT_NAME` from the hook payload via jq
- resolves identity with triple fallback:
  - `session.agent_name` from payload (not consistently populated in all payload versions)
  - `COPILOT_AGENT_NAME` environment variable (set when launching orin explicitly)
  - `/tmp/.orin-active` or `/tmp/.stratia-active` lock files (agents create on entry, subagent-cleanup removes)
- orin (`*orin*` substring match on resolved name): always exits 0
- stratia (`*stratia*` match): exits 0 for read-adjacent gh commands — `gh pr review`, `gh pr view`, `gh pr diff`, `gh pr list`, `gh auth` — blocked from write operations
- all other agents: blocked on:
  - `git push`, `git commit`, `git merge`, `git rebase`, `git reset`, `git tag`
  - `gh pr create/merge/close/reopen/edit`
  - `gh issue create/close/reopen/edit/delete`
- block exits 2 with message naming the responsible agent, the blocked command, the resolved agent name

**design note from source:** `session.agent_name` is not consistently populated in PreToolUse payloads — the env var + lock file fallbacks exist precisely because of this. if you launch orin via a wrapper, set `COPILOT_AGENT_NAME=hs-shannon-theseus-orin-github-ops` in that wrapper's environment.

---

### 3. autoformat.sh

**event:** `PostToolUse` — matcher `Edit|Write`

**purpose:** keep written files in valid formatted state without requiring agents to remember to format. surface unfixable errors immediately so the writing agent sees them in the same turn.

**behavior:**

- reads `FILE_PATH` from payload; exits 0 if file does not exist
- scoped to project source paths: `src/`, `tests/`, `scripts/` — ignores config, docs, `.claude/`
- for all matched files: runs `npx prettier --write` first
- for JS/TS variants (`.js`, `.ts`, `.jsx`, `.tsx`, `.mjs`, `.cjs`):
  - runs `npx eslint --fix` (auto-fixable issues)
  - runs `npx eslint` check-only pass to capture remaining errors
  - emits remaining errors as `hookSpecificOutput.additionalContext` JSON so Claude Code surfaces them in the active turn without requiring a separate read
  - caps at 10 error lines; escapes quotes; pipes-delimitates for the JSON field
- for Rust (`.rs`):
  - runs `rustfmt` if available
  - walks up directory tree to find `Cargo.toml`, runs `cargo clippy --quiet` on the containing crate
  - emits clippy `^error` lines as `additionalContext` (capped at 5)

**error reporting format:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "eslint errors in foo.js (fix before committing):\nerror text here"
  }
}
```

this format is required by the Claude Code hooks spec — the key `hookSpecificOutput` with `additionalContext` is what surfaces text back to the agent turn.

---

### settings.json wiring

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/harald-code-gate.sh",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/git-orin-gate.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/autoformat.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

matcher syntax is a pipe-separated substring match against the tool name. `Edit|Write` matches both tools. `Bash` matches only the Bash tool. timeout is in seconds — gate hooks are fast (5s ceiling), autoformat needs headroom for eslint cold start (30s).

## results

| risk                           | without hooks        | with hooks                                                     |
| ------------------------------ | -------------------- | -------------------------------------------------------------- |
| entropy writes source directly | happens silently     | blocked at tool call, message names correct delegate           |
| any agent runs `git push`      | happens silently     | blocked; orin identified as owner                              |
| PR contains lint failures      | discovered at review | surfaced in same turn the file was written                     |
| stratia blocked from PR review | N/A                  | stratia passes; write ops still blocked                        |
| subagent falsely blocked       | N/A                  | is_subagent flag + lock file fallback prevents false positives |

## adoption checklist

- [ ] copy `harald-code-gate.sh` to `.claude/hooks/` — update the `src/`/`tests/`/`scripts/` block list to match your project structure
- [ ] copy `git-orin-gate.sh` to `.claude/hooks/` — no edits required unless you have additional gate-allowed agents beyond orin + stratia
- [ ] copy `autoformat.sh` to `.claude/hooks/` — update the path scope (`src/`, `tests/`, `scripts/`) to match your project; remove rust block if no Rust in the project
- [ ] wire all three hooks in `.claude/settings.json` using the matcher + timeout values shown above
- [ ] confirm `jq` is available on the host — hooks degrade to grep fallback but jq is preferred
- [ ] if launching orin via a wrapper script, set `COPILOT_AGENT_NAME=hs-shannon-theseus-orin-github-ops` in wrapper environment
- [ ] test: verify entropy is blocked from writing to `src/` — open a session, attempt an Edit to a source file, confirm exit 2 message appears
- [ ] test: verify a theseus subagent is NOT blocked — check is_subagent detection or create a lock file manually
- [ ] test: run autoformat by writing a deliberately un-formatted file; confirm prettier runs; confirm eslint errors surface as additionalContext if any remain

## reference implementation

- repo: `chasko-labs/chrome-extension-moodle-uploader`
- issue: BryanChasko/shannon-claude-code-cli#42
- files: `.claude/hooks/harald-code-gate.sh`, `.claude/hooks/git-orin-gate.sh`, `.claude/hooks/autoformat.sh`, `.claude/settings.json`
