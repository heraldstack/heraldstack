# agent tooling pattern

reduce redundant work across multi-agent sessions by backing four coordination subsystems with valkey: diagnostic cache, checkpoint state, file locking, file digests. agents query these before touching source files or re-running builds.

## problem

multi-agent sessions repeat expensive work. an agent re-runs a 45-second build to see the same errors the last agent already parsed. two agents open the same file concurrently. a session starts from scratch because the prior session's progress lived only in context. a large file is read in full when only two functions matter.

valkey-backed tooling cuts all four failure modes at the infrastructure level.

---

## pattern

### diagnostic cache

`build-and-test.js` runs the full build + test suite, captures stdout+stderr, writes the raw output and a structured parse to valkey. agents read from the cache instead of triggering another run.

**valkey key schema**

| key                       | type          | contents                             |
| ------------------------- | ------------- | ------------------------------------ |
| `diag:latest`             | string (JSON) | raw_output, timestamp, session_id    |
| `diag:history:N` (N=1–10) | string (JSON) | prior diag records; GC keeps last 10 |

**`diag:latest` structure**

```json
{
  "session_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "timestamp": 1743932400,
  "raw_output": "...",
  "errors": [...],
  "warnings": [...],
  "success_states": [...],
  "timings": { "build_ms": 3200, "test_ms": 12345, "total_ms": 15545 },
  "blockers": [...]
}
```

**MCP tool**

```
read-diagnostic-summary() → diag:latest (parsed fields only, not raw_output)
```

**cache invalidation** — any code change (file write, git checkout) should trigger a fresh `build-and-test.js` run. agents check the `timestamp` field against recent git activity before trusting cached results.

**`diagnostic-parser.js`** reads `diag:latest`, extracts structured fields (errors, warnings, success_states, timings, blockers), writes `.claude/diagnostics/latest-parsed.json`. blocker patterns include: `Cannot find module`, `SyntaxError`, `ReferenceError`, `ENOENT`, `webpack.*fatal`, `jest.*did not run`. run directly: `node .claude/agent-tooling/diagnostic-parser.js`.

---

### checkpoint system

agents resume from prior session state instead of re-reading git log or re-scanning files. `checkpoint:current` holds the last committed session state. `record-agent-work(changes)` updates it atomically via MULTI/EXEC.

**valkey key schema**

| key                            | type          | contents                              |
| ------------------------------ | ------------- | ------------------------------------- |
| `checkpoint:current`           | string (JSON) | latest session state                  |
| `checkpoint:history:N` (N=1–5) | string (JSON) | rolling prior states; GC keeps last 5 |

**`checkpoint:current` structure**

```json
{
  "session_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "started_at": 1743932400,
  "completed_prs": ["#213", "#212", "#211"],
  "completed_fixes": {
    "domStructureCloner_missing_build": "fixed in #213"
  },
  "next_blocker": "activity_steps_failing_on_quiz_import",
  "file_context": {
    "src/background/background.js": {
      "read_sections": ["executeNextStep", "handleStepCompletion"],
      "last_edited_by": "hs-shannon-theseus-chrome-extension-service-worker-runtime",
      "timestamp": 1743932400
    }
  },
  "timestamp": 1743932400
}
```

`file_context[path].read_sections` names the logical sections the agent read, so the next agent reads only those ranges instead of the whole file. values correspond to section names in `.claude/file-digests/`.

**history entries** add one field: `superseded_at` (unix timestamp when this state was replaced).

**MCP tools**

```
read-checkpoint() → checkpoint:current

record-agent-work(changes: Object) → { success: boolean, checkpoint: Object }
```

`record-agent-work` input schema:

```json
{
  "session_id": "...",
  "completed_pr": "#214",
  "fix_name": "activity_steps_retry_logic",
  "file_edits": {
    "src/background/background.js": {
      "sections": ["executeNextStep", "handleStepCompletion"],
      "last_edited_by": "hs-shannon-theseus-chrome-extension-service-worker-runtime"
    }
  },
  "next_blocker": null,
  "notes": "fixed race condition in executeNextStep"
}
```

**atomicity** — `record-agent-work` MUST use MULTI/EXEC. the history rotation, current update, file_context merge are all-or-nothing. if an agent crashes between commit and checkpoint update, `checkpoint:current` remains at prior state; the next agent re-applies rather than skipping.

**history rotation sequence** (inside MULTI/EXEC):

- copy `checkpoint:current` to `checkpoint:history:1` with `superseded_at = NOW`
- shift existing history: `history:1→2`, `history:2→3`, ..., `history:4→5`
- drop `history:5`
- write updated state to `checkpoint:current`

full schema reference: `.claude/agent-tooling/CHECKPOINT_SCHEMA.md`

---

### file locking

prevents two agents writing the same file concurrently. locks are stored as valkey keys with TTL — they self-expire on agent crash without requiring a cleanup job.

**valkey key schema**

| key           | type          | contents                               |
| ------------- | ------------- | -------------------------------------- |
| `lock:{path}` | string (JSON) | agent_id, acquired_at, ttl, expires_at |

key uses full relative path: `lock:src/background/background.js`

**lock value structure**

```json
{
  "agent_id": "hs-shannon-theseus-chrome-extension-service-worker-runtime",
  "acquired_at": 1743932400,
  "ttl": 300,
  "expires_at": 1743932700
}
```

TTL enforcement uses valkey `SET NX EX` — atomic acquire. if the key already exists, the lock is denied. valkey `EX` handles expiry with no cron.

