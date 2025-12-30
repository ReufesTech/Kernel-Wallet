# Contributing

Kernel Wallet is security-first. Every change must align with the threat model and document explicit assumptions.

## Expectations for contributions
- State which documents or components you are modifying and why.
- Enumerate assumptions and how they relate to [v3 architecture](docs/v3-architecture/README.md) and the [threat model](docs/v2-threat-model/README.md).
- Highlight user-facing risk mitigations (e.g., confirmations, warnings, offline fallbacks).
- Keep keys and seed material device-local; do not introduce remote dependencies without an ADR.

## Review checklist
- [ ] Keys/seed material never leave the device; crypto operations remain within the trusted boundary.
- [ ] Network interactions are documented (endpoint, auth expectations, failure handling) and respect the trust boundaries.
- [ ] Storage interactions state encryption, integrity, and access-control assumptions.
- [ ] UI surfaces explicit user confirmation for sensitive actions (signing, backup, restore).
- [ ] Tests or validation notes updated to cover new flows or risks.
- [ ] Relevant ADRs and the [Open Questions](adr/open-questions.md) list are updated or referenced as needed.

## Process
1. Open an issue using the provided template to describe scope, touched documents, and risks.
2. Discuss alignment with existing ADRs or propose a new ADR when changing architecture.
3. Submit a PR using the template to summarize document changes and risk considerations.
4. Ensure reviewers can trace each change back to threat-model assumptions and architecture boundaries.
