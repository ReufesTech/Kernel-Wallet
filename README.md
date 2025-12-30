# Kernel Wallet Documentation Index

This repository collects the evolving Kernel Wallet design. Start with the latest architecture and threat model, then dive into prior versions for historical context.

## Document map (latest first)
- [v3 Architecture & Trust Boundaries](docs/v3-architecture/README.md) — current component layout, trust boundaries, and attack surface assumptions. See the accompanying [diagrams](docs/v3-architecture/diagrams.md).
- [v2 Model & Security Boundaries](docs/v2-threat-model/README.md) — threat model and security considerations that informed the v3 update.
- [v1 Foundations](docs/v1-foundations/README.md) — original white paper outlining the core concept.

_All versioned white papers above are the original texts moved from the repository root, preserved intact for reference._

## Design governance
- [Architecture Decision Records](adr/) capture major design choices and how to propose changes.
- [Open Questions](adr/open-questions.md) tracks unresolved items with owners and next steps.
- [Changelog](docs/CHANGELOG.md) summarizes how each version evolves to reduce confusion when comparing documents.
- [Creation review](docs/creation-review.md) lists the concrete deliverables and proposals needed for the minimal wallet slice.

## Contributing
Review [CONTRIBUTING.md](CONTRIBUTING.md) before opening changes. Issue and PR templates prompt you to note which documents you touch and the risks considered.

## Planning and validation
- [Roadmap](docs/roadmap.md) lays out milestones that align with threat-model assumptions.
- [Testing Strategy](docs/testing-strategy.md) describes unit, property, integration, and manual checks ahead of implementation.
