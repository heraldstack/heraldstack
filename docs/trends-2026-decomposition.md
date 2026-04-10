# 2026 trends decomposition and heraldstack improvements

this document captures 2026-priority shifts and how this repository now decomposes them into standards.

## trend: stronger github projects + issues as planning substrate

decomposition: feed-to-issue promotion now uses explicit state labels, project field mapping, and promotion schema gating.

repo implementation: `specs/ingestion-pipeline-spec.md`, `specs/promotion-criteria.schema.json`, `.github/config/project-fields.json`.

## trend: higher governance demands for automation trust

decomposition: webhook handler contract and check-gate policy are treated as first-class control-plane docs.

repo implementation: `.github/config/webhook-events.json`, `.github/config/check-gates.md`, `.github/workflows/docs-schema-validate.yml`.

## trend: security hardening for actions and runners

decomposition: define an actions security baseline with oidc, runner minimums, and review constraints.

repo implementation: `.github/config/actions-security-baseline.yml` and workflow checks.

## trend: structured agent prompt contracts for reliability

decomposition: risen fields become default planning and dispatch contract, including role boundaries and explicit narrowing.

repo implementation: `docs/risen-framework-playbook.md`, `docs/heraldstack-harness-charter.md`, `docs/scrum-github-implementation-guide.md`.

## trend: better evidence traceability for issue triage

decomposition: issue-form captures evidence links for audit, promotion validation, and reviewer confidence.

repo implementation: `.github/ISSUE_TEMPLATE/feed_signal.yml` with evidence file field and joint attribution controls.

## trend: attribution and accountability in mixed human/agent workflows

decomposition: joint attribution policy normalized across schema, issue forms, gate docs, and promotion examples.

repo implementation: `specs/promotion-criteria.schema.json`, `.github/ISSUE_TEMPLATE/feed_signal.yml`, `.github/config/check-gates.md`, `specs/examples/`.

## next practical improvements

add a branch-protection setup script using the github api and the gate baseline in `.github/config/check-gates.md`.

add automated project-field sync checks against the contributing organization's project board through a github app or cli task.

add nightly validation for feed freshness and stale triage items with automatic `state/triaged` aging alerts.
