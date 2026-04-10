# heraldstack character sheets

this directory separates persistent character entities from agent-cli designations.

character entities are long-lived role identities used by product orchestration and persona-based dispatch.

agent-cli designations are platform-local names for running heraldstack on specific tools and should not be treated as character entities.

registry index: `entity-registry.json`. the index lists core character entities only — platform-level subagent definitions live in their respective collective repositories and are the authoritative runtime contracts.

current entities in the index: harald, stratia, myrren, liora, kade vox, solan, ellow, orin, kerouac, voss, tarn, ralph wiggum, scribe, hcom, arion, nyxen. the roster will continue to grow as additional character entities are added.

character sheets should include or link a risen contract for role, instructions, steps, expectation, and narrowing.

## core persona vs platform variant

a character entity is the persistent soul: who the persona is, what their natural role is, what triggers they respond to. a variant is a specific deployment of that soul in an agent-type, domain, and role on a particular platform.

the slug pattern is:

```
<agent-type>-<persona>-<domain>-<role>
```

one character can anchor many variants across collectives. the character sheet in this directory describes who the persona is — the slug in each collective's repository describes what a given variant does.

this split matters because the same persona can appear in multiple collectives with different duties. for example, a single character may anchor a research variant in one collective and a validation variant in another. the character sheet captures identity once; the variants capture duty per deployment.

character sheets in this directory should stay focused on the core persona. variant-specific duties, tooling, and responsibilities belong in the collective-level definitions, not here.
