# 16 - CAK Failure Modes

## Why this document exists

If CAK owns the tool gateway, CAK becomes a privileged infrastructure component.
It can block production work, leak sensitive trace data, or become the target of
attacks.

CAK must threat-model itself, not only the agents it governs.

## Privileged component risk

The tool gateway may hold or route:

- service-account credentials;
- OAuth tokens;
- local shell authority;
- deployment authority;
- billing or finance authority;
- audit traces with sensitive payloads.

That makes the gateway a high-value target.

## Failure modes

| Failure | Impact | Required design response |
|---|---|---|
| Gateway compromise | Attacker can execute governed tools | Least privilege, key isolation, signing, audit, rotation |
| Verifier bug blocks safe work | Production teams bypass CAK | Policy staging, canary rollout, fast rollback |
| Verifier bug allows unsafe work | CAK creates false trust | Defense in depth, post-exec checks, incident replay |
| Trace store leak | PII, prompts, secrets, and tool output leak | Redaction, encryption, retention, payload separation |
| Policy misconfiguration | Too much block or too much allow | Linting, dry run, review, effective-policy diff |
| Gateway outage | Agents cannot perform governed actions | Risk-tiered fail-open/fail-closed behavior |
| Supply-chain compromise | Kernel or policy packages become attack path | Signed releases, dependency review, reproducible builds |
| Alert fatigue | Teams downgrade policies to warn-only | Low false-block target, developer value, bypass audit |

## Fail-open and fail-closed

CAK should not use one global failure behavior.

Suggested default:

| Action class | Gateway degraded behavior |
|---|---|
| Read-only, low-risk | fail open with trace marker |
| Reversible write | fail closed or require local approval |
| External send | fail closed |
| Payment, delete, deploy, credential change | fail closed |
| Emergency break-glass action | allow only with explicit break-glass token and audit |

## Break-glass

Break-glass is not a hidden bypass.

It should require:

- explicit reason;
- named actor;
- narrow scope;
- expiration;
- post-incident review;
- trace marker visible to auditors and developers.

## Developer value against bypass

If CAK is only a compliance blocker, developers will route around it.

v0.1 must provide direct developer value:

- fast answer to why an agent action was blocked;
- local trace replay for debugging;
- clear policy decision explanations;
- dry-run mode before enabling block mode;
- small integration surface.

## Gateway SLO

v0.1 should define an operational target before production adoption:

```text
Availability target
latency budget
maximum false-block rate
maximum false-allow severity
incident response owner
rollback procedure
```

Without this, CAK moves risk instead of reducing it.

