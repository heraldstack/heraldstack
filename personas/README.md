# personas

canonical persona library for the heraldstack. each file is one character entity — who the persona is, how they sound, what they study. variant duty (what a persona does in a specific collective, tier, and role) lives in the collective repo alongside the agent definition.

## structure

each persona file uses yaml frontmatter + markdown body:

```yaml
---
id: <slug>
display_name: <human name>
pronouns: <he/him | she/her | they/them | —>
marvel_ai: <reference or —>
origin: <city or —>
birthdate: <yyyy-mm-dd or —>
core_role: <one-line description>
studies: [optional reading list / intellectual lineage]
voice: <one-line voice description>
triggers: [dispatch keywords]
variants: [list of collective + slug + domain]
---
```

## slug standard

variant slugs follow `hs-<collective>-<tier>-<persona>-<role>`

- collectives: shannon, haunting, gander, ibeji, splintercells, squad
- tiers per collective: shannon uses entropy/theseus; haunting uses poltergeist/ghost; gander uses profile
- persona: lowercase id from registry
- role: hyphenated role slug

example: `hs-shannon-theseus-ellow-scrum-mentor`

## access channels

agents should query canonical persona data via whichever channel has least friction:

| channel | use when |
|---|---|
| mcp `qdrant-shared-knowledge` | in-session lookup by id, embedded similarity search |
| filesystem (microvm) | firecracker microvm with read-only mount at `/srv/heraldstack` |
| github raw url | ci workflows, one-off fetches, no clone needed |
| `gh repo clone heraldstack/heraldstack` | interactive agent workers on a dev host |

assumed reader identity: bryanchasko or chasko-labs-linked worker with github mcp access

## registry

see [registry.json](registry.json) for the machine-readable index
