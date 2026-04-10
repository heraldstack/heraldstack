# adr-0001: persona library split — identity here, duty in collective repos

date: 2026-04-10
status: accepted

## context

the heraldstack runs agent variants across multiple cli platforms (claude code, kiro, goose, gemini cli, copilot). prior to this decision, persona identity (pronouns, marvel ai reference, origin, voice) was duplicated inline in every variant definition file across every collective repo. when we added a new collective or updated a persona's voice, 25+ files needed to change in sync.

## decision

canonical character identity lives in `personas/<id>.md` at the root of github.com/heraldstack/heraldstack. variant duty lives in the collective repo alongside the agent definition (e.g. `shannon-claude-code-cli/.claude/agents/hs-shannon-theseus-ellow-scrum-mentor.md`).

collective agent files reference the canonical persona by url and scope only their variant-specific duty, tools, and narrowing constraints.

## consequences

**positive**

- single source of truth for persona identity across all collectives
- voice and reading list updates happen once, propagate everywhere
- new collectives can add variants without duplicating character data
- public repo makes identity shareable and auditable

**negative**

- claude code and similar tools load agent files locally at dispatch — the canonical reference is documentation, not runtime fetch. prompt caching handles the runtime dedup
- split introduces a mental model shift: who vs what
- variant files now carry a url that must stay valid (mitigated by repo stability and adr-0002 slug discipline)

## alternatives considered

- **mcp-served personas (query at dispatch)** — adds infrastructure, gains nothing over prompt caching for claude code specifically
- **git submodule** — too much ceremony for an identity library, breaks the "pull one repo" assumption for agent workers
- **inline duplication (status quo)** — maintenance burden grows quadratically with collectives × personas

## references

- [personas/README.md](../../personas/README.md) — canonical library structure
- adr-0002 — slug standard that makes this split unambiguous
