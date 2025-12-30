Kernel Wallet  
White Paper — Version 1  
Foundations for Safe Self-Custody

Overview

Kernel Wallet is a design-first project focused on one simple goal:

helping people safely store and control their own cryptocurrency.

This document represents Version 1 of the Kernel Wallet white paper. It defines the philosophy, scope, and technical direction of a self-custodial wallet before any production code is written.

The purpose of this document is to establish clear ideas, boundaries, and expectations so future development can happen carefully, transparently, and safely.


What “self-custody” means

Self-custody means the user — and only the user — controls access to their funds.

In practical terms:

- A seed phrase is generated locally on the user’s device  
- Private keys never leave the device  
- Nothing is stored in the cloud  
- There are no accounts or logins  
- No third party can recover funds  
- Wallets can be restored using the seed alone  

If the seed phrase is lost, access to funds is permanently lost.  
This is an intentional and unavoidable property of self-custody.


Why this project exists

Many wallets prioritize convenience, speed, or growth over clarity and user understanding. This often results in:

- hidden trust assumptions  
- unclear security models  
- server dependencies users don’t realize exist  
- blurred lines between custody and self-custody  
- complex or misleading interfaces  

Kernel Wallet is documenting how wallet is going to be built and be safe with transparency, and user understanding come first.

This project is about learning, documenting, and eventually building a wallet that does one thing well:

store cryptocurrency safely under the user’s control.


What Kernel Wallet is

- A design-first wallet project  
- A documentation-driven effort  
- A reference for safe self-custody practices  
- A foundation for a future open-source wallet  
- A place for discussion, review, and iteration  


What Kernel Wallet is not

- A bank  
- A hosted service  
- A recovery service  
- An exchange  
- A token  
- Financial advice  


Scope of Version 1

Version 1 focuses on definition and design, not implementation.

It covers:
- self-custody principles  
- security assumptions  
- wallet architecture concepts  
- user safety expectations  
- threat awareness  
- high-level technical direction  

There is no production wallet code in this version.


Assets in scope (initial)

To keep scope realistic and well understood, early design work focuses on:

- Monero (XMR) — privacy-first, seed-based wallet model  
- Litecoin (LTC) — mature UTXO model with strong documentation  

Additional assets may be considered later if they align with the same principles.


Core principles

1. User control  
Users control their keys. The software does not.

2. Local-first security  
Key generation, storage, and signing happen locally on the user’s device.

3. Deterministic wallets  
Keys are derived from a seed phrase using well-established methods.

4. Explicit behavior  
Nothing happens silently. Actions and risks should be visible and understandable.

5. Minimal trust  
The system minimizes reliance on external services or assumptions.

6. Transparency  
Design decisions should be inspectable and explainable.


High-level wallet lifecycle

1. A wallet is created and a seed phrase is generated locally  
2. The user securely records the seed  
3. Wallet data is encrypted and stored on the device  
4. Keys are deterministically derived from the seed  
5. Transactions are constructed locally  
6. Transactions are signed locally  
7. Signed transactions are broadcast to the network  
8. Wallet state updates through synchronization  

At no point do private keys leave the device.


Security mindset

Kernel Wallet assumes real-world risks exist, including:

- malware on user systems  
- phishing attempts  
- malicious or compromised nodes  
- network monitoring  
- user mistakes  

The goal is not to eliminate all risk, but to reduce unnecessary risk and make trade-offs visible and understandable.


Technical direction (high level)

This section outlines intended design direction without committing to implementation.

Architecture overview:

Kernel Wallet is conceptually divided into layers:

- User Interface Layer — user interaction and display  
- Wallet Engine — key handling and transaction logic  
- Cryptographic Core — deterministic derivation and signing  
- Network Layer — communication with blockchain nodes  
- Storage Layer — encrypted local persistence  

Each layer has a clear responsibility and minimal coupling.


Language and platform direction (conceptual)

The project favors technologies that are:

- memory-safe  
- well-documented  
- auditable  
- widely supported  
- suitable for long-term maintenance  

Potential candidates include:

- Rust (preferred for safety and correctness)  
- Go (simple and readable alternative)  

Final language choices are intentionally left open at this stage.


Storage model

- Wallet data stored locally  
- Encrypted at rest  
- Password-derived encryption keys  
- Atomic file writes  
- Corruption detection  
- No plaintext secrets on disk  


Network model

- User-configurable nodes  
- Support for local or remote nodes  
- No hardcoded infrastructure  
- Optional proxy or Tor routing  
- Clear visibility into network activity  


User interface philosophy

The interface should be:

- simple  
- honest  
- predictable  
- explicit  
- non-deceptive  

Key goals:
- clear warnings  
- explicit confirmations  
- understandable errors  
- no dark patterns  
- safe defaults  


Contribution and feedback

Thoughtful discussion and feedback are welcome, especially around:

- security assumptions  
- architecture decisions  
- threat modeling  
- usability and safety  
- clarity of explanations  

Please keep contributions focused on design quality and safety.


Project status

Status: Version 1 — Design phase

Current focus:
- documenting architecture  
- defining boundaries  
- identifying risks  
- writing clear explanations  
- gathering feedback  

There is no production wallet yet.


Planned repository structure

still to be determand.


Disclaimer

This document is provided for educational and research purposes only.

Kernel Wallet does not provide financial advice or custody services.

You are solely responsible for securing your own seed phrase.  
Loss of a seed phrase results in permanent loss of access to funds.


Document status: Version 1 (draft, open for discussion)
