Kernel Wallet
White Paper — Version 4
Cryptography and Key Management

Purpose and scope

Version 4 defines the cryptographic primitives, key lifecycles, and operational controls required to enforce the trust boundaries described in Version 3. It is intentionally precise: algorithms, parameters, memory constraints, and validation rules are specified to reduce ambiguity before implementation.

This document applies to the local-only client described in previous versions. It does not introduce server-side custody, recovery escrow, or remote signing.

Security objective

Private keys, seed material, and signing authority must remain under the user’s exclusive control. All cryptographic operations must preserve integrity and authenticity, minimize exposure of secrets, and fail closed.

Cryptographic primitives (baseline)

- Entropy: 256 bits of locally generated entropy using the platform CSPRNG (e.g., /dev/urandom, CryptGenRandom, or platform-approved equivalent). No network or hardware RNG mixing.
- Seed format: BIP-39 mnemonic + checksum for human backup, encoded only at user request and never stored in plaintext.
- Root key: BIP-32/BIP-44 compatible master seed derived with PBKDF2-HMAC-SHA512, iteration count ≥ 2048; parameters documented and versioned.
- Symmetric encryption: AES-256-GCM with 96-bit nonce, 128-bit tag for any at-rest ciphertext produced by the wallet.
- Key derivation for storage: HKDF-SHA-256 with distinct context/info strings for each data class (seed vault, metadata, cache) to prevent key reuse.
- Message authentication: HMAC-SHA-256 for integrity of unencrypted control messages between wallet engine and crypto core when applicable.
- Digital signatures: Ed25519 for default accounts; secp256k1 retained for chains requiring it. Signing algorithms are deterministic per RFC 8032 and RFC 6979 respectively.
- Hashing: SHA-256 for general hashing; double-SHA-256 only where the target chain mandates it.

Trust boundary reinforcements

- Crypto core isolation: Only the wallet engine may call into the cryptographic core. The core has no network, filesystem, UI, or logging access. All calls are synchronous and deterministic with explicit return codes; no ambient global state.
- Data flow: Wallet engine passes canonicalized inputs to the core (length-delimited, schema-validated). The core returns signatures or derived keys but never persists them.
- Error discipline: Fail closed. On validation failure, the core returns explicit error codes and zeroizes temporary buffers.

Seed lifecycle and handling

- Generation: Seeds are generated entirely locally using the platform CSPRNG. No external entropy or mnemonic generators are permitted.
- Presentation: Mnemonics are only rendered for user backup workflows. Rendering is opt-in, time-bounded, and blocked during screen sharing or clipboard operations when detectable.
- Storage: Plaintext seeds are never written to disk. When persisted, seeds are encrypted using a key derived from a user secret (passphrase) via Argon2id with parameters tuned per platform (baseline: memory 64 MiB, iterations 3, parallelism 1). Parameters are version-tagged for future tuning.
- Zeroization: Temporary seed buffers are zeroed immediately after use. Languages without deterministic memory management require explicit scrub calls and avoidance of unnecessary copies.
- Export: Seed export is disabled by default. If enabled for advanced users, it requires re-authentication, explicit warnings, and cannot be automated via scripting interfaces.

Key derivation and hierarchy

- Deterministic paths: Use BIP-44 derivation paths with coin-type registries documented per chain. Hardened derivation is mandatory for account-level nodes.
- Context binding: Each derived key includes metadata (path, chain ID, creation time) stored separately from the key to prevent misuse across networks.
- Separation of duties: Signing keys are derived only inside the crypto core. The wallet engine receives public keys and extended public keys only when needed, never private components.
- Versioning: Derivation parameters (curve, path schema, hardened depth) are versioned. Migration plans must include compatibility checks before allowing upgrades.

Signing operations

- Determinism: Signatures must be deterministic. Nonces are derived from private keys and messages per algorithm standard; no random nonces.
- Preflight validation: The wallet engine validates transaction payloads (schema, chain rules, fee bounds) before invoking the crypto core. The core validates message length and domain separation tags.
- Domain separation: All sign requests include an explicit domain tag (chain/network identifier + purpose). The crypto core refuses to sign if the domain tag is missing or unrecognized.
- Rate limits: The crypto core enforces request-rate controls (e.g., max N sign calls per second) to reduce exfiltration side-channel attempts from compromised engines.
- Auditability: Each signing call returns a structured log entry (hash of payload, domain tag, derivation path, monotonic counter) to the wallet engine for audit. No sensitive material is included in logs.

