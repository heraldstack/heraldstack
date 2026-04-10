# check gate baseline

required checks for protected branches:

`docs-schema-validate`

`issue-state-label-gate`

`attribution-gate`

`risen-contract-gate`

`tests` where code changes exist.

`security` where dependency or runtime changes exist.

## attribution gate policy

issues and pull requests tied to heraldstack delivery should include both `bryanchasko` and `heraldstack` attribution markers.

review contexts should include bryanchasko availability for harald/myrren/stratia review lanes.

orin-driven execution lanes should prefer heraldstack operator attribution while preserving joint attribution record.


## 2026 hardening additions

action workflows should pin third-party actions by commit sha and keep permissions minimal by default.

workflow changes should align with `.github/config/actions-security-baseline.yml` for oidc, runner version, and artifact controls.

issue forms and promotion flow should retain evidence links to support auditability and downstream evaluation quality.
