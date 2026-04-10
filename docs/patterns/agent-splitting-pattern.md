# agent splitting pattern

split a monolithic theseus agent into domain-specific specialists when it has grown beyond its useful scope. maintain explicit routing in a ROUTING.md so the entropy anchor dispatches without guessing.

## problem

a monolithic agent accumulates scope over time. it grows to cover background runtime logic, UI concerns, config parsing, and file access patterns all at once. above ~5KB the definition costs more tokens to load than any single task needs. more critically: a large agent makes conflicting edits — it reaches into files it does not fully understand, creating race conditions when cross-cutting changes dispatch it twice in a session.

the chrome-extension-moodle-uploader shannon hit this with `hs-shannon-theseus-chrome-developer`. that agent owned both `src/background/background.js` (2,400 lines, service worker lifecycle) and `src/ui/sidepanel/` (upload module, automation-logic, CSV display). any change touching the message protocol required full context for both layers simultaneously. the solution was a clean domain split into `hs-shannon-theseus-chrome-extension-service-worker-runtime` and `hs-shannon-theseus-chrome-extension-sidepanel-ui`.

## when to split

split when any of these are true:

- agent definition file exceeds 5KB on disk
- agent routinely edits files in two distinct architectural layers (e.g. runtime vs. presentation, schema vs. API)
- agent has a "narrowing" section that routes more than two concerns elsewhere — that is evidence of scope creep in the original
- sequential dispatches of the same agent on the same branch produce conflicting edits
- the agent's context-file table spans domains that have no shared runtime dependency

do not split on size alone. a 6KB agent that owns a single coherent domain is fine. split on domain coherence first, size second.

## naming

slugs must be specific enough to route by reading alone. a maintainer who has never seen the codebase should be able to match a file path to the correct slug from the name.

use the pattern `hs-shannon-theseus-<project>-<domain>-<role>`:

- `hs-shannon-theseus-chrome-extension-service-worker-runtime` — not `hs-shannon-theseus-chrome-bg`
- `hs-shannon-theseus-chrome-extension-sidepanel-ui` — not `hs-shannon-theseus-chrome-ui`

the domain segment names the architectural layer. the role segment names the function within that layer. abbreviations that save characters at the cost of clarity fail the maintainer six months later.

## routing guide

every project that has two or more theseus agents needs a `.claude/agents/ROUTING.md`. the entropy anchor reads this file when deciding which agent to dispatch. it is not a convenience — it is the dispatch contract.

ROUTING.md structure:

```markdown
# Agent Routing Guide

For <entropy-anchor-slug> — dispatch rules for <project> work.

## <agent-slug>

Dispatch when the issue is in:

- <file or directory> — <brief rationale>
- <message type or API surface> — <brief rationale>

## <second-agent-slug>

Dispatch when the issue is in:

- ...

## Cross-cutting changes (both <domain-a> + <domain-b>)

Dispatch both agents sequentially. Use file-locking (lock_file / unlock_file) to prevent collision:

1. Dispatch <agent-a> first if the change originates in <domain-a entry point>
2. Dispatch <agent-b> second for the <domain-b> adaptation
3. Each agent acquires locks before editing; releases after surfacing changes to hs-shannon-theseus-orin-github-ops

## When neither agent fits

Escalate to <entropy-anchor-slug>. Do not dispatch <deprecated-agent-slug> (deprecated — split into the two agents above).
```

routing rules must be explicit file paths, not domain descriptions. "dispatch for background issues" is not a routing rule. "dispatch when the issue is in `src/background/background.js`" is.

include a cross-cutting section whenever two agents can plausibly touch the same change. leave it out only when the domains are structurally isolated with no shared files.

## cross-cutting change protocol

when a change spans both domains — for example, a new message case in `handleRuntimeMessage` that requires a corresponding UI state update in `automation-logic.js` — dispatch both agents sequentially, not concurrently. concurrent dispatch to the same repo without coordination produces merge conflicts.

ordering rule: the agent that owns the change origin goes first. if the change is initiated by a background event, dispatch service-worker-runtime first. if the change is initiated by a user action in the sidepanel, dispatch sidepanel-ui first.

