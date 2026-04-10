# adr-0002: slug standard — hs-<collective>-<tier>-<persona>-<role>

date: 2026-04-10
status: accepted

## context

the heraldstack previously used inconsistent slug patterns across collectives:

- shannon: `theseus-<persona>-<role>` (e.g. `theseus-orin-github-ops`)
- haunting: `<tier>-<persona>-<domain>-<role>` (e.g. `poltergeist-harald-core-anchor`)
- gander: profile names without a clear tier marker

agents crossing collective boundaries had to learn multiple naming conventions. searching for "all ellow variants" required grepping different patterns per repo.

## decision

all heraldstack agent variants use the slug pattern:

```
hs-<collective>-<tier>-<persona>-<role>
```

**components**

- `hs-` — literal prefix, signals heraldstack ownership and keeps the repo namespace identifiable in search results
- `<collective>` — shannon, haunting, gander, ibeji, splintercells, mujallad, squadron
- `<tier>` — role level within the collective
  - shannon: entropy (primary session), theseus (subagent)
  - haunting: poltergeist (primary orchestrator), ghost (discrete subagent)
  - gander: profile (goose profile)
  - mujallad: codex-cli profile
  - squadron: subagent configs (brady gaster pattern)
  - ibeji, splintercells: tbd
- `<persona>` — lowercase character id from `personas/registry.json`
- `<role>` — hyphenated role slug (e.g. `github-ops`, `scrum-mentor`, `technical-writer`)

**examples**

- `hs-shannon-theseus-orin-github-ops`
- `hs-shannon-theseus-ellow-scrum-mentor`
- `hs-shannon-theseus-harald-product-owner`
- `hs-shannon-entropy-harald-core-anchor`
- `hs-haunting-poltergeist-harald-core-anchor`
- `hs-gander-profile-harald-session`

## consequences

**positive**

- one grep pattern finds all variants of a persona across all repos: `hs-*-*-ellow-*`
- collective and tier are first-class filterable components
- hs- prefix is portable across external indexes and llms.txt

**negative**

- requires a one-time rename across all existing agent files (25 in shannon, TBD in haunting and gander)
- longer slugs
- external references to old slugs break — mitigated by redirect notes in collective repo CHANGELOGs

## migration

- shannon: pr-b of the canonical persona refactor renames all `.claude/agents/*.md`
- haunting: follow-up pr renames `agents/*` directories
- gander: follow-up pr renames goose profiles

## references

- [personas/registry.json](../../personas/registry.json) — canonical persona ids
- [personas/README.md](../../personas/README.md) — slug standard in context
- adr-0001 — persona library split that this standard enables
