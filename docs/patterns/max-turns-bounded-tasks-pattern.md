# maxturns bounded tasks pattern

set an explicit `maxTurns` on any agent whose task has a known completion boundary.

## problem

an agent without a `maxTurns` ceiling will continue until it decides it is done, hits a context limit, or enters a loop. for agents with open-ended research tasks, this is appropriate — stopping too early loses value. for agents with bounded, verifiable tasks (file a PR, run a validation, scan a directory), an unbounded run is a risk: loop states persist, token costs accumulate, and the entropy anchor gets no signal that something went wrong.

a bounded agent that hits `maxTurns` surfaces as a failed run with a clear count. an unbounded agent that loops surfaces as a timeout or a confusing partial result.

## pattern

assess task boundedness before setting the field:

| task type                                           | maxTurns | rationale                                                |
| --------------------------------------------------- | -------- | -------------------------------------------------------- |
| single git operation (commit, PR, branch)           | 20–40    | four to eight tool calls per step, bounded by repo state |
| file audit / scan (read-only pass over known scope) | 15–25    | bounded by file count, not open-ended                    |
| schema validation                                   | 10–15    | deterministic, few steps                                 |
| UX test session (multi-step automation)             | 40–60    | bounded by test script steps, not research depth         |
| deep research or open-ended synthesis               | omit     | value scales with depth; early cutoff loses signal       |
| session anchor / orchestrator                       | omit     | must remain alive for the full session                   |

### Claude Code format

in a theseus agent definition (`.claude/agents/*.md` frontmatter):

```yaml
---
name: hs-shannon-theseus-orin-github-ops
model: claude-sonnet-4-6
maxTurns: 40
---
```

### kiro-cli format

kiro does not expose a `maxTurns` field in agent JSON. bounded execution in kiro is enforced by the DUTIES contract (`DUTIES.md` exit conditions) and the poltergeist anchor's supervision pattern.

## calibration notes

- `maxTurns` counts agent turns (model responses), not tool calls. a single turn can contain multiple tool calls.
- set it 20–30% above the expected turn count for the happy path. too tight causes spurious failures on minor detours; too loose defeats the purpose.
- after a `maxTurns` failure, check the transcript for loop patterns before raising the ceiling — the limit often surfaces a real problem.

## applied across the heraldstack

| repo                             | agent                                           | maxTurns |
| -------------------------------- | ----------------------------------------------- | -------- |
| shannon-claude-code-cli          | hs-shannon-theseus-orin-github-ops              | 40       |
| ux-testing-moodle-uploader       | hs-shannon-theseus-liora-ux-field-tester        | 60       |
| ux-testing-moodle-uploader       | hs-shannon-theseus-stratia-ux-reviewer          | 20       |
| chrome-extension-moodle-uploader | hs-shannon-theseus-orin-github-ops (ux variant) | 40       |

## reference

- source pattern: shannon audit (2026-04-11), propagated to ux-testing PR #14, chrome-extension PR #503
