# heraldstack user research and ux standards

this document adds user-research and usability standards to heraldstack delivery governance without changing the lightweight readme style.

## intent

heraldstack planning and execution should include explicit user-research evidence before promoting experience changes into sprint commitments. standards in this file complement scrum, risen, and feed-signal promotion artifacts.

## external standards references

harvard enterprise architecture user research methods and recommendations: https://enterprisearchitecture.harvard.edu/user-research-methods-and-recommendations

stanford experience standards: https://improvement.stanford.edu/resources/experience-standards

stanford usability principles: https://improvement.stanford.edu/resources/usability-principles

stanford 5 steps for better user experience: https://itcommunity.stanford.edu/unconference/sessions/2021/5-steps-start-providing-great-user-experience

mit ocw 6.831 lecture notes and course context: https://ocw.mit.edu/courses/6-831-user-interface-design-and-implementation-spring-2011/pages/lecture-notes/

mit ux learning resource path: https://next.learn.mit.edu/c/topic/arvrmrxr?resource=3857

## operational standards for heraldstack

all backlog proposals that modify user flows should include a user-research method tag and evidence summary.

accepted method tags are interview, survey, usability-test, heuristic-review, analytics-trace, field-observation, and comparative-benchmark.

all pull requests with experience impact should include before-state and after-state acceptance criteria tied to explicit usability outcomes.

all sprint reviews should include a user-experience evidence segment with artifacts linked in issue comments or pr bodies.

retrospectives should capture one user-experience process improvement candidate and one measurement-improvement candidate each sprint.

## required sprint artifacts for ux-sensitive work

planning artifact must include user problem statement, user segment, method selection, sample size target, and expected confidence threshold.

execution artifact must include data capture source, date range, limitation notes, and synthesis summary.

review artifact must include what changed, what improved, what regressed, and what should be tested next sprint.

## promotion gate alignment

when a feed signal proposes ux or workflow change, the issue form should capture method selection and evidence link before promotion to scheduled state.

promotion quality should prefer direct user evidence over proxy opinion when both are available.

## attribution alignment

ux and research artifacts produced in this repository follow joint attribution policy for bryanchasko and heraldstack where promotion governance requires both identities.