**MCP tools**

```
lock_file(path: string, agent_id: string, ttl: number = 300)
  → { locked: boolean, expires_at: number | null }

unlock_file(path: string, agent_id: string)
  → { unlocked: boolean }

check_lock(path: string)
  → { locked: boolean, held_by: string | null, expires_in: number | null }

wait_for_lock(path: string, agent_id: string, timeout: number = 60)
  → { acquired: boolean }
```

`unlock_file` is idempotent — returns `{ unlocked: true }` when the key is already gone (expired or never existed). returns `{ unlocked: false }` when agent_id does not match the current holder.

`wait_for_lock` polls every 2 seconds up to `timeout` seconds, then acquires on success. use for sequential agents that need the same file but can tolerate a wait. do not use when parallel agents must not be serialized — dispatch to different files instead.

**dispatch protocol** — before dispatching any agent that writes files: call `check_lock(path)` for each target file. if locked, either wait or route the agent to a different file. orchestrator acquires locks before dispatch; agent releases after commit.

implementation: `.claude/agent-tooling/file-lock.js`

---

### file digests

pre-computed section maps for large source files. agents read the digest to identify which line ranges cover the functions they need, then read only those ranges. avoids whole-file reads on files exceeding ~500 lines.

**location**: `.claude/file-digests/<filename>.digest.md`

**digest structure** (example: `background.js.digest.md`)

```
# File Digest: background.js
Path: src/background/background.js
Size: 85149 bytes
Last scanned: 2026-04-06T20:50:18.206Z
Sections: 50

| Section | Lines | Purpose |
|---------|-------|---------|
| executeNextStep | 1913-2057 | schedules next step via chrome |
| handleRuntimeMessage | 362-805 | handles runtime messages from extension components |
| injectAutomatorScripts | 896-967 | AUTO003 error |
...
```

**agent read protocol** — before reading a source file, check whether a digest exists for it. read the digest first, identify relevant sections by name, then read only those line ranges from the source file. record the section names read in `file_context` when calling `record-agent-work`.

**regenerate digests**: `npm run digest` — run after any structural change (function added, moved, or removed). digests become stale when the source file's logical structure changes; timestamp in the digest header is the last scan time.

**current digests**: `automation-logic.js`, `manifest.json`, `upload.js`, `build.js`, `background.js`

---

## results

| metric                     | before (no tooling)           | after (valkey-backed)            |
| -------------------------- | ----------------------------- | -------------------------------- |
| build re-runs per session  | 3-5 (each agent re-runs)      | 0-1 (agents read cache)          |
| session start context cost | full git log + source reads   | checkpoint resume, ~5 tool calls |
| concurrent edit collisions | frequent with parallel agents | eliminated via TTL locks         |
| large file read tokens     | full file per agent           | targeted ranges via digest       |

## valkey key reference

| key pattern            | subsystem        | ttl                        |
| ---------------------- | ---------------- | -------------------------- |
| `diag:latest`          | diagnostic cache | none (manual invalidation) |
| `diag:history:N`       | diagnostic cache | none (GC on write)         |
| `checkpoint:current`   | checkpoint       | none (persistent)          |
| `checkpoint:history:N` | checkpoint       | none (GC on write)         |
| `lock:{path}`          | file locking     | 300s default (valkey EX)   |

all values are JSON strings. all timestamps are unix seconds (not milliseconds).

---

## agent dispatch sequence

a well-behaved agent session follows this order:

- read `checkpoint:current` — know what was already done, what the next blocker is, which file sections were last read
- read `diag:latest` — know current error state without re-running build
- read relevant file digests — identify line ranges before opening source files
- call `check_lock` for target files before dispatch
- acquire locks (`lock_file`) then dispatch agents
- agents read only the sections identified by digest + checkpoint
- agents commit, then call `record-agent-work`
- agents call `unlock_file` after commit

---

## adoption checklist

- [ ] confirm valkey is reachable at `localhost:6379` (heraldstack-infra `heraldstack-valkey`)
- [ ] add `build-and-test.js` to populate `diag:latest` after each build run
- [ ] wire `read-diagnostic-summary` MCP tool to valkey `diag:latest`
- [ ] initialize `checkpoint:current` with an empty-state seed before first session
- [ ] wire `read-checkpoint` MCP tool to valkey `checkpoint:current`
- [ ] wire `record-agent-work` MCP tool with MULTI/EXEC implementation
- [ ] deploy `file-lock.js` and wire `lock_file`, `unlock_file`, `check_lock`, `wait_for_lock` as MCP tools
- [ ] run `npm run digest` to generate initial file digests
- [ ] add digest regeneration to CI or post-commit hook
- [ ] update CLAUDE.md agent dispatch rules to require lock check before dispatch

---

## reference implementation

- repo: `chasko-labs/chrome-extension-moodle-uploader`
- files:
  - `.claude/agent-tooling/CHECKPOINT_SCHEMA.md` — full checkpoint key schema, MCP tool signatures, atomicity rules, error cases
  - `.claude/agent-tooling/file-lock.js` — node.js implementation (ioredis, SET NX EX, MULTI/EXEC not required for locking)
  - `.claude/agent-tooling/file-lock-tools.md` — MCP tool definitions mapping file-lock.js to tool call semantics
  - `.claude/agent-tooling/diagnostic-parser.js` — reads `diag:latest`, writes `.claude/diagnostics/latest-parsed.json`
  - `.claude/file-digests/` — section maps for background.js, automation-logic.js, upload.js, build.js, manifest.json