Storage encryption and integrity

- Envelope keys: A per-wallet envelope key is derived from the user secret via Argon2id, then expanded with HKDF for distinct uses: seed vault encryption, metadata encryption, and cache MAC keys.
- Nonce management: Nonces are generated with a monotonic counter stored alongside ciphertext and verified before decryption to prevent reuse. Counter corruption triggers decryption failure and recovery guidance.
- Integrity: Every ciphertext includes a versioned header, nonce, associated data (wallet ID, data class), and GCM tag. Decryption verifies header, version, and tag before returning plaintext.
- Backups: Encrypted backups reuse the same envelope key derivation but rotate nonces and attach export metadata (creation time, app version). Plaintext backups are explicitly unsupported.

Memory and process hygiene

- Allocation: Sensitive buffers are allocated in locked memory where possible (mlock/VirtualLock) to reduce paging risk. Fallbacks are documented per platform.
- Copy minimization: APIs avoid implicit copies; callers provide preallocated buffers when feasible.
- Crash behavior: On fatal errors, the crypto core scrubs working memory before process termination to the extent allowed by the runtime.

Randomness and health checks

- CSPRNG validation: On startup, the crypto core performs a basic RNG sanity check (rejection of repeated outputs across calls, failure on entropy source errors). It fails closed if the platform CSPRNG is unavailable.
- Health counters: The core maintains monotonic counters for key derivations and signatures to detect anomalous rates indicative of misuse.

Interoperability and chain-specific rules

- Multiple curves: The architecture supports multiple curves per chain, but only a single curve is active per account. Curve selection is explicit and stored with account metadata.
- Address encoding: Address derivation follows chain standards (e.g., Bech32 for compatible chains, Base58Check where required). Encoding parameters are versioned and validated before display.
- Message formats: The wallet engine is responsible for chain-specific message canonicalization. The crypto core signs only canonical byte strings, not high-level objects.

Operational controls and UX constraints

- Unlock flow: Deriving the envelope key and unlocking the crypto core requires a user passphrase. Idle timers lock the core and zeroize envelope material after configurable inactivity (default: 5 minutes).
- Recovery: Restoring from mnemonic re-derives the root key and all subsequent keys; no cloud state is trusted. Any mismatch in derived public keys during restore triggers warnings and halts signing until resolved.
- Policy gating: High-risk actions (deriving new accounts, enabling seed export, disabling passphrase) are gated behind policy prompts that cannot be suppressed by configuration.

Testing and verification requirements

- Test vectors: Provide deterministic test vectors for seed generation, derivation paths, signing outputs, and encryption headers. Vectors must include version metadata and domain tags.
- Property tests: Include property-based tests for determinism (same input → same signature), rejection of malformed inputs, and nonce uniqueness for storage encryption.
- Fuzzing: Apply API-level fuzzing to the crypto core boundary (serialization, length fields, domain tags) to catch parsing and validation weaknesses.
- Continuous verification: CI enforces linting of cryptographic parameter versions and regenerates documentation if parameters change.

Non-goals

- Hardware security modules: Integration with HSMs or secure enclaves is out of scope for this version; future work may define optional adapters.
- Multi-party computation: MPC-based signing and threshold schemes are deferred. This version focuses on single-actor local custody.
- Cloud key recovery: No remote recovery or custodial backup mechanisms are introduced.

Expected outputs and follow-up

- Proposal: Draft a proposal (using the proposal template) to ratify these primitives, parameter baselines, and operational controls. Identify reviewers across security, storage, and platform.
- ADR: Upon acceptance, record an ADR covering cryptographic parameter versions, envelope key derivation, and signing domain rules.
- Documentation updates: Update v3 architecture diagrams to reflect the stricter crypto core boundary and storage encryption model; align roadmap milestone 1 (key/seed module) and milestone 2 (storage encryption) with these requirements.
