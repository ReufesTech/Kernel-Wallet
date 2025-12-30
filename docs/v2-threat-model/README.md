Kernel Wallet
White Paper — Version 2
Threat Model and Security Boundaries 


Purpose of this document

This document defines the threat model for Kernel Wallet at a technical level.

A threat model describes:
- which adversaries are considered
- what capabilities those adversaries may have
- which assets are protected
- which threats are explicitly out of scope
- where responsibility shifts from software to the user

The purpose of this document is to make security assumptions explicit, avoid ambiguous guarantees, and prevent unsafe design decisions during future implementation.

This document does not describe implementation details or code. It defines security boundaries and design constraints.


Scope of this threat model

This threat model applies to a self-custodial wallet system that:

- runs on a user-controlled general-purpose operating system
- derives keys from a deterministic seed
- does not use custody, accounts, or hosted key storage
- does not rely on trusted servers
- operates as a client-side application

This model applies equally to desktop environments regardless of platform.


Security objective

The primary security objective of Kernel Wallet is:

Ensure that private keys and signing authority remain under the exclusive control of the user and are never intentionally transmitted outside the local execution environment.

All architectural and design decisions are evaluated against this objective.


Assets under protection

Primary assets (critical):

- seed phrase
- private keys derived from the seed
- ability to produce valid cryptographic signatures

Loss or compromise of these assets results in irreversible loss of control over funds.

Secondary assets (important but non-critical):

- wallet metadata
- transaction history
- address labels
- user preferences
- configuration files

Exposure of secondary assets may impact privacy but does not directly grant spending authority.


Trust assumptions

Kernel Wallet operates under the following assumptions:

- the user owns and controls the device
- the operating system may be partially or fully compromised
- the execution environment cannot be assumed trustworthy
- network connections are hostile by default
- remote infrastructure may behave maliciously or dishonestly
- users may make mistakes or misunderstand instructions

The system does not assume a trusted runtime environment.


Adversary model

The following adversary classes are considered.


Local malware adversary

Description:
Malicious software executing with user-level or elevated privileges on the same system.

Capabilities:
- read process memory
- monitor keystrokes
- intercept clipboard contents
- modify local files
- inject or alter UI behavior
- observe filesystem activity
- hook system APIs

Potential impact:
- seed exposure
- transaction manipulation
- unauthorized signing
- fund loss

Design position:
Kernel Wallet cannot guarantee safety on a compromised host.

Mitigation approach:
- minimize in-memory lifetime of sensitive material
- avoid unnecessary persistence of secrets
- reduce attack surface
- clearly document this limitation
- encourage users to maintain system security


Remote social engineering adversary

Description:
An attacker who manipulates users into revealing secrets or authorizing actions.

Examples:
- phishing websites
- fake wallet downloads
- impersonation of support staff
- fake update prompts
- malicious instructions via messages or social media
- clipboard replacement attacks

Capabilities:
- influence user behavior
- trick users into disclosing seed phrases
- redirect transactions
- convince users to install malware

Design position:
Social engineering cannot be fully prevented by software.

Mitigation approach:
- explicit warnings that seed phrases must never be shared
- seed entry only during explicit wallet recovery
- confirmation screens before sensitive actions
- clear display of destination addresses and amounts
- avoidance of deceptive or ambiguous UI flows


Malicious or compromised network infrastructure

Description:
Remote blockchain nodes or intermediate network infrastructure may be adversarial.

Capabilities:
- log IP addresses
- infer transaction timing
- censor or delay transactions
- provide incomplete or misleading blockchain data
- fingerprint client behavior

Design position:
Network services are treated as untrusted.

Mitigation approach:
- user-configurable node endpoints
- ability to use local nodes
- optional proxy or Tor routing
- transparency about network usage
- no hardcoded infrastructure dependencies

Network privacy is probabilistic and not guaranteed.


Supply-chain adversary

Description:
An attacker compromises dependencies, build systems, or distribution channels.

Capabilities:
- inject malicious code
- alter dependencies
- distribute trojaned binaries
- tamper with updates

Design position:
Supply-chain compromise is a serious risk and must be mitigated defensively.

Mitigation approach:
- open-source development
- minimal dependency surface
- reproducible builds
- signed releases
- verifiable source-to-binary correspondence
- public review processes

Complete elimination of supply-chain risk is not possible.


User error and operational mistakes

Description:
Users may unintentionally compromise their own security.

Examples:
- losing seed phrases
- storing seeds insecurely
- sending funds to incorrect addresses
- misunderstanding transaction fees
- approving unintended transactions

Design position:
User error is expected and unavoidable.

Mitigation approach:
- explicit warnings
- confirmation steps
- clear explanations
- consistent UI behavior
- avoidance of silent defaults

Final responsibility remains with the user.


Network surveillance adversary

Description:
Passive observers monitor network traffic.

Capabilities:
- IP address correlation
- timing analysis
- traffic volume analysis

Design position:
Kernel Wallet does not guarantee anonymity.

Mitigation approach:
- support for proxy or Tor routing
- documentation of privacy trade-offs
- no misleading anonymity claims

Users must understand that privacy exists on a spectrum.


Explicit non-goals

Kernel Wallet does not attempt to:

- protect against fully compromised operating systems
- recover lost seed phrases
- guarantee anonymity
- prevent all user mistakes
- obfuscate all metadata
- replace hardware wallets
- act as a mixing or anonymization service
- provide legal, financial, or custodial services


Responsibility boundaries

Software responsibilities:
- correct cryptographic operations
- secure defaults
- deterministic behavior
- explicit warnings
- avoidance of secret leakage

User responsibilities:
- securing their operating system
- protecting their seed phrase
- validating addresses and transactions
- understanding risks
- choosing appropriate network settings

Security is shared, but ownership and control remain with the user.


Design principles reinforced by this threat model

- explicit trust boundaries
- minimal assumptions
- defensive defaults
- transparency over obscurity
- user agency over automation
- documented limitations


Relationship to Version 1

This document extends Version 1 by defining:

- attacker classes
- trust boundaries
- security assumptions
- responsibility allocation
- explicit non-goals

Future versions may include:
- detailed mitigations
- architectural enforcement mechanisms
- component-level threat analysis
- testing and verification strategies
- audit guidance


Document status

Version 2 — Model and Security Boundaries 
Open for review and discussion.


Disclaimer

This document is provided for educational and research purposes only.

Kernel Wallet does not provide financial advice or custody services.

Users are solely responsible for securing their devices and seed phrases.  
Loss of a seed phrase results in permanent loss of access to funds.
