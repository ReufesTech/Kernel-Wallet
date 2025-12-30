# ADR 0003: Deterministic Wallets for Recovery

- **Status**: Proposed
- **Context**: Repeatable key derivation is required for recovery across devices and future implementations.
- **Decision**: Use deterministic wallet schemes (e.g., BIP-39/32 style seed + path) with explicit derivation paths per asset/network. Document versioned derivation to avoid collisions when adding assets.
- **Consequences**: Simplifies backup/restore, enables reproducible signing, and requires strict handling of seed material and derivation path migrations.
