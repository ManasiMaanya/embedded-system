# Mathematics

Academic core of the tank-vapor monitor. Symbols match `firmware/src/math_params.h` and `sim/adaptive_threshold.py`. Architecture layers: `docs/architecture.md`.

All vapor-index math is in **ADC counts**, not ppm. MQ-2 is a combustible-vapor **index**.

Symbols below use firmware names (`T_mod`, `T_MOD_0`, …) so they stay readable in the editor. Cursor’s Markdown preview does not render LaTeX; use `scripts\preview-docs.cmd` only if you still want KaTeX.

## 1. ADC (L1)

12-bit converter, full scale `N_max = 4095`. Attenuation `ADC_11db` so the pin full-scale is about `V_FS ≈ 3.3 V` (check the ESP32 core; treat 3.3 V as the working assumption).

```
V ≈ (N / N_max) * V_FS
```

Firmware **does not** convert to volts for the threshold. Averaging `M = 32` i.i.d. samples:

```
N_bar = (1/M) * sum_{i=1..M} N_i
```

reduces uncorrelated noise variance by about `M` (if the noise is white). Thresholds are applied to `N_bar`, never to a single conversion.

## 2. Speed map (L2)

Speed pot code `N_v` in `[0, N_max]`:

```
v = v_max * (N_v / N_max),    v_max = 120 km/h
```

Unit of `v`: km/h. This is a **calibration of the bench pot**, not a vehicle speed sensor.

## 3. Baseline and delta (L2)

Clean-air (or dry-pot zero) baseline `N_0 = N_bar` at calibrate / end of warm-up.

```
d = max(0, N_bar - N_0)
```

Unit of `d`: **counts**. Using `d` rather than `N_bar` rejects heater offset and slow clean-air drift until the next calibrate.

## 4. Adaptive threshold law (L3) — main object of the project

Affine (degree-1) schedules:

```
T_mod(v)  = T_MOD_0  + K_MOD  * v
T_high(v) = T_HIGH_0 + K_HIGH * v
```

| Symbol | Role | Default | Unit |
|--------|------|---------|------|
| `T_MOD_0` | intercept, parked moderate trip | 180 | counts |
| `K_MOD` | slope vs speed | 0.8 | counts / (km/h) |
| `T_HIGH_0` | intercept, parked high trip | 420 | counts |
| `K_HIGH` | slope | 1.2 | counts / (km/h) |
| `H` | hysteresis width (moderate band) | 40 | counts |

**Why affine:** one intercept (parked sensitivity) and one slope (how fast the boundary rises). Two numbers per band; identifiable from two bench points (e.g. trip `d` at `v=0` and `v=80`).

**Why `K > 0`:** for **fixed** `d`, `T(v)` increases with `v`, so a leak that alarms when parked can fall below the boundary at speed (false-alarm rejection). A leak that still satisfies `d ≥ T(v)` is treated as more severe.

Compare to a **fixed** threshold `T_fix = T_MOD_0`:

```
adaptive MOD if  d ≥ T_mod(v)
fixed MOD if     d ≥ T_MOD_0
```

The extra region `{ T_MOD_0 ≤ d < T_mod(v) }` is exactly the set of `(v, d)` that a parked calibrator would call MOD but the scheduled law calls SAFE.

## 5. Inverse problems (report formulas)

Hold `d` fixed (Experiment A / speed pot). Enter MOD when `d = T_mod(v)` (ignoring hysteresis):

```
v_enter_mod(d) = (d - T_MOD_0) / K_MOD
                 (K_MOD ≠ 0, d ≥ T_MOD_0)
```

Leave toward SAFE under the **implemented** test `d < T_mod(v) - H`:

```
v_leave_mod(d) = (d + H - T_MOD_0) / K_MOD
```

So `v_leave - v_enter = H / K_MOD` (speed width of the hysteresis, in km/h).

Default numbers, `d = 200`:

```
v_enter_mod = (200 - 180) / 0.8 = 25 km/h
v_leave_mod = (200 + 40 - 180) / 0.8 = 75 km/h
```

Hold `v` fixed (Experiment B). MOD trip in counts:

```
d_enter_mod(v) = T_mod(v) = T_MOD_0 + K_MOD * v
```

At `v=0`: `180`. At `v=80`: `180 + 0.8 * 80 = 244`. The **shift** `K_MOD * v = 64` counts is the quantitative claim of the project.

HIGH band (no extra `H` on `T_high` in the current code; see F-001):

```
d_enter_high(v) = T_high(v)
```

At `v=0`: `420`. At `v=80`: `420 + 1.2 * 80 = 516`.

## 6. Decision (L4) — implemented inequalities

Let `T_m = T_mod(v)`, `T_h = T_high(v)`. Current firmware/sim:

```
if d >= Th:     HIGH
else if d >= Tm: MOD
else if d < Tm - H: SAFE
else:           keep previous state
```

**Intended** (for viva, two-sided hysteresis) would also shrink HIGH with a band on `T_h`. Gaps vs that intent are **F-001** (HIGH/MOD chatter) and **F-002** (possible stuck HIGH). Do not “fix” those in prose; they live in `docs/fault-ledger.md` until approved.

Warm-up: `d` is forced to 0; no trip.

## 7. Worked example (must match the sim)

Constants as in the table in §4. `d=200`, sweep `v=0, 10, …, 120`.

- `v=0`: `T_m=180`, `d ≥ 180` → **MOD**.
- `v=70`: `T_m=236`, `200 < 236` but `200 ≥ 236-40=196` → **keep MOD**.
- `v=80`: `T_m=244`, `200 < 244-40=204` → **SAFE**.

That is why the lab uses `d ≈ 200`, not `250`: `v_leave(250)=137.5 km/h > v_max`.

## 8. Optional plant story (not coded)

A one-pole dilution cartoon `d_plant(v) = d_leak / (1 + beta * v)` can be **discussed**. Firmware still uses **measured** `d` and **scheduled** `T(v)`. Do not fit beta unless you collect MQ-2 data vs fan and say it is empirical.

MQ-2 datasheet `log(Rs/R0)` vs ppm is **not** used. If introduced later, it is a separate L2 map `d → c_hat` with its own uncertainty.

## 9. What to put in the report

1. Equations (1)–(4) with units.
2. Inverse `v_enter`, `v_leave`, `d_enter(v)`.
3. One plot: `T_mod(v)`, `T_high(v)`, and a horizontal `d = const` (sim CSV).
4. One plot: `d_enter_mod(v)` vs a **fixed** `T_MOD_0` (architecture claim).
5. Table: predicted vs pot-measured `d_enter` at `v=0` and `v=80`.

The sim prints the closed-form speeds for the default `d=200` run (`scripts\p0.cmd`).
