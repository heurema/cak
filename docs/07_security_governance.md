# 07 — Security and Governance

## Threat model

| Threat | Attack path | CAK defense |
|---|---|---|
| Prompt injection | Untrusted docs/tools smuggle instructions | Scope labels, quarantine, policy checks |
| Memory poisoning | Bad records become future precedent | EvidenceSpec, contradiction checks, unlearning |
| Skill supply-chain | Imported skill encodes unsafe behavior | Signed registry, trust tiers, package audit |
| Delegation laundering | Agent gets another agent to do forbidden work | Delegation contracts, authority inheritance |
| Capability escalation | Tool or skill expands its own rights | Capability checker, no self-escalation |
| Kernel bypass | Agent calls governed tool with direct credentials | Credential-owning tool gateway, no governed secrets in agent process |
| Corrupt success | Final state succeeds but violates policy | Procedure-aware replay, Completion Under Policy |
| Silent drift | Provider/env/policy changes invalidate behavior | ProviderProfile diff, EnvDiff, replay suites |
| Repo poisoning | Config/hooks/rules manipulate coding agent | Trust inspector, context firewall, secret scan |
| Trace exfiltration | Trace store leaks PII, secrets, prompts, or tool output | Redaction, payload separation, retention rules, encrypted sensitive payloads |

## Verifier stack

| Verifier | Checks |
|---|---|
| Static verifier | CAK IR schema, types, dependency graph |
| Pre-exec verifier | action allowed before execution |
| Post-exec verifier | outcome and collateral damage |
| Learning verifier | memory/effect/skill promotion |
| Replay verifier | regression and shadow testing |
| Security verifier | injection, poisoning, supply chain |
| Temporal verifier | history-dependent rules |
| Semantic-fidelity verifier | NL intent preserved in formalization |

## Proof levels

```text
L0 schema valid
L1 policy checked
L2 sandbox tested
L3 regression tested
L4 temporal/model checked
L5 formally proven / certified
```

Example requirements:

```text
summarize_notes        → L1
send_email             → L2 + approval
archive_invoice        → L3
delete_invoice         → L4 + explicit approval
modify_verifier_policy → L5 + human review
```

## Governance roles

```text
Artifact Author
Domain Steward
Verifier Owner
Runtime Operator
Approval Authority
Incident Commander
Privacy Owner
```

## Approval principles

- Human approval should be typed, scoped, and logged.
- Approval tokens should expire.
- Approval tokens should be non-replayable.
- Low-risk reversible actions can be auto-approved by policy.
- High-risk irreversible actions require explicit, preview-backed approval.
