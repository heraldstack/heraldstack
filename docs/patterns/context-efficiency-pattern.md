# context efficiency pattern

reduce CLAUDE.md token cost by splitting monolithic project context into core + on-demand reference files, with a SessionStart hook for branch-aware injection.

## problem

CLAUDE.md loads every session at full cost. most sessions don't need reference tables (activity types, CSV specs, API endpoints). a 5KB CLAUDE.md burns ~1,500 tokens every conversation — wasted when the session is about CSS or test infrastructure.

## pattern

### 1. slim CLAUDE.md to core-only

keep in CLAUDE.md:

- what the project is (1-2 lines)
- architecture overview (pipeline, data flow)
- code conventions (enforced rules, not derivable from code)

drop from CLAUDE.md:

- reference tables (move to `.claude/reference/`)
- derivable info (commands from package.json, directories from ls, repo URL from git remote)
- domain-specific lookup data (API schemas, activity types, format specs)

### 2. reference files in `.claude/reference/`

place extracted content in individual markdown files:

```
.claude/reference/
  moodle-activity-types.md
  csv-format.md
  test-courses.md
```

agents read these on-demand when working on relevant features. zero token cost in sessions that don't need them.

### 3. SessionStart hook for branch-aware injection

`.claude/hooks/session-context.sh` — a SessionStart hook that:

- reads current git branch name
- matches branch keywords to reference files
- injects relevant content into conversation context (stdout → context, 10,000 char cap)

branch keyword mapping example:

- `*moodle*|*activity*|*quiz*` → moodle-activity-types.md
- `*csv*|*parser*|*data*` → csv-format.md
- `*test*|*e2e*` → test-courses.md

hook design rules:

- every command uses `|| true` — hook must never exit nonzero
- stderr redirected to /dev/null — nothing leaks into context
- output is self-describing: prefix with `## [reference: filename]`
- explicit `exit 0` at end

### 4. settings.json wiring

add the hook to `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/session-context.sh"
          }
        ]
      }
    ]
  }
}
```

## results

| metric                 | before        | after                         |
| ---------------------- | ------------- | ----------------------------- |
| CLAUDE.md size         | 5,460 bytes   | ~1,200 bytes                  |
| token cost per session | ~1,500        | ~350 (core only)              |
| reference availability | always loaded | on-demand or branch-triggered |
| reduction              | —             | 78%                           |

## adoption checklist

- [ ] audit CLAUDE.md — classify each section as CORE / REFERENCE / DERIVABLE
- [ ] create `.claude/reference/` directory
- [ ] move REFERENCE sections to individual files
- [ ] delete DERIVABLE sections
- [ ] write `session-context.sh` with branch keyword mapping for your project
- [ ] wire hook in `.claude/settings.json`
- [ ] test: start session on main (minimal context), switch to feature branch (relevant refs injected)

## reference implementation

- repo: `chasko-labs/chrome-extension-moodle-uploader`
- PR: #190
- files: `CLAUDE.md`, `.claude/reference/*`, `.claude/hooks/session-context.sh`
