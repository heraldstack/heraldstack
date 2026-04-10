# heraldstack harness charter for long-running delivery

this charter institutionalizes high-level operating behavior for long-running autonomous development in heraldstack.

external research reference that informed this charter: https://www.anthropic.com/engineering/harness-design-long-running-apps

RISEN institutional reference: `docs/risen-framework-playbook.md`.

## harness architecture using heraldstack entities

HARALD owns orchestration continuity, sprint framing, and final decision arbitration.

Stratia owns strategic planning quality, sprint contract clarity, and acceptance criteria integrity.

Orin owns github execution mechanics, issue and pull request traceability, and workflow-state hygiene.

Solan and Myrren provide research and foresight signals when scope risk or architectural uncertainty is high.

Liora and Kade Vox can be dispatched when product creativity or execution momentum is the bottleneck.

Ellow is dispatched when communication quality, team trust, or feedback quality becomes a limiting factor.

## institutional behavior rules

the builder and evaluator must be separated. no work item is self-approved by the same entity that implemented it.

every sprint chunk must start with a sprint contract that defines scope, testable behaviors, and done criteria before coding begins.

every sprint chunk must end with evaluator scoring against explicit thresholds. failed thresholds must return to implementation with concrete feedback.

long sessions must use structured handoff artifacts so continuation does not depend on raw chat history alone.

context management is policy-driven. use compaction by default and context resets when coherence or quality drifts.

## repository-level artifacts

this repository should treat artifacts as first-class process controls.

planning artifact path: `specs/<sprint-id>/plan.md`

contract artifact path: `specs/<sprint-id>/contracts/<chunk-id>.md`

evaluation artifact path: `specs/<sprint-id>/evaluations/<chunk-id>.md`

handoff artifact path: `specs/<sprint-id>/handoffs/<chunk-id>.md`

retro artifact path: `specs/<sprint-id>/retro.md`

## github behavior contract

each sprint chunk maps to a github issue and a pull request with linked artifact references.

blocked items must include impediment class and owner for unblock action.

merge readiness requires done criteria evidence and evaluator pass confirmation.

review quality is measured by defect escape, rework rate, and time-to-accept.

## learning loop contract

each sprint contributes actionable learning into `docs/agile-software-development-resources.json` only when evidence is reproducible and backlog-relevant.

learning capture must include source, observation, decision impact, and proposed action.

this charter is high-level by design. implementation details belong in entity sheets, sprint specs, and integration repositories.


## risen enforcement baseline

RISEN contract fields are required for planning and execution prompts used by heraldstack entities.

missing role, expectation, or narrowing fields should be treated as invalid prompt contracts and returned for correction before dispatch.

HARALD must include model-awareness metadata in planning handoffs so planner variants can route by capability, latency, and token efficiency.
