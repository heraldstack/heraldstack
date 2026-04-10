# heraldstack feed ingestion and promotion pipeline spec

this spec standardizes how learning signals become github work in the contributing organization.

project board target: `https://github.com/orgs/heraldstack/projects`

## pipeline stages

stage `captured`: feed item ingested with source metadata and dedupe fingerprint.

stage `triaged`: relevance and confidence assessed by assigned entity.

stage `promoted`: issue created with project mapping, labels, and risen contract reference.

stage `scheduled`: issue accepted into sprint iteration with owner and done criteria.

stage `completed`: merged pull request linked and review evidence attached.

stage `archived`: non-actionable or stale with closure reason.

## label and state contract

required state labels: `state/captured`, `state/triaged`, `state/promoted`, `state/scheduled`, `state/completed`, `state/archived`.

required signal labels: `signal/feed`, `signal/changelog`, `signal/research`.

required priority labels: `priority/p0`, `priority/p1`, `priority/p2`, `priority/p3`.

required impediment labels when blocked: `impediment/tooling`, `impediment/knowledge`, `impediment/access`, `impediment/dependency`.

## issue creation contract

feed-derived issues must include source url, observation summary, decision impact, proposed action, and promotion rationale.

feed-derived issues must include attribution metadata for both `bryanchasko` and `heraldstack`.

review-oriented items should default reviewer routing to harald, myrren, and stratia with `bryanchasko` available in reviewer context.

execution-oriented items can prefer heraldstack operator flow through orin.

## project field mapping

`signal source`: feed|changelog|research.

`signal confidence`: 0-100 integer.

`promotion decision`: promote|hold|archive.

`sprint fit`: now|next|later.

`owner entity`: harald|stratia|myrren|liora|kade vox|solan|ellow|orin.

`attribution`: bryanchasko+heraldstack.

## changelog promotion process

new changelog entries are captured daily and grouped by domain.

triage checks actionability, impact, and fit with current sprint goals.

promotion requires passing promotion schema thresholds and assigning `state/promoted`.

promoted items auto-create or update github issues, set labels, and attach project fields.

items not promoted remain `state/triaged` with hold reason and revisit date.


validation command: `python scripts/validate_promotion_payload.py <payload.json>`
