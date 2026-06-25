# Adversarial Review - CAK Install / Update UX

## Attack: one installer becomes a supply-chain bottleneck

If `curl | sh` becomes the default, CAK inherits a high-risk install path.
`uv` mitigates partly by making the script inspectable, while GitHub CLI's OS
package docs show signed repository metadata and checksum guidance. CAK v0
should not claim production-grade distribution until release artifacts have
checksums and a signature plan.

Required response:

- local smoke can use unsigned dev artifacts;
- public release needs checksums at minimum;
- package-manager distribution needs signed metadata or equivalent trust.

## Attack: global update breaks old projects

A global `cak update` can change policy and runtime behavior under existing
repositories. This conflicts with CAK's own governance framing around
versioned, auditable artifacts.

Required response:

- project pin is mandatory before promoting update UX beyond local experiments;
- `cak doctor` must report active global version and project-pinned version;
- update must not rewrite project pins silently.

## Attack: host adapters drift from the binary

If users manually copy skill packages, wrappers can keep calling an old binary
or the wrong path. H2 appears simple but creates hidden drift.

Required response:

- `cak host install <host>` owns adapter installation;
- adapter metadata records expected CLI version or compatibility range;
- `cak doctor` checks adapter and binary compatibility.

## Attack: rollback only rolls back the binary

Rollback is incomplete if adapter templates, install manifests, or project
pins move independently.

Required response:

- rollback records must include binary path, version, adapter versions, and
  install manifest snapshot;
- v0 rollback can be local-only, but it must be tested.

## Attack: package-manager-first would avoid custom installer code

Homebrew or OS packages provide familiar update commands and signed package
paths, but adopting them first makes CAK solve release-channel complexity
before its host adapter contract is stable.

Required response:

- defer package-manager channels;
- design `cak update` so it can later detect package-manager-managed installs
  and tell users to use `brew upgrade cak` or equivalent.

## Residual risk

The packet chooses a direction but does not prove implementation. It remains
implementation-blocked until `minimal_experiment.md` is run with real release
artifacts and a temporary host directory.
