# Tests: software sim then bench (no petrol)

Goal: show **T(v)** moving, and alarms following **delta vs T(v)**. Run the PC sim first; then pots; then MQ-2.

## Experiment 0 — Software simulation

Same `T(v)` as `firmware/src/math_params.h`. Prints closed-form `v_enter`, `v_leave` (`docs/mathematics.md` §5). No board required.

```
scripts\p0.cmd
```

Writes `sim/out/sim_speed_sweep_d200.csv` and `sim/out/sim_delta_sweep_v0.csv`, `sim_delta_sweep_v80.csv`.

Check: closed form `v_leave(200)=75` km/h; sweep **MOD → SAFE** near that speed. At `v = 80`, `d_enter_mod=244` vs `180` at rest.

If L3 constants change, update `math_params.h` and the Python file in the same edit.

## What you need

| Role | Hardware |
|------|----------|
| Independent variable (speed) | 10 kΩ pot on GPIO 33 |
| Vapor index | Dry: second pot on GPIO 34. Live: MQ-2 AO on GPIO 34 |
| Airflow (optional) | USB fan aimed at MQ-2, not at the ESP32 |
| Record | USB serial → Notepad/Excel |

Mark pot travel: speed 0 / 40 / 80 / 120 km/h using the OLED `v=` reading.

## Experiment 1 — Dry: threshold vs speed (do this first)

Wiring: **two pots only** (no MQ-2). GPIO 34 = “leak,” GPIO 33 = speed.

1. Flash firmware. Skip long heater wait if `DRY_POT` is on.
2. Set leak pot so OLED `d` is about **200** (moderate at v=0, but can fall back to Safe by ~80 km/h with default \(K\) and hysteresis). Hold leak pot still.
3. Sweep speed 0 → 120 slowly.
4. Watch `Tm` / `Th` **rise** and the RGB fall from yellow/red back to green when `T_mod` crosses `d`.

That is the adaptive law with **zero chemical risk**. Photograph OLED at 0, 60, 120 km/h.

**Table to fill**

| v (km/h) | T_mod | T_high | delta (held) | state |
|----------|-------|--------|----------------|-------|
| 0 | | | | |
| 40 | | | | |
| 80 | | | | |
| 120 | | | | |

## Experiment 2 — Dry: leak vs fixed speed

Hold speed pot at **0 km/h**. Sweep leak pot 0 → max. Note `delta` when green→yellow and yellow→red.

Repeat at **80 km/h**. Trip points must **move up** (need a larger leak to alarm). That is the result the report needs.

## Experiment 3 — MQ-2 bring-up (air only)

MQ-2 on 5 V heater, AO → GPIO 34 (remove the leak pot). Common GND. 60 s warm-up. Button = new baseline in clean air.

Confirm `d` sits near 0 and state stays SAFE while you turn **only** the speed pot. `Tm`/`Th` still change; alarm must not, if delta is ~0. That proves speed does not fake a leak.

## Experiment 4 — MQ-2 + IPA (optional, careful)

Open window. IPA bottle **far** from the PCB (tens of cm). Short exposure, then close the bottle.

1. Baseline in clean air, v = 0. Expose until yellow. Note `delta`.
2. Same distance, turn speed pot to 80–120 **or** turn on the USB fan (airflow stand-in for speed). `delta` often **drops**; if it drops below `T_mod(v)` the alarm clears — same story as raising T with v.
3. Do **not** use petrol, lighters in a closed room, or soak the sensor.

Fan is the honest “speed-like” disturbance on a table; the pot is the honest **controlled** independent variable for graphs.

## Experiment 5 — Tune K

If Experiment 2 trip points barely move, increase `K_MOD` / `K_HIGH`. If SAFE is almost unreachable at 0 km/h, lower `T_MOD_0`. Change one constant at a time; log serial.

## What not to test

- Fuel tank, petrol, running vehicle, exhaust as “vapor.”
- MQ-2 and leak pot on the same AO net.
- Judging success by smell instead of OLED `d` vs `Tm`.
