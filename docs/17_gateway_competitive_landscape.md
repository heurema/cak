# 17 - Gateway Competitive Landscape (v0.1 Wedge Check)

Date: 2026-06-11

## Why this document exists

The lab radar (digest 2026-06-11) surfaced live MCP/infrastructure gateways
with policy enforcement. The v0.1 kill criteria in `docs/13` include:

```text
teams prefer existing tooling with much less integration cost
```

This note checks that criterion before any v0.1 build starts, per the lab
decision of 2026-06-11. Sources: project READMEs and repo metadata as of
2026-06-11.

## Competitors

| Project | Since | Stars | What it is |
|---|---|---|---|
| hoophq/hoop | 2022 | 721 | L7 gateway in front of infrastructure (PostgreSQL, MySQL, K8s, SSH, HTTP, MCP). ML-based data masking, pattern-based command blocking, Slack/Teams approval for risky writes, full session recording with replay, SSO/identity federation. Production references (NYSE-listed customers) |
| Kuadrant/mcp-gateway | 2025 | 80 | Envoy/Istio-based MCP gateway for Kubernetes: aggregation and routing of MCP server fleets, authN/authZ/rate limiting via Gateway API policy attachment (Authorino/Keycloak). Red Hat ecosystem |
| DunkelCloud/ToolMesh | 2026 | 3 | Self-hosted MCP gateway: credential injection at execution time, OpenFGA fine-grained authz (user→plan→tool), JS input/output gating policies, SQLite audit. DADL: declarative YAML describing REST APIs as MCP tools |

Adjacent: ~6 smaller MCP-gateway repos in the same digest; "Five-Plane
Reference Architecture for Runtime Governance of Production AI Agents"
(arXiv 2606.12320) signals the category is being formalized.

## Feature matrix vs CAK v0.1 scope

v0.1 scope items from `docs/13`:

| v0.1 capability | hoop | Kuadrant | ToolMesh |
|---|---|---|---|
| Credential-owning gateway | yes | yes (K8s-native) | yes (injection at exec time) |
| MCP proxy form factor | yes (one of many protocols) | yes (core) | yes (core) |
| Policy: allow/block | yes (pattern-based: `DROP TABLE`, custom) | yes (authz rules) | yes (JS gate policies) |
| Policy: require-approval | yes (Slack/Teams, time-bound, logged) | no | no |
| Capability manifest (typed, per tool/identity) | partial (role/plan RBAC) | partial (authz policy) | partial (OpenFGA tuples) |
| `ActionSpec` (typed action signatures) | no | no | partial (DADL describes tools, without semantics) |
| `EffectSpec` (risk + reversibility per action) | no (implicit 3-tier: read/write/destructive) | no | no |
| Pre-exec verification against declared effects | no | no | no |
| Postcondition check after execution | no | no | no |
| Trace recorder (decision-explainable) | partial (session log + risk score) | no | partial (audit log) |
| Recorded tool-call replay, semantic checkpoints | no (replay = forensic playback) | no | no |
| Path to learning plane (trace→evidence→skill) | no | no | no |

## Reading of the kill criterion

Not triggered, with one condition.

The coarse version of the target user's pain — "agents read freely, write
with approval, destructive blocked, everything recorded" — is already
shipped by hoop, mature and credible. If CAK v0.1 reproduces that, it is the
tenth gateway and loses.

The typed version is shipped by nobody:

- effects with risk and reversibility instead of string patterns;
- decisions that reference typed artifacts ("action X classified as effect
  Y, policy Z decided, capability C authorized") instead of log lines;
- replay as regression semantics (re-run against recorded tool calls with
  semantic checkpoints) instead of forensic playback;
- postcondition verification of declared effects;
- a road from traces to evidence-backed learned behavior.

## Scope consequences for v0.1

Do not build (table stakes, owned by the ecosystem):

```text
SSO / identity federation
authn/authz engines (OpenFGA, Authorino exist)
rate limiting
PII masking
MCP fleet aggregation/routing
credential vaulting beyond minimal gateway custody
```

Double down on (nobody has it):

```text
EffectSpec with risk/reversibility per action
pre-exec verifier + policy referencing typed artifacts
explainable decision traces (the five-line audit answer of docs/13)
recorded tool-call replay with semantic checkpoints
postcondition checks
```

Positioning boundary: hoop governs infrastructure wire protocols (SQL, SSH,
kubectl). CAK governs business-tool semantics for SaaS/ops agents — the
`docs/13` target user. Do not compete on infra-access governance.

Form factor hedge: keep v0.1 as a standalone MCP proxy (per `docs/13`), but
design the verifier/decision API as an embeddable component, so it can later
mount into existing gateways (Envoy ext_proc for Kuadrant-class, gate hooks
for ToolMesh-class) instead of competing with them.

## Demo consequence

The v0.1 demo must show something hoop cannot express:

```text
amount > 10000            → require approval
else                      → auto-allow as Effect<compensable>
after execution           → postcondition check (invoice.status == "sent")
every decision            → replayable, typed audit answer
```

If the demo only shows block/approve on a risky call, it demonstrates hoop.

## Proposed decision log entry (for docs/11, on ratification)

```text
Date: 2026-06-11
Project: CAK
Decision: v0.1 proceeds; gateway table stakes are out of scope; typed
  effect/verifier/replay layer is the wedge; verifier designed embeddable
Reason: hoop/Kuadrant/ToolMesh own coarse gateway governance; nobody owns
  typed effects, semantic replay, postconditions
What this prevents: building the tenth MCP gateway; competing with hoop on
  infra-access governance
Review date: first replayable gateway demo (2026-06-24)
```
