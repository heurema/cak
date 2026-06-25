# Pattern Matrix - CAK Install / Update UX

Status: derived from inspected sources; not an implementation spec.

| Pattern | Source evidence | Fit for CAK | Constraint |
|---|---|---|---|
| Single product command owns lifecycle | `src_cak_runtime_v0`, `src_rustup_installation`, `src_uv_installation` | Strong. CAK should present one public product CLI and keep runtime/adapters behind it. | Requires `cak doctor`, manifest state, and adapter compatibility checks. |
| Project-local version pin | `src_rustup_overrides`, `src_cak_failure_modes` | Strong. CAK policy/runtime behavior must not silently drift across repositories. | v0 must define precedence before update UX is considered safe. |
| Explicit update instead of background update | `src_cak_failure_modes`, `src_github_cli_install_linux` | Strong. Policy/runtime tools need auditable version changes. | Package-manager-managed installs should later delegate updates to the package manager. |
| Inspectable standalone installer | `src_uv_installation`, `src_rustup_installation` | Medium. Useful for early CLI distribution and CI bootstrap. | Public release still needs checksums or signatures; inspectability is not enough. |
| Signed package-manager distribution | `src_github_cli_install_linux`, `src_cak_failure_modes` | Later. Important for mature public distribution. | Too much release-channel complexity before the CAK adapter contract is proven. |
| Self uninstall or rollback path | `src_rustup_installation`, `src_cak_failure_modes` | Strong. CAK needs rollback more than plain uninstall because behavior changes affect decisions. | Rollback must cover binary, manifest, and adapter compatibility state. |
| Thin host adapters | `src_cak_runtime_v0` | Strong. Adapters should call `cak`, not duplicate policy/runtime logic. | `cak host install <host>` must prevent copied adapters from drifting silently. |

## Pattern synthesis

The distribution contract should be:

```text
one public product CLI
  -> explicit install/update/rollback
  -> project pin for behavior stability
  -> host adapter install managed by the CLI
```

The package-manager layer is a release channel, not the core contract. It can
be added later if it preserves the same lifecycle model.
