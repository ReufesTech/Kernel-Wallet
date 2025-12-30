Kernel Wallet
White Paper — Version 3
Architecture and Trust Boundaries
(Revised from a defensive security perspective)


Context and intent

This document reflects the perspective of long-term security engineering experience across offensive (red team) and defensive (blue team) roles, with a focus on open-source, self-custodial systems.

The purpose is not to describe an idealized system, but to define realistic boundaries: what can be protected, what cannot, and where responsibility necessarily shifts to the user.

Most wallet failures come from unclear assumptions. This document exists to make those assumptions explicit before any implementation work begins.


Core security objective

Kernel Wallet exists to preserve one thing above all else:

Private keys must remain under the exclusive control of the user and must never be intentionally transmitted outside the local execution environment.

Everything else — usability, performance, convenience — is secondary to that goal.

If a design decision weakens this property, it is rejected.


Operating assumptions

This project assumes a hostile environment by default.

Specifically:

- user devices may be partially or fully compromised  
- operating systems are not trusted  
- networks are adversarial  
- dependencies may eventually fail  
- users make mistakes  
- attackers are persistent  

Security design starts from failure, not from ideal conditions.


Assets under protection

Primary assets (catastrophic if compromised):

- seed phrase  
- private keys derived from the seed  
- signing authority  

Secondary assets (privacy-impacting but not spend-authorizing):

- transaction history  
- metadata  
- address labels  
- configuration data  

Loss of primary assets results in irreversible loss of funds. No recovery mechanisms exist by design.


Trust boundaries (high-level)

Kernel Wallet enforces separation between components with different trust assumptions.

The major trust boundaries are:

- user ↔ application  
- application ↔ operating system  
- wallet engine ↔ cryptographic core  
- application ↔ network  
- memory ↔ persistent storage  

Crossing any of these boundaries introduces risk. The architecture exists to make those crossings explicit and minimized.


User boundary

Users are not assumed to behave perfectly.

They may:
- misunderstand warnings  
- click through prompts  
- reuse passwords  
- follow bad advice  
- fall for social engineering  

Design implications:
- dangerous actions require explicit confirmation  
- wording must be unambiguous  
- no implicit consent  
- no silent behavior  
- no misleading UI shortcuts  

The software must never assume intent beyond what the user explicitly confirms.


Operating system boundary

The OS is assumed to be potentially compromised.

This includes:
- malware  
- keyloggers  
- memory inspection  
- malicious drivers  
- clipboard hijacking  
- process injection  

This is a hard boundary that cannot be “secured away.”

Design consequences:
- secrets should exist in memory only when required  
- secrets should never be logged  
- plaintext secrets must never be written to disk  
- exposure windows should be minimized  
- reliance on OS guarantees should be limited  

Kernel Wallet does not claim to protect against a compromised OS.


Wallet engine boundary

The wallet engine coordinates application behavior.

Its role is control, not secrecy.

Responsibilities:
- manage wallet state  
- enforce workflow rules  
- coordinate signing requests  
- validate inputs  
- mediate between layers  

Constraints:
- must not hold private keys  
- must not perform cryptographic operations  
- must not perform network I/O  
- must be deterministic and auditable  

This layer exists to reduce complexity and prevent accidental privilege escalation.


Cryptographic core boundary

This is the most sensitive component in the system.

Responsibilities:
- seed handling  
- deterministic key derivation  
- signing operations  
- secure memory handling  

Constraints:
- no network access  
- no filesystem access  
- no UI access  
- minimal API surface  
- deterministic behavior  
- explicit zeroization where possible  

Only the wallet engine may invoke this component.

Isolation here is critical.


Network boundary

All network interaction is treated as hostile.

Assumptions:
- nodes may be malicious  
- traffic may be observed  
- responses may be incomplete or misleading  
- metadata leakage is unavoidable  

Responsibilities:
- communicate with user-selected nodes  
- handle transport configuration  
- expose network status transparently  

Constraints:
- no access to private keys  
- no signing capability  
- no seed material  
- no implicit trust  

Privacy is a gradient, not a guarantee.


Storage boundary

Persistent storage is treated as hostile unless encrypted.

Responsibilities:
- store encrypted wallet data  
- support atomic writes  
- detect corruption  
- support versioning  

Constraints:
- no plaintext secrets on disk  
- encryption before persistence  
- access limited to wallet engine  
- format must be documented and inspectable  

Storage compromise should not automatically imply key compromise.


Data flow summary

Normal operation follows strict directional flow:

User  
→ Interface  
→ Wallet Engine  
→ Cryptographic Core  
→ Wallet Engine  
→ Network  

Persistence path:

Wallet Engine  
→ encryption  
→ storage  

Secrets should exist only briefly and only inside constrained components.


Adversary classes considered

Local adversary:
- malware
- keyloggers
- memory scrapers
- injected processes

Remote adversary:
- malicious nodes
- network observers
- censorship infrastructure

Social adversary:
- phishing
- impersonation
- fake support
- deceptive instructions

Supply-chain adversary:
- compromised dependencies
- malicious build artifacts
- poisoned updates

User error:
- lost seeds
- incorrect addresses
- unsafe backups
- misunderstanding warnings


What this system does not protect against

Kernel Wallet explicitly does not attempt to:

- protect against a fully compromised OS  
- recover lost seed phrases  
- guarantee anonymity  
- prevent all user mistakes  
- defeat advanced malware  
- act as a mixer or obfuscation tool  
- replace hardware wallets  
- provide legal or financial guarantees  

These limitations are intentional and documented.


Responsibility boundaries

Software responsibilities:
- correct cryptographic behavior  
- safe defaults  
- predictable execution  
- clear warnings  
- minimized trust  

User responsibilities:
- secure their environment  
- protect their seed phrase  
- verify transactions  
- understand risks  
- choose appropriate network configuration  

Security is shared, but ownership always remains with the user.


Design principles reinforced

- least privilege  
- explicit trust boundaries  
- defensive defaults  
- simplicity over cleverness  
- transparency over abstraction  
- predictability over automation  


Relationship to previous documents

This document builds on:

Version 1 — goals, scope, philosophy  
Version 2 — threat model and adversary definitions  

This version turns those ideas into enforceable architectural boundaries.


Future work

Future documents may cover:

- cryptographic primitives and derivation schemes  
- interface contracts between components  
- audit strategy  
- reproducible build process  
- update verification  
- hardware wallet integration  
- formal threat matrices  

All future work must respect the constraints defined here.


Document status

Version 3 — Draft  
Open for review and iteration.


Disclaimer

This document is provided for educational and research purposes only.

Users are solely responsible for securing their devices and seed material.  
Loss of a seed phrase results in permanent loss of access to funds.

