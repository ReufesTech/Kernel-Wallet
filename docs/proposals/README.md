# Proposal playbook

This guide explains how to write and socialize proposals that may become Architecture Decision Records (ADRs) or updates to the Kernel Wallet design docs.

## When to write a proposal
- You want to change a trust boundary, dependency, or protocol assumption.
- You are introducing a new component or deprecating an existing one.
- You need buy-in on a significant trade-off (e.g., security vs. performance) before implementation.

Smaller documentation fixes or clarifications can be sent directly as pull requests without a proposal.

## Preparation checklist
- **Map the scope.** Identify affected documents (ADR entries, threat model versions, diagrams, and roadmap items).
- **Gather context.** Link to relevant issues, prior ADRs, and any experiments or prototypes.
- **Stakeholders.** List reviewers needed for security, storage, wallet UX, and platform concerns.

## Proposal structure
Use the [proposal template](./proposal-template.md) as a starting point and cover these sections:

1. **Summary.** One or two sentences describing the decision being proposed.
2. **Problem statement.** What user, operational, or security problem are you solving? Why now?
3. **Goals and non-goals.** Keep the blast radius explicit so reviewers can judge trade-offs.
4. **Context and constraints.** Note trust boundaries, threat model assumptions, performance budgets, and compliance requirements.
5. **Options considered.** Present at least two options with pros/cons, risks, and mitigation strategies.
6. **Recommendation.** State the preferred option and justify it with evidence (benchmarks, prototypes, prior art).
7. **Impact.** List documents, APIs, data formats, and operational playbooks that would change.
8. **Open questions.** Track unresolved items and expected owners.
9. **Decision and follow-up.** Once accepted, record the ADR number, timeline, and success metrics.

## Review process
- Open a draft PR targeting `docs/` or `adr/` that includes your proposal and the filled template.
- Request reviews from the stakeholders you listed. Encourage asynchronous comments before scheduling live discussions.
- Update the proposal with review feedback. Keep a brief changelog section for clarity.
- When converged, graduate the proposal into a numbered ADR or update the relevant docs. Close the draft PR when superseded.

## Tips for effective proposals
- Prefer diagrams for complex data flows—reuse the diagram conventions in `docs/v3-architecture/diagrams.md`.
- Call out threat-model changes explicitly; security reviewers look for these first.
- Be explicit about rollout plans and how to measure success or regressions.
- Limit scope to what can be decided in one iteration. Split large topics into staged proposals.
