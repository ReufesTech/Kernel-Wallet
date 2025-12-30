# Kernel Wallet Documentation Index

This repository collects the evolving Kernel Wallet design. Start with the latest cryptography guidance and architecture/threat model, then dive into prior versions for historical context.

## Document map (latest first)
- [v4 Cryptography & Key Management](docs/v4-cryptography/README.md) — deterministic primitives, key lifecycles, storage encryption, and operational controls that reinforce the v3 trust boundaries before implementation.
- [v3 Architecture & Trust Boundaries](docs/v3-architecture/README.md) — current component layout, trust boundaries, and attack surface assumptions. See the accompanying [diagrams](docs/v3-architecture/diagrams.md).
- [v2 Model & Security Boundaries](docs/v2-threat-model/README.md) — threat model and security considerations that informed the v3 update.
- [v1 Foundations](docs/v1-foundations/README.md) — original white paper outlining the core concept.

_All versioned white papers above are the original texts moved from the repository root, preserved intact for reference._

## Design governance
- [Architecture Decision Records](adr/) capture major design choices and how to propose changes.
- [Open Questions](adr/open-questions.md) tracks unresolved items with owners and next steps.
- [Changelog](docs/CHANGELOG.md) summarizes how each version evolves to reduce confusion when comparing documents.
- [Proposal playbook](docs/proposals/README.md) explains when and how to draft proposals before promoting them to ADRs.

## Contributing
Review [CONTRIBUTING.md](CONTRIBUTING.md) before opening changes. Issue and PR templates prompt you to note which documents you touch and the risks considered.

## Planning and validation
- [Roadmap](docs/roadmap.md) lays out milestones that align with threat-model assumptions.
- [Testing Strategy](docs/testing-strategy.md) describes unit, property, integration, and manual checks ahead of implementation.

## Desktop client for Litecoin (LTC) and Monero (XMR)
A local-only desktop client lives in `gui/` to illustrate how the UI can delegate
validation to an offline engine while keeping seed material and signing inputs
within the device boundary described in the v3 architecture. The client is
self-custodial: users must provide their own wallet name and seed phrase, which
stay in memory for the current session only. Features include:

- Asset toggle between LTC and XMR with per-asset balances and addresses.
- Local validation of recipient, amount, fee bounds, and node connectivity before any transaction is
  staged.
- Bring-your-own node endpoints with TLS opt-in for each asset.
- Explicit confirmation prompts so signing flows are never triggered implicitly.
- Send actions stay disabled until you load a wallet profile and assign a node for the selected
  asset, reinforcing the self-custodial, offline-first flow.

Run the client with Python and Tkinter (no external dependencies):

```bash
python gui/wallet_gui.py
```

The client does not make network calls; it prepares transactions locally so the
engine can later be swapped for a fully verified implementation. To interact
with mainnet or testnet you must point the engine at your own trusted
Litecoin/Monero node; no shared infrastructure is bundled. Seed phrases and
wallet names are collected only to keep the flow self-custodial—no data leaves
the local process.
