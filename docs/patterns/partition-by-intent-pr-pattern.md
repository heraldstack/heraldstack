# partition by intent pr pattern

when a branch accumulates unrelated dirty files, do not mash them into a single commit and do not discard them to get a clean tree. review each dirty file, group by intent, open one pr per intent. lose zero data, incorporate every useful change, leave no mess

## problem

long-lived local worktrees collect drift. a session that started as a typo fix on `main` ends up carrying an unrelated dependency bump, a stray debug print, a half-finished refactor, and a hook fix discovered mid-session. the naive options:

- **mash everything into one commit** — unreviewable pr, title cannot describe the changeset, reviewer cannot approve portions independently, revert is all-or-nothing
- **`git stash` + cherry-pick later** — stashes get forgotten, the useful work never resurfaces, the session effectively throws away innovation
- **`git checkout .` to get a clean tree** — straight up data loss, the operator discovers the loss a week later
- **stop-work and ask the human to sort it** — bureaucratic, the whole point of agent operators is to figure it out

none of those respect the two non-negotiables: do not lose data, do not leave messes

## resolution

partition the dirty tree by **intent**, not by **file type or directory**. each intent becomes one branch, one pr, one commit (or a small coherent commit series). the steps:

1. **inventory** — list every modified, added, and untracked file. `git status --short` plus a walk of untracked directories. write the list down explicitly; do not trust a mental model
2. **classify by intent** — for each file, write one phrase describing *why* it changed. "fix stdin in hook", "add chrome dockerfile", "rename agent slug". files with the same why go in the same bucket. a file with two reasons gets split (use `git add -p` or a scratch diff)
3. **order by dependency** — some intents block others. a hook fix that unblocks pre-commit must land before any pr that will trip that pre-commit. draw the dag, pick a valid order
4. **per intent: branch, stage, commit, push, pr** — create a named branch per intent (`fix/hook-stdin`, `feat/chrome-mcp`, `refactor/agent-slugs`), stage only the files in that bucket, commit with a message that names the intent, push, open the pr. tag reviewers per bucket
5. **validate each pr independently** — each pr must pass its own validation gate. a bucket that cannot validate alone is a sign the partition is wrong; re-bucket
6. **merge in dependency order** — unblocking prs first. if a later pr conflicts after an earlier merge, rebase, do not re-mash

## what counts as an intent

an intent is a one-phrase answer to "why did this change". good intents:

- "fix the autoformat stdin bug"
- "add chrome-devtools-mcp to infra"
- "rename theseus agents to the hs-slug standard"

bad intents (too broad, will produce an unreviewable pr):

- "cleanup"
- "refactor"
- "various fixes"

if the intent phrase has an "and" in it, split it

## what not to do

- do not let orin (or any commit agent) refuse to commit until the tree is clean — that creates a deadlock loop. the partition-by-intent workflow is the resolution, not a failure mode
- do not use `git stash --include-untracked` as a workaround. stashes are writeonce memory holes
- do not create a single pr with multiple commits each tagged with a different intent — that still requires a single approval on a mixed changeset. use separate prs
- do not skip the inventory step. working from memory loses files
- do not reorder intents for convenience. dependency order is load-bearing

## applicability

observed in shannon during a multi-repo refactor where three unrelated changes had accumulated on one local branch. applies to any collective that uses agent-driven commit workflows where the commit agent enforces a clean-scope policy. the pattern scales: four intents is still fine, ten is a smell that suggests the worktree should be reset and each intent rebuilt from scratch with smaller sessions

## related

- see dual-identity-pr-pattern.md for how to route each partitioned pr through the commit/review identity split
- see hook-governance-pattern.md for why a commit agent rejecting a mixed-intent commit is desirable behavior, not a bug
