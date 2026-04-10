# worktree isolation scope pattern

an agent with `isolation: worktree` in its frontmatter binds to the git repository that defines it. it cannot operate on git state in sibling repositories. cross-repo git ops must run inline via bash, never via dispatch to the worktree-isolated agent

## problem

claude code subagents can declare `isolation: worktree` to carve a temporary git worktree on dispatch. this is the right default for a code-writing agent — changes land in an isolated branch, the parent session is never contaminated, and the WorktreeCreate hook can log or validate the branch name before the agent touches anything

the hidden coupling: the worktree is carved from the repo that defines the agent file. if orin lives at `~/code/repo-a/.claude/agents/orin.md` with `isolation: worktree`, dispatching orin to commit files in `~/code/repo-b/` will fail. the WorktreeCreate hook fires against repo-a's git state, observes the cwd is outside repo-a, and rejects the dispatch with `no successful output from hook`. the worktree cannot span repos

this is not a bug — it is the correct isolation behavior. worktree isolation exists precisely so one agent cannot mutate another repo's history. but it catches operators by surprise the first time they try to use a "universal git ops agent" across a multi-repo monorepo-of-repos like heraldstack

## symptoms

- dispatching the agent returns a WorktreeCreate hook failure immediately, before the agent's own instructions run
- the hook log shows the cwd does not match the expected worktree parent
- retrying the same dispatch produces identical failure — this is not a transient
- git state in the target repo is untouched, as expected

## resolution

for git operations in any repo other than the one defining the worktree-isolated agent, run git + gh commands directly via bash from the primary session. do not retry the dispatch

```
# wrong — orin defined in shannon cannot operate on heraldstack-infra
Agent(subagent_type="hs-shannon-theseus-orin-github-ops", prompt="commit X in heraldstack-infra")

# right — primary session runs git inline for cross-repo work
cd ~/code/heraldstack/heraldstack-infra
git add ...
git commit -m "..."
git push
gh pr create ...
```

when a persistent "always use orin for git ops" rule exists in CLAUDE.md, scope it explicitly: orin is authoritative within its defining repo, inline bash is authoritative elsewhere. do not let the rule override the technical constraint

## follow-up options

three viable fixes if cross-repo agent dispatch becomes a frequent need:

- drop `isolation: worktree` from the agent definition so it runs in the parent cwd. loses the isolation guarantee but enables cross-repo ops
- introduce a sibling agent variant per target repo, each with its own worktree binding. higher maintenance but preserves isolation
- promote git ops to a tool-based mcp server that runs outside any worktree and accepts `--repo` as an argument. cleanest long-term but requires server work

until one of those ships, inline bash from the primary session is the only path for cross-repo git state mutation

## logging the limitation

when this limitation blocks work, log the attempt and the fallback in session notes or auto-memory so the next session does not repeat the mistake. a feedback-type memory with the agent slug, the failure mode, and the inline alternative is sufficient. do not retry the same dispatch — diagnose, log, switch to inline

## applicability

observed in shannon (claude code cli) with orin-github-ops. the same constraint applies to any agent in any collective that declares worktree isolation: haunting ghosts, gander profiles with worktree sandboxes, ibeji agents if they gain equivalent hooks. the principle generalizes: isolation scope binds to the declaration site, not the task site
