# ADR 0002: Local-First Encrypted Storage

- **Status**: Proposed
- **Context**: Users control their keys; dependency on cloud services introduces additional trust and attack vectors.
- **Decision**: Default to local-first storage with encryption-at-rest and integrity checks. Remote sync (if added) must be opt-in, end-to-end encrypted, and avoid exposing seed material.
- **Consequences**: Simplifies trust assumptions and offline usage but requires careful backup UX to prevent data loss.
