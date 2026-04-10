# RISEN institutional playbook for heraldstack

this playbook institutionalizes RISEN as the default contract format for new custom agents, configuration updates, and sprint-planning delegation behavior.

primary references:

https://www.anthropic.com/engineering/harness-design-long-running-apps
https://communityresources.service-now.com/ai
https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects
https://github.blog/changelog/2025-04-09-evolving-github-issues-and-projects/
https://www.scrum.org/resources/implementing-scrum-github-projects

## RISEN contract

R role defines who the entity is and what expertise lens it must apply.

I instructions define the mission for the current scope.

S steps define execution order and checkpoints.

E expectation defines the output schema required by downstream agents.

N narrowing defines exclusions, constraints, and escalation boundaries.

## heraldstack role mapping

HARALD role contract: orchestration continuity, model-aware routing, sprint-goal arbitration.

Stratia role contract: planning quality, strategy validation, acceptance-criteria fitness.

Orin role contract: github execution correctness, traceability, and workflow hygiene.

Solan/Myrren role contract: research and foresight for uncertain domains.

Liora/Kade Vox role contract: creative divergence and execution momentum when throughput stalls.

Ellow role contract: communication quality and team-safety diagnostics.

## system prompt template for new custom agents

Role: define entity specialization, operating context, and authority boundaries.

Instructions: define concrete mission and success target for this run.

Steps: define ordered phases from intake to final handoff.

Expectation: define strict response schema, required sections, artifacts, and scoring fields.

Narrowing: define forbidden actions, off-scope topics, resource limits, and escalation triggers.

## sprint planning allocation contract

harald planner variant must generate a RISEN contract for each assigned sprint chunk before dispatch.

allocation to any entity must include expected artifact path, done criteria, and evaluator pass threshold.

if confidence is below 7/10, planner must emit a revised RISEN contract with narrower scope and explicit unblock path.

## model awareness contract

before dispatching planning work, HARALD must publish available model inventory and intended fit-for-purpose routing.

routing choices should optimize for delivery speed, quality threshold, and token efficiency rather than defaulting to highest-cost models.

each sprint planning brief should include a model-selection rationale block to make routing decisions auditable.

## repo policy hooks

new entity sheets should include a RISEN block or link to a RISEN contract template.

new automation or mcp integrations should declare expected output schema in expectation form and forbidden behaviors in narrowing form.

pull request templates should capture RISEN alignment checks for role fit, step coverage, expectation fidelity, and narrowing compliance.


promotion schema and issue-form controls are defined in `specs/promotion-criteria.schema.json` and `.github/ISSUE_TEMPLATE/feed_signal.yml`.

project field and webhook contracts are defined in `.github/config/project-fields.json` and `.github/config/webhook-events.json`.
