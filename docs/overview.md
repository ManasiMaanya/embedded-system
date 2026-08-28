# Project overview

**ESP32 fuel-tank vapor monitor with speed-adaptive thresholds**

VIT Embedded Systems hardware project. This document is the course-facing summary. **Architecture** (`docs/architecture.md`) and **mathematics** (`docs/mathematics.md`) are the academic core; hardware instantiates them. Phase order: `docs/implementation-plan.md`. Live execution status (update before commit): `docs/phase-execution-status.md`. What you run: `docs/execution-plan.md`. Fault ledger: `docs/fault-ledger.md`.

## Problem

Fuel leaks around a tank, pump, or filler can release flammable vapor. A parked vehicle and a vehicle at speed do not see the same local concentration: airflow dilutes vapor and adds sensor noise, while a fixed alarm trip point either false-triggers on the move or is too deaf when stationary.

This prototype does **not** certify a car and does **not** identify petrol as a chemical. It studies one embedded question: **how a speed-scheduled threshold `T(v)` moves the decision boundary in the $(v,d)$ plane**, with a documented layer architecture (sense → features → law → FSM → HMI).

## Objective

Build a bench system that:

1. Reads one **MQ-2** analog output as a **combustible-vapor index** at the fuel-tank zone.
2. Subtracts a **clean-air baseline** so alarms use a delta, not a raw ADC count.
3. Treats **speed** as an independent input (potentiometer on the bench, standing in for a vehicle speed signal).
4. Computes **adaptive thresholds** `T_mod(v)` and `T_high(v)` and drives OLED, RGB LED, and buzzer from the comparison of delta vs `T(v)`.
5. Produces **repeatable measurements** (OLED + serial CSV) so the speed–threshold relationship can be tabulated and plotted.
6. Includes a **PC software simulation** of the same `T(v)` law and state machine so figures and expected trip points exist before (and beside) hardware runs.

Multi-zone leak *localization* (several MQ-2 modules) is **out of scope**.

## System idea

```
  PC sim (Python)                    Bench
  v, d as numbers                    speed pot + MQ-2 or vapor pot
         │                                    │
         └──────────► T_mod(v), T_high(v) ◄───┘
                              │
                 same SAFE / MOD / HIGH rule
                              │
              sim: CSV + tables     HW: OLED, RGB, buzzer, serial CSV
```

Software and hardware share the same constants and hysteresis. The sim does not replace the ESP32 demo; it predicts trip points and report plots. Hardware must still show the same behaviour with pots (then MQ-2).


| State    | Condition (with hysteresis)           | RGB         | Buzzer       |
| -------- | ------------------------------------- | ----------- | ------------ |
| Warm-up  | Heater settle; no alarms              | Off / blink | Off          |
| Safe     | delta below `T_mod`        | Green       | Off          |
| Moderate | delta at or above `T_mod`  | Yellow      | Intermittent |
| High     | delta at or above `T_high` | Red         | Continuous   |


OLED always shows delta `d`, speed `v`, both thresholds, and the state so the adaptive law is visible in a demo.

## Adaptive threshold

Default law (ADC delta counts, 12-bit averaged; constants are tuned after bench tests):

```
T_mod(v)  = T_MOD_0  + K_MOD  * v
T_high(v) = T_HIGH_0 + K_HIGH * v
```

with `v` in km/h, mapped from the speed potentiometer over 0 … 120.

**Viva rationale:** at higher speed, tank-area vapor is more likely to be diluted and the sensor noisier. Raising `T` reduces false alarms. A leak that still exceeds `T(v)` is treated as more severe. Speed itself must not create a leak: with delta near zero, sweeping the speed pot must keep the system Safe while `T` still moves.

Alarms never use raw ADC against a magic constant; they use **delta vs `T(v)`**.

## Course concepts


| Concept              | Where it appears                                                  |
| -------------------- | ----------------------------------------------------------------- |
| ADC                  | MQ-2 AO and speed pot, averaged samples, ADC1                     |
| Sensor interfacing   | MQ-2 heater on 5 V, AO ≤ 3.3 V into ESP32                         |
| GPIO                 | RGB, buzzer, calibrate button                                     |
| I²C                  | SSD1306 OLED                                                      |
| Layered architecture | L0–L5 in `docs/architecture.md`; L3 must not be skipped           |
| Affine `T(v)`        | `docs/mathematics.md`; `math_params.h`                            |
| Inverse trip speeds  | `v_enter`, `v_leave = v_enter + H/K` |
| Real-time loop       | `millis()` for buzzer cadence; no blocking beep delays            |
| Embedded C/C++       | PlatformIO, Arduino-ESP32, `firmware/`                            |
| Software simulation  | Python model of `T(v)` and the alarm state machine, `sim/`        |




