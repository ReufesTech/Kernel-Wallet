# Creation review: upcoming deliverables

This note summarizes what still needs to be produced to turn the Kernel Wallet design into a usable minimal slice. It pulls together open decisions, build milestones, and supporting documentation so contributors can quickly align on priorities.

## Decision proposals to author
- **Seed backup UX** — propose how users generate, split, and store recovery materials while staying in line with the offline-first threat model.
- **Node selection defaults** — document whether to ship curated endpoints or require manual entry, along with fallback and verification behaviors.
- **Update mechanism** — outline how updates are delivered and verified without compromising offline installs.
- **Hardware wallet interoperability** — compare supported signing protocols and how the wallet detects and validates connected devices.
- **Telemetry boundaries** — define the minimal telemetry policy that helps security without exposing sensitive usage patterns.

## Build outputs to create
- **Key and seed module prototype** — deterministic seed generation, derivation paths, and signing stubs that never leave the local boundary.
- **Encrypted storage layer** — integrity-checked storage for seeds, configuration, and history, consistent with the local-first assumption.
- **Transaction constructor** — routines to build, validate, and sign basic transactions with explicit user intent before signing.
- **Minimal user interface** — screens for seed creation, send/receive flows, and clear confirmations that discourage phishing.
- **Network abstraction** — swappable node endpoints with validation and robust error handling for adversarial networks.
- **Integration testing harness** — local harness against reference nodes and signing vectors to validate threat-model controls.

## Supporting documentation to expand
- **Traceability to v3 trust boundaries** — each deliverable should reference the relevant trust boundary and note deviations.
- **Changelog entries** — record changes as milestones land to keep historical context clear across versions.
- **Testing notes** — document planned coverage and manual checks for new modules so security assumptions remain auditable.
