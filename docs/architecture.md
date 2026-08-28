# Architecture

This project is an **embedded closed-loop detector**: analog sensing → discrete-time signal processing → **speed-parameterized threshold law** → finite-state alarm → actuators. Hardware exists to **instantiate the math**, not the other way around.

Pin map: `.cursor/skills/esp32-fuel-vapor/hardware.md`. Equations: `docs/mathematics.md`. Phases: `docs/implementation-plan.md`.

## Design thesis

- **Plant (not modelled in firmware):** tank-area vapor field, airflow vs speed, MQ-2 chemistry. We do not invert the MQ-2 Rs/R0 curve into ppm.
- **Measured signals:** vapor-index ADC `N`, speed-pot ADC `N_v`.
- **Controller:** baseline, delta `d`, affine laws `T_mod(v)`, `T_high(v)`, hysteresis FSM.
- **Study output:** how the **decision boundary** in the $(v,d)$ plane moves, and that the same numbers appear on OLED, serial, and the PC sim.

A second MQ-2 (localization) would be a different architecture (argmax over channels). It is out of scope.

## Layered architecture

```
┌─────────────────────────────────────────────────────────────┐
│ L5  HMI          OLED (I²C)  RGB  buzzer  UART CSV          │
├─────────────────────────────────────────────────────────────┤
│ L4  Decision     hysteresis FSM  {WARMUP, SAFE, MOD, HIGH}  │
├─────────────────────────────────────────────────────────────┤
│ L3  Threshold    T_mod(v), T_high(v)   affine in v          │
├─────────────────────────────────────────────────────────────┤
│ L2  Features     v = map(N_v)    d = max(0, N − N0)         │
├─────────────────────────────────────────────────────────────┤
│ L1  Acquisition  analog MA filter, ADC1, sample counts      │
├─────────────────────────────────────────────────────────────┤
│ L0  Analog       MQ-2 AO or vapor pot | speed pot | 3.3 V   │
└─────────────────────────────────────────────────────────────┘
```

| Layer | Inputs | Outputs | Must stay replaceable |
|-------|--------|---------|------------------------|
| L0 | voltages | — | Pot **or** MQ-2 on the vapor channel; never both |
| L1 | GPIO 34, 33 | `N_bar`, `N_bar_v` | Averaging length `M` |
| L2 | averages, `N_0` | `d`, `v` | Baseline button |
| L3 | `d`, `v` | `T_mod`, `T_high` | `T_0`, `K` (same in sim) |
| L4 | `d`, `T(·)` | state | Hysteresis `H` (see fault ledger for gaps) |
| L5 | state, `d`, `v`, `T` | light, sound, text | Display layout |

**Rule:** do not skip layers (e.g. raw ADC compared to a magic constant). L3 must be a **named function of `v`**.

## Dual runtime (same controller)

```
            ┌──────────────┐
   v, d ───►│  L3 + L4     │───► state, T(v)
            │  (spec)      │
            └──────┬───────┘
                   │ identical constants
          ┌────────┴────────┐
          ▼                 ▼
   sim/adaptive_      firmware/src
   threshold.py       (ESP32 loop)
          │                 │
          ▼                 ▼
        CSV              OLED + GPIO + CSV
```

If sim and firmware disagree at the same $(v,d)$, that is a **fault** (`docs/fault-ledger.md`), not a “display issue.”

## Control view (for viva)

Treat `v` as a **scheduling parameter**, not as a second alarm. The switching surface in the `(v, d)` plane is the pair of lines

```
d = T_mod(v)
d = T_high(v)
```

A **fixed** threshold is the horizontal line `d = T_mod(0)`. The project is the comparison of those two families (tables + inverse-speed formulas in `docs/mathematics.md`).

Plant (optional narrative, not coded): dilution may decrease `d` as `v` rises. The controller **raises** `T(v)` so false alarms fall even if `d` were constant (pot experiment). Fan/MQ-2 is a qualitative plant check only.

## Timing architecture

| Symbol | Role | Nominal |
|--------|------|---------|
| `M` | samples per average | 32 |
| `T_log` | UART period | 500 ms |
| `T_beep` | MOD buzzer toggle | 300 ms |
| `T_w` | warm-up | 2 s dry / 60 s MQ-2 |

The **decision** should use `d`, `v` from the current averaged sample, not the UART tick. Buzzer cadence is independent (`millis()`), not `delay()` in the MOD/HIGH path.

## Firmware mapping (target)

Even while `main.cpp` is still one file, names must map to layers:

| Code | Layer |
|------|--------|
| `avgRead` | L1 |
| `captureBaseline`, `deltaOf`, speed map | L2 |
| `kTmod0`, `kKmod`, … | L3 (`math_params` / `docs/mathematics.md`) |
| `Alert` + comparisons | L4 |
| `showStudy`, `setRgb`, buzzer, `Serial.printf` | L5 |

Do not add Wi-Fi, extra ADCs, or a second gas sensor without a new architecture revision.

## What the architecture forbids

- Localizing a leak with one sensor (impossible in this structure).
- Calling ADC counts “ppm gasoline.”
- Using vehicle CAN/GPS until L2’s `v` map is swapped; the **L3 law stays**.
- Testing with petrol (not an architectural layer; safety).
