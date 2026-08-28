# ESP32 tank vapor monitor — adaptive threshold vs speed

VIT Embedded Systems hardware project. **One MQ-2** at the fuel-tank zone. The work is an **architecture + math** study of a speed-scheduled alarm \(T(v)\) on one tank-zone index, not multi-zone localization.

Overview: `docs/overview.md`. Architecture: `docs/architecture.md`. Mathematics: `docs/mathematics.md`. Implementation: `docs/implementation-plan.md`. Execution status (update before commit): `docs/phase-execution-status.md`. What you run: `docs/execution-plan.md`. Fault ledger: `docs/fault-ledger.md`.

## Software simulation

```
scripts\p0.cmd
```

Commands by phase, Ready?, expected output: `docs/execution-plan.md`.

## Firmware

```
scripts\p1-build.cmd
scripts\p1-upload.cmd
scripts\p1-monitor.cmd
```

`DRY_POT` in `firmware/src/pins.h` is `1` for two-pot dry tests (short warm-up). Set `0` before MQ-2 heater runs.
