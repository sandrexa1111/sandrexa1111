# Alexandre Mosiashvili

Early-career developer focused on Python, software verification, cybersecurity, and open-source tooling.

I learn mostly by building projects, testing failure cases, and turning vague claims into things that can be checked.

## Selected projects

### [Continuum](https://github.com/sandrexa1111/continuum-agent)
Portable execution state for long-lived agents.

Continuum can checkpoint, fork, inspect, migrate, and resume agent execution state through a versioned, content-addressed format. The core has zero runtime dependencies and includes integrity checks, capability-gated resume, migration diagnostics, and a separate LangGraph adapter that demonstrates fresh-runtime resume.

**Python · 264 core tests + 32 adapter tests · strict mypy · multi-OS CI**

### [PatchProof](https://github.com/sandrexa1111/patchproof)
Evidence-based verification for repository patches.

PatchProof compares a repository before and after a candidate patch, attributes regressions, executes task contracts, runs deterministic behavioral probes, and shrinks failures to useful counterexamples. Verdicts come from executed evidence rather than a model score.

**Python · 72 tests · adversarial patch corpus · strict mypy · CI**

### [EffectProof](./projects/effectproof)
Deterministic verification of observable side effects.

EffectProof compares state before and after an operation and checks the delta against explicit allow/forbid rules and postconditions. The included calendar example catches a permission mutation even though the requested title change succeeded.

**Python · zero runtime dependencies · 7 tests · stable proof IDs**

### [SchedShrink](./projects/schedshrink)
Small, reproducible counterexamples for concurrency failures.

SchedShrink enumerates legal cooperative task interleavings, evaluates an invariant, and returns the failing full schedule with the fewest context switches. Its lost-update example explores all six legal schedules and isolates a two-switch failure.

**Python · zero runtime dependencies · 10 tests · deterministic replay traces**

## Other work

- **ThreatVeil** — personal AI security and governance project exploring execution risk, policy controls, and failure visibility.
- **5G anomaly detection** — unsupervised ML project for network-traffic anomaly detection; presented at an international student olympiad.
- **Cybersecurity tooling** — small reconnaissance, networking, and anomaly-analysis utilities plus hands-on lab work with Linux and Splunk.
- **Web projects** — built and deployed several small web applications and sites.

## Tools

Python · JavaScript / TypeScript · Bash · FastAPI · pytest · GitHub Actions · Linux · Docker · Postgres

## Contact

- [sandro@threatveil.com](mailto:sandro@threatveil.com)
- [LinkedIn](https://www.linkedin.com/in/alexandre-mosiashvili/)
