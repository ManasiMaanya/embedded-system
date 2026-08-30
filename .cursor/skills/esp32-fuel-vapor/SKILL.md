---
name: esp32-fuel-vapor
description: >-
  Guides this ESP32 hardware project: single MQ-2 at the fuel-tank zone,
  architecture (docs/architecture.md), T(v) mathematics, PC simulation, OLED/I2C, RGB LED,
  buzzer, ADC, GPIO, potentiometer bench tests, and PlatformIO firmware. Use when
  writing firmware, the Python sim, wiring the tank sensor and speed pot, tuning
  T(v), running experiments, logging faults, updating phase-execution-status
  before commits, or debugging ADC/I2C for this capstone.
---

# ESP32 tank vapor + adaptive threshold (this repo)

Hardware + firmware repo. **One MQ-2** (fuel-tank area) and a **speed input**. The academic centre is **architecture (L0–L5)** and **mathematics** of \(T(v)\) in the \((v,d)\) plane — not multi-zone localization and not a wiring-only demo.

Read this file first. Architecture: `docs/architecture.md`. Mathematics: `docs/mathematics.md`. Pins: [hardware.md](hardware.md). Firmware patterns: [firmware.md](firmware.md). Experiments: [tests.md](tests.md). Overview: `docs/overview.md`. Phases: `docs/implementation-plan.md`. **Live execution board:** `docs/phase-execution-status.md`.

## What we are building

Tank MQ-2 → ADC → `delta = reading − baseline` → compare to **adaptive** `T_mod(v)` and `T_high(v)` → OLED + RGB + buzzer.

Speed `v` comes from a **potentiometer** on the bench (stand-in for vehicle speed). OLED must show `v`, `delta`, `T_mod`, `T_high`, and state so the adaptive law is visible.

| Level | Display | RGB | Buzzer |
|-------|---------|-----|--------|
| Safe (`delta < T_mod`) | `System Safe` | Green | Off |
| Moderate | `Tank vapor moderate` | Yellow | Intermittent |
| High | `Danger! High vapor` | Red | Continuous |

Viva story: layers L0–L5 (`docs/architecture.md`), then equations for \(d\), \(T(v)\), and inverse trip speeds (`docs/mathematics.md`), then the bench.

## Adaptive law (default)

```
T_mod(v)  = T_MOD_0  + K_MOD  * v
T_high(v) = T_HIGH_0 + K_HIGH * v
v in [0, 120] km/h from the speed pot
```

Rationale to defend: at higher speed, airflow dilutes tank-area vapor and adds sensor noise; **raising** T reduces false alarms. A leak that still exceeds `T(v)` is treated as more severe. `T_MOD_0`, `K_MOD`, `T_HIGH_0`, `K_HIGH` are named constants — tune from serial plots, do not invent ppm.

Alarms use **delta vs T(v)**, never raw ADC vs a magic number.

## Safety

Not automotive-certified. MQ-2 is not gasoline-specific.

- No petrol, petrol vapour, or open fuel systems.
- Bench: vapor **pot** for algorithm tests; optional tiny **isopropyl alcohol** far from the PCB for a chemical demo. Never fuel.
- MQ-2 heater on **external 5 V**, not ESP32 3V3. AO into ESP32 **≤ 3.3 V**.
- Common GND. Keep solvents off the board.

## Agent workflow

1. Pins from [hardware.md](hardware.md) only. One MQ-2 analog pin, one speed-pot pin.
2. Firmware under `firmware/` (PlatformIO, Arduino-ESP32). L3 constants only in `firmware/src/math_params.h` and `sim/adaptive_threshold.py` — **same numbers**. Change both together; cite `docs/mathematics.md`.
3. Serial 115200, 2 Hz CSV: `t_ms,raw,baseline,delta,speed,Tmod,Thigh,state`. Sim CSV uses the same columns.
4. After pin or `T(v)` constant changes, update `hardware.md`, `sim/adaptive_threshold.py`, and this file in the same edit.
5. Windows: `scripts\p0.cmd` for the sim. Firmware: `scripts\p1-build.cmd` / `scripts\pio.cmd run`. Operator table: `docs/execution-plan.md`.

## Runnable scripts (mandatory)

Always add a script the user can run and edit (`scripts\<name>.cmd` from repo root, or a lab `*.py` they invoke via that `.cmd`). Do **not** leave verification as `python -c` only.

**Reuse before adding a new `.cmd`:**

