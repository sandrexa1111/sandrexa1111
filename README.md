# sandromosi

AI systems and agent infrastructure. Mostly interested in the unglamorous parts:
state, determinism, evaluation, and what happens when an agent fails.

## Current focus

**Agent infrastructure.** If agents are going to be long-lived software, they
need the things ordinary software already has — a way to snapshot state, move it,
branch it, diff it, and verify it. Most of that does not exist yet.

**Governance and evidence for AI-initiated actions.** Deterministic decisions,
reviewer disposition, source-of-record read-back, signed proof. This is my
day-to-day work at ThreatVeil and it is not public.

**Evaluation over demos.** A system that can only be judged by watching it work
is a system nobody can trust at scale.

## Selected work

### [continuum-agent](https://github.com/sandrexa1111/continuum-agent)

Checkpoint a running AI agent, move it somewhere else, and continue.

A portable, content-addressed representation of agent execution state, with a
verified container format, cheap forking through structural sharing, and a
migration report that names every piece of state that does *not* survive a move
instead of dropping it quietly.

The interesting part is not the agent angle. Strip the words "AI" and "agent"
out and what is left is a content-addressed object store, a canonical
serialization with a versioned schema, a self-verifying archive format, and a
secret scanner — ordinary systems engineering, and all of it deterministic.
The reference runtime deliberately uses no model, so the test suite is
reproducible and the whole thing is evaluable offline.

`Python · zero runtime dependencies · 243 tests · strict mypy · CI on 4 Python versions × 3 OSes`

## Elsewhere

Most of my substantial work is in private repositories — a governance control
plane for AI-initiated changes to enterprise systems of record (FastAPI,
Next.js, Postgres, GCP, signed evidence export). The public repositories here
are a mix: some early learning work, some client frontends. I have not deleted
them.

## Stack

Python · TypeScript · FastAPI · Postgres · Docker · pytest · GitHub Actions

Comfortable in the parts that are less fun: serialization formats, schema
migration, failure modes, and writing down why a decision was made.

## Contact

sandroplayz11@gmail.com
