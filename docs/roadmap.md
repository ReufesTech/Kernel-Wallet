# Roadmap

This roadmap outlines a minimal viable wallet slice and sequences work to stay aligned with the threat model and trust boundaries.

## Minimal viable wallet slice
- Single-asset send/receive
- Local seed generation and backup guidance
- Manual node configuration

## Milestones
1. **Prototype key/seed module**
   - Deterministic seed generation, derivation paths, and signing stubs.
   - Maps to: keys stay inside local trusted boundary; no remote entropy sources.
2. **Storage encryption**
   - Encrypted, integrity-checked storage for seeds, settings, and transaction history.
   - Maps to: local-first storage assumption and attack surface on device tampering.
3. **Transaction construction**
   - Build and sign basic transactions; validate inputs/outputs before signing.
   - Maps to: network trust boundary and explicit signing intent.
4. **Basic UI**
   - Minimal screens for seed creation, send/receive, and confirmations.
   - Maps to: clear user confirmations and phish-resistant prompts.
5. **Network abstraction**
   - Swappable node endpoints with validation of responses and error handling.
   - Maps to: adversarial node model and ability to switch endpoints.
6. **Testing harness**
   - Local integration harness against reference nodes and signing test vectors.
   - Maps to: verification of threat-model controls before expansion.

## Alignment notes
- Each milestone should trace to the [v3 trust boundaries](docs/v3-architecture/README.md) and call out assumptions in PRs.
- Deviations from ADRs require updates or new records before implementation proceeds.
