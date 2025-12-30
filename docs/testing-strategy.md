# Testing Strategy

Testing and validation should start alongside design to keep controls aligned with the threat model.

## Automated testing
- **Unit tests**: Key derivation, signing routines, and serialization/deserialization of transactions and addresses.
- **Property-based tests**: Validate deterministic outputs for derivation/signing across seeds and paths; ensure serialization round-trips.
- **Integration tests**: Run against reference nodes with mocked and real responses; assert trust-boundary checks (e.g., reject unsigned headers or malformed fee data).

## Manual validation
- **Seed generation**: Confirm entropy sources, checksum display, and user acknowledgement of backup responsibilities.
- **Backup and restore**: Walk through recovery flows on fresh installs; verify restored addresses/signatures match expected derivations.
- **Send/receive flows**: Validate address entry warnings, fee confirmations, and post-broadcast status updates.

## Security reviews (future)
- Static analysis and linting tailored to the chosen memory-safe language.
- Dependency auditing for crypto and networking libraries; pin versions.
- Periodic threat-model reviews when adding assets or remote services.
