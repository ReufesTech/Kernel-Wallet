# ADR 0001: Memory-Safe Language Preference

- **Status**: Proposed
- **Context**: Wallet components handle secret material and untrusted network data. Memory safety eliminates broad classes of exploits (use-after-free, buffer overflow) common in C/C++ stacks.
- **Decision**: Prefer a memory-safe language (e.g., Rust, Swift, Kotlin, or TypeScript+WASM) for all core wallet components. Only use unsafe blocks with explicit justification and additional review.
- **Consequences**: Limits library choices but reduces exploit surface. Requires tooling (linters, static analysis) compatible with the chosen language.