- Shared env: `call "%~dp0_lib.cmd"` (sets `REPO`, `PY`, `PIO`, `PIO_PROJECT`). Do not copy Python/PIO lookup into a new file.
- Forward `%*` so the user can pass flags (`scripts\p0.cmd --help`, `scripts\p1-upload.cmd --upload-port COM3`).
- Firmware: implement as `scripts\pio.cmd <platformio args>` (or a one-line alias that calls it). Override project with `set PIO_PROJECT=...`.
- Python labs: argparse + `--help`; defaults must still match the P0 checklist when run with no args.

Keep the operator plan in `docs/execution-plan.md`: what to run, in order, expected output, **Ready?** yes/no. When a phase becomes runnable, add the script **and** a table row there in the same change. The user may edit Ready? and the order list themselves.

Windows: prefer `scripts\*.cmd`. PowerShell `.ps1` is often blocked by execution policy.

## Phase execution status (mandatory)

Live board: `docs/phase-execution-status.md`.

**Before the user commits** (when they ask to commit, or say they are about to commit): update that file in the **same** change — Last updated, board table, current work, next action, execution log. Tick matching checklists in `docs/implementation-plan.md`.

Also update the board when a phase **starts**, **finishes**, or **blocks** — do not wait for a commit if the phase moved.

Do not mark a phase `done` unless the plan’s **exit criterion** is met (hardware phases need the bench check, not only source files). P7 may be `skipped`. Open faults stay in `docs/fault-ledger.md`; this board may **name** IDs as blockers, not fix them.

## Fault ledger (mandatory)

Live list: `docs/fault-ledger.md`.

When you find a bug, mismatch (sim vs firmware), wiring hazard, or demo-breaking behaviour:

1. Add a new **F-NNN** row, status `open`. Do not reuse IDs.
2. Tell the user the ID and the one-line fault.
3. **Do not correct the code or “quick-fix” docs for that fault** unless the user names the ID(s) and explicitly approves (e.g. `Approve F-001 F-002`).
4. After an approved fix: set status `fixed` or `verify`, move to Closed, list files. Never delete an ID.

Do not apply a batch of unrelated cleanups under one approval. Safety refusals (petrol tests, etc.) are not ledger items; they stay in this skill’s Safety section.

## Firmware rules

- ADC1 only (speed pot + MQ-2).
- Average 16–32 ADC samples.
- `WARMUP` ≥ 60 s with MQ-2 connected; skip long wait only in a documented dry-pot mode.
- Baseline after warm-up; recalibrate button.
- Hysteresis on `T_mod`. No `delay()` for buzzer cadence (`millis()`).
- OLED shows speed and both thresholds every update.
- No Wi-Fi unless asked. No second/third gas sensor unless the user explicitly reverses this.

## Academic output

Lead with architecture (which layer) and math (which equation), then the GPIO demo.

- Name layers L0–L5; never skip L3 (raw ADC vs a magic constant).
- Write `T_mod(v) = T_MOD_0 + K_MOD * v` with **units** (counts, counts/(km/h), km/h).
- Show inverse `v_enter`, `v_leave`, `d_enter(v)` from `docs/mathematics.md` §5, then the matching sim printout / pot table.
- Do not invent MQ-2 ppm. Counts only unless a new L2 map is specified.
- Faults in the FSM (F-001, F-002) stay logged until the user approves IDs.

When adding firmware: keep L1–L5 separable; put L3 numbers in `math_params.h`.

## Additional resources

- [hardware.md](hardware.md) — pins, BOM, power. In this repo, `.md` opens in Cursor’s built-in **Markdown Preview** (`.vscode/settings.json`). Close the tab and reopen `hardware.md`, or **Ctrl+Shift+V**. To edit source: Command Palette → **View: Reopen Editor With…** → **Text Editor**.
- `docs/buy.md` — BUY photos, specs, typical ₹
- [firmware.md](firmware.md) — loop and PlatformIO
- [tests.md](tests.md) — Python sim, then pots, then MQ-2
- `docs/electronics-components.md` — how ADC, pots, MQ-2, OLED, RGB, buzzer work in this circuit
- `docs/circuit-diagram.md` — pin schematic, Fig A/B, breadboard pictures, netlist
- `docs/architecture.md` — layers L0–L5, dual sim/firmware controller
- `docs/mathematics.md` — ADC, \(T(v)\), inverses, worked example
- `docs/implementation-plan.md` — phases, dependencies, checklists
- `docs/execution-plan.md` — what **you** run; Ready?; scripts
- `docs/phase-execution-status.md` — live board; refresh **before every commit**
- `docs/fault-ledger.md` — faults; fix only after explicit ID approval
