# harness design gap analysis

gap analysis between anthropic's "harness design for long-running application development" (2026-03-24) and shannon collective operations. triggered by the 2026-04-07 mac mini UX test session: 6 scenarios, 17 bugs, D+ agentic UX grade, two P0 blockers (#292, #297)

---

## what the blog describes

a three-role harness: planner, generator, evaluator. the planner decomposes goals. the generator writes code. the evaluator interacts with the running application — not the code — to verify behavior. the evaluator uses browser tools (playwright, chrome devtools) to click through the product as a user would

key evolution: v1 harness had detailed sprint plans and structured handoffs. v2 removed sprint decomposition entirely because newer models (opus-class) handled it natively. the blog frames every harness component as "an assumption about what the model can't do on its own" — and says to audit those assumptions as model capability grows

---

## what shannon does well

**planner/generator/evaluator separation exists**

- harald plans, hs-shannon-theseus-\* agents build, stratia reviews
- this maps directly to the blog's three-role architecture

**structured handoff artifacts**

- CONTEXT.md, SPRINT_BREAKDOWN.md, dispatch templates
- agents have explicit routing, not ad-hoc delegation

**evaluator-with-browser-tools precedent**

- the 2026-04-07 mac mini UX test used chrome-devtools MCP to interact with the live extension
- this IS the evaluator pattern the blog describes — it found 17 bugs that code review missed

---

## gaps

### evaluator reviews diffs, not the running app

stratia reads PR diffs. the blog's evaluator launches the app in a browser and clicks through it. diff review catches syntax errors and logic mismatches. it does not catch:

- state management bugs (Start Over button #297 — passed code review, didn't reset state)
- first-load failures (#292 — error on initial extension load)
- visual regressions, stuck states, dark mode contrast problems

both P0 blockers from the mac mini session should have been caught before reaching a user. stratia reading diffs will never catch them

### no sprint contracts

generator and evaluator do not negotiate testable "done" criteria before work starts. issues get filed, agents pick them up, PRs appear. no explicit contract on what "done" looks like for the evaluator to verify against

this is why bugs slip through — there is no shared definition of success between the agent that builds and the agent that reviews

### self-evaluation is broken

agents praise their own work. when the same session files UX issues and fixes them, it marks things done that are not done. the blog is explicit: generator and evaluator MUST be separate sessions with separate context. separate incentives prevent the generator from grading its own homework

### harness is too heavy

current ceremony:

- dispatch templates with branch names, PR bases, tool usage
- file-locking system with TTL
- file digests mapping source files to logical sections
- checkpoint system in valkey
- diagnostic cache in valkey
- hook enforcement topology

the blog says "every component encodes an assumption about what the model can't do on its own." the blog's v2 harness removed sprint decomposition because the newer model handled it natively. with opus 4.6, some of these components may be ceremony that costs more than it saves

candidates for audit:

- file digests — does opus 4.6 need pre-mapped line ranges, or can it navigate files on its own?
- checkpoint system — does the model benefit from explicit checkpoints, or does git history suffice?
- dispatch templates — do agents need branch names and tool usage pre-specified, or can they figure that out?
- sprint decomposition — the blog removed this entirely in v2

### planner over-specifies

SPRINT_BREAKDOWN.md and dispatch templates specify file paths and line numbers. when the planner is wrong about implementation paths, those errors cascade into every agent that reads the plan. the blog recommends the planner stay high-level — describe outcomes, not file edits. let agents figure out implementation paths with their own tool calls

### evaluator lacks skepticism prompting

out-of-the-box claude is a poor QA agent. the blog observes that it identifies issues then talks itself out of them. stratia needs explicit prompting that penalizes leniency — the same way the blog's design evaluator penalized generic AI patterns. without this, stratia defaults to approval

---

## action items

- wire chrome-devtools MCP into stratia's eval loop — interact with running extension, not diffs alone
- add sprint contracts: before each batch, generator and evaluator agree on testable "done" criteria
- separate generation from evaluation sessions — different context, different agent, different incentives
- audit agent tooling infrastructure (sprints 1-3) for what is still load-bearing vs ceremony on opus 4.6
- add explicit skepticism prompting to stratia's agent definition — penalize leniency, require evidence for approval
- treat the D+ UX grade as the baseline. the next UX test pass is the measure of whether these changes work

---

## evidence log

**2026-04-07 mac mini UX test**

- 6 scenarios tested against live extension
- 17 bugs filed
- 2 P0 blockers: #292 (error on first load), #297 (Start Over broken)
- D+ agentic UX grade
- test used chrome-devtools MCP — proving the evaluator-with-browser-tools pattern works
- neither P0 was caught by stratia's diff-based review process