## Hardware (summary)


| Item               | Role                                                       |
| ------------------ | ---------------------------------------------------------- |
| ESP32 DevKit       | MCU                                                        |
| One MQ-2           | Tank vapor index                                           |
| 10 kΩ pot          | Simulated speed                                            |
| Second 10 kΩ pot   | Dry stand-in for vapor (GPIO 34 when MQ-2 is disconnected) |
| SSD1306 128×64     | Operator display                                           |
| RGB LED + buzzer   | Alarm HMI                                                  |
| Button             | Recapture baseline                                         |
| 5 V supply         | MQ-2 heater; common ground with ESP32                      |
| USB fan (optional) | Airflow analogy for “speed”                                |


GPIO map, BOM, and power rules: `.cursor/skills/esp32-fuel-vapor/hardware.md`. Firmware: `firmware/`.

**Power:** ESP32 from USB. MQ-2 heater from an external 5 V adapter, not the ESP32 3V3 pin. Measure AO before connecting; divide if it can exceed 3.3 V. Never wire MQ-2 AO and the vapor pot to GPIO 34 at the same time.

## Firmware (summary)

PlatformIO project under `firmware/`. `DRY_POT` in `pins.h` shortens warm-up for two-pot tests; set it to `0` for real MQ-2 heater runs.

Serial (115200, ~2 Hz):

```
t_ms,raw,baseline,delta,speed,Tmod,Thigh,state
```

This CSV is the source for hardware report plots. Compare those rows to `sim/out/*.csv`.

## Software simulation

PC model of the **control law only** (no ADC noise, no MQ-2 chemistry). Path: `sim/adaptive_threshold.py`. Constants must match `firmware/src/math_params.h`. The sim prints closed-form `v_enter`, `v_leave` (`docs/mathematics.md` §5).

**What it is for**

- Sweep `v` at fixed delta and delta at fixed `v` without wiring.
- Print expected SAFE / MOD / HIGH regions for the report.
- Write CSV with the same columns as the ESP32 serial log (`raw` / `baseline` left empty).
- Tune `K` on the PC, then flash the same numbers and confirm on pots.

**What it is not**

- Not a full ESP32 / OLED / I²C emulator (Wokwi is optional later if a browser wiring demo is needed).
- Not a substitute for the hardware viva: pots and MQ-2 still required.

```
scripts\p0.cmd
```

Outputs under `sim/out/` (speed sweep at `d = 200`; delta sweeps at 0 km/h and 80 km/h).

## How we test (no petrol)

Order: **simulate → dry pots → MQ-2**. The speed pot is the controlled independent variable on the bench. A USB fan is an optional physical stand-in for airflow. Petrol, open fuel systems, and in-vehicle tests are forbidden.

1. **Software** — run the Python sim; keep the printed tables / CSV as predicted trip points.
2. **Dry, threshold vs speed** — two pots. Hold vapor pot (fixed `d`), sweep speed. `T` rises; alarm can clear when `T_mod` crosses `d`. States should match the sim at the same `d` and `v`.
3. **Dry, leak vs fixed speed** — sweep vapor at 0 km/h, then at 80 km/h. Trip deltas must be **higher** at speed (same as sim experiment B).
4. **MQ-2, air only** — warm-up, baseline, sweep speed only. `T` moves; state stays Safe if `d ≈ 0`.
5. **MQ-2 + IPA (optional)** — brief exposure far from the PCB; optional fan. Never fuel.

Full procedure and result tables: `.cursor/skills/esp32-fuel-vapor/tests.md`.

## Limitations (state these in the report)

- MQ-2 responds to several combustible gases and smoke, not petrol alone. Output is an **index**, not ppm of gasoline.
- Speed on the bench is a **potentiometer**. A production design would take a speed pulse, GPS, or vehicle bus; the algorithm under test is `T(v)`, not the speed sensor. The Python sim is a third, fully numeric, speed source.
- Bench geometry is not a fuel tank. Placement and airflow dominate the reading.
- Prototype only; not automotive-certified.



## Safety

Bench work only. No petrol or petrol vapor. Prefer two-pot dry tests for algorithm bring-up. If a chemical demo is required, use a small amount of isopropyl alcohol well away from the board. Keep solvents off the PCB and heaters on a proper 5 V supply with common ground.