# lazy context pattern

extend context-efficiency-pattern.md with on-demand loading: skills that hydrate context only when invoked, plus a branch-aware SessionStart hook that injects reference files without touching CLAUDE.md.

## problem

context-efficiency-pattern.md solves the CLAUDE.md bloat problem — slim the core file, move reference data to `.claude/reference/`. that pattern still loads branch-injected references at session start for every session on a matching branch, even when the task won't use them.

the remaining gap: github issue context and rarely-needed reference files still require either manual lookup or a CLAUDE.md entry to be available. skills close that gap by making context a pull, not a push.

## skills as lazy loaders

a skill is a small markdown file with a RISEN-style instruction set, invoked by a slash command. skills live in `.claude/skills/<name>/SKILL.md`. they cost zero tokens until invoked.

### SKILL.md frontmatter

every skill file carries three frontmatter fields:

```
---
name: <slug>
description: <one-line description>
argument-hint: <argument format>
---
```

the `name` field maps to the slash command. `argument-hint` documents what to pass. the description surfaces in skill listings.

### /issue skill

invoking `/issue <number>` hydrates full github issue context for that issue: title, state, labels, body, last five comments. the skill fetches only the requested issue via github MCP — no other issues load.

reference implementation at `.claude/skills/issue/SKILL.md`:

```
---
name: issue
description: Hydrate GitHub issue context on-demand — fetches title, body, labels, comments
argument-hint: <issue-number>
---
```

the skill body instructs the agent to: parse the issue number from $ARGUMENTS (strip leading # if present), call the github MCP issue_read tool, display title/state/labels/body plus last five comments, note cross-references without recursively fetching them.

### /ref skill

invoking `/ref <name>` reads a file from `.claude/reference/` and displays it. supports exact match (`$ARGUMENTS.md`) and partial match (any file containing the argument string). if no match, lists available reference files.

reference implementation at `.claude/skills/ref/SKILL.md`:

```
---
name: ref
description: Load a reference file from .claude/reference/ on-demand
argument-hint: <reference-name>
---
```

the skill body: parse reference name from $ARGUMENTS, search `.claude/reference/` for exact then partial match, read and display, list available files on no match.

available references are documented in the skill body so the agent can answer "what refs exist?" without reading the filesystem.

## branch-aware SessionStart hook

`session-context.sh` is a SessionStart hook separate from the operational `session-start.sh`. it handles only context injection — no git health checks, no agent roster, no MCP port status. that separation keeps the context-injection surface narrow.

the hook writes to stdout. Claude Code reads stdout from SessionStart hooks into conversation context. the 10,000-character cap is a hard limit — reference files injected here must be concise.

### what the hook injects

three things, always:

- current branch name under `## [context: branch]`
- issue numbers from the last five commit messages (if any), with a prompt to use `/issue` for full context
- a short list of available on-demand commands under `## [context: on-demand tools]`

branch-matched reference files are injected conditionally based on a keyword case statement. each injected file is prefixed with `## [reference: <name>]`.

### hook design rules

- `|| true` on every command — the hook must never exit nonzero
- stderr redirected to `/dev/null` on every command that could fail — nothing leaks into context
- output is self-describing: every section prefixed with `## [context: ...]` or `## [reference: ...]`
- explicit `exit 0` at end

### keyword-to-reference mapping

the case statement matches branch name patterns to reference files. each pattern block is a separate case statement so multiple references can inject in the same session.

example structure from the reference implementation:

```bash
case "$BRANCH" in
  *moodle*|*activity*|*quiz*|*automat*|*section*|*course*)
    if [ -f "$REF_DIR/moodle-activity-types.md" ]; then
      echo "## [reference: moodle-activity-types]"
      cat "$REF_DIR/moodle-activity-types.md" 2>/dev/null || true
      echo ""
    fi
    ;;
esac
```

the file-existence check (`-f`) prevents the hook from failing silently on missing reference files when a developer hasn't created them yet.

## settings.json wiring

the context hook wires into SessionStart separately from the operational hook:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/session-start.sh"
          },
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

## relationship to context-efficiency-pattern

| concern                    | pattern                    | mechanism                                            |
| -------------------------- | -------------------------- | ---------------------------------------------------- |
| CLAUDE.md size             | context-efficiency-pattern | slim to core, move reference to `.claude/reference/` |
| branch-triggered injection | both patterns              | `session-context.sh` keyword case statement          |
| issue context              | lazy-context-pattern       | `/issue` skill, github MCP, zero upfront cost        |
| reference file access      | lazy-context-pattern       | `/ref` skill, filesystem read, zero upfront cost     |
| derivable info             | context-efficiency-pattern | delete from CLAUDE.md entirely                       |

the patterns compose. implement context-efficiency-pattern first (slim CLAUDE.md, create reference files), then add skills and the context hook.

## results

| metric                 | before (eager loading)                     | after (lazy loading)                                   |
| ---------------------- | ------------------------------------------ | ------------------------------------------------------ |
| issue context cost     | not available, or pre-fetched in CLAUDE.md | zero until /issue invoked, then ~500 tokens            |
| reference access       | always loaded via branch hook or CLAUDE.md | zero until /ref invoked or branch-triggered            |
| session start overhead | all references inject on matching branch   | only branch-matched refs inject; skills cost nothing   |
| maintenance burden     | CLAUDE.md edits for every new reference    | add file to .claude/reference/, update /ref skill body |

## adoption checklist

- [ ] confirm `.claude/reference/` exists (prerequisite: context-efficiency-pattern)
- [ ] create `.claude/skills/issue/SKILL.md` with frontmatter + instruction body
- [ ] set owner/repo in the issue skill to match the project
- [ ] create `.claude/skills/ref/SKILL.md` with frontmatter + instruction body
- [ ] list available references in the ref skill body
- [ ] write `.claude/hooks/session-context.sh` — branch extraction, issue scan, on-demand tools list, keyword case statements
- [ ] add `|| true` to every command in the hook
- [ ] redirect stderr to `/dev/null` on all fallible commands
- [ ] wire `session-context.sh` in `.claude/settings.json` under SessionStart
- [ ] test: start session on main — verify on-demand tools list appears, no reference files inject
- [ ] test: start session on a branch matching a keyword — verify the correct reference injects
- [ ] test: invoke `/issue <number>` — verify full issue context loads
- [ ] test: invoke `/ref <name>` — verify reference file contents display
- [ ] when adding new reference files to `.claude/reference/`, update the `/ref` skill body's available-references list to match

## reference implementation

- repo: `chasko-labs/chrome-extension-moodle-uploader`
- files: `.claude/skills/issue/SKILL.md`, `.claude/skills/ref/SKILL.md`, `.claude/hooks/session-context.sh`