file-locking prevents collision between the two dispatches. each agent must:

1. call `lock_file` on every file it intends to edit before making any edit
2. if `lock_file` returns `{ "locked": false }`, call `wait_for_lock` with a reasonable timeout (60s is the default) rather than aborting
3. release all locks via `unlock_file` before surfacing its result to the entropy anchor
4. never proceed to edit a file if `wait_for_lock` returns `{ "acquired": false }`

the file-lock MCP tools use valkey SET NX EX under the hood. locks self-expire via valkey TTL — no cron or cleanup agent needed. the default TTL is 300 seconds; for large files or slow lint pipelines, pass an explicit `ttl` parameter.

manifest files that have sections owned by both agents (e.g. `manifest.json` with both `background` and `side_panel` sections) must be locked by the first dispatched agent for the duration of both agent runs, then released by the second. the entropy anchor must coordinate this: acquire the manifest lock explicitly before dispatching agent one, pass the lock state in the task description, release after agent two completes.

## creating the successor agents

each successor agent definition must:

- open with a role statement that identifies it as "a narrowed split of `<original-slug>`"
- list only the files it owns in its context-files section
- have an explicit "out of scope" section that names the sibling agent for cross-domain escalation
- carry a `<!-- validate with hs-shannon-theseus-stratia-shannon-auditor -->` comment at the end

the original agent's narrowing section is the fastest source of domain boundaries. where the original said "route X to someone else," that is where the split line belongs.

## deprecation path

do not delete the original agent on the day of the split. agents may be cached in session context or referenced in notes that have not been updated yet.

deprecation sequence:

1. add the successor agents to `.claude/agents/`
2. update ROUTING.md to name both successors and add a "when neither agent fits" section that explicitly marks the original as deprecated
3. update the original agent's description field: prefix with `DEPRECATED — split into <slug-a> and <slug-b>. do not dispatch.`
4. leave the original file in place for one full sprint cycle
5. delete after confirming no active dispatches reference it

the ROUTING.md deprecation notice is the public signal. the description prefix is the safeguard for any automated dispatch that reads the agent list before checking ROUTING.md.

## results

| metric                | before (monolithic)                                         | after (domain split)                           |
| --------------------- | ----------------------------------------------------------- | ---------------------------------------------- |
| agent definition size | >5KB, growing                                               | ~2-3KB per successor, stable                   |
| cross-domain edits    | frequent — agent touches files it half-understands          | eliminated — each agent owns its domain        |
| concurrent dispatch   | risky — same agent dispatched twice creates race conditions | safe — different agents with file-locking      |
| routing clarity       | implicit — entropy guesses                                  | explicit — ROUTING.md is the dispatch contract |

## adoption checklist

sequential procedure — do these in order:

1. confirm the split threshold: agent definition > 5KB, or cross-domain file edits, or conflicting tool needs
2. identify the domain boundary — use the agent's narrowing section as the split line
3. draft successor slugs using the `hs-shannon-theseus-<project>-<domain>-<role>` pattern — verify they are self-describing
4. create each successor agent `.md` in `.claude/agents/` with role, context files, expertise, out-of-scope section, and narrowing
5. run each successor through `hs-shannon-theseus-stratia-shannon-auditor` before proceeding
6. write or update `.claude/agents/ROUTING.md` with explicit file-path dispatch rules for each successor
7. add a cross-cutting section to ROUTING.md if the domains share any files or message contracts
8. mark the original agent deprecated in ROUTING.md and prefix its description
9. validate ROUTING.md is readable end-to-end by someone unfamiliar with the project
10. delete the original agent after one sprint cycle with no active dispatches

## reference implementation

- repo: `chasko-labs/chrome-extension-moodle-uploader`
- original agent: `hs-shannon-theseus-chrome-developer` (deprecated)
- successor agents: `hs-shannon-theseus-chrome-extension-service-worker-runtime`, `hs-shannon-theseus-chrome-extension-sidepanel-ui`
- routing file: `.claude/agents/ROUTING.md`
- file-lock tooling: `.claude/agent-tooling/file-lock-tools.md` — valkey-backed distributed locks, MCP tool semantics
