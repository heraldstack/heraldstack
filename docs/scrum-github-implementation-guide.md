# heraldstack scrum implementation guide for git, github, orgs, and apps

this guide operationalizes scrum for heraldstack using github-native execution. it keeps README lightweight and keeps detailed mechanics here.

resource manifest: `docs/agile-software-development-resources.json`.
charter: `docs/heraldstack-harness-charter.md`.
trend decomposition: `docs/trends-2026-decomposition.md`.
ux standards: `docs/user-research-and-ux-standards.md`.

## source references

agile manifesto: https://agilemanifesto.org/
scrum guide: https://scrumguides.org/scrum-guide.html
github issues: https://docs.github.com/issues
github projects: https://docs.github.com/issues/planning-and-tracking-with-projects
github pull requests: https://docs.github.com/pull-requests
github actions: https://docs.github.com/actions
github apps: https://docs.github.com/apps
github webhooks: https://docs.github.com/webhooks
github organizations: https://docs.github.com/organizations

## role model and language

use scrum mentor as the facilitation role name in all heraldstack materials and automation labels. the scrum mentor facilitates events, coaches self-management, surfaces impediments, and helps teams and product owner improve flow without becoming a task owner.

harald-core acts as orchestrator and product owner function. planner variant is sprint-planning only. sprint execution remains under harald-core orchestration.

character entities and agent-cli designations are different identity classes. use `docs/character-sheets/entity-registry.json` as the taxonomy source of truth.

## scrum cadence mapped to github

sprint planning starts from a seed todo list and open github backlog. planning output is a sprint goal, a decomposed backlog, explicit definition-of-done notes, and per-agent confidence ratings.

each backlog item should map to a github issue with acceptance criteria and risk notes. sprint assignment should use github projects iteration fields with explicit status columns and blocked reasons.

if any assigned agent confidence is below 7/10, create an impediment issue tagged `impediment` and resolve with one of four intervention types: knowledge, tooling, mcp access, or dispatch to a better-fit agent.

during sprint execution, every work unit must have a linked issue and pull request. agents post an "on it" claim before touching high-collision surfaces, then post a follow-up intent note describing findings and next action.

sprint review is demo-driven and artifact-backed. each done issue must map to a merged pull request, demo note, and measurable outcome signal.

retrospective is team-only and scrum-mentor facilitated. product owner and stakeholder perspectives are reviewed through artifacts, but psychological safety of retrospective discussion remains team-internal.

## git and pull request workflow

branch naming convention should encode sprint and issue identity, for example `sprint-24/issue-318-agent-orin`.

pull request templates should capture summary, done criteria check, risk/rollback note, telemetry note, follow-up backlog suggestions, RISEN alignment fields, and joint attribution checks. see `.github/pull_request_template.md`.

required status checks should include formatting/linting, unit/integration tests where relevant, security scan, and policy checks.

squash merges keep history concise for high-volume autonomous contribution. keep issue linkage in pull request body for traceability.

## github organization operating model

organization-level standards should define repository defaults for branch protection, required reviews, codeowners, issue templates, pull request templates, and secret handling.

projects should be organization-wide where cross-repository coordination is needed. issue forms should include sprint relevance, confidence input, impediment class, and expected demo evidence.

use labels to encode workflow primitives: `sprint`, `impediment`, `confidence-low`, `needs-mentor`, `needs-mcp`, `demo-ready`, `retro-input`.

use milestones or project iterations as sprint boundary objects. keep sprint scope immutable after planning except for production incidents and explicitly approved swap-ins.

## github apps and automation patterns

github app responsibilities for heraldstack should include event intake, policy evaluation, orchestration triggers, and audit trace capture.

a github app can subscribe to issue_comment, issues, pull_request, pull_request_review, check_suite, and workflow_run events to coordinate dispatch and learning capture.

recommended app actions include automatic issue-to-project routing, low-confidence escalation comments, definition-of-done checks, retrospective note harvesting, and impediment dashboard updates.

all app mutations should log correlation identifiers that map github events to otel trace ids for full observability.

## mcp integration blueprint

rss and changelog inputs should flow into a learning queue, then into vector memory and sprint intel briefing context.

github backlog sync mcp should convert approved learning items into issue drafts tagged by domain and urgency.

sprint intel brief mcp should summarize open risk clusters, blocked durations, confidence trends, and dependency shifts before each planning session.

## measurement model

primary sprint metrics should include throughput, cycle time, blocked time, review latency, escaped defect rate, and confidence delta.

secondary efficiency metrics can include model/token efficiency, parallel dispatch breadth, mcp call success, and trace completeness.

forecasting should remain empirical. prediction quality is considered reliable only after at least 12 comparable sprints on similar stacks and team composition.

## agile learning ingestion targets

scrum.org blog rss: https://www.scrum.org/resources/blog/rss.xml
less blog feed: https://less.works/blog/feed.xml
infoq feed endpoint: https://feed.infoq.com/
github changelog: https://github.blog/changelog/
github releases atom pattern: https://github.com/<owner>/<repo>/releases.atom

store source url, retrieval timestamp, relevance tags, and extracted action proposals with each ingested item. promote to backlog only when linked to product goals or clear impediment removal.


## risen-guided planning and dispatch

all sprint planning allocations should be emitted as RISEN contracts to ensure consistent role boundaries, procedural steps, required output schema, and explicit constraints.

planner dispatch payloads should include model inventory visibility so assigned entities know available models and intended use cases.

model routing should prioritize time-to-market, outcome quality, and token efficiency with rationale captured in planning artifacts.


## feed signal governance and issue promotion

standard process references: `specs/ingestion-pipeline-spec.md`, `specs/promotion-criteria.schema.json`, `.github/ISSUE_TEMPLATE/feed_signal.yml`, `.github/config/project-fields.json`, `.github/config/check-gates.md`, `.github/config/webhook-events.json`.

state transitions should be enforced via labels and project field sync for captured, triaged, promoted, scheduled, completed, and archived states.

joint attribution policy requires both bryanchasko and heraldstack on feed-promoted work items in chasko-labs.

## user research and usability standards integration

for ux-impacting backlog items, include user-research method tag and evidence summary before scheduling work.

preferred methods are interview, survey, usability-test, heuristic-review, analytics-trace, field-observation, and comparative-benchmark.

review and retrospective artifacts should include measured experience outcomes and one process improvement candidate for the next sprint.
