# Alexandre Mosiashvili

Early-career developer focused on Python, software verification, cybersecurity, and open-source tooling.

I learn mostly by building projects, testing failure cases, and turning vague claims into things that can be checked.

## Selected projects

### [agent-checkpoint](https://github.com/sandrexa1111/continuum-agent)
Portable execution state for long-lived agents.

`agent-checkpoint` can checkpoint, fork, inspect, migrate, and resume agent execution state through a versioned, content-addressed format. The core has zero runtime dependencies and includes integrity checks, capability-gated resume, migration diagnostics, and a separate LangGraph adapter that demonstrates fresh-runtime resume.

**Python · 264 core tests + 32 adapter tests · strict mypy · multi-OS CI**

### [patch-eval](https://github.com/sandrexa1111/patchproof)
Evidence-based verification for repository patches.

`patch-eval` compares a repository before and after a candidate patch, attributes regressions, executes task contracts, runs deterministic behavioral probes, and shrinks failures to useful counterexamples. Verdicts come from executed evidence rather than a model score.

**Python · 72 tests · adversarial patch corpus · strict mypy · CI**

### [state-delta](https://github.com/sandrexa1111/state-delta)
Deterministic verification of observable state changes.

`state-delta` compares JSON state before and after an operation and checks the resulting changes against explicit allow/forbid rules and postconditions. The included example catches a permission mutation even though the requested title change succeeds.

**Python · zero runtime dependencies · 7 tests · strict mypy · Python 3.10–3.13 CI**

### [interleaving-lab](https://github.com/sandrexa1111/interleaving-lab)
Deterministic exploration of small concurrency failures.

`interleaving-lab` enumerates legal cooperative task interleavings, evaluates an invariant, and reports the failing schedule with the fewest context switches. Its lost-update example explores all six legal schedules and isolates a two-switch failure with a replayable state trace.

**Python · zero runtime dependencies · 10 tests · strict mypy · Python 3.10–3.13 CI**

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
